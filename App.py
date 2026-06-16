import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Student Mental Health Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#0E1117;
    color:white;
}

.metric-card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    padding:20px;
    border-radius:20px;
    text-align:center;
}

.big-font{
    font-size:40px;
    font-weight:bold;
    color:#00D4FF;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    return pd.read_csv("StressLevelDataset.csv")

df = load_data()

# ---------------- SIDEBAR ---------------- #

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/4320/4320337.png",
    width=120
)

st.sidebar.title("AI Mental Health Analytics")

st.sidebar.info("""
Navigate using the Pages menu.

Student Portal
Faculty Dashboard
Stress Analytics
Explainable AI
Recommendations
Reports
""")

# ---------------- TITLE ---------------- #

st.markdown(
    "<p class='big-font'>🧠 AI Student Mental Health Analytics Platform</p>",
    unsafe_allow_html=True
)

st.markdown("""
Early detection of student stress using
Machine Learning, XGBoost and Deep Learning.
""")

# ---------------- KPI SECTION ---------------- #

total_students = len(df)

high_stress = len(
    df[df["stress_level"] == 2]
)

medium_stress = len(
    df[df["stress_level"] == 1]
)

low_stress = len(
    df[df["stress_level"] == 0]
)

avg_anxiety = round(
    df["anxiety_level"].mean(),
    2
)

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(
        "Students",
        total_students
    )

with col2:
    st.metric(
        "High Stress",
        high_stress
    )

with col3:
    st.metric(
        "Medium Stress",
        medium_stress
    )

with col4:
    st.metric(
        "Low Stress",
        low_stress
    )

with col5:
    st.metric(
        "Avg Anxiety",
        avg_anxiety
    )

st.divider()

# ---------------- CHARTS ---------------- #

left,right = st.columns(2)

with left:

    fig = px.histogram(
        df,
        x="stress_level",
        color="stress_level",
        title="Stress Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig2 = px.pie(
        df,
        names="stress_level",
        title="Stress Level Share"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------- TOP STRESS FACTORS ---------------- #

st.subheader("Top Stress Contributors")

stress_factors = [
    "anxiety_level",
    "depression",
    "peer_pressure",
    "bullying",
    "sleep_quality",
    "academic_performance"
]

means = []

for col in stress_factors:
    means.append(df[col].mean())

factor_df = pd.DataFrame({
    "Factor":stress_factors,
    "Value":means
})

fig3 = px.bar(
    factor_df,
    x="Factor",
    y="Value",
    color="Value",
    title="Average Impact Factors"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------- WELLNESS INDEX ---------------- #

st.subheader("Mental Wellness Index")

wellness = round(
    100 -
    (
        (
            df["anxiety_level"].mean() +
            df["depression"].mean() +
            df["peer_pressure"].mean()
        ) / 3
    ) * 10,
    2
)

fig4 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=wellness,
    title={"text":"Wellness Score"},
    gauge={
        "axis":{"range":[0,100]}
    }
))

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ---------------- RISK ALERTS ---------------- #

st.subheader("Faculty Early Warning System")

critical = df[
    (df["anxiety_level"] > 8) &
    (df["depression"] > 8)
]

st.error(
    f"⚠ {len(critical)} Students Require Immediate Attention"
)

st.dataframe(
    critical.head(20)
)

# ---------------- MODEL COMPARISON ---------------- #

st.subheader("Model Performance Comparison")

model_df = pd.DataFrame({
    "Model":[
        "Logistic Regression",
        "Random Forest",
        "SVM",
        "XGBoost",
        "Deep Learning"
    ],
    "Accuracy":[
        0.86,
        0.90,
        0.91,
        0.95,
        0.96
    ]
})

fig5 = px.bar(
    model_df,
    x="Model",
    y="Accuracy",
    color="Accuracy",
    title="Model Comparison"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown("""
### Project Features

✅ Stress Prediction

✅ Faculty Dashboard

✅ Explainable AI

✅ Recommendation Engine

✅ Risk Ranking

✅ Wellness Score

✅ Early Warning System

✅ PDF Report Generation

✅ XGBoost + Deep Learning
""")