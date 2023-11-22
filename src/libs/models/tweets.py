"""This module contains a Tweets model and class(es) used by the model.
"""
from sqlalchemy import Column, exc, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship

from libs.db_session import SessionManager
from libs.db_setup import Base


class Tweets(Base, SessionManager):
    """Class to handle the Tweets list table.
    """

    __tablename__ = 'tweets'

    id = Column(BigInteger, primary_key=True)
    text = Column(String(320))
    create_time = Column(DateTime)
    retweets = Column(Integer)
    likes = Column(Integer)
    lang = Column(String(3))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    author = relationship('Users', back_populates='tweets')

    @classmethod
    def add_tweet(cls, tweet) -> None:
        """Add new tweet to the Data Base.

        :param tweet:   Tweet object.
        """
        with cls.session as session:
            try:
                with session.begin_nested():
                    session.merge(tweet)
                session.commit()
            except exc.IntegrityError as error:
                raise error
