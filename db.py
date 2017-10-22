import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

DB_USERNAME = os.environ.get('MYSQLUSERNAME', 'root')
DB_PASS = os.environ.get('MYSQLPASS', 'P@ssword1')
DB_SERVER_IP = os.environ.get('MYSQLSERVERIP', 'localhost:3306')
DB_PATH = 'mysql+pymysql://{}:{}@{}/roll_d20'.format(DB_USERNAME, DB_PASS, DB_SERVER_IP)


def get_session_factory():
    engine = create_engine(DB_PATH, pool_size=50, max_overflow=0, pool_recycle=3600)
    session = sessionmaker(bind=engine, expire_on_commit=False)
    return session


def create_all_tables():
    engine = create_engine(DB_PATH)
    models.Base.metadata.create_all(engine)
