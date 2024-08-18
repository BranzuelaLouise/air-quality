import schedule
import time
import os
from data_pipeline.extract.fetch_data import fetch_stations, save_data
from data_pipeline.load.database import load_data
from data_pipeline.config.settings import cities


def job():
    for city in cities:
        air_data = fetch_stations(city)
        if air_data:
            save_data(air_data, city)

    raw_data_dir = os.path.join("../", "raw-data")
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            load_data(file_path, filename)


# Schedule the job to run every hour
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

