import math
import pandas as pd
import numpy as np
import os
from data_pipeline.config.settings import code, pm10_breakpoints


def pm10_to_aqi(value):
    for bp in pm10_breakpoints:
        if bp[2] <= value <= bp[3]:
            aqi = (bp[1] - bp[0]) / (bp[3] - bp[2]) * (value - bp[2]) + bp[0]
            return math.floor(aqi)

    # If the value is outside the expected range, return None
    return None


def process_historical():
    final_df = pd.DataFrame()
    historical_data_dir = os.path.join("../", "historical-data")
    for filename in os.listdir(historical_data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(historical_data_dir, filename)
            df = pd.read_csv(file_path, skiprows=4)
            df = clean_historical(df)
            final_df = pd.concat([final_df, df])
    return final_df


def clean_historical(df):
    # Remove all the other types of measurements that aren't pm10
    df = df.loc[df.Specie.isin(['pm10'])]

    # Keep only relevant columns (Date, City, Specie and Median)
    df = df[df['Country'] == code].drop(columns=['Country', 'count', 'min', 'max', 'variance'])

    # Pivot the DataFrame so that it has pm10 as a column
    df = df.pivot(index=['City', 'Date'], columns='Specie', values='median').reset_index()

    # Make sure that there's a column for pm10 even when there are no records for it
    if 'pm10' not in df.columns:
        df['pm10'] = np.nan

    # Apply pm10_to_aqi function to get the aqi for pm10
    df['pm10_aqi'] = df['pm10'].apply(pm10_to_aqi)

    return df
