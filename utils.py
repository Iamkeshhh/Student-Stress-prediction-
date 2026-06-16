import pandas as pd
import joblib

def load_data():
    return pd.read_csv("StressLevelDataset.csv")

def load_model():
    return joblib.load("models/xgb_model.pkl")

def load_scaler():
    return joblib.load("models/scaler.pkl")