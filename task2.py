import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

MODEL_PATH = 'house_price_model.pkl'

def train_and_save_model():
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    X = df.drop('MedHouseVal', axis=1)
    y = df['MedHouseVal']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

# Streamlit frontend
st.title("California House Price Prediction")

st.write("Enter the following features to predict the median house value:")

MedInc = st.number_input('Median Income (10k USD)', min_value=0.0, max_value=20.0, value=3.0)
HouseAge = st.number_input('House Age', min_value=1, max_value=100, value=20)
AveRooms = st.number_input('Average Rooms', min_value=1.0, max_value=20.0, value=5.0)
AveBedrms = st.number_input('Average Bedrooms', min_value=1.0, max_value=10.0, value=1.0)
Population = st.number_input('Population', min_value=1, max_value=10000, value=1000)
AveOccup = st.number_input('Average Occupancy', min_value=1.0, max_value=10.0, value=3.0)
Latitude = st.number_input('Latitude', min_value=32.0, max_value=42.0, value=34.0)
Longitude = st.number_input('Longitude', min_value=-124.0, max_value=-114.0, value=-120.0)

if st.button('Predict'):
    model = load_model()
    features = np.array([[MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]])
    prediction = model.predict(features)[0]
    st.success(f"Predicted Median House Value: ${prediction * 100000:.2f}")