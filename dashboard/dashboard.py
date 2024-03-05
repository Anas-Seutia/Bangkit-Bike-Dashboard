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

# Set up the figure size and style
fig, ax = plt.subplots(figsize=(16, 8))
sns.set(style="whitegrid")  # Set the seaborn style

# Plot the data
ax.plot(
    daily_rides_df["dteday"],
    daily_rides_df["total_rides"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

# Set the title and labels
ax.set_title('Average Bike Rentals per Month', fontsize=20)
ax.set_xlabel('Month', fontsize=16)
ax.set_ylabel('Average Rentals', fontsize=16)

ax.tick_params(axis='x', rotation=45)
ax.tick_params(axis='y', labelsize=12)

ax.set_yticks(range(0, 10000, 500))
ax.set_ylim(bottom=0)

ax.set_xlim([daily_rides_df["dteday"].min(), daily_rides_df["dteday"].max()])

ax.grid(True)

st.pyplot(fig)


# Plot rides by weather condition
st.subheader('Rides by Weather Condition')

fig, ax = plt.subplots(figsize=(8, 5))
sns.set(style="whitegrid")  # Set the seaborn style

sns.barplot(
    x=weather_df['weather_condition'],
    y=weather_df['total_rides'],
    hue=weather_df['weather_condition'],
    palette='muted',
    ax=ax
)

ax.set_title('Average Bike Rentals by Weather Condition', fontsize=18)
ax.set_xlabel('Weather Condition', fontsize=15)
ax.set_ylabel('Average Rentals', fontsize=15)

ax.set_ylim(0, weather_df['total_rides'].max() + 0.5e6) 

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

ax.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(fig)



st.caption('By Anas Banta Seutia - for Bangkit :)')
