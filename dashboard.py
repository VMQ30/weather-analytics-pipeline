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
def load_historical_data(days_filter=int):
    engine = create_engine(DB_URL)
    query = f"""
    SELECT * 
    FROM cities_weather_info
    WHERE
        date >= CURRENT_DATE - INTERVAL '{days_filter} days'
    ORDER BY 
        date DESC , 
        time DESC
    """
    return pd.read_sql(query, con=engine)


try:
    st.sidebar.header("Dashboard Configuration")
    time_window = st.sidebar.selectbox(
        "Select Timeframe",
        options=[7, 14, 30, 90, 365],
        format_func=lambda x: f"Last {x} Days",
    )

    df = load_historical_data(time_window)

    if df.empty:
        st.warning(
            f"Database table is empty for the last {time_window} days. Run your ETL pipeline."
        )
    else:
        city_list = sorted(df["city"].unique())
        selected_city = st.sidebar.selectbox("Select a City", city_list)

        city_df = df[df["city"] == selected_city]
        city_df["datetime"] = pd.to_datetime(
            city_df["date"].astype(str) + " " + city_df["time"].astype(str)
        )
        city_df = city_df.sort_values(by="datetime", ascending=False).reset_index(
            drop=True
        )

        st.subheader(f"Latest Conditions for {selected_city}")

        if len(city_df) >= 1:
            latest_row = city_df.iloc[0]
            temp_delta, humidity_delta = None, None

            if len(city_df) > 1:
                prev_row = city_df.iloc[1]
                temp_delta = round(
                    float(latest_row["temperature_c"] - prev_row["temperature_c"]), 2
                )
                humidity_delta = int(
                    latest_row["humidity_pct"] - prev_row["humidity_pct"]
                )

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature", f"{latest_row['temperature_c']} °C")
        col2.metric("Feels Like", f"{latest_row['feels_like_c']} °C")
        col3.metric("Humidity", f"{latest_row['humidity_pct']}%")
        col4.metric("Wind Condition", latest_row["wind_force_scale"])

        st.markdown("---")
        st.subheader(f"Historical Summary ({time_window} Days Window)")

        max_col, min_col, mean_col = st.columns(3)
        max_col.metric(
            "HIghest Recorded Temperature", f"{city_df['temperature_c'].max()} °C"
        )
        min_col.metric(
            "Lowest Recorded Temperature", f"{city_df['temperature_c'].min()} °C"
        )
        mean_col.metric(
            "Average Recorded Temperature",
            f"{round(city_df['temperature_c'].mean(), 2)} °C",
        )

        st.markdown("---")
        st.subheader("Analytics & Historical Trends")
        tab1, tab2, tab3 = st.tabs(
            ["Thermals", "Atmosphere & Dynamics", "Distribution Breakdown"]
        )

        plotly_template = (
            "plotly_dark"
            if "dark" in st.get_option("theme.backgroundColor").lower()
            else "plotly"
        )

        with tab1:
            fig_temp = px.line(
                city_df,
                x="datetime",
                y=["temperature_c", "feels_like_c"],
                title="Temperature vs. Feels Like over Time",
                labels={"value": "Temperature (°C)", "datetime": "Timeline"},
                markers=True,
            )
            st.plotly_chart(fig_temp, use_container_width=True)

        with tab2:
            fig_wind_humidity = px.bar(
                city_df,
                x="datetime",
                y="humidity_pct",
                title="Humidity Tracking Over Time",
                labels={"humidity_pct": "Humidity (%)", "datetime": "Timeline"},
                template="plotly_dark",
            )
            st.plotly_chart(fig_wind_humidity, use_container_width=True)

        with tab3:
            d_col1, d_col2 = st.columns(2)

            with d_col1:
                fig_hist = px.histogram(
                    city_df,
                    x="temperature_c",
                    nbins=15,
                    title="Temperature Variance & Spread Density",
                    labels={"temperature_c": "Temperature (°C)", "count": "Frequency"},
                    color_discrete_sequence=["#FF4B4B"],
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            with d_col2:
                # Grouping by category to show dynamic wind layout percentages
                wind_counts = city_df["wind_force_scale"].value_counts().reset_index()
                wind_counts.columns = ["Wind Force", "Count"]

                fig_pie = px.pie(
                    wind_counts,
                    values="Count",
                    names="Wind Force",
                    title="Wind Scale Distribution Mix",
                    hole=0.4,
                )
                st.plotly_chart(fig_pie, use_container_width=True)

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
            st.success("No extreme weather anomalies recorded")

except Exception as e:
    st.error(f"Could not connect to the database dashboard layer: {e}")
