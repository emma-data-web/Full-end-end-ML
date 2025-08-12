from utils.db_pull import get_data
import joblib
from utils.config_hepler import load_config

df = get_data()
config = load_config()

model = joblib.load(config["model_path"]["trained_model"])

def predict():

  data = df.copy()

  data.drop("Survived", axis=1)

  predictions = model.predict(data)

  return predictions

