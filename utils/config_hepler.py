import os
import json

def load_config():
  app_env = os.getenv('APP_ENV', 'dev')

  config_path = f'config/config.{app_env}.json'
  
  with open(config_path, 'r') as f:
    return json.load(f)
  
