from utils.db_pull import get_data

df = get_data()

def age_fare(df):
  df = df.copy()

  df['age_fare'] = df['Age'] + df['Fare']
  return df


def age_parch(df):
  df = df.copy()

  df['age_parch'] = df['Age'] + df['Parch']
  return df


def add_features(df):
  df = age_fare(df)
  df = age_parch(df)

  return df


test_x = df.copy()
new = add_features(test_x)

#print(new)

