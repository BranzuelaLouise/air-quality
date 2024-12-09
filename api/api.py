from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import sqlite3

app = Flask(__name__)
# Allow all origins in development
CORS(app)


# API route for air quality data
@app.route('/api/air-quality')
def air_quality():
    with sqlite3.connect(f'database/air_quality.db') as conn:
        air_quality_df = pd.read_sql("SELECT * FROM air_quality", conn)

    air_quality_df['time'] = air_quality_df['time'].str.split(' ').str[0]
    air_quality_df['time'] = pd.to_datetime(air_quality_df['time'])
    air_quality_df = air_quality_df.groupby(['time', 'station'])['aqi'].mean().reset_index()
    air_quality_df['aqi'] = air_quality_df['aqi'].apply(lambda x: int(x))
    air_quality_df = air_quality_df.sort_values(by='time')

    # Convert the DataFrame to JSON
    air_quality_json = air_quality_df.to_dict(orient='records')

    # Return the data as JSON
    return jsonify(air_quality_json)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')