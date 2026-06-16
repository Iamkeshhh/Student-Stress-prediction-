import streamlit as st
import plotly.express as px
from utils import load_data

df = load_data()

st.title("🏫 Faculty Dashboard")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Students",len(df))
c2.metric("Average Anxiety",round(df["anxiety_level"].mean(),2))
c3.metric("Average Depression",round(df["depression"].mean(),2))
c4.metric("Average Stress",round(df["stress_level"].mean(),2))

fig = px.histogram(
    df,
    x="stress_level",
    color="stress_level"
)

st.plotly_chart(fig,use_container_width=True)

fig2 = px.scatter(
    df,
    x="anxiety_level",
    y="depression",
    color="stress_level"
)

st.plotly_chart(fig2,use_container_width=True)