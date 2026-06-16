import streamlit as st

st.title("💡 Wellness Recommendations")

stress = st.selectbox(
    "Stress Level",
    ["Low","Medium","High"]
)

if stress == "Low":

    st.success("""
    Maintain current routine
    Exercise regularly
    Continue healthy sleep
    """)

elif stress == "Medium":

    st.warning("""
    Improve sleep quality
    Reduce study overload
    Improve social interaction
    """)

else:

    st.error("""
    Seek counselling
    Reduce academic burden
    Increase social support
    Practice mindfulness
    """)