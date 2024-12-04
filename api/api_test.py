import requests
import pandas as pd

# Fetch data from the API
response = requests.get("http://127.0.0.1:5000/api/air-quality")

if response.status_code == 200:
    air_quality_data = response.json()

    # Convert JSON data to a DataFrame
    air_quality_df = pd.DataFrame(air_quality_data)

    # Check if data is ordered
    time_values = pd.to_datetime(air_quality_df['time']).values
    is_ordered = all(time_values[i] <= time_values[i + 1] for i in range(len(time_values) - 1))

    if is_ordered:
        print("Data is ordered correctly.")
    else:
        print("Data is NOT ordered.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
