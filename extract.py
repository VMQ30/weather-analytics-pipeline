import os
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)


def get_cities():
    q = "SELECT name FROM cities WHERE is_active = true;"
    df_cities = pd.read_sql(q, con=engine)
    return df_cities["name"].tolist()


def extract_weather_data(cities):
    weather_records = []

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            record = {
                "city": city,
                "temperature_c": data["main"]["temp"],
                "feels_like_c": data["main"]["feels_like"],
                "humidity_pct": data["main"]["humidity"],
                "wind_speed_mps": data["wind"]["speed"],
                "weather_condition": data["weather"][0]["main"],
                "extracted_at": datetime.now(),
            }
            weather_records.append(record)

    return pd.DataFrame(weather_records)


cities = get_cities()
df = extract_weather_data(cities)
print(df.columns)
print(df.dtypes)
print(df)
