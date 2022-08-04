import logging
import sqlalchemy
import os
import datetime
from typing import List, Set, Tuple, TypeVar, Generic, get_args, Optional, Union, FrozenSet
from functools import lru_cache
from .errors import RepositoryError
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression

# TODO transactions high prio https://docs.sqlalchemy.org/en/14/orm/session_transaction.html
# TODO async low prio


M = TypeVar('M')


logger = logging.getLogger(__name__)


class Repository(Generic[M]):

    @classmethod
    def _create_engine(cls, database_uri: str = None) -> sqlalchemy.engine.base.Engine:
        db_uri = database_uri or os.getenv('SQLALCHEMY_DATABASE_URI')
        logger.info(f'Creating engine automatically for {cls.__name__}')
        if not db_uri:
            raise RepositoryError('Cant automatically create an engine, either provide the database uri'
                                  ' or set the SQLALCHEMY_DATABASE_URI environment variable')
        engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
        return engine

    @classmethod
    def get_engine(cls):
        if not hasattr(cls, '__engine__'):
            cls.set_engine(cls._create_engine())
        @classmethod
        def get_engine(cls):
            return cls.__engine__
        cls.get_engine = get_engine
        return cls.__engine__

    @classmethod
    def set_engine(cls, engine: sqlalchemy.engine.base.Engine):
        logger.info(f'Engine is set for {cls.__name__} with id {id(engine)}')
        cls.__engine__ = engine

    @classmethod
    @lru_cache(maxsize=1)
    def _get_model_type(cls):
        model = get_args(cls.__orig_bases__[0])[0]  # noqa
        if 'sqlalchemy' in str(model.__mro__):
            return model
        raise RepositoryError(f'Provided Model {model} in {cls.__name__} probably is not a sqlalchemy model. '
                              f'MRO of the class is {model.__mro__}')

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
    def _get_column_names(cls) -> Set[str]:
        columns = sqlalchemy.inspection.inspect(cls._get_model_type()).c
        return set(alchemy_column.name for alchemy_column in columns)  # noqa

    @classmethod
    @lru_cache(maxsize=1)
    def _get_unique_constraints(cls) -> Set[FrozenSet[str]]:
        tablename: str = cls._get_model_type().__tablename__
        # Get multicolumn unique constraints
        sqlalchemy_unique_constraints: List[dict] = sqlalchemy.inspect(cls.get_engine()).get_unique_constraints(tablename)

        # Get Primary keys
        pks = list(cls._get_primary_keys())
        unique_with_pks: List[list] = [c.get('column_names') for c in sqlalchemy_unique_constraints]
        unique_with_pks.append(pks)

        # Get field declared unique constraints
        for col in sqlalchemy.inspect(cls._get_model_type()).c:
            if col.unique:
                unique_with_pks.append([col.name])
        return set(frozenset(c) for c in unique_with_pks)

    @classmethod
    def _add_and_commit(cls, entity: M) -> Optional[M]:
        #with sqlalchemy.orm.Session(bind=persistence.engine, expire_on_commit=True) as session:
        with sqlalchemy.orm.Session(bind=cls.get_engine()) as session:
            try:
                merged_entity = session.merge(entity)
                session.add(merged_entity)
                session.flush()
                # session.refresh(merged_entity)
                session.expunge_all()
                session.commit()
                return merged_entity
            except (sqlalchemy.exc.IntegrityError,
                    sqlalchemy.exc.ProgrammingError,
                    sqlalchemy.exc.DatabaseError,
                    sqlalchemy.exc.InvalidRequestError) as e:
                logger.exception(e)
                logger.warning(f'Rolling back the db session because of an error')
                session.rollback()
                return None
            finally:
                session.close()

    @classmethod
    def query(cls):
        session = sqlalchemy.orm.Session(bind=cls.get_engine(), expire_on_commit=True)
        return session.query(cls._get_model_type())

    @classmethod
    def _get_filtered_query(cls, *args: BinaryExpression, **kwargs) -> sqlalchemy.orm.query.Query:  # noqa
        for a in args:
            if not isinstance(a, BinaryExpression):
                raise RepositoryError(f'args of type sqlalchemy.sql.elements.BinaryExpression are only allowed, but got {a} of type {type(a)}')
        for k in kwargs.keys():
            if k not in cls._get_column_names():
                # TODO maybe raise an error?
                logger.warning(f'Tried to query "{cls._get_model_type_name()}" by "{k}",'
                             f' but it is not a member of the class')
        return cls.query().filter(*args).filter_by(**kwargs)

    # CREATE
    @classmethod
    #@rollback_on_error
    def create(cls, entity: M) -> Optional[M]:
        if not entity:
            logger.error(f'Tried to create empty object')
            return None
        if entity.id:
            logger.error(f'The instance you passing in has already an id. Aborting'
                         f'Probably tried to create already existing entity: {entity}')
            return None
        entity = cls._add_and_commit(entity)
        logger.debug(f'Created {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    #@rollback_on_error
    def create_all(cls, entities_list: List[M]) -> List[M]:
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
        logger.debug(f'Reading {cls._get_model_type_name()} with primary keys: {pks_values}')
        return cls.query().get(pks_values)

    @classmethod
    def read_by_unique(cls, *args: Union[BinaryExpression, bool], **kwargs) -> Optional[M]:
        column_names = set(kwargs.keys())
        if column_names not in cls._get_unique_constraints():
            # logger.warning(f'The column combination {column_names} is not a unique constraint in "{cls._get_model_type_name()}". '
            #                f'Existing constraints are {cls._get_unique_constraints()}')
            # return None
            raise RepositoryError(f'The column combination {column_names} is not a unique constraint in "{cls._get_model_type_name()}". '
                           f'Existing constraints are {cls._get_unique_constraints()}')
        logger.debug(f'Reading {cls._get_model_type_name()} by unique: {kwargs}')
        return cls._get_filtered_query(*args, **kwargs).first()

    @classmethod
    def read_first(cls, *args: Union[BinaryExpression, bool], **kwargs) -> Optional[M]:
        logger.debug(f'Reading first {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(*args, **kwargs).first()

    # @classmethod
    # def read_last(cls, **kwargs) -> Optional[M]:
    #     logger.debug(f'Reading last {cls._get_model_type_name()} with filters {kwargs}')
    #     return cls._get_filtered_query(**kwargs).order_by(cls._get_model_type().id.desc()).first()

    @classmethod
    def read_all(cls, *args: Union[BinaryExpression, bool], limit: int = None, offset: int = None, **kwargs) -> Optional[List[M]]:
        # TODO change limit and offset, because some columns can be named like that
        str_args = str([str(a) for a in args]) if args else ''
        logger.debug(f'Reading all "{cls._get_model_type_name()}" with limit={limit} offset={offset} filters: {kwargs if kwargs else ""} {str_args}')
        filtered_query = cls._get_filtered_query(*args, **kwargs)
        if limit:
            filtered_query = filtered_query.limit(limit)
        if offset:
            filtered_query = filtered_query.offset(offset)
        return filtered_query.all()

    @classmethod
    def read_all_paged(cls, *args: Union[BinaryExpression, bool], page=0, page_size=None, **kwargs) -> Optional[List[M]]:
        return cls.read_all(*args, limit=page_size, offset=page*page_size, **kwargs)

    @classmethod
    def exists(cls, *args: Union[BinaryExpression, bool], **kwargs) -> bool:
        logger.debug(f'Checking existence of {cls._get_model_type_name()} with filters {kwargs}')
        return cls._get_filtered_query(*args, **kwargs).first() is not None

    # @classmethod
    # def distinct(cls, **kwargs) -> Optional[List[Any]]:
    #     pass # TODO

    # UPDATE
    @classmethod
    #@rollback_on_error
    def update(cls, entity: M) -> M:
        if hasattr(entity, 'updated_at'):
            entity.updated_at = datetime.datetime.now()
        entity = cls._add_and_commit(entity)
        logger.debug(f'Updated {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    #@rollback_on_error
    def update_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.update(e)
        logger.debug(f'Updated {len(entities_list)} entities')
        return entities_list

    # DELETE
    @classmethod
    #@rollback_on_error
    def delete(cls, entity: M) -> M:
        entity = cls._add_and_commit(entity)
        logger.debug(f'Deleted {cls._get_model_type_name()} {entity}')
        return entity

    @classmethod
    #@rollback_on_error
    def delete_all(cls, entities_list: List[M]) -> List[M]:
        for e in entities_list:
            cls.delete(e)
        logger.debug(f'Deleted {len(entities_list)} entities')
        return entities_list

