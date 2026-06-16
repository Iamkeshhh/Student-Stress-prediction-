import streamlit as st
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet

st.title("📄 Student Report Generator")

name = st.text_input("Student Name")

stress = st.selectbox(
    "Stress Level",
    ["Low","Medium","High"]
)

if st.button("Generate Report"):

    doc = SimpleDocTemplate("report.pdf")

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Student Mental Health Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Student Name : {name}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Stress Level : {stress}",
            styles["Normal"]
        )
    )

    doc.build(content)

    with open("report.pdf","rb") as f:

        st.download_button(
            "Download Report",
            f,
            "Student_Report.pdf"
        )