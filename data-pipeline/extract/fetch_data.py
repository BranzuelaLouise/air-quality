import os
import requests
import json
from dotenv import load_dotenv
from unidecode import unidecode
from ..config.settings import COUNTRY   # Import settings for the COUNTRY constant

# Specify where the .env file is in the directory and load it
env_path = "../config/.env"
load_dotenv(dotenv_path=env_path)

# Get API key from the .env file
api_key = os.getenv("WAQI_API_KEY")

# Base URL of the API
base_url = "https://api.waqi.info/"


def fetch_stations(country_name):
    # Fetch the data from stations through the search endpoint using the country as the keyword.
    url = f"{base_url}/search/?token={api_key}&keyword={country_name}"

    # Send the GET request
    response = requests.get(url)
    data = response.json()

    # Check if request was successful
    if response.status_code != 200 or data['status'] != "ok":
        print(f"Failed to fetch cities list. Status code: {response.status_code}")
        return None

    return data['data']


def save_data(data, station_name):
    # Unidecode to transliterate unicode string to the closest representation in ASCII text.
    filename = (unidecode(station_name).
                replace(COUNTRY, "").   # Remove country name
                replace(",", "").   # Remove commas
                replace(" ", "_").  # Replace spaces with underscore for readability
                lower())

    # Define file path output
    output_path = os.path.join("../", "raw-data", f"{filename}_air_quality.json")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the data as a JSON file
    with open(output_path, "w") as outfile:
        json.dump(data, outfile, indent=4)
    print(f"Data for {station_name} saved successfully.")


if __name__ == "__main__":
    # Fetch the stations and their data through the country's name
    stations = fetch_stations(COUNTRY)

    # Loop over the stations in the fetched data and save it
    if stations:
        for station in stations:
            save_data(station, station['station']['name'])
