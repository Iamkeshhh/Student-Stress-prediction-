import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils import load_model, load_scaler

st.set_page_config(page_title="Student Portal", layout="wide")

model = load_model()
scaler = load_scaler()

st.title("🎓 Student Mental Health Assessment")

col1, col2 = st.columns(2)

with col1:
    anxiety_level = st.slider("Anxiety Level",0,10,5)
    self_esteem = st.slider("Self Esteem",0,30,15)
    mental_health_history = st.selectbox("Mental Health History",[0,1])
    depression = st.slider("Depression",0,10,5)
    headache = st.slider("Headache",0,5,2)
    blood_pressure = st.slider("Blood Pressure",0,5,2)
    sleep_quality = st.slider("Sleep Quality",0,10,5)
    breathing_problem = st.slider("Breathing Problem",0,5,2)
    noise_level = st.slider("Noise Level",0,5,2)
    living_conditions = st.slider("Living Conditions",0,5,3)

with col2:
    safety = st.slider("Safety",0,5,3)
    basic_needs = st.slider("Basic Needs",0,5,3)
    academic_performance = st.slider("Academic Performance",0,5,3)
    study_load = st.slider("Study Load",0,5,3)
    teacher_student_relationship = st.slider("Teacher Student Relationship",0,5,3)
    future_career_concerns = st.slider("Future Career Concerns",0,5,3)
    social_support = st.slider("Social Support",0,5,3)
    peer_pressure = st.slider("Peer Pressure",0,5,3)
    extracurricular_activities = st.slider("Extracurricular Activities",0,5,3)
    bullying = st.slider("Bullying",0,5,2)

if st.button("Predict Stress Level"):

    features = np.array([[
        anxiety_level,self_esteem,mental_health_history,
        depression,headache,blood_pressure,sleep_quality,
        breathing_problem,noise_level,living_conditions,
        safety,basic_needs,academic_performance,study_load,
        teacher_student_relationship,future_career_concerns,
        social_support,peer_pressure,
        extracurricular_activities,bullying
    ]])

    scaled = scaler.transform(features)

    prediction = model.predict(scaled)[0]

    if prediction == 0:
        st.success("🟢 Low Stress")
        risk = 25
    elif prediction == 1:
        st.warning("🟡 Medium Stress")
        risk = 60
    else:
        st.error("🔴 High Stress")
        risk = 90

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={"text":"Stress Risk"},
        gauge={"axis":{"range":[0,100]}}
    ))

    st.plotly_chart(fig,use_container_width=True)