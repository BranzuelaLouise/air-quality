import sqlite3
import pandas as pd
import numpy as np

# Data Validation
with sqlite3.connect(f'../../database/air_quality.db') as conn:
    df = pd.read_sql("SELECT * FROM air_quality", conn)

df['time'] = df['time'].str.split(' ').str[0]
df['time'] = pd.to_datetime(df['time'])
df = df.groupby(['time', 'station'])['aqi'].mean().reset_index()
df['aqi'] = np.floor(df['aqi']).astype(int)

df.to_json('test.json', orient='values')
