import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mydatabase.db')

df = pd.read_sql('SELECT * FROM users', engine)
print(df)
new_df = pd.DataFrame({'id': [3], 'username': ["panda"],"password": ["pandas"]})
new_df.to_sql('users', engine, if_exists='append',index=False)
df = pd.read_sql('SELECT * FROM users', engine)
print(df)