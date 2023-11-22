"""This module contains Users model and class(es) used by the model.
"""
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import relationship

from libs.db_session import SessionManager
from libs.db_setup import Base


class Users(Base, SessionManager):
    """Class to handle the Users list table.
    """

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    created = Column(DateTime)
    description = Column(String(200))
    location = Column(String(200))
    followers = Column(Integer)
    friends = Column(Integer)
    statuses = Column(Boolean)
    tweets = relationship('Tweets', back_populates='author')
