import urllib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from src.libs.settings import (
    DB_DIALECT,
    DB_DRIVER,
    DB_USERNAME,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_PASSWORD
)

DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)
DB_URL = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DB_URL,
                       future=True,
                       echo=False,
                       poolclass=QueuePool,
                       pool_size=20,
                       max_overflow=10,
                       pool_pre_ping=True,
                       connect_args={"keepalives": 1,
                                     "keepalives_idle": 60,
                                     "keepalives_interval": 10,
                                     "keepalives_count": 20})

Base = declarative_base()
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine, future=True))


def create_tables():
    """Create Tables."""
    Base.metadata.create_all(engine)
