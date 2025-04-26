from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import os
import folium
import json
import requests



app = Flask(__name__)

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

def preprocess_time(df):
    """Preprocess time features"""
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
    seconds_in_day = 24 * 60 * 60
    df['Time_seconds'] = df['Time'].dt.hour * 3600 + df['Time'].dt.minute * 60 + df['Time'].dt.second
    df['Time_sin'] = np.sin(2 * np.pi * df['Time_seconds'] / seconds_in_day)
    df['Time_cos'] = np.cos(2 * np.pi * df['Time_seconds'] / seconds_in_day)
    return df.drop(columns=['Time', 'Time_seconds'], errors='ignore')

def feature_engineering(df):
    """Create additional features"""
    # Gender features
    df['GenderRatio'] = df['FemaleCount'] / (df['MaleCount'] + 1e-5)
    df['DPG_Male'] = (df['MaleCount'] > df['FemaleCount']).astype(int)
    df['DPG_Female'] = (df['FemaleCount'] > df['MaleCount']).astype(int)
    
    # Time features
    df['Hour'] = (np.arctan2(df['Time_sin'], df['Time_cos']) * 24 / (2 * np.pi) % 24)
    df['NightTime'] = df['Hour'].apply(lambda h: 1 if (h >= 18 or h < 6) else 0)
    
    # Population features
    df['RollingAvgPop'] = df['TotalPopulation'].rolling(5, min_periods=1).mean()
    df['SuddenDrop'] = (df['TotalPopulation'] < 0.5 * df['RollingAvgPop']).astype(int)
    
    # Signal features
    df['NoSignal'] = (df['SignalStrength (dBm)'] < -109).astype(int)
    df['LowCrowdDensity'] = (df['CrowdDensity (people/m²)'] < 0.01).astype(int)
    
    return df

# --- Updated Risk Classification Function ---
def classify_risk(row):
    """
    Classifies the risk level based on multiple feature thresholds.
    Returns:
        2 -> High Risk
        1 -> Median Risk
        0 -> Low Risk
    """
    high_risk_conditions = 0
    median_risk_conditions = 0

    # --- High Risk Conditions ---
    if row['CrowdDensity (people/m²)'] < 0.01:  # Very low crowd density is a major indicator of high risk.
        high_risk_conditions += 1
    if row['SignalStrength (dBm)'] < -100:  # Poor signal strength indicating potential communication failure.
        high_risk_conditions += 1
    if row['GenderRatio'] < 0.2:  # Very low female-to-male ratio indicates higher safety risks for women.
        high_risk_conditions += 1
    if row['Isolation'] == 1:  # Isolation indicates an area with fewer people and no access to help.
        high_risk_conditions += 1
    if row['TotalPopulation'] < 10:  # A very low population count suggests the area may lack witnesses or support.
        high_risk_conditions += 1
    if row['SuddenDrop'] == 1:  # A sudden drop in population or activity suggests an emergency or anomaly.
        high_risk_conditions += 1
    if row['NoSignal'] == 1:  # Complete lack of signal means no way to call for help.
        high_risk_conditions += 1
    if row['LowCrowdDensity'] == 1:  # Very low crowd density can indicate isolation or dangerous situations.
        high_risk_conditions += 1

    # --- Median Risk Conditions ---
    if 0.01 <= row['CrowdDensity (people/m²)'] < 0.05:  # Moderate crowd density is a sign of potential risks.
        median_risk_conditions += 1
    if -100 <= row['SignalStrength (dBm)'] < -90:  # Low signal strength can still result in communication issues.
        median_risk_conditions += 1
    if 0.2 <= row['GenderRatio'] < 0.5:  # Moderate gender ratio may indicate less risk, but not fully safe.
        median_risk_conditions += 1
    if 10 <= row['TotalPopulation'] < 50:  # A moderate population can provide some safety but is still vulnerable.
        median_risk_conditions += 1
    if row['NightTime'] == 1:  # Night time increases the potential risk due to reduced visibility and activity.
        median_risk_conditions += 1

    # --- Final Risk Level Decision ---
    if high_risk_conditions >= 2:
        return 2  # High Risk: At least 2 high-risk conditions were met.
    elif median_risk_conditions >= 2 or high_risk_conditions == 1:
        return 1  # Median Risk: Either 2 median-risk conditions met, or 1 high-risk condition.
    else:
        return 0  # Low Risk: No conditions met for high or medium risk.


def inverse_time(sin_val, cos_val):
    """Convert encoded time back to HH:MM:SS"""
    angle = np.arctan2(sin_val, cos_val)
    if angle < 0: angle += 2 * np.pi
    hours = angle * 24 / (2 * np.pi)
    h = int(hours)
    m = int((hours - h) * 60)
    s = int((hours - h - m/60) * 3600)
    return f"{h:02d}:{m:02d}:{s:02d}"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template("map.html")


# OpenCage API key (replace with your actual API key)
API_KEY = '7a5c6dd793864d70a1acd2055dfbb13d'

BASE_URL = 'https://api.opencagedata.com/geocode/v1/json'

