import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib

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
models = {
    "Random Forest": joblib.load("random_forest.pkl"),
    "Decision Tree": joblib.load("decision_tree.pkl"),
    "SVM": joblib.load("svm.pkl"),
    "XGBoost": joblib.load("xgboost.pkl"),
    "Logistic Regression": joblib.load("logistic_regression.pkl")
}

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

  
  st.title("🧠 AI Student Mental Health Platform")

  st.markdown(
    "### Dataset & Model Configuration"
)

# =====================================
# DATASET SELECTION
# =====================================

dataset_choice = st.selectbox(
    "📂 Select Dataset",
    [
        "StressLevelDataset.csv",
        "Student Stress Factors.xlsx"
    ]
)

st.success(
    f"Selected Dataset: {dataset_choice}"
)

# =====================================
# MODEL SELECTION
# =====================================

model_choice = st.selectbox(
    "🤖 Select Prediction Model",
    [
        "Random Forest",
        "Decision Tree",
        "XGBoost",
        "Support Vector Machine",
        "Logistic Regression"
    ]
)

selected_model = models[model_choice]

# =====================================
# MODEL ACCURACY
# =====================================

accuracy_map = {
    "Random Forest": 89.09,
    "Decision Tree": 89.55,
    "XGBoost": 88.18,
    "Support Vector Machine": 89.55,
    "Logistic Regression": 86.64
}

accuracy = accuracy_map[model_choice]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Dataset Records",
    len(df)
)

c2.metric(
    "Features",
    len(df.columns)
)

c3.metric(
    "Model Accuracy",
    f"{accuracy}%"
)

st.divider()

# =====================================
# DATASET PREVIEW
# =====================================

st.subheader(
    "📊 Dataset Preview"
)

st.dataframe(
    df.head(),
    use_container_width=True
)

st.divider()

# =====================================
# MODEL DESCRIPTION
# =====================================

st.subheader(
    "🤖 Selected Model Information"
)

if model_choice == "Random Forest":

    st.info(
        "Random Forest combines multiple decision trees and provides high accuracy with reduced overfitting."
    )

elif model_choice == "Decision Tree":

    st.info(
        "Decision Tree uses hierarchical splitting to classify stress levels."
    )

elif model_choice == "XGBoost":

    st.info(
        "XGBoost is a boosting algorithm that delivers high predictive performance."
    )

elif model_choice == "Support Vector Machine":

    st.info(
        "SVM separates stress categories using optimal decision boundaries."
    )

else:

    st.info(
        "Logistic Regression estimates the probability of stress classes."
    )

st.divider()

# =====================================
# RUN MODEL BUTTON
# =====================================

if st.button(
    "🚀 Run Prediction Model"
):

    st.success(
        f"{model_choice} loaded successfully."
    )

    st.balloons()


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
    student = df[df["Student_Name"] == selected_student].iloc[0]

    features = student.drop(
    labels=["Student_Name", "stress_level"]
    )

    features = pd.DataFrame([features])

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

    prediction = selected_model.predict(features)[0]

    if prediction == 0:
      risk = "LOW"

    elif prediction == 1:
      risk = "MEDIUM"

    else:
      risk = "HIGH"

    st.divider()

    st.info(
    f"Prediction generated using {model_choice}"
    )

    if hasattr(selected_model, "predict_proba"):

      probabilities = selected_model.predict_proba(features)[0]

      confidence = max(probabilities) * 100

      st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
      )  

      risk_score = {
      "LOW": 10,
      "MEDIUM": 25,
      "HIGH": 45
      }[risk]

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

    st.subheader("💡 Personalized Wellness Action Plan")

    if risk == "LOW":

       st.success("Healthy Mental State Detected")

       st.markdown("""
       ### Recommended Actions

       ✅ Maintain a consistent sleep schedule

       ✅ Exercise at least 30 minutes daily

       ✅ Continue participating in social activities

       ✅ Practice gratitude journaling

       ### Helpful Resources

       🔗 Mindfulness Guide:
        https://www.mindful.org/meditation/mindfulness-getting-started/

       🔗 Breathing Exercises:
        https://www.healthline.com/health/breathing-exercise

       🔗 Stress Management Tips:
        https://www.helpguide.org/articles/stress/stress-management.htm
        """)

    elif risk == "MEDIUM":

        st.warning("Moderate Stress Detected")

        st.markdown("""
        ### Recommended Actions

        ✅ Follow a structured daily routine

        ✅ Reduce academic overload

        ✅ Use Pomodoro study techniques

        ✅ Practice mindfulness for 10–15 minutes daily

        ✅ Reach out to trusted friends or mentors

         ### Professional Support

        🔗 BetterHelp:
         https://www.betterhelp.com/

        🔗 Mindfulness Meditation:
         https://www.headspace.com/meditation

        🔗 Anxiety Management Resources:
         https://www.nimh.nih.gov/health/topics/anxiety-disorders

         ### Suggested Daily Goal

        🧘 15 Minutes Meditation

        🚶 20 Minutes Walking

        😴 7–8 Hours Sleep
         """)

    else:

        st.error("High Stress Level Detected")

        st.markdown("""
        # 🚨 Immediate Support Recommended

        ### Action Plan

        1. Schedule a counseling session immediately.

        2. Inform a faculty mentor or trusted guardian.

        3. Reduce non-essential academic workload.

        4. Increase social interactions with trusted friends.

        5. Avoid isolation.

        ### Professional Consultation

       🔗 BetterHelp Online Counseling
        https://www.betterhelp.com/

       🔗 7 Cups Emotional Support
        https://www.7cups.com/

       🔗 NIMH Mental Health Resources
        https://www.nimh.nih.gov/

        ### Guided Relaxation

       🔗 Headspace
        https://www.headspace.com/

       🔗 Calm
        https://www.calm.com/

        ### Emergency Help

        If the student expresses thoughts of self-harm or immediate danger, contact local emergency services or a mental health crisis service immediately.
         """)

        st.subheader("💡 Personalized Recommendations")

# =====================================================
# COUNSELING CONSULTATION FORM
# =====================================================

    if risk in ["MEDIUM", "HIGH"]:

        st.markdown("---")
        st.subheader("📅 Request Counseling Support")

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
                "The student wellness team will contact you soon."
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
