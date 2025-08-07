from  sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger('db_pull_logger','logs/logging.txt')

print(logger)

load_dotenv


def get_data():
  db_url = f"mysql+pymysql://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_database')}"

  engine = create_engine(db_url)
  query = ('select * from titanic_train')
  df = pd.read_sql(query, con=engine)
  logger.info(f'if query loaded, return {len(df)}')
  return df


