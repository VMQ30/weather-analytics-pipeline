import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dotenv import load_dotenv


st.set_page_config(page_title="Weather Analytics BI Dashboard", layout="wide")
st.title("Real-Time Weather Analytics Dashboard")


load_dotenv()
DB_URL = os.getenv("DB_URL")


@st.cache_data(ttl=60)
def load_historical_data():
    engine = create_engine(DB_URL)
    query = "SELECT * FROM cities_weather_info ORDER BY date DESC, time DESC;"
    df = pd.read_sql(query, con=engine)
    return df


try:
    df = load_historical_data()

    if df.empty:
        st.warning("Database table is empty. Run the ETL pipeline to add data!")
    else:
        st.sidebar.header("Filter Options")
        city_list = sorted(df["city"].unique())
        selected_city = st.sidebar.selectbox("Select a City", city_list)

        city_df = df[df["city"] == selected_city]

        st.subheader(f"Current Metrics for {selected_city}")
        col1, col2, col3, col4 = st.columns(4)

        latest_row = city_df.iloc[0]
        col1.metric("Temperature", f"{latest_row['temperature_c']} °C")
        col2.metric("Feels Like", f"{latest_row['feels_like_c']} °C")
        col3.metric("Humidity", f"{latest_row['humidity_pct']}%")
        col4.metric("Wind Condition", latest_row["wind_force_scale"])

        st.markdown("---")
        st.subheader("Historical Trends")

        fig_temp = px.line(
            city_df,
            x="time",
            y=["temperature_c", "feels_like_c"],
            title="Temperature vs. Feels Like over Time",
            labels={"value": "Temperature (°C)", "time": "Time of Day"},
            markers=True,
        )
        st.plotly_chart(fig_temp, use_container_width=True)

        st.markdown("---")
        st.subheader("Extreme Conditions Log")
        extreme_events = city_df[
            city_df["is_extreme_heat"] | city_df["is_extreme_cold"]
        ]
        if not extreme_events.empty:
            st.dataframe(
                extreme_events[
                    [
                        "date",
                        "time",
                        "temperature_c",
                        "is_extreme_heat",
                        "is_extreme_cold",
                    ]
                ],
                use_container_width=True,
            )
        else:
            st.success("No extreme weather events recorded for this city!")

except Exception as e:
    st.error(f"Could not connect to the database dashboard layer: {e}")
