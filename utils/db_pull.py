from  sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.config_hepler import load_config

config = load_config()

db_logger = get_logger(config["logger_names"]["db_logger"],config["log_path"]["db_logger_file_path"])



load_dotenv()


def get_data():
  db_url = f"mysql+pymysql://{os.getenv('db_username')}:{os.getenv('db_password')}@{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_database')}"

  engine = create_engine(db_url)
  query = (config["Queries"]["db_pull_query"])
  df = pd.read_sql(query, con=engine)
  db_logger.info(f'if query loaded, return {len(df)}')
  return df


