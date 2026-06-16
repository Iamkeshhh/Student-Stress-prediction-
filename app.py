import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64

# =====================================================

# PAGE CONFIG

# =====================================================

st.set_page_config(
page_title="AI Student Mental Health Platform",
page_icon="🧠",
layout="wide"
)

# =====================================================

# LOAD DATA

# =====================================================

@st.cache_data
def load_data():
 df = pd.read_csv("StressLevelDataset.csv")

# Remove unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove spaces
df.columns = df.columns.str.strip()

return df


df = load_data()

# =====================================================

# BACKGROUND VIDEO

# =====================================================

 def autoplay_background_video(video_path):


with open(video_path, "rb") as file:
    video_bytes = file.read()

encoded_video = base64.b64encode(
    video_bytes
).decode()

st.markdown(
    f"""
    <style>

    .hero {{
        position: relative;
        width: 100%;
        height: 450px;
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 25px;
    }}

    .hero video {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .hero-text {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: white;
        background: rgba(0,0,0,0.45);
        padding: 25px 40px;
        border-radius: 15px;
    }}

    .hero-text h1 {{
        font-size: 3rem;
        margin-bottom: 10px;
    }}

    .hero-text p {{
        font-size: 1.2rem;
    }}

    </style>

    <div class="hero">

        <video autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
        </video>

        <div class="hero-text">
            <h1>🧠 AI Student Mental Health Analytics</h1>
            <p>Early Detection • Risk Assessment • Personalized Recommendations</p>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================

# VIDEO PLAYER

# =====================================================

def autoplay_video(video_path):


with open(video_path, "rb") as file:
    video_bytes = file.read()

encoded_video = base64.b64encode(
    video_bytes
).decode()

st.markdown(
    f"""
    <video width="100%"
           autoplay
           muted
           loop
           playsinline>
        <source src="data:video/mp4;base64,{encoded_video}"
                type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)


# =====================================================

# TOP BANNER

# =====================================================

autoplay_background_video("Background.mp4")

# =====================================================

# FIND STUDENT NAME COLUMN

# =====================================================

student_column = None

for col in df.columns:


if "name" in col.lower():
    student_column = col
    break


if student_column is None:


st.error(
    f"Student name column not found.\nAvailable Columns: {list(df.columns)}"
)

st.stop()


# =====================================================

# STUDENT SELECTOR

# =====================================================

st.subheader("🎓 Select Student")

selected_student = st.selectbox(
"Choose Student",
sorted(
df[student_column]
.dropna()
.astype(str)
.unique()
)
)

student = df[
df[student_column].astype(str)
== selected_student
].iloc[0]

# =====================================================

# STUDENT PROFILE

# =====================================================

st.markdown("---")

st.subheader("👤 Student Profile")

col1, col2 = st.columns(2)

with col1:

st.metric(
    "Student Name",
    selected_student
)

with col2:


if "stress_level" in df.columns:

    st.metric(
        "Dataset Stress Level",
        int(student["stress_level"])
    )


# =====================================================

# RISK SCORE

# =====================================================

risk_score = 0

risk_features = [
"anxiety_level",
"depression",
"peer_pressure",
"bullying",
"future_career_concerns"
]

for feature in risk_features:

if feature in df.columns:

    try:
        risk_score += float(
            student[feature]
        )
    except:
        pass


if "sleep_quality" in df.columns:


try:
    risk_score -= float(
        student["sleep_quality"]
    )
except:
    pass


risk_score = max(
risk_score,
0
)

# =====================================================

# RISK CATEGORY

# =====================================================

if risk_score < 15:


risk = "LOW"


elif risk_score < 30:

risk = "MEDIUM"


else:


risk = "HIGH"


# =====================================================

# GAUGE + VIDEO

# =====================================================

st.markdown("---")

left, right = st.columns([1.2, 1])

with left:


st.subheader(
    "🧠 Mental Health Risk Gauge"
)

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={
            "text":
            "Stress Risk Score"
        },
        gauge={
            "axis": {
                "range": [0, 50]
            },

            "bar": {
                "color":
                "darkred"
            },

            "steps": [

                {
                    "range": [0, 15],
                    "color": "#90EE90"
                },

                {
                    "range": [15, 30],
                    "color": "#FFD700"
                },

                {
                    "range": [30, 50],
                    "color": "#FF7F7F"
                }
            ]
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)


with right:


st.subheader(
    "🎥 Wellness Guidance"
)

if risk == "LOW":

    st.success(
        "LOW RISK STUDENT"
    )

    autoplay_video(
        "low stress.mp4"
    )

elif risk == "MEDIUM":

    st.warning(
        "MEDIUM RISK STUDENT"
    )

    autoplay_video(
        "medium stress.mp4"
    )

else:

    st.error(
        "HIGH RISK STUDENT"
    )

    autoplay_video(
        "high stress.mp4"
    )


# =====================================================

# RECOMMENDATIONS

# =====================================================

st.markdown("---")

st.subheader(
"💡 Personalized Recommendations"
)

if risk == "LOW":


st.success("""


✅ Maintain current healthy lifestyle

✅ Continue physical activity

✅ Maintain good sleep quality

✅ Stay socially active

✅ Continue positive routines
""")

elif risk == "MEDIUM":


st.warning("""


⚠ Improve sleep quality

⚠ Practice mindfulness

⚠ Reduce academic overload

⚠ Improve time management

⚠ Seek peer support
""")

else:


st.error("""


🚨 Immediate counselling recommended

🚨 Faculty intervention required

🚨 Reduce academic burden

🚨 Mental health monitoring

🚨 Increase social support

🚨 Consult a psychologist
""")

# =====================================================

# COMPLETE STUDENT DETAILS

# =====================================================

st.markdown("---")

st.subheader(
"📋 Complete Student Details"
)

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

# =====================================================

# FEATURE ANALYSIS

# =====================================================

st.markdown("---")

st.subheader(
"📊 Student Feature Analysis"
)

numeric_features = {}

for col in df.columns:


try:

    numeric_features[col] = float(
        student[col]
    )

except:
    pass


if len(numeric_features) > 0:


chart_df = pd.DataFrame(
    {
        "Feature":
        list(numeric_features.keys()),

        "Value":
        list(numeric_features.values())
    }
)

st.bar_chart(
    chart_df.set_index(
        "Feature"
    )
)
