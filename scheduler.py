import time
import logging
import schedule
from main import run_pipeline


logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(message)s", level=logging.INFO
)


def pipeline_schedule():
    logging.info("Running scheduled ETL pipeline run")
    try:
        run_pipeline()
    except Exception as e:
        logging.error(f"Scheduler intercepted a pipeline failure: {e}")


schedule.every(1).hours.do(pipeline_schedule)


if __name__ == "__main__":
    logging.info("Weather Analytics Scheduler started successfully.")
    logging.info("Pipeline is scheduled to run every day at 12:00nn")

    while True:
        schedule.run_pending()
        time.sleep(1)
