import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src import extract, transform, load


logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def run_pipeline():
    logging.info("=============================================")
    logging.info("Starting Weather Analytics ETL Pipeline Run")
    logging.info("=============================================")

    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DB_URL = os.getenv("DB_URL")

    if not API_KEY or not DB_URL:
        logging.critical(
            "Missing environment variables (API_KEY or DB_URL). Aborting pipeline."
        )
        return

    try:
        engine = create_engine(DB_URL)
        cities = extract(engine, API_KEY)
        transformed_cities = transform(cities)
        load(transformed_cities, engine)
        logging.info("=============================================")
        logging.info("Weather Analytics ETL Pipeline Run completed successfully.")
        logging.info("=============================================")
    except Exception as e:
        logging.critical(f"Pipeline crashed due to an unexpected unhandled error: {e}")


if __name__ == "__main__":
    run_pipeline()
