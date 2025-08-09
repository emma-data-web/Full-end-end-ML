def age_fare(df):
  df = df.copy()

  df['age_fare'] = df['Age'] + df['Fare']
  return df


def age_parch(df)