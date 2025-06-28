import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Fetal Health Clinical Dashboard", page_icon="🩺", layout="wide")

# Soft styling
st.markdown("""
    <style>
    .reportview-container {
        background: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background: #e9f5ff;
    }
    .stButton>button {
        color: white;
        background-color: #1976d2;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🩺 Fetal Health Risk Classifier")
st.markdown("""
This dashboard predicts fetal health status (Normal, Suspect, Pathologic) from Cardiotocogram (CTG) data, 
using a Gradient Boosting model, to support early detection of fetal distress.
""")

# Sidebar inputs
st.sidebar.header("📋 Patient CTG Parameters")
inputs = {
    "baseline_value": st.sidebar.slider("Baseline FHR (bpm)", 100, 200, 120),
    "accelerations": st.sidebar.number_input("Accelerations", 0.0, 1.0, 0.003, step=0.001),
    "fetal_movement": st.sidebar.number_input("Fetal Movement", 0.0, 1.0, 0.0),
    "uterine_contractions": st.sidebar.number_input("Uterine Contractions", 0.0, 1.0, 0.0),
    "light_decelerations": st.sidebar.number_input("Light Decelerations", 0.0, 1.0, 0.0),
    "severe_decelerations": st.sidebar.number_input("Severe Decelerations", 0.0, 1.0, 0.0),
    "prolongued_decelerations": st.sidebar.number_input("Prolongued Decelerations", 0.0, 1.0, 0.0),
    "abnormal_short_term_variability": st.sidebar.number_input("Abnormal STV", 0.0, 1.0, 0.0),
    "mean_value_of_short_term_variability": st.sidebar.slider("Mean STV", 0.0, 10.0, 1.0),
    "percentage_of_time_with_abnormal_long_term_variability": st.sidebar.slider("Abnormal LTV %", 0.0, 100.0, 5.0),
    "mean_value_of_long_term_variability": st.sidebar.slider("Mean LTV", 0.0, 10.0, 2.0),
    "histogram_width": st.sidebar.slider("Histogram Width", 0.0, 100.0, 30.0),
    "histogram_min": st.sidebar.slider("Histogram Min", 0.0, 100.0, 50.0),
    "histogram_max": st.sidebar.slider("Histogram Max", 0.0, 200.0, 140.0),
    "histogram_number_of_peaks": st.sidebar.slider("Histogram Peaks", 0, 10, 2),
    "histogram_number_of_zeroes": st.sidebar.slider("Histogram Zeroes", 0, 10, 0),
    "histogram_mode": st.sidebar.slider("Histogram Mode", 0.0, 200.0, 120.0),
    "histogram_mean": st.sidebar.slider("Histogram Mean", 0.0, 200.0, 125.0),
    "histogram_median": st.sidebar.slider("Histogram Median", 0.0, 200.0, 130.0),
    "histogram_variance": st.sidebar.slider("Histogram Variance", 0.0, 100.0, 20.0),
    "histogram_tendency": st.sidebar.slider("Histogram Tendency", -10, 10, 0)
}

# Main diagnostic section
st.markdown("---")
st.header("🩺 Diagnostic Output")

if st.button("Run Fetal Health Analysis"):
    try:
        response = requests.post("https://predictcare-1.onrender.com/predict", json=inputs)
        result = response.json()
        prediction = result["prediction"]

        # Color coded prediction card
        color_map = {
            "Normal": "#d0f0c0",
            "Suspect": "#fff3cd",
            "Pathologic": "#f8d7da"
        }
        bg_color = color_map.get(prediction, "#e2e3e5")

        st.markdown(
            f"""
            <div style="background-color: {bg_color}; padding: 20px; border-radius: 8px; border: 1px solid #ccc;">
            <h3 style='text-align: center;'>🩺 Predicted Fetal Health Status: <strong>{prediction}</strong></h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Summary of input parameters
        st.subheader("📊 CTG Input Summary")
        summary_table = "| Parameter | Value |\n|-----------|-------|\n"
        for key, value in inputs.items():
            summary_table += f"| {key.replace('_',' ').capitalize()} | {value} |\n"
        st.markdown(summary_table)

    except Exception as e:
        st.error(f"API call failed. Ensure FastAPI is running.\n\n{e}")