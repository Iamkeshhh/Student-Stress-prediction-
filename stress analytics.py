import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_data

df = load_data()

st.title("📈 Stress Analytics")

corr = df.corr(numeric_only=True)

fig,ax = plt.subplots(figsize=(12,8))

sns.heatmap(
    corr,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)