def load(cities, engine):
    try:
        cities.to_sql(
            name="cities_weather_info",
            con=engine,
            if_exists="append",
            index=False,
        )
    except Exception as e:
        print(f"Database insertion failed: {e}")
