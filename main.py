from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datetime
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Laden der Umgebungsvariablen aus der .env-Datei

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_data(hours=1):
    now = datetime.datetime.now(datetime.timezone.utc)
    end_time = now.replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=1)
    start_time = end_time - datetime.timedelta(hours=hours)

    start_time_str = start_time.isoformat()
    end_time_str = end_time.isoformat()

    url = "https://api.hystreet.com/locations/257"
    querystring = {"from": start_time_str, "to": end_time_str, "resolution": "hour"}
    headers = {
        "Content-Type": "application/json",
        "X-API-Token": os.getenv("API_TOKEN")
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        if 'measurements' not in data:
            raise ValueError("The key 'measurements' is not in the JSON response.")
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

def convert_to_dataframe(data):
    dataset_columns = [
        'location', 'timestamp', 'weekday', 'pedestrians_count', 'weather_condition', 'temperature'
    ]

    rows = []
    for measurement in data['measurements']:
        timestamp = measurement['timestamp']
        row = [
            '257',  # location ID as provided in the URL
            timestamp,  # timestamp
            datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%A'),  # weekday
            measurement['pedestrians_count'],  # pedestrians count
            measurement['weather_condition'],  # weather condition
            measurement['temperature']  # temperature
        ]
        rows.append(row)

    df = pd.DataFrame(rows, columns=dataset_columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S.%f%z')
    return df

@app.get("/fetch_last_hour_data")
def fetch_last_hour_data():
    raw_data = fetch_data(hours=1)
    df = convert_to_dataframe(raw_data)
    return df.to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

