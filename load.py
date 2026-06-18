import logging


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)


def load(cities, engine):
    if cities.empty:
        logging.warning("DataFrame is empty. Skipping database load stage.")
        return

    logging.info("Attempting to load transformed data to database")
    try:
        cities.to_sql(
            name="cities_weather_info",
            con=engine,
            if_exists="append",
            index=False,
        )
        logging.info("Successfully loaded transformed data to the database")
    except Exception as e:
        logging.error(f"Failed to load data into the database: {e}")
