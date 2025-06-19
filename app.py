from flask import Flask, render_template, jsonify, request
import pandas as pd
import joblib
import random

app = Flask(__name__)
df = pd.read_csv('irrigation_dataset.csv')
model = joblib.load('irrigation_model.pkl')
weather_data = [
    {"date": "2025-01-25", "temperature": 22, "rainfall": 3.5},
    {"date": "2025-01-26", "temperature": 28, "rainfall": 7},
    {"date": "2025-01-27", "temperature": 28, "rainfall": 1.7},
    {"date": "2025-01-28", "temperature": 24, "rainfall": 4.3},
]
crops = [
    {"name": "Tomatoes", "current_moisture": random.uniform(50, 80), "optimal_moisture": 70},
    {"name": "Lettuce", "current_moisture": random.uniform(70, 90), "optimal_moisture": 80},
    {"name": "Carrots", "current_moisture": random.uniform(40, 60), "optimal_moisture": 60},
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
    return jsonify({
        "predicted_irrigation_amount": prediction
    })

if __name__ == '__main__':
    app.run(debug=True)
