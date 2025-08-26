import pandas as pd
import os
from utils.db_pull import get_data
from utils.logger import get_logger
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from features.feat_engineering import add_features
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder
from utils.config_hepler import load_config
import joblib


config = load_config()

logger = get_logger(config["logger_names"]["train_logger"],config["log_path"]["train_file_path"])



df = get_data()

def train_model(filename="trained_model.pkl"):
  try:
    logger.info('starting the training process')
    features = ['PassengerId','Pclass','Sex' ,'Age','SibSp','Parch','Fare','Embarked']

    cat_columns = ['Sex','Embarked']

    num_columns = ['PassengerId','Pclass','Age','SibSp','Parch','Fare']

    target = ['Survived']



    transformed_features = FunctionTransformer(add_features, validate=False)


    x_train, x_test, y_train, y_test = train_test_split(df[features], df[target], 
    test_size=0.2, random_state=101)


    num_pipeline = Pipeline(steps=[
      ('impute', SimpleImputer(strategy='mean'))
    ]
    )

    cat_pipeline = Pipeline(steps=[
      ('impute', SimpleImputer(strategy='most_frequent')),
      ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    processed_columns = ColumnTransformer(transformers=[
      ('num_processing',num_pipeline,num_columns),
      ('cat_processing',cat_pipeline,cat_columns)
    ], remainder='passthrough', verbose=True,force_int_remainder_cols=False)

    model = XGBClassifier()

    final_preprocessing = Pipeline(steps=[
      ('feature_engr',transformed_features),                            
      ('processing',processed_columns),
      ('model', model )
    ])

    param_dist = {
      'model__n_estimators': [100,200,500],
      'model__learning_rate': [0.01,0.1,0.5],
      'model__max_depth': [3,5,7,10]
    }

    grid = RandomizedSearchCV(
      estimator=final_preprocessing,
      param_distributions=param_dist,
      n_iter=3,
      verbose=2,
      cv=3,
      scoring='accuracy',
      n_jobs=-1
    )

    grid.fit(x_train, y_train)
    

    joblib.dump(grid, filename)
    logger.info(f'saved to {filename}')
    
  except Exception as e:
    logger.exception(f'the error {e}')
  return None


if __name__ == "__main__":
  train_model()