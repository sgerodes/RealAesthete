import logging
import sqlalchemy
import datetime
from typing import List, Set, Tuple, TypeVar, Generic, get_args, Optional, Union, Any, FrozenSet
from .utils import rollback_on_error
from src import persistence
from functools import lru_cache
from .errors import RepositoryError
from sqlalchemy.orm import sessionmaker


M = TypeVar("M")


logger = logging.getLogger(__name__)


class Repository(Generic[M]):

    @classmethod
    def _get_session(cls):
        # TODO probably replace with Session(bind=engine, expire_on_commit=False) or with a sessionmaker()
        # https://stackoverflow.com/questions/12223335/sqlalchemy-creating-vs-reusing-a-session
        # return persistence.session
        return sqlalchemy.orm.Session(bind=persistence.engine, expire_on_commit=True)

    @classmethod
    def _get_query(cls):
        return cls._get_session().query(cls._get_model_type())

    @classmethod
    def _get_filtered_query(cls, **kwargs) -> sqlalchemy.orm.query.Query:  # noqa
        for k in kwargs.keys():
            if k not in dir(cls._get_model_type()):
                logger.error(f'Tried to query "{cls._get_model_type_name()}" by "{k}",'
                             f' but it is not a member of the class')
        return cls._get_query().filter_by(**kwargs)

    @classmethod
    @lru_cache(maxsize=1)
    def _get_model_type(cls):
        return get_args(cls.__orig_bases__[0])[0]  # noqa

    @classmethod
    @lru_cache(maxsize=1)
    def _get_model_type_name(cls):
        return cls._get_model_type().__name__

    @classmethod
    @lru_cache(maxsize=1)
    def _get_primary_keys(cls) -> Tuple[str]:
        alchemy_pks = sqlalchemy.inspection.inspect(cls._get_model_type()).primary_key
        return tuple(alchemy_column.name for alchemy_column in alchemy_pks)  # noqa

    @classmethod
    @lru_cache(maxsize=1)
    def _get_unique_constraints(cls) -> Set[FrozenSet[str]]:
        tablename: str = cls._get_model_type().__tablename__
        # Get multicolumn unique constraints
        sqlalchemy_unique_constraints: List[dict] = sqlalchemy.inspect(persistence.engine).get_unique_constraints(tablename)

        # Get Primary keys
        pks = list(cls._get_primary_keys())
        unique_with_pks: List[list] = [c.get('column_names') for c in sqlalchemy_unique_constraints]
        unique_with_pks.append(pks)

        # Get field declared unique constraints
        for col in sqlalchemy.inspect(cls._get_model_type()).c:
            if col.unique:
                unique_with_pks.append([col.name])
        return set(frozenset(c) for c in unique_with_pks)

    # CREATE
    @classmethod
    @rollback_on_error
    def create(cls, entity: M) -> Optional[M]:
        if not entity:
            logger.error(f'Tried to create empty object')
            return None
        if entity.id:
            logger.error(f'The instance you passing in has already an id. Aborting'
                         f'Probably tried to create already existing entity: {entity}')
            return None
        session = cls._get_session()
        session.add(entity)
        session.commit()
        logger.debug(f'Created {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def create_all(cls, entities_list: List[M]) -> Optional[List[M]]:
        for e in entities_list:
            cls.create(e)
        logger.debug(f'Created {len(entities_list)} entities')
        return entities_list

    # READ
    @classmethod
    #def read_by_primary_keys(cls, primary_keys: Union[List, Set, Tuple, Any]) -> Optional[M]:
    def read_by_primary_keys(cls, *args, **kwargs) -> Optional[M]:
        if args and kwargs:
            raise RepositoryError(f'You cant read by primary keys using both args and kwargs')
        pks_values = args or kwargs
        # model_pks = cls._get_primary_keys()
        # if args:
        #     if len(args) != len(model_pks):
        #         raise RepositoryError(f'Invalid amount of primary keys provided for model {cls._get_model_type_name()}.'
        #                               f'got primary_keys={args}, model primary key names are {model_pks}')
        #     pks_values = args
        # elif kwargs:
        #     if len(kwargs) != len(model_pks):
        #         raise RepositoryError(f'Invalid amount of primary keys provided for model {cls._get_model_type_name()}.'
        #                               f'got primary_keys={kwargs}, model primary key names are {model_pks}')
        #     pks_values = kwargs
        # else:
        #     raise RepositoryError(f'Tried to read by primary keys without specifying arguments')
        logger.debug(f'Reading {cls._get_model_type_name()} with primary keys: {pks_values}')
        return cls._get_query().get(pks_values)

    @classmethod
    def read_by_unique(cls, **kwargs) -> Optional[M]:
        column_names = set(kwargs.keys())
        if column_names not in cls._get_unique_constraints():
            # logger.warning(f'The column combination {column_names} is not a unique constraint in "{cls._get_model_type_name()}". '
            #                f'Existing constraints are {cls._get_unique_constraints()}')
            # return None
            raise RepositoryError(f'The column combination {column_names} is not a unique constraint in "{cls._get_model_type_name()}". '
                           f'Existing constraints are {cls._get_unique_constraints()}')
        logger.debug(f'Reading {cls._get_model_type_name()} by unique: {kwargs}')
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
    def read_all(cls, limit: int = None, offset: int = None, **kwargs) -> Optional[List[M]]:
        logger.debug(f'Reading all "{cls._get_model_type_name()}" with {limit=} {offset=} filters {kwargs}')
        filtered_query = cls._get_filtered_query(**kwargs)
        if limit:
            filtered_query = filtered_query.limit(limit)
        if offset:
            filtered_query = filtered_query.offset(offset)
        return filtered_query.all()

    @classmethod
    def read_all_paged(cls, page=0, page_size=None, **kwargs) -> Optional[List[M]]:
        return cls.read_all(limit=page_size, offset=page*page_size, **kwargs)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        logger.debug(f'Checking existence of {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(**kwargs).first() is not None

    # UPDATE
    @classmethod
    @rollback_on_error
    def update(cls, entity: M) -> M:
        if hasattr(entity, 'updated_at'):
            entity.updated_at = datetime.datetime.now()
        session = cls._get_session()
        session.add(entity)
        session.commit()
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
        session = cls._get_session()
        session.delete(entity)
        session.commit()
        logger.debug(f'Deleted {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    @rollback_on_error
    def delete_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.delete(e)
        logger.debug(f'Deleted {len(entities_list)} entities')
        return entities_list
