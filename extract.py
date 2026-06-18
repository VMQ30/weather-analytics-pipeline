from datetime import datetime
import logging
import requests
import pandas as pd


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


def get_cities(engine):
    q = "SELECT name FROM cities WHERE is_active = true;"
    logging.info("Fetching active cities list from the database")
    try:
        df_cities = pd.read_sql(q, con=engine)
        logging.info("Successfully extracted active cities list")
        return df_cities["name"].tolist()
    except Exception as e:
        logging.error("Failed to extract cities from database: {e}")
        return []


def extract(engine, API_KEY):
    cities = get_cities(engine)

    if not cities:
        logging.warning(
            "No active cities found or failed to fetch city list. Skipping API extraction"
        )
        return pd.DataFrame()

    weather_records = []
    logging.info("Fetching weather information of active cities")

    try:
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

            else:
                logging.warning(
                    f"Failed to fetch data for {city}. HTTP Status: {response.status_code}"
                )
        logging.info(
            f"Successfully extracted weather information for {len(weather_records)}/{len(cities)} cities"
        )
        return pd.DataFrame(weather_records)

    except Exception as e:
        logging.error(f"Failed to extract weather information from API: {e}")
        return pd.DataFrame()
