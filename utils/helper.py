import os
from sqlalchemy import create_engine


def get_engine():
    db_url = f"mysql+pymysql://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_database')}"

    engine = create_engine(db_url)

    return engine