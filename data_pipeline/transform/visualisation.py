import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Data Validation
with sqlite3.connect('../../database/air_quality.db') as conn:
    df = pd.read_sql("SELECT * FROM air_quality", conn)

df['time'] = df['time'].str.split(' ').str[0]
df['time'] = pd.to_datetime(df['time'])
df = df.groupby(['time', 'station'])['aqi'].mean().reset_index()
df['aqi'] = np.floor(df['aqi']).astype(int)

# Group data by city
df['year'] = df['time'].dt.year

# Group data by year
grouped_by_year = df.groupby('year')

# Create subplots
fig, axes = plt.subplots(nrows=len(grouped_by_year), figsize=(10, 6 * len(grouped_by_year)))

# Iterate over years and create plots
for i, (year, group) in enumerate(grouped_by_year):
    ax = axes[i]
    grouped = group.groupby('station')

    for name, city_group in grouped:
        ax.plot(city_group['time'], city_group['aqi'], label=name)

    ax.set_title(f"AQI {year}")
    ax.set_xlabel('Time')
    ax.set_ylabel('AQI')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.legend()

plt.tight_layout()
plt.show()

