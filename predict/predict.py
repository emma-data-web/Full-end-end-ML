from utils.db_pull import get_data
import  pandas as pd
from datetime import datetime
import joblib
from utils.config_hepler import load_config
from utils.helper import get_engine

df = get_data()
config = load_config()
engine = get_engine()

model = joblib.load(config["model_path"]["trained_model"])

def predict():

  data = df.copy()

  data.drop("Survived", axis=1)

  predictions = model.predict(data)

  return predictions



df_pred = predict()

df_new = pd.DataFrame({
  "PassengerId": df["PassengerId"],
  "predictions": df_pred,
  "createdAT" : datetime.now()
})

df_new.to_sql("pred", con=engine, if_exists="append", index=False)


