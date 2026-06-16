import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Mental Health Platform",
    page_icon="🧠",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    return pd.read_csv("StressLevelDataset.csv")

df = load_data()

# ---------------- SIDEBAR ----------------

st.sidebar.title("🧠 AI Mental Health Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Student Risk Analyzer"
    ]
)

# ==================================================
# HOME
# ==================================================

if page == "Home":

    st.title("🎓 AI Powered Student Mental Health Analytics")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Total Students",
        len(df)
    )

    c2.metric(
        "Features",
        len(df.columns)
    )

    if "stress_level" in df.columns:

        c3.metric(
            "High Risk",
            len(df[df["stress_level"] == 2])
        )

        c4.metric(
            "Low Risk",
            len(df[df["stress_level"] == 0])
        )

    st.markdown("---")

    st.info("""
This platform helps faculty identify students
who may require mental health support.

Select **Student Risk Analyzer** from the sidebar.
""")

# ==================================================
# STUDENT ANALYZER
# ==================================================

elif page == "Student Risk Analyzer":

    st.title("🎯 Student Risk Analyzer")

    # ---------------- Student Selection ----------------

    student_column = None

    possible_names = [
        "student_name",
        "name",
        "Name",
        "Student_Name",
        "StudentName"
    ]

    for col in possible_names:
        if col in df.columns:
            student_column = col
            break

    if student_column is None:
        st.error(
            "No student name column found.\nPlease rename it as 'student_name'"
        )
        st.stop()

    selected_student = st.selectbox(
        "Select Student",
        sorted(df[student_column].unique())
    )

    student = df[
        df[student_column] == selected_student
    ].iloc[0]

    # ==================================================
    # PROFILE SECTION
    # ==================================================

    st.markdown("## 👤 Student Profile")

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Student",
        selected_student
    )

    if "age" in df.columns:
        col2.metric(
            "Age",
            student["age"]
        )

    if "stress_level" in df.columns:
        col3.metric(
            "Dataset Stress",
            student["stress_level"]
        )

    st.markdown("---")

    # ==================================================
    # SHOW ALL DETAILS
    # ==================================================

    st.subheader("📋 Complete Student Details")

    details_df = pd.DataFrame(
        {
            "Feature": student.index,
            "Value": student.values
        }
    )

    st.dataframe(
        details_df,
        use_container_width=True,
        hide_index=True
    )

    # ==================================================
    # CALCULATE RISK SCORE
    # ==================================================

    risk_score = 0

    risk_features = [
        "anxiety_level",
        "depression",
        "self_esteem",
        "mental_health_history",
        "peer_pressure",
        "academic_pressure",
        "bullying"
    ]

    for feature in risk_features:

        if feature in df.columns:

            try:
                risk_score += float(student[feature])
            except:
                pass

    if risk_score <= 10:
        risk = "LOW"
        gauge_color = "green"

    elif risk_score <= 20:
        risk = "MEDIUM"
        gauge_color = "orange"

    else:
        risk = "HIGH"
        gauge_color = "red"

    # ==================================================
    # GAUGE CHART
    # ==================================================

    st.subheader("🧠 Mental Health Risk Gauge")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={
                "text":"Stress Risk Score"
            },
            gauge={
                "axis":{"range":[0,30]},
                "bar":{"color":gauge_color},

                "steps":[
                    {
                        "range":[0,10],
                        "color":"lightgreen"
                    },
                    {
                        "range":[10,20],
                        "color":"yellow"
                    },
                    {
                        "range":[20,30],
                        "color":"salmon"
                    }
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # RISK STATUS
    # ==================================================

    st.subheader("🚨 Risk Assessment")

    if risk == "LOW":

        st.success(
            "LOW RISK STUDENT"
        )

    elif risk == "MEDIUM":

        st.warning(
            "MEDIUM RISK STUDENT"
        )

    else:

        st.error(
            "HIGH RISK STUDENT"
        )

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    st.subheader("💡 Personalized Recommendations")

    if risk == "LOW":

        st.success("""
✅ Continue healthy lifestyle

✅ Maintain good sleep

✅ Participate in activities

✅ Continue social engagement

✅ Regular exercise
""")

    elif risk == "MEDIUM":

        st.warning("""
⚠ Improve sleep quality

⚠ Reduce academic overload

⚠ Practice mindfulness

⚠ Time management training

⚠ Peer mentoring support
""")

    else:

        st.error("""
🚨 Immediate counselling recommended

🚨 Faculty intervention required

🚨 Reduce academic pressure

🚨 Frequent mental health monitoring

🚨 Connect with support groups

🚨 Schedule psychologist consultation
""")

    # ==================================================
    # FEATURE VISUALIZATION
    # ==================================================

    st.markdown("---")
    st.subheader("📊 Student Feature Analysis")

    numeric_data = []

    numeric_cols = []

    for col in df.columns:

        try:
            value = float(student[col])

            numeric_cols.append(col)
            numeric_data.append(value)

        except:
            pass

    chart_df = pd.DataFrame(
        {
            "Feature": numeric_cols,
            "Value": numeric_data
        }
    )

    st.bar_chart(
        chart_df.set_index("Feature")
    )
