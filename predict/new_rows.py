import pandas as pd
from utils.config_hepler import load_config
from utils.helper import get_engine
from utils.logger import get_logger
import joblib
from  datetime import datetime
import time



config = load_config()

logger = get_logger(config["logger_names"]["new_data_logger"], config["log_path"]["new_data_path"])

(config["logger_names"]["new_data_logger"], config["log_path"]["new_data_path"])

model = joblib.load(config["model_path"]["trained_model"])
def get_new_rows():
  try:
    engine = get_engine()

    query = """
      SELECT *
      FROM titanic_train t
      WHERE t.PassengerId NOT IN (
          SELECT PassengerId FROM pred
      )
      """
    df_new = pd.read_sql(query, con=engine)

    if df_new.empty:
      logger.info('no new rows founds!!')
      
      return 

    data =df_new.drop("Survived", axis=1, errors="ignore")

    predictions = model.predict(data)

    df_results = pd.DataFrame({
          "PassengerId": df_new["PassengerId"],
          "predictions": predictions,
          "createdAT": datetime.now()
          })
    df_results.to_sql("pred",con=engine, if_exists="append", index=False)
      
    logger.info(f"{len(df_results)}")
  except Exception as e:
    logger.error(f"Error in get_new_rows: {e}")



if __name__ == "__main__":
  wait_time = config.get("loop_time", 60)
  logger.info(f"starting automateed looping: {wait_time} seconds!")


  while True:
    start_time = datetime.now()
    logger.info(f"starting to find new rows at {start_time}")
    
    get_new_rows()

    logger.info(f"waiting for {wait_time}")

    time.sleep(60)