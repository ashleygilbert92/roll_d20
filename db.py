import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

DB_USERNAME = os.environ.get('MYSQLUSERNAME', 'root')
DB_PASS = os.environ.get('MYSQLPASS', 'P@ssword1')
DB_SERVER_IP = os.environ.get('MYSQLSERVERIP', 'localhost:3306')
DB_PATH = 'mysql+pymysql://{}:{}@{}/roll_d20'.format(DB_USERNAME, DB_PASS, DB_SERVER_IP)


def get_session_factory():
    engine = create_engine(DB_PATH)
    session = sessionmaker(bind=engine)
    return session


def create_all_tables():
    engine = create_engine(DB_PATH)
    models.Base.metadata.create_all(engine)
