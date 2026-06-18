import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Student Mental Health Platform",
    page_icon="🧠",
    layout="wide"
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


    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------
    # ---------------------------------------------------
    # RISK CATEGORY
    # ---------------------------------------------------

    if risk_score < 15:
       risk = "LOW"

    elif risk_score < 30:
       risk = "MEDIUM"

    else:
       risk = "HIGH"

    # ---------------------------------------------------
    # RISK RESULT
    # ---------------------------------------------------

    st.subheader("🚨 Risk Assessment")

    if risk == "LOW":
       st.success("🟢 LOW RISK STUDENT")

    elif risk == "MEDIUM":
       st.warning("🟡 MEDIUM RISK STUDENT")

    else:
       st.error("🔴 HIGH RISK STUDENT")

    # ---------------------------------------------------
    # WELLNESS ACTION PLAN
    # ---------------------------------------------------

    st.subheader("💡 Personalized Wellness Action Plan")

    if risk == "LOW":

       consultation_note = """
       Maintain healthy lifestyle and regular monitoring.
       """

       st.success("""
       ### Recommended Actions

      ✅ Maintain a consistent sleep schedule

      ✅ Exercise at least 30 minutes daily

      ✅ Continue participating in social activities

      ✅ Practice gratitude journaling

       ### Helpful Resources

      🔗 https://www.mindful.org

      🔗 https://www.healthline.com

      🔗 https://www.helpguide.org
       """)

    elif risk == "MEDIUM":

       consultation_note = """
       Counseling session recommended within 2 weeks.
       """

       st.warning("""
       ### Recommended Actions

      ✅ Follow a structured routine

      ✅ Improve sleep quality

      ✅ Reduce study overload

      ✅ Practice mindfulness

      ### Professional Support

     🔗 https://www.betterhelp.com

     🔗 https://www.headspace.com

     🔗 https://www.nimh.nih.gov
     """)

    else:

      consultation_note = """
      Immediate counseling and faculty intervention required.
      """

    st.error("""
# 🚨 Immediate Support Recommended

1. Schedule counseling immediately

2. Inform faculty mentor

3. Reduce academic burden

4. Increase social support

### Consultation Resources

🔗 https://www.betterhelp.com

🔗 https://www.7cups.com

🔗 https://www.headspace.com

🔗 https://www.calm.com
""")

# ---------------------------------------------------
# CONSULTATION FORM
# ---------------------------------------------------

if risk in ["MEDIUM", "HIGH"]:

    st.markdown("---")

    st.subheader("📅 Counseling Request Form")

    with st.form("consultation_form"):

        student_email = st.text_input(
            "Student Email"
        )

        preferred_date = st.date_input(
            "Preferred Consultation Date"
        )

        concern = st.text_area(
            "Describe Your Concern"
        )

        submitted = st.form_submit_button(
            "Submit Counseling Request"
        )

        if submitted:

            st.success(
                "✅ Counseling request submitted successfully."
            )

            st.info(
                "Wellness team will contact you shortly."
            )
    
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
