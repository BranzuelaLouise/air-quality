import os
import json
import sqlite3


def create_table():
    conn = sqlite3.connect('air_quality.db')
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
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO air_quality (station, aqi, time)
        VALUES (?, ?, ?)
    ''', (station, aqi, time))
    conn.commit()
    conn.close()


def load_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
        station = data['station']['name']
        aqi = data['aqi']
        time = data['time']['stime']
        insert_data(station, aqi, time)


if __name__ == "__main__":
    create_table()
    # Load and store data from the raw JSON files
    raw_data_dir = os.path.join("../", "raw-data")
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            load_data(file_path)
