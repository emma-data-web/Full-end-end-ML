import pandas as pd
import os
import joblib
from utils.helper import get_engine
from utils.db_pull import get_data
from utils.config_hepler import load_config
from utils.logger import get_logger
from datetime import datetime
import time

engine = get_engine()

data = get_data()

config = load_config()

model = joblib.load(config["model_path"]["trained_model"])


logger = get_logger(config["logger_names"]["loop_logger"], config["log_path"]["loop_path"])


while True:
  logger.info("loadinng up new rows adn returnig predictions!!")
  data = get_data()
  engine = get_engine()
  if not data.empty:
    logger(f"returned a total of {len(data)} rows!s")

    if not data.empty:
      try:
        new_data = data.drop(columns=["Survived"], errors="ignore")
        logger.info("sroped target columns!!!")
        logger.info(f"dataframe shape; {data.shape}")
        logger.info(f"the first five rows!; {data.head()}")

        predictions = model.predict(new_data)

        df_new = pd.DataFrame({
        "PassengerId": new_data["PassengerId"],
        "predictions": predictions,
        "createdAT" : datetime.now()
        })

        df_new.to_sql("pred", con=engine, if_exists="append")
        
      except Exception as e:
        logger.info(f"The error {e}")
      