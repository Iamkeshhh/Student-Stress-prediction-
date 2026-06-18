import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="Student Stress Prediction", layout="wide")

@st.cache_data
def load_data():
    df1 = pd.read_csv("StressLevelDataset(2).csv")
    try:
        df2 = pd.read_excel("Student Stress Factors (2).xlsx")
    except Exception:
        df2 = pd.DataFrame()
    return df1, df2

def categorize_stress(v):
    if v <= 1:
        return "Low"
    elif v == 2:
        return "Medium"
    return "High"

def gauge(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value),
        gauge={"axis":{"range":[0,3]}}
    ))
    st.plotly_chart(fig, use_container_width=True)

def build_pdf(student, pred):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = [Paragraph("Student Stress Report", styles["Title"]),
             Spacer(1,12),
             Paragraph(f"Student: {student}", styles["BodyText"]),
             Paragraph(f"Predicted Stress: {pred}", styles["BodyText"])]
    doc.build(story)
    buffer.seek(0)
    return buffer

st.title("🎓 Student Stress Prediction Dashboard")

df, survey = load_data()

page = st.sidebar.selectbox(
    "Navigation",
    ["Dataset Analytics","Model Training","Student Analysis","Prediction"]
)

if page == "Dataset Analytics":
    st.subheader("StressLevelDataset")
    st.write(df.head())
    st.write(df.describe())

    if not survey.empty:
        st.subheader("Student Stress Factors")
        st.write(survey.head())

elif page == "Model Training":
    target = "stress_level"

    cols_to_drop = [c for c in ["stress_level","Student_Name","Unnamed: 22"] if c in df.columns]
    X = df.drop(columns=cols_to_drop, errors="ignore")
    y = df[target]

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    model_name = st.selectbox(
        "Model",
        ["XGBoost","Random Forest","SVM","Decision Tree","Linear Regression"]
    )

    if st.button("Train Model"):
        if model_name == "XGBoost":
            model = XGBClassifier()
        elif model_name == "Random Forest":
            model = RandomForestClassifier()
        elif model_name == "SVM":
            model = SVC()
        elif model_name == "Decision Tree":
            model = DecisionTreeClassifier()
        else:
            model = LinearRegression()

        model.fit(X_train,y_train)

        preds = model.predict(X_test)

        if model_name != "Linear Regression":
            acc = accuracy_score(y_test,preds)
            st.success(f"Accuracy: {acc:.4f}")
        else:
            st.info("Linear Regression trained successfully")

elif page == "Student Analysis":
    if "Student_Name" in df.columns:
        student = st.selectbox("Select Student", sorted(df["Student_Name"].astype(str).unique()))
        row = df[df["Student_Name"].astype(str)==student]

        st.dataframe(row)

        if "stress_level" in row.columns:
            val = row["stress_level"].iloc[0]
            gauge(val)

            category = categorize_stress(val)
            st.success(f"Stress Category: {category}")

            if category == "Low":
                st.video("low stress.mp4")
            elif category == "Medium":
                st.video("medium stress.mp4")
            else:
                st.video("high stress.mp4")

            pdf = build_pdf(student, category)
            st.download_button(
                "Download PDF Report",
                pdf,
                file_name=f"{student}_report.pdf",
                mime="application/pdf"
            )

elif page == "Prediction":
    st.subheader("Manual Prediction")

    feature_cols = [c for c in df.columns if c not in ["stress_level","Student_Name","Unnamed: 22"]]

    values = {}
    for col in feature_cols[:10]:
        values[col] = st.number_input(col, value=0.0)

    st.info("Extend remaining inputs as needed for your dataset.")
