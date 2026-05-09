import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import joblib
import numpy as np
st.set_page_config(
    page_title="AI Career Risk Analyzer",
    page_icon="🚀",
    layout="wide"
)
modern_theme = """
<style>

.stApp {
    background-color: #F5F7FB;
}

.main {
    background-color: #F5F7FB;
}

h1 {
    color: #111827;
    font-weight: 800;
}

h2, h3 {
    color: #1F2937;
}

p, label {
    color: #4B5563;
}

[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

div.stButton > button {
    background: linear-gradient(to right, #4F46E5, #7C3AED);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    border: none;
    font-size: 18px;
    font-weight: 600;
}

div.stButton > button:hover {
    opacity: 0.9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
"""

st.markdown(modern_theme, unsafe_allow_html=True)
st.sidebar.title("About")
st.sidebar.write(
    "This AI model predicts placement probability based on academic and skill factors."
)
model = joblib.load(r"D:\ai career analyzer\models\placement_model.pkl")
st.title("🚀 AI Career Risk Analyzer")
st.caption("ML-powered placement prediction dashboard")
st.markdown("""
<div style="
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 4px 15px rgba(0,0,0,0.06);
margin-bottom:25px;
">

<h3 style="color:#111827;">
🎯 AI Placement Analysis
</h3>

<p style="color:#4B5563;font-size:16px;">
Analyze placement readiness using CGPA, aptitude,
projects, internships, communication skills,
and extracurricular performance.
</p>

</div>
""", unsafe_allow_html=True)
st.write("Predict placement chances using AI")
cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)

internships = st.number_input("Internships", 0, 10, 1)

projects = st.number_input("Projects", 0, 20, 2)

certifications = st.number_input("Certifications", 0, 20, 1)

aptitude = st.slider("Aptitude Score", 0, 100, 50)

soft_skills = st.slider("Soft Skills Rating", 0.0, 10.0, 5.0)

extracurricular = st.selectbox(
    "Extracurricular Activities",
    [0, 1]
)

training = st.selectbox(
    "Placement Training",
    [0, 1]
)

ssc = st.slider("SSC Marks", 0, 100, 70)

hsc = st.slider("HSC Marks", 0, 100, 70)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CGPA", cgpa)

with col2:
    st.metric("Projects", projects)

with col3:
    st.metric("Aptitude", aptitude)
if st.button("Predict Placement"):

    input_data = np.array([[
        cgpa,
        internships,
        projects,
        certifications,
        aptitude,
        soft_skills,
        extracurricular,
        training,
        ssc,
        hsc
    ]])

    prediction = model.predict(input_data)
    probability=model.predict_proba(input_data)

    if prediction[0] == 1:
        st.success("High Chance of Placement 🎉")
    else:
        st.error("Placement Risk Detected ⚠️")
        placement_probability = probability[0][1] * 100
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = placement_probability,
            title = {'text': "Placement Confidence"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'thickness': 0.3},
                'steps': [
                    {'range': [0, 40], 'color': "lightcoral"},
                    {'range': [40, 70], 'color': "khaki"},
                    {'range': [70, 100], 'color': "lightgreen"}
                 ]
            }
    ))

    if placement_probability >= 80:
        st.success("Excellent profile! Keep applying confidently 🚀")
    elif placement_probability >= 60:
        st.info("Good chances! Improving aptitude and projects can help 📈")
    else:
        st.warning("Focus on skills, projects, and aptitude improvement ⚡")
        st.markdown("---")
        st.subheader("AI Career Suggestions")
    if projects < 2:
        st.warning("Build more real-world projects to strengthen your resume.")
    if aptitude < 70:
        st.warning("Improve aptitude skills for placement tests.")
    if internships < 1:
        st.warning("Try gaining internship experience.")
    if soft_skills < 7:
        st.warning("Improve communication and teamwork skills.")
    if cgpa > 8:
        st.success("Strong academic profile detected 🎓")
        st.caption("Built with ❤️ using Python, Machine Learning & Streamlit")
        st.subheader("Feature Impact Overview")

        importance = model.feature_importances_

        feature_names = [
            "CGPA",
            "Internships",
            "Projects",
            "Certifications",
            "Aptitude",
            "Soft Skills",
            "Extracurricular",
            "Training",
            "SSC",
            "HSC"
        ]

        fig, ax = plt.subplots(figsize=(10,5))

        bars = ax.bar(feature_names, importance)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:.2f}",
                ha='center',
                va='bottom'
        )

    plt.xticks(rotation=45)

    st.subheader("AI Insights")

    top_feature = max(
        {
            "CGPA": cgpa,
            "Aptitude": aptitude,
            "Projects": projects,
            "Soft Skills": soft_skills
        },
        key=lambda x: {
            "CGPA": cgpa,
            "Aptitude": aptitude,
            "Projects": projects,
            "Soft Skills": soft_skills
        }[x]
    )

    st.write(f"Strongest area detected: **{top_feature}**")
    st.markdown("---")
    st.subheader("📄 AI Career Report")

    report = []

    if cgpa >= 8:
        report.append("✅ Strong academic performance detected.")

    if aptitude >= 80:
        report.append("🧠 Excellent aptitude skills.")

    if projects >= 3:
        report.append("💻 Good practical project experience.")

    if internships >= 1:
        report.append("🏢 Internship experience adds strong value.")

    if soft_skills >= 8:
        report.append("🗣️ Strong communication and soft skills.")

    if placement_probability < 60:
        report.append("⚠️ Placement probability is below ideal range. Focus on projects and aptitude.")

    if placement_probability >= 80:
        report.append("🚀 Profile looks highly placement-ready.")

    for item in report:
        st.write(item)