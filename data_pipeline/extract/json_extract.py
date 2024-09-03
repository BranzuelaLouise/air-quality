import sqlite3
import pandas as pd
import numpy as np
from data_pipeline.config.settings import COUNTRY

# Data Validation
with sqlite3.connect(f'../../database/{COUNTRY}.db') as conn:
    df = pd.read_sql("SELECT * FROM air_quality", conn)

df['time'] = df['time'].str.split(' ').str[0]
df['time'] = pd.to_datetime(df['time'])
df = df.groupby(['time', 'station'])['aqi'].mean().reset_index()
df['aqi'] = np.floor(df['aqi']).astype(int)

df.to_json('test.json', orient='values')
