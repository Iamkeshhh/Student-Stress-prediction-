import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AI Student Mental Health Platform",
    page_icon="🧠",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("StressLevelDataset.csv")

df = load_data()

# ---------- SIDEBAR ----------

st.sidebar.title("🧠 Mental Health Platform")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Student Assessment",
        "Faculty Dashboard",
        "Student Explorer",
        "Recommendations"
    ]
)

# ---------- HOME ----------

if page == "Home":

    st.title("AI-Powered Student Mental Health Analytics")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Students", len(df))
    c2.metric("Features", len(df.columns)-1)
    c3.metric(
        "High Stress",
        len(df[df["stress_level"] == 2])
    )
    c4.metric(
        "Low Stress",
        len(df[df["stress_level"] == 0])
    )

    st.info(
        "Use the sidebar to switch between modules."
    )

# ---------- STUDENT ASSESSMENT ----------

elif page == "Student Assessment":

    st.title("🎓 Student Assessment")

    tab1, tab2 = st.tabs(
        ["Personal Details", "Mental Health Inputs"]
    )

    with tab1:

        student_name = st.text_input(
            "Student Name"
        )

        age = st.number_input(
            "Age",
            16,
            40,
            20
        )

        department = st.selectbox(
            "Department",
            [
                "CSE",
                "ECE",
                "EEE",
                "MECH",
                "MBA"
            ]
        )

    with tab2:

        anxiety = st.slider(
            "Anxiety Level",
            0,
            10,
            5
        )

        depression = st.slider(
            "Depression",
            0,
            10,
            5
        )

        peer_pressure = st.slider(
            "Peer Pressure",
            0,
            10,
            5
        )

        sleep_quality = st.slider(
            "Sleep Quality",
            0,
            10,
            5
        )

        bullying = st.slider(
            "Bullying",
            0,
            10,
            5
        )

    if st.button("Evaluate Student"):

        score = (
            anxiety +
            depression +
            peer_pressure +
            bullying
        ) - sleep_quality

        if score < 10:
            level = "Low Stress"
        elif score < 20:
            level = "Medium Stress"
        else:
            level = "High Stress"

        st.success(
            f"Predicted Stress Level: {level}"
        )

# ---------- FACULTY DASHBOARD ----------

elif page == "Faculty Dashboard":

    st.title("🏫 Faculty Dashboard")

    stress_filter = st.selectbox(
        "Stress Level",
        sorted(df["stress_level"].unique())
    )

    filtered = df[
        df["stress_level"] == stress_filter
    ]

    st.write(
        f"Students in selected category: {len(filtered)}"
    )

    st.dataframe(
        filtered,
        use_container_width=True
    )

# ---------- STUDENT EXPLORER ----------

elif page == "Student Explorer":

    st.title("🔍 Student Explorer")

    student_index = st.selectbox(
        "Select Student",
        df.index
    )

    student = df.loc[student_index]

    st.subheader("Student Details")

    st.write(student)

    feature = st.selectbox(
        "Feature",
        df.columns
    )

    st.metric(
        feature,
        student[feature]
    )

# ---------- RECOMMENDATIONS ----------

elif page == "Recommendations":

    st.title("💡 Recommendations")

    stress_choice = st.selectbox(
        "Stress Category",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    if stress_choice == "Low":

        st.success("""
Maintain current lifestyle

Continue exercise

Maintain social interactions
""")

    elif stress_choice == "Medium":

        st.warning("""
Improve sleep quality

Reduce study overload

Practice mindfulness
""")

    else:

        st.error("""
Seek counselling support

Reduce academic burden

Increase social support

Monitor mental health regularly
""")
