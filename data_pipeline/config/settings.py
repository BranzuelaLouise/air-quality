import pycountry
import pandas as pd

# Global config for the country
COUNTRY = "New Zealand"  # Replace with country of interest
env_path = "../config/.env"  # Change with the path for env if making one in a different directory
code = pycountry.countries.get(name=COUNTRY).alpha_2  # Country Code

# Get the cities from country code
df = pd.read_csv("../historical-data/waqi-covid19-airqualitydata-2019Q1.csv", skiprows=4)
cities = df[df['Country'] == code]['City'].unique()

pm10_breakpoints = [
    (0, 50, 0, 54),  # Good
    (51, 100, 55, 154),  # Moderate
    (101, 150, 155, 254),  # Unhealthy for Sensitive Groups
    (151, 200, 255, 354),  # Unhealthy
    (201, 300, 355, 424),  # Very Unhealthy
    (301, 400, 425, 504),  # Hazardous
    (401, 500, 505, 604)  # Hazardous
]