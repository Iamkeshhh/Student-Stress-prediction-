import streamlit as st
import pandas as pd
import plotly.graph_objects as go

LOW_VIDEO = "low stress.mp4"
MEDIUM_VIDEO = "medium stress.mp4"
HIGH_VIDEO = "high stress.mp4"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Student Mental Health Platform",
    page_icon="🧠",
    layout="wide"
)

import base64

# ---------- BACKGROUND HERO VIDEO ----------

video_file = open("Background.mp4", "rb")
video_bytes = video_file.read()
video_base64 = base64.b64encode(video_bytes).decode()

st.markdown(
    f"""
    <style>

    .video-container {{
        position: relative;
        width: 100%;
        height: 450px;
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 20px;
    }}

    .video-container video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .video-text {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        text-align: center;
        background: rgba(0,0,0,0.45);
        padding: 20px;
        border-radius: 15px;
    }}

    .video-text h1 {{
        font-size: 42px;
    }}

    </style>

    <div class="video-container">

        <video autoplay muted loop>
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>

        <div class="video-text">
            <h1>🧠 AI Student Mental Health Analytics</h1>
            <p>Early Detection • Risk Assessment • Personalized Recommendations</p>
        </div>

    </div>

    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("StressLevelDataset.csv")

    # Remove unwanted columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🧠 Mental Health Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Student Analysis"
    ]
)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if page == "Home":

    st.title("🎓 AI Powered Student Mental Health Platform")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", len(df))
    c2.metric("Features", len(df.columns))

    c3.metric(
        "High Stress",
        len(df[df["stress_level"] == 2])
    )

    c4.metric(
        "Low Stress",
        len(df[df["stress_level"] == 0])
    )

    st.info(
        "Use the Student Analysis page to view complete student profiles and recommendations."
    )

# ---------------------------------------------------
# STUDENT ANALYSIS
# ---------------------------------------------------

elif page == "Student Analysis":

    st.title("🎯 Student Mental Health Analyzer")

    # Student Name Column
    student_column = "Student_Name"

    # Student Dropdown
    selected_student = st.selectbox(
        "Select Student",
        sorted(df[student_column].dropna().unique())
    )

    # Student Record
    student = df[df[student_column] == selected_student].iloc[0]

    # ---------------------------------------------------
    # PROFILE HEADER
    # ---------------------------------------------------

    st.markdown("## 👤 Student Profile")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Student Name",
        student["Student_Name"]
    )

    col2.metric(
        "Dataset Stress Level",
        int(student["stress_level"])
    )

    risk_score = (
        student["anxiety_level"]
        + student["depression"]
        + student["peer_pressure"]
        + student["bullying"]
        + student["future_career_concerns"]
        - student["sleep_quality"]
    )

    col3.metric(
        "Risk Score",
        round(risk_score, 1)
    )

    st.divider()

    # ---------------------------------------------------
    # GAUGE CHART
    # ---------------------------------------------------

    st.subheader("🧠 Stress Risk Gauge")

    gauge_max = 50

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Stress Risk Score"},
            gauge={
                "axis": {"range": [0, gauge_max]},
                "bar": {"color": "darkred"},
                "steps": [
                    {"range": [0, 15], "color": "lightgreen"},
                    {"range": [15, 30], "color": "yellow"},
                    {"range": [30, 50], "color": "salmon"}
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------------------
    # RISK CATEGORY
    # ---------------------------------------------------

    if risk_score < 15:
        risk = "LOW"

    elif risk_score < 30:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    st.subheader("🚨 Risk Assessment")

    if risk == "LOW":
        st.success("LOW RISK STUDENT")

    elif risk == "MEDIUM":
        st.warning("MEDIUM RISK STUDENT")

    else:
        st.error("HIGH RISK STUDENT")

    if risk == "LOW":

    st.success("LOW RISK STUDENT")

    st.video(LOW_VIDEO)

elif risk == "MEDIUM":

    st.warning("MEDIUM RISK STUDENT")

    st.video(MEDIUM_VIDEO)

else:

    st.error("HIGH RISK STUDENT")

    st.video(HIGH_VIDEO)

    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------

    st.subheader("💡 Personalized Recommendations")

    if risk == "LOW":

        st.success("""
        ✅ Maintain current healthy habits

        ✅ Continue regular exercise

        ✅ Participate in extracurricular activities

        ✅ Maintain good sleep schedule

        ✅ Stay socially connected
        """)

    elif risk == "MEDIUM":

        st.warning("""
        ⚠ Improve sleep quality

        ⚠ Reduce study overload

        ⚠ Practice mindfulness

        ⚠ Seek peer support

        ⚠ Monitor stress regularly
        """)

    else:

        st.error("""
        🚨 Immediate counseling recommended

        🚨 Faculty intervention advised

        🚨 Reduce academic pressure

        🚨 Increase social support

        🚨 Regular mental health monitoring

        🚨 Professional psychologist consultation
        """)

    st.divider()

    # ---------------------------------------------------
    # COMPLETE STUDENT DETAILS
    # ---------------------------------------------------

    st.subheader("📋 Complete Student Information")

    details = pd.DataFrame({
        "Feature": student.index,
        "Value": student.values
    })

    st.dataframe(
        details,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ---------------------------------------------------
    # FEATURE ANALYSIS
    # ---------------------------------------------------

    st.subheader("📊 Student Mental Health Factors")

    numeric_features = student.drop(
        labels=["Student_Name"]
    )

    numeric_features = pd.to_numeric(
        numeric_features,
        errors="coerce"
    ).dropna()

    st.bar_chart(numeric_features)


