import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper functions for preparing various dataframes
def create_daily_rides_df(df):
    daily_rides_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_rides_df = daily_rides_df.reset_index()
    daily_rides_df.rename(columns={
        "cnt": "total_rides"
    }, inplace=True)
    
    return daily_rides_df

def create_weather_df(df):
    weather_df = df.groupby("weathersit").agg({
        "cnt": "sum"
    }).reset_index()
    weather_df.rename(columns={
        "cnt": "total_rides",
        "weathersit": "weather_condition"
    }, inplace=True)
    weather_conditions = {
        1: "Clear",
        2: "Mist + Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow"
    }
    weather_df["weather_condition"] = weather_df["weather_condition"].map(weather_conditions)
    
    return weather_df

# Load data
bike_df = pd.read_csv("./dashboard/data.csv")

# Convert 'dteday' column to datetime
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Filter data
min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

with st.sidebar:
    # Taking start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Time Range', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df["dteday"] >= pd.to_datetime(start_date)) &
                  (bike_df["dteday"] <= pd.to_datetime(end_date))]

# Prepare various dataframes
daily_rides_df = create_daily_rides_df(main_df)
weather_df = create_weather_df(main_df)

# Plot number of daily rides
st.subheader('Daily Rides')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rides_df["dteday"],
    daily_rides_df["total_rides"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Plot rides by weather condition
st.subheader('Rides by Weather Condition')

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="weather_condition",
    y="total_rides",
    data=weather_df,
    palette="Blues_d",
    ax=ax
)
ax.set_ylabel("Total Rides")
ax.set_xlabel("Weather Condition")
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)


st.caption('By Anas Banta Seutia - for Bangkit :)')
