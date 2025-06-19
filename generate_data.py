import pandas as pd #Data manipulation, reading/writing CSV files.
import numpy as np #to generate random dta for the synthies dataset 
from datetime import datetime, timedelta #datetime use generating the data and time  and timedelta for incrementing the date and time
num_records = 100 # number of row to generate the dataset
start_date = datetime(2025, 1, 1) #starting data
crop_types = ['Corn', 'Wheat', 'Tomato','paddy'] #listing number of crops
data = [] #to store generated data
for i in range(num_records):
    date = start_date + timedelta(days=i // 24) #to generte the different date for new date
    time = f"{(i % 24):03d}:00"#genrating the time
    soil_moisture = np.random.randint(0, 101)  # 0-100% soil moisture
    temperature = np.random.uniform(15, 36)  # 15-36 °C
    humidity = np.random.randint(25, 100)  # 25-100% humidity
    rainfall = np.random.uniform(0, 30)  # 0-30 mm rain fall
    irrigation_amount = np.random.randint(0, 100)  # 0-100 liters water well pumped
    crop_type = np.random.choice(crop_types)
    irrigation_status = 1 if soil_moisture < 30 else 0  # Irrigate the soil if soil moisture is below 30% 
    data.append([date.strftime('%Y-%m-%d'), time, soil_moisture, temperature, humidity, rainfall, irrigation_amount, crop_type, irrigation_status])
df = pd.DataFrame(data, columns=['Date', 'Time', 'Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)', 'Irrigation Amount (liters)', 'Crop Type', 'Irrigation Status']) # storing the data in dataframe
df.to_csv('irrigation_dataset.csv', index=False) #index is false to not ensure the row numbers
print(df.head())