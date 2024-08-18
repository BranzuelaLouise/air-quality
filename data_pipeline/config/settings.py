import pycountry
import pandas as pd
import os

# Global config for the country
COUNTRY = "New Zealand"  # Replace with country of interest
env_path = "../config/.env"  # Change with the path for env if making one in a different directory
code = pycountry.countries.get(name=COUNTRY).alpha_2  # Country Code

# Get the cities from country code
# Reading every historical csv file to make sure that we get all the cities
# This is due to some of them not having a measurement for the city at the time
final_df = pd.DataFrame()
historical_data_dir = os.path.join("../", "historical-data")
for filename in os.listdir(historical_data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(historical_data_dir, filename)
        df = pd.read_csv(file_path, skiprows=4)
        final_df = pd.concat([final_df, df])

cities = final_df[final_df['Country'] == code]['City'].unique()


pm10_breakpoints = [
    (0, 50, 0, 54),  # Good
    (51, 100, 55, 154),  # Moderate
    (101, 150, 155, 254),  # Unhealthy for Sensitive Groups
    (151, 200, 255, 354),  # Unhealthy
    (201, 300, 355, 424),  # Very Unhealthy
    (301, 400, 425, 504),  # Hazardous
    (401, 500, 505, 604)  # Hazardous
]