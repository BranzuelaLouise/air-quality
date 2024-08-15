import os
import json
import sqlite3
from data_pipeline.transform.transform_historical import process_historical


def create_table():
    conn = sqlite3.connect('../../database/air_quality.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_quality (
            station TEXT,
            aqi INTEGER,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_data(station, aqi, time):
    conn = sqlite3.connect('../../database/air_quality.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO air_quality (station, aqi, time)
        VALUES (?, ?, ?)
    ''', (station, aqi, time))
    conn.commit()
    conn.close()


def load_data(path, name):
    with open(path, 'r') as f:
        data = json.load(f)
        aqi = data['aqi']

        # Get the city's name from the file's name
        station = name.replace('.json', '').capitalize()

        # The 's' field is sometimes missing for when there are no measurements on the API
        try:
            time = data['time']['s']
        except KeyError:
            return None

        # Make sure record is more up-to-date than the latest record in the database
        with sqlite3.connect('../../database/air_quality.db') as conn:
            cursor = conn.cursor()
            latest_time = cursor.execute('SELECT MAX(time) FROM air_quality').fetchone()[0]

            # For when the database has no records
            try:
                if time > latest_time:
                    insert_data(station, aqi, time)
            except TypeError:
                # Load historical data if not loaded already
                df = process_historical()
                for index, row in df.iterrows():
                    insert_data(row['City'], row['pm10_aqi'], row['Date'])
                insert_data(station, aqi, time)
                return None


if __name__ == "__main__":
    create_table()
    # Load and store data from the raw JSON files
    raw_data_dir = os.path.join("../", "raw-data")
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            load_data(file_path, filename)
