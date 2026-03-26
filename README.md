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
