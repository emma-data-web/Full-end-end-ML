import pandas as pd
from utils.db_pull import get_data
from utils.logger import get_logger
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer


logger = get_logger('training_logger','logs/logging.txt')
df = get_data()