# Function to get place name from coordinates using OpenCage API
def get_place_name(lat, lon):
    params = {
        'q': f'{lat},{lon}',
        'key': API_KEY,
        'language': 'en'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['results']:
        return data['results'][0]['formatted']  # Return the first result's formatted address
    else:
        return "Unknown Location"  # Fallback if no result found

@app.route('/map/<float:lat>/<float:lon>')
def show_map(lat, lon):
    # Get the place name from OpenCage API
    place_name = get_place_name(lat, lon)

    # Create map centered at given location
    map_obj = folium.Map(location=[lat, lon], zoom_start=75, control_scale=True)

    # Add main tower marker (Red Pin) with the place name in the popup
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"<b>Location:</b> {place_name}<br><b>Coordinates:</b> ({lat}, {lon})", max_width=300, min_width=200),
        tooltip="Main Tower",
        icon=folium.Icon(color='red', icon='cloud')
    ).add_to(map_obj)

    # Load nearby user pins
    json_path = os.path.join('locations', 'locations.json')
    with open(json_path, 'r') as f:
        nearby_locations = json.load(f)

    # Add nearby user markers (Blue Pins)
    for loc in nearby_locations:
        # Skip adding again if it is same as main tower
        if abs(loc['lat'] - lat) < 0.0001 and abs(loc['lon'] - lon) < 0.0001:
            continue

        popup_html = f"""
        <div style="font-family: Arial; font-size: 14px;">
            <b>Name:</b> {loc['info']['full_name']}<br>
            <b>Aadhar No:</b> {loc['info']['aadhar_no']}<br>
            <b>Phone:</b> {loc['info']['phone_no']}<br>
            <b>Home Address:</b> {loc['info']['home_address']}<br>
            <b>Work Info:</b> {loc['info']['work_info']}<br>
            <a href="/info/{loc['lat']}/{loc['lon']}"</a>
        </div>
        """

        folium.Marker(
            [loc['lat'], loc['lon']],
            popup=folium.Popup(popup_html, max_width=300, min_width=200),
            tooltip=loc['info']['full_name'],
            icon=folium.Icon(color='blue', icon='user')
        ).add_to(map_obj)

    # Convert map to HTML
    map_html = map_obj._repr_html_()

    # Now pass lat, lon separately to template for redirect button
    return render_template('folium_map.html', map_html=map_html, lat=lat, lon=lon)

# Info Page Route
@app.route('/info/<float:lat>/<float:lon>')
def show_info(lat, lon):
    return f"<h1>Information Page</h1><p>Location: {lat}, {lon}</p>"

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    form_data = {
        'Tower ID': int(request.form['tower_id']),
        'Latitude': float(request.form['latitude']),
        'Longitude': float(request.form['longitude']),
        'SignalStrength (dBm)': int(request.form['signal']),
        'MaleCount': int(request.form['male_count']),
        'FemaleCount': int(request.form['female_count']),
        'CrowdDensity (people/m²)': float(request.form['density']),
        'TotalPopulation': int(request.form['population']),
        'Time': request.form['time']
    }
    
    # Create DataFrame
    input_df = pd.DataFrame([form_data])
    
    # Preprocess time
    input_df = preprocess_time(input_df)
    
    # Load base dataset and fit scaler
    base_df = pd.read_csv(os.path.join(DATA_DIR, 'with_time_new.csv'))
    base_df = preprocess_time(base_df)
    scaler1 = StandardScaler().fit(base_df)
    
    # Predict Isolation
    with open(os.path.join(MODEL_DIR, 'rf_model.pkl'), 'rb') as f:
        rf_model = pickle.load(f)
    input_scaled = scaler1.transform(input_df)
    input_df['Isolation'] = rf_model.predict(input_scaled)
    
    # Feature engineering
    input_df = feature_engineering(input_df)
    
    # Load final dataset and fit second scaler
    final_df = pd.read_csv(os.path.join(DATA_DIR, 'prefinal.csv'))
    scaler2 = StandardScaler().fit(final_df)
    
    # Predict Risk Level
    with open(os.path.join(MODEL_DIR, 'log_model.pkl'), 'rb') as f:
        log_model = pickle.load(f)
    final_scaled = scaler2.transform(input_df[final_df.columns])
    ml_risk = log_model.predict(final_scaled)[0]
    
    # Rule-based risk
    rule_risk = classify_risk(input_df.iloc[0])
    
    # Hybrid risk calculation
    final_risk = int(0.4 * ml_risk + 0.6 * rule_risk)
    final_risk = 2 if final_risk >= 1.5 else 1 if final_risk >= 0.5 else 0
    
    # Generate time string
    time_str = inverse_time(input_df['Time_sin'].iloc[0], input_df['Time_cos'].iloc[0])
    
    # Prepare result
    result = {
        'tower_id': form_data['Tower ID'],
        'location': f"{form_data['Latitude']}, {form_data['Longitude']}",
        'signal_strength':form_data['SignalStrength (dBm)'],
        'Male_count' :form_data['MaleCount'],
        'Female_count': form_data['FemaleCount'],
        'time': time_str,
        'risk_level': final_risk,
        'alert': generate_alert(final_risk, form_data)
    }
    
    return render_template('result.html', result=result)

def generate_alert(risk_level, data):
    """Generate alert message based on risk level"""
    messages = {
        2: f"🚨 URGENT: HIGH risk at Tower {data['Tower ID']} ({data['Latitude']}, {data['Longitude']})",
        1: f"⚠️ WARNING: MEDIUM risk at Tower {data['Tower ID']} ({data['Latitude']}, {data['Longitude']})",
        0: f"✅ SAFE: LOW risk at Tower {data['Tower ID']} ({data['Latitude']}, {data['Longitude']})"
    }
    return messages[risk_level] + f" at {data['Time']}"



if __name__ == '__main__':
    app.run(debug=True)


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
