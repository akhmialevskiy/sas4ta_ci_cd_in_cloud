"""Main module with different DB actions"""
from sqlalchemy.dialects.postgresql import insert

from src.libs.db_setup import DBSession


class SessionManager:
    """Session manager for sqlalchemy"""

    session = DBSession()

    @classmethod
    def save(cls, return_cursor: bool = False, **kwargs):
        with cls.session as session:
            stmt = insert(cls).values(**kwargs)
            cursor = session.execute(stmt)
            return cursor if return_cursor else None

    @classmethod
    def get_query_by_filter(cls, columns=None, offset=None, limit=None, **kwargs):
        if columns is None:
            columns = [cls]
        with cls.session as session:
            return session.query(*columns).filter_by(**kwargs).offset(offset).limit(limit)

    @classmethod
    def get_count(cls, **kwargs):
        with cls.session as session:
            return session.query(cls).filter_by(**kwargs).count()
