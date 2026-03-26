# 🌱 Smart Irrigation System

A machine learning-powered web application that predicts crop irrigation needs based on real-time soil moisture, temperature, humidity, and rainfall data. The system helps farmers optimize water usage by intelligently deciding **when** and **how much** to irrigate — replacing rigid fixed schedules with data-driven decisions.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#-usage)
  - [Web Dashboard](#web-dashboard)
  - [REST API](#rest-api)
  - [Google Sheets Integration (Optional)](#google-sheets-integration-optional)
- [ML Model](#-ml-model)
  - [Dataset](#dataset)
  - [Training](#training)
- [Code Overview](#-code-overview)
  - [app.py — Flask Application](#apppy--flask-application)
  - [generate_data.py — Dataset Generation](#generate_datapy--dataset-generation)
  - [train_model.py — Model Training](#train_modelpy--model-training)
  - [upload_google_sheet.py — Google Sheets Sync](#upload_google_sheetpy--google-sheets-sync)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **ML-Based Irrigation Prediction** — Uses a trained Random Forest model to predict irrigation needs from soil and weather sensor data.
- **Multi-Crop Monitoring** — Tracks multiple crops (Tomatoes, Lettuce, Carrots, Corn, Wheat, Paddy) with individual moisture thresholds.
- **Three-State Irrigation Status** — Each crop is classified as `Idle`, `Scheduled`, or `Watering` in real time.
- **4-Day Weather Forecast** — Displays upcoming temperature and rainfall forecasts to help plan irrigation.
- **REST API** — Exposes a JSON endpoint for external sensor integration.
- **Google Sheets Integration** — Optionally sync your dataset to Google Sheets for remote monitoring and data sharing.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Machine Learning | scikit-learn (RandomForestClassifier), joblib |
| Data Processing | pandas, NumPy |
| Frontend | HTML5, Bootstrap 5.3, Jinja2 |
| Data Storage | CSV files, Pickle (model) |
| Cloud Integration | Google Sheets API (gspread, google-auth) |

---

## 📁 Project Structure

```
Smart-irrigation/
├── app.py                    # Flask web application & API endpoints
├── train_model.py            # ML model training script
├── generate_data.py          # Synthetic dataset generation script
├── upload_google_sheet.py    # Google Sheets upload integration
├── irrigation_dataset.csv    # Training dataset (root copy)
├── irrigation_model.pkl      # Trained RandomForest model (serialized)
├── data/
│   └── irrigation_dataset.csv  # Training dataset (data/ copy)
└── templates/
    └── index.html            # Web dashboard HTML template
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/vivvek69/Smart-irrigation.git
   cd Smart-irrigation
   ```

2. **Install dependencies:**

   ```bash
   pip install flask pandas numpy scikit-learn joblib gspread google-auth google-auth-oauthlib
   ```

3. **Generate the synthetic dataset:**

   ```bash
   python generate_data.py
   ```

   This creates `irrigation_dataset.csv` with 100 synthetic records containing soil moisture, temperature, humidity, rainfall, crop type, and irrigation status.

4. **Train the ML model:**

   ```bash
   python train_model.py
   ```

   This loads the dataset, trains a `RandomForestClassifier`, prints the model accuracy, and saves the model to `irrigation_model.pkl`.

### Running the Application

```bash
python app.py
```

The server starts in debug mode. Open your browser and navigate to:

```
http://localhost:5000/
```

---

## 📖 Usage

### Web Dashboard

The dashboard provides an at-a-glance view of your irrigation system:

| Section | Description |
|---|---|
| **Weather Forecast** | 4-day forecast showing temperature (°C) and rainfall (mm) |
| **Crop Status** | Real-time moisture levels and irrigation state for each crop |
| **Irrigation Status** | `Idle` · `Scheduled` · `Watering` indicators per crop |

**Status Logic:**

| Status | Condition |
|---|---|
| `Watering` | Current soil moisture < (optimal moisture − 10%) |
| `Scheduled` | Current moisture < optimal, but above the urgent threshold |
| `Idle` | Current moisture ≥ optimal moisture level |

### REST API

#### `GET /get_irrigation_status`

Predicts the irrigation amount required based on soil sensor input.

**Query Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `soil_moisture` | float | Current soil moisture percentage (0–100) |
| `humidity` | float | Current air humidity percentage (0–100) |

**Example Request:**

```
GET /get_irrigation_status?soil_moisture=25&humidity=60
```

**Example Response:**

```json
{
  "predicted_irrigation_amount": 42.5
}
```

### Google Sheets Integration (Optional)

To sync your irrigation dataset to a Google Sheet:

1. Create a **Google Cloud project** and enable the **Google Sheets API** and **Google Drive API**.
2. Create a **Service Account** and download the `credentials.json` key file.
3. Place `credentials.json` in the project root directory.
4. Update the email in `upload_google_sheet.py` with your Google account email.
5. Run:

   ```bash
   python upload_google_sheet.py
   ```

This will create (or update) a Google Sheet named **"Irrigation Dataset"** and populate it with all records from `data/irrigation_dataset.csv`.

---

## 🤖 ML Model

### Dataset

The dataset is generated by `generate_data.py` and contains **100 records** with the following schema:

| Column | Type | Description |
|---|---|---|
| `Date` | Date | Record date (starting 2025-01-01) |
| `Time` | String | Hour of the reading (e.g., `006:00`) |
| `Soil Moisture (%)` | Integer | Soil moisture level (0–100) |
| `Temperature (°C)` | Float | Ambient temperature (15–36°C) |
| `Humidity (%)` | Integer | Air humidity (25–100%) |
| `Rainfall (mm)` | Float | Rainfall amount (0–30 mm) |
| `Irrigation Amount (liters)` | Integer | Water applied (0–100 liters) |
| `Crop Type` | String | Corn, Wheat, Tomato, or Paddy |
| `Irrigation Status` | Integer | 0 = No irrigation, 1 = Irrigate |

**Irrigation rule used for labelling:** `Irrigation Status = 1` when `Soil Moisture < 30%`

### Training

`train_model.py` trains a `RandomForestClassifier` using:

- **Features:** Soil Moisture (%), Temperature (°C), Humidity (%), Rainfall (mm)
- **Target:** Irrigation Status (binary: 0 or 1)
- **Split:** 80% training / 20% testing
- **Output:** `irrigation_model.pkl`

---

## 💻 Code Overview

### `app.py` — Flask Application

The main entry point. Loads the trained model and dataset, defines the web dashboard route, and exposes the prediction API endpoint.

```python
from flask import Flask, render_template, jsonify, request
import pandas as pd
import joblib
import random

app = Flask(__name__)
df = pd.read_csv('irrigation_dataset.csv')
model = joblib.load('irrigation_model.pkl')

# Hardcoded 4-day weather forecast data
weather_data = [
    {"date": "2025-01-25", "temperature": 22, "rainfall": 3.5},
    {"date": "2025-01-26", "temperature": 28, "rainfall": 7},
    {"date": "2025-01-27", "temperature": 28, "rainfall": 1.7},
    {"date": "2025-01-28", "temperature": 24, "rainfall": 4.3},
]

# Crop definitions with simulated current moisture readings
crops = [
    {"name": "Tomatoes", "current_moisture": random.uniform(50, 80), "optimal_moisture": 70},
    {"name": "Lettuce",  "current_moisture": random.uniform(70, 90), "optimal_moisture": 80},
    {"name": "Carrots",  "current_moisture": random.uniform(40, 60), "optimal_moisture": 60},
]

@app.route('/')
def index():
    for crop in crops:
        if crop["current_moisture"] < crop["optimal_moisture"] - 10:  # 10% below optimal
            crop["status"] = "Watering"
        elif crop["current_moisture"] < crop["optimal_moisture"]:
            crop["status"] = "Scheduled"
        else:
            crop["status"] = "Idle"
    return render_template('index.html', weather=weather_data, crops=crops)

@app.route('/get_irrigation_status', methods=['GET'])
def get_irrigation_status():
    soil_moisture = float(request.args.get('soil_moisture'))
    humidity = float(request.args.get('humidity'))
    prediction = model.predict([[soil_moisture, humidity]])[0]
    return jsonify({"predicted_irrigation_amount": prediction})

if __name__ == '__main__':
    app.run(debug=True)
```

---

### `generate_data.py` — Dataset Generation

Generates 100 synthetic records and writes them to `irrigation_dataset.csv`. The irrigation label is determined by a simple threshold rule: irrigate when soil moisture drops below 30%.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

num_records = 100
start_date = datetime(2025, 1, 1)
crop_types = ['Corn', 'Wheat', 'Tomato', 'paddy']
data = []

for i in range(num_records):
    date             = start_date + timedelta(days=i // 24)
    time             = f"{(i % 24):03d}:00"
    soil_moisture    = np.random.randint(0, 101)       # 0–100 %
    temperature      = np.random.uniform(15, 36)       # 15–36 °C
    humidity         = np.random.randint(25, 100)      # 25–100 %
    rainfall         = np.random.uniform(0, 30)        # 0–30 mm
    irrigation_amount = np.random.randint(0, 100)      # 0–100 liters
    crop_type        = np.random.choice(crop_types)
    irrigation_status = 1 if soil_moisture < 30 else 0  # Irrigate if moisture < 30%

    data.append([date.strftime('%Y-%m-%d'), time, soil_moisture, temperature,
                 humidity, rainfall, irrigation_amount, crop_type, irrigation_status])

df = pd.DataFrame(data, columns=[
    'Date', 'Time', 'Soil Moisture (%)', 'Temperature (°C)',
    'Humidity (%)', 'Rainfall (mm)', 'Irrigation Amount (liters)',
    'Crop Type', 'Irrigation Status'
])
df.to_csv('irrigation_dataset.csv', index=False)
print(df.head())
```

---

### `train_model.py` — Model Training

Loads the generated CSV, trains a `RandomForestClassifier` on four sensor features, evaluates its accuracy, and serializes the model to `irrigation_model.pkl`.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('irrigation_dataset.csv')

X = df[['Soil Moisture (%)', 'Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)']]
y = df['Irrigation Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

joblib.dump(model, 'irrigation_model.pkl')
```

---

### `upload_google_sheet.py` — Google Sheets Sync

Authenticates with the Google Sheets API using a service account, then uploads the local CSV dataset to a Google Sheet named **"Irrigation Dataset"**.

```python
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
gc = gspread.authorize(credentials)

spreadsheet_name = "Irrigation Dataset"

try:
    sh = gc.open(spreadsheet_name)
    print(f"Spreadsheet '{spreadsheet_name}' already exists.")
except gspread.exceptions.SpreadsheetNotFound:
    sh = gc.create(spreadsheet_name)
    print(f"Spreadsheet '{spreadsheet_name}' created.")

# Share with your Google account (replace the email below)
sh.share('your-email@gmail.com', perm_type='user', role='writer')

worksheet = sh.sheet1
df = pd.read_csv('data/irrigation_dataset.csv')

worksheet.clear()
worksheet.update([df.columns.values.tolist()] + df.values.tolist())

print(f"Dataset uploaded to Google Sheet: {spreadsheet_name}")
```

---

## 🌿 Supported Crops

| Crop | Monitored in Dashboard |
|---|---|
| Tomatoes | ✅ |
| Lettuce | ✅ |
| Carrots | ✅ |
| Corn | Training data only |
| Wheat | Training data only |
| Paddy | Training data only |

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request.

---

## 📄 License

This project is open source. See the repository for license details.
