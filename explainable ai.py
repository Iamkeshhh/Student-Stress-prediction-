import streamlit as st
import shap
import pandas as pd
from utils import load_data, load_model

st.title("🤖 Explainable AI")

df = load_data()
model = load_model()

X = df.drop("stress_level",axis=1)

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

st.subheader("Feature Importance")

fig = shap.summary_plot(
    shap_values,
    X,
    show=False
)

st.pyplot()