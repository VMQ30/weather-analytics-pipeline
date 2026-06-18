import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from extract import extract
from transform import transform
from load import load

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
cities = extract(engine, API_KEY)
CLEANED_CITIES = transform(cities)
load(CLEANED_CITIES, engine)
