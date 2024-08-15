import requests
import json
import os
from dotenv import load_dotenv
from unidecode import unidecode
from data_pipeline.config.settings import COUNTRY, cities, env_path

# Load env file
load_dotenv(dotenv_path=env_path)

# Get API key from the .env file
api_key = os.getenv("WAQI_API_KEY")

# Base URL of the API
base_url = "https://api.waqi.info/"


def fetch_stations(city_name):
    # Fetch the data from stations through the search endpoint using the country as the keyword.
    url = f"{base_url}/feed/{city_name}/?token={api_key}"

    # Send the GET request
    response = requests.get(url)
    data = response.json()

    # Check if request was successful
    if response.status_code != 200 or data['status'] != "ok":
        print(f"Failed to fetch cities list. Status code: {response.status_code}")
        return None

    return data['data']


def save_data(data, city_name):
    # Define file path output
    output_path = os.path.join("../", "raw-data", f"{city_name}.json")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the data as a JSON file
    with open(output_path, "w") as outfile:
        json.dump(data, outfile, indent=4)
    print(f"Data for {city_name} saved successfully.")


if __name__ == "__main__":
    # Loop for each city in the cities list to fetch the air quality data
    for city in cities:
        air_data = fetch_stations(city)
        if air_data:
            save_data(air_data, city)
