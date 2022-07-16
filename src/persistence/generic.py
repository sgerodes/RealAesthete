import logging
import sqlalchemy
import datetime
from typing import List, Set, Tuple, TypeVar, Generic, get_args, Optional, Union, Any
from .utils import rollback_on_error
from src import persistence

M = TypeVar("M")


logger = logging.getLogger(__name__)


class Repository(Generic[M]):

    @classmethod
    def _get_session(cls):
        return persistence.session

    @classmethod
    def _get_model_type(cls):
        return get_args(cls.__orig_bases__[0])[0]  # noqa

    @classmethod
    def _get_model_type_name(cls):
        return cls._get_model_type().__name__

    @classmethod
    def _get_class_field(cls, field_name: str):
        if field_name not in cls._get_model_type().__dict__:
            return None
        return cls._get_model_type().__dict__[field_name]

    @classmethod
    def _get_models_primary_keys(cls, db_model) -> Tuple[str]:
        alchemy_pks = sqlalchemy.inspection.inspect(db_model).primary_key
        return tuple(alchemy_column.name for alchemy_column in alchemy_pks) # noqa

    @classmethod
    def _get_filtered_query(cls, **kwargs) -> sqlalchemy.orm.query.Query:  # noqa
        for k in kwargs.keys():
            if k not in dir(cls._get_model_type()):
                logger.error(f'Tried to query "{cls._get_model_type_name()}" by "{k}",'
                             f' but it is not a member of the class')
        return cls._get_model_type().query.filter_by(**kwargs)

    # CREATE
    @classmethod
    @rollback_on_error
    def create(cls, entity: M) -> M:
        if entity.id:
            logger.error(f'The instance you passing in has already an id. try updating instead. '
                         f'Probably tried to create already existing entity: {entity}')
            return entity
        cls._get_session().add(entity)
        cls._get_session().commit()
        logger.debug(f'Created {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def create_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.create(e)
        logger.debug(f'Created {len(entities_list)} entities')
        return entities_list

    # READ
    @classmethod
    def read_by_primary_keys(cls, primary_keys: Union[List[Any], Set[Any], Any]) -> Optional[M]:
        model_pks = cls._get_models_primary_keys(cls._get_model_type())
        if isinstance(primary_keys, list) or isinstance(primary_keys, set) or isinstance(primary_keys, tuple):
            for pk in primary_keys:
                if len(primary_keys) != len(model_pks):
                    logger.error(f'Invalid amount of primary keys provided for model {cls._get_model_type_name()}.'
                                 f'got {primary_keys}, model primary key names are {model_pks}')
                    return None
        else:
            if len(model_pks) != 1:
                logger.error(f'Invalid amount of primary keys provided for model {cls._get_model_type_name()}.'
                             f'got {primary_keys=}, model primary key names are {model_pks}')
                return None
        logger.debug(f'Reading {cls._get_model_type_name()} with primary keys: {primary_keys}')
        return cls._get_model_type().query.get(primary_keys)

    @classmethod
    def read_by_unique(cls, **kwargs) -> Optional[M]:
        if len(kwargs) != 1:
            logger.warning(f'You should only query by a single unique identifier')
            return None
        field_name = list(kwargs.keys())[0]
        field = cls._get_class_field(field_name)
        if not field:
            logger.warning(f'No unique field found "{field_name}" in "{cls._get_model_type_name()}"')
            return None
        if not field.unique:
            logger.warning(f'You tried to perform a unique query on a non-unique field "{field_name}" of "{cls._get_model_type_name()}"')
            return None
        return cls._get_filtered_query(**kwargs).first()

    @classmethod
    def read_first(cls, **kwargs) -> Optional[M]:
        logger.debug(f'Reading first {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(**kwargs).first()

    @classmethod
    def read_last(cls, **kwargs) -> Optional[M]:
        logger.debug(f'Reading last {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(**kwargs).order_by(cls._get_model_type().id.desc()).first()

    @classmethod
    def read_all(cls, limit: int = None, **kwargs) -> List[M]:
        logger.debug(f'Reading all "{cls._get_model_type_name()}" with {limit=} filters {kwargs}')
        filtered_query = cls._get_filtered_query(**kwargs)
        if limit:
            filtered_query = filtered_query.limit(limit)
        return filtered_query.all()

    # UPDATE
    @classmethod
    @rollback_on_error
    def update(cls, entity: M) -> M:
        if hasattr(entity, 'updated_at'):
            entity.updated_at = datetime.datetime.now()
        cls._get_session().add(entity)
        cls._get_session().commit()
        logger.debug(f'Updated {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def update_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.update(e)
        logger.debug(f'Updated {len(entities_list)} entities')
        return entities_list

    # DELETE
    @classmethod
    @rollback_on_error
    def delete(cls, entity: M) -> M:
        cls._get_session().delete(entity)
        cls._get_session().commit()
        logger.debug(f'Deleted {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def delete_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.delete(e)
        logger.debug(f'Deleted {len(entities_list)} entities')
        return entities_list