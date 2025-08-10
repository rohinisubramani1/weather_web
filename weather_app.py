import os
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

API_KEY = "b897479a1a149177fa82e4074faa9725"
file_path = r"C:\Users\Rohini S\Downloads\Weather Data.csv"

if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["date", "city", "temp_C", "humidity_%"])
    df.to_csv(file_path, index=False)
else:
    df = pd.read_csv(file_path)

st.title("Live Weather Tracker 🌤️")
CITY = st.text_input("Enter city name:")

if st.button("Get Weather") and CITY:
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(URL)

    if response.status_code != 200:
        st.error(f"Error: {response.status_code} - {response.text}")
    else:
        weather_data = response.json()
        new_row = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": CITY,
            "temp_C": weather_data['main']['temp'],
            "humidity_%": weather_data['main']['humidity']
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success("Weather data added!")
        st.write(new_row)

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(
            [new_row["temp_C"], new_row["humidity_%"]],
            labels=["Temperature (°C)", "Humidity (%)"],
            autopct='%1.1f%%',
            colors=['orange', 'skyblue']
        )
        ax.set_title(f"Temp vs Humidity for {CITY}")
        st.pyplot(fig)

        st.subheader("Historical Data")
        st.dataframe(df)
