import schedule
import time
from data_pipeline.extract.fetch_data import fetch_stations, save_data
from data_pipeline.config.settings import COUNTRY


def job():
    stations = fetch_stations(COUNTRY)

    if stations:
        for station in stations:
            save_data(station, station['station']['name'])


# Schedule the job to run every hour
schedule.every().hour.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

