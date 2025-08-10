import pandas as pd
from utils.db_pull import get_data
from utils.logger import get_logger
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from features.feat_engineering import add_features
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier


logger = get_logger('training_logger','logs/logging.txt')

df = get_data()

features = ['PassengerId','Pclass','Sex' ,'Age','SibSp','Parch','Fare','Embarked']

cat_columns = ['Sex','Embarked']

num_columns = ['PassengerId','Pclass','Age','SibSp','Parch','Fare']

target = ['Survived']

for col in cat_columns:
  df[col] = df[col].astype('category')

transformed_features = FunctionTransformer(add_features, validate=False)


x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], 
test_size=0.2, random_state=101)


num_pipeline = Pipeline(steps=[
  'impute', SimpleImputer(strategy='mean')
]
)

cat_pipeline = Pipeline(steps=[
  'impute', SimpleImputer(strategy='most_frequent')
])

processed_columns = ColumnTransformer(transformers=[
  ('num_processing',num_pipeline,num_columns),
  ('cat_processing',cat_pipeline,cat_pipeline)
], remainder='passthrough', verbose=True)

model = LGBMClassifier()

final_preprocessing = Pipeline(steps=[
  ('feature_engr',transformed_features),                            
  ('processing',processed_columns),
  ('model', model )
])