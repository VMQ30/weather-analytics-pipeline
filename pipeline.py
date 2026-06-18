from extract import extract
from transform import transform

cities = extract()
cleaned_cities = transform(cities)
