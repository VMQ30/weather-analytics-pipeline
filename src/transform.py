import logging
import pandas as pd
import numpy as np


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


def transform(cities):
    if cities.empty:
        logging.warning("Received an empty DataFrame. Skipping transformation stage.")
        return cities

    logging.info("Starting transformation on extracted data")
    cities["extracted_at"] = pd.to_datetime(cities["extracted_at"])
    cities["date"] = cities["extracted_at"].dt.date
    cities["time"] = cities["extracted_at"].dt.time
    cities["day_of_the_week"] = cities["extracted_at"].dt.day_name()

    ranges = [
        0,
        0.2,
        1.5,
        3.3,
        5.4,
        7.9,
        10.7,
        13.8,
        17.1,
        20.7,
        24.4,
        28.4,
        32.6,
        np.inf,
    ]
    group_names = [
        "Calm",
        "Light Air",
        "Light Breeze",
        "Gentle Breeze",
        "Moderate Breeze",
        "Fresh Breeze",
        "Strong Breeze",
        "Moderate Gale",
        "Gale",
        "Strong Gale",
        "Storm",
        "Violent Storm",
        "Hurricane",
    ]

    cities["wind_force_scale"] = pd.cut(
        cities["wind_speed_mps"], bins=ranges, labels=group_names, include_lowest=True
    )

    cities["is_extreme_heat"] = cities["temperature_c"] > 35
    cities["is_extreme_cold"] = cities["temperature_c"] < -10

    cities["humidity_pct"] = cities["humidity_pct"].astype("int8")
    cities["weather_condition"] = cities["weather_condition"].astype("category")
    cities["day_of_the_week"] = cities["day_of_the_week"].astype("category")

    cities = cities.drop(columns="extracted_at")

    logging.info("Finished transforming the extracted data")
    return cities
