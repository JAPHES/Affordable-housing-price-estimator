import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Affordable Housing Price Predictor",
    page_icon="",
    layout="centered",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 30px;
        width: 100%;
        border: none;
    }
    .stButton > button:hover { background-color: #1b5e20; }
    .result-box {
        background: linear-gradient(135deg, #2e7d32, #66bb6a);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(46,125,50,0.3);
    }
    .info-box {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .section-header {
        color: #2e7d32;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load model
# ─────────────────────────────────────────────
MODEL_PATH = "affordable_price_model.pkl"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

model = load_model()

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.title("Affordable Housing Price Estimator")
st.subheader("Predicted House Price Estimator")

st.markdown("""
<div class="info-box">
    Fill in the house details below to get an estimated price in Kenyan Shillings (KES).
    The model was trained on affordable housing data using Linear Regression.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Model check
# ─────────────────────────────────────────────
if model is None:
    st.error(
        f"Model file `{MODEL_PATH}` not found!\n\n"
        "Please make sure `affordable_price_model.pkl` is in the same directory as this app."
    )
    st.info("Run your training notebook first to generate the model file, then relaunch this app.")
    st.stop()

# ─────────────────────────────────────────────
# Feature info (columns selected by correlation > 0.25)
# The model used high-correlation features from the dataset.
# Common high-corr features in Kenya housing data:
# final_price_ksh (target), size_sqft, num_bedrooms, num_bathrooms,
# floor_number, distance_to_cbd_km, monthly_rent_ksh,
# proximity_to_school_km, proximity_to_hospital_km,
# house_type (encoded), location (encoded), housing_category (encoded)
# ─────────────────────────────────────────────

# Retrieve feature names from model if possible
try:
    feature_names = model.feature_names_in_.tolist()
except AttributeError:
    # Fallback: common high-corr features from Kenya affordable housing dataset
    feature_names = [
        'size_sqft', 'num_bedrooms', 'num_bathrooms',
        'floor_number', 'distance_to_cbd_km', 'monthly_rent_ksh',
        'proximity_to_school_km', 'proximity_to_hospital_km',
        'house_type', 'location', 'housing_category'
    ]

# ─────────────────────────────────────────────
# Build UI inputs dynamically based on feature names
# ─────────────────────────────────────────────

st.markdown('<div class="section-header">Property Details</div>', unsafe_allow_html=True)

inputs = {}
col1, col2 = st.columns(2)

# Define friendly labels & sensible defaults for known features
feature_config = {
    'size_sqft':                 {"label": "House Size (sq ft)",              "min": 100,   "max": 5000,  "default": 800,  "step": 10,   "col": col1, "help": "Total area of the house"},
    'num_bedrooms':              {"label": "Number of Bedrooms",               "min": 1,     "max": 10,    "default": 3,    "step": 1,    "col": col2, "help": "Bedrooms count"},
    'num_bathrooms':             {"label": "Number of Bathrooms",              "min": 1,     "max": 8,     "default": 2,    "step": 1,    "col": col1, "help": "Bathrooms count"},
    'floor_number':              {"label": "Floor Number",                     "min": 0,     "max": 30,    "default": 0,    "step": 1,    "col": col2, "help": "0 = ground floor"},
    'distance_to_cbd_km':        {"label": "Distance to CBD (km)",             "min": 0.0,   "max": 80.0,  "default": 10.0, "step": 0.5,  "col": col1, "help": "Distance to Nairobi CBD"},
    'monthly_rent_ksh':          {"label": "Monthly Rent (KES)",               "min": 1000,  "max": 500000,"default": 25000,"step": 500,  "col": col2, "help": "Estimated monthly rent"},
    'proximity_to_school_km':    {"label": "Distance to Nearest School (km)",  "min": 0.0,   "max": 20.0,  "default": 2.0,  "step": 0.1,  "col": col1, "help": "km to nearest school"},
    'proximity_to_hospital_km':  {"label": "Distance to Nearest Hospital (km)","min": 0.0,   "max": 20.0,  "default": 3.0,  "step": 0.1,  "col": col2, "help": "km to nearest hospital"},
    'house_type':                {"label": "House Type (encoded int)",          "min": 0,     "max": 20,    "default": 1,    "step": 1,    "col": col1, "help": "Label-encoded house type from training"},
    'location':                  {"label": "Location (encoded int)",            "min": 0,     "max": 100,   "default": 5,    "step": 1,    "col": col2, "help": "Label-encoded location from training"},
    'housing_category':          {"label": "Housing Category (encoded int)",    "min": 0,     "max": 10,    "default": 1,    "step": 1,    "col": col1, "help": "Label-encoded housing category from training"},
}

for feat in feature_names:
    cfg = feature_config.get(feat)
    if cfg:
        container = cfg["col"]
        if isinstance(cfg["default"], float) or isinstance(cfg["step"], float):
            inputs[feat] = container.number_input(
                cfg["label"],
                min_value=float(cfg["min"]),
                max_value=float(cfg["max"]),
                value=float(cfg["default"]),
                step=float(cfg["step"]),
                help=cfg["help"]
            )
        else:
            inputs[feat] = container.number_input(
                cfg["label"],
                min_value=int(cfg["min"]),
                max_value=int(cfg["max"]),
                value=int(cfg["default"]),
                step=int(cfg["step"]),
                help=cfg["help"]
            )
    else:
        # Generic fallback for unknown features
        inputs[feat] = st.number_input(
            f"{feat.replace('_', ' ').title()}",
            value=0.0,
            help=f"Enter value for {feat}"
        )

# ─────────────────────────────────────────────
# Encoded columns notice
# ─────────────────────────────────────────────
if any(f in feature_names for f in ['house_type', 'location', 'housing_category']):
    st.markdown("""
    <div class="info-box" style="margin-top:15px; font-size:13px;">
        ℹ️ <b>Note on encoded fields:</b> <code>house_type</code>, <code>location</code>, and 
        <code>housing_category</code> are integer codes produced by LabelEncoder during training. 
        Enter the same integer codes used in your training data for accurate predictions.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Predict button
# ─────────────────────────────────────────────
st.markdown("---")
if st.button("Predict House Price"):
    try:
        input_df = pd.DataFrame([inputs])
        input_df = input_df[feature_names]  # ensure correct column order

        predicted_price = model.predict(input_df)[0]
        predicted_price = max(0, predicted_price)  # no negative prices

        formatted = f"KES {predicted_price:,.0f}"
        st.markdown(f"""
        <div class="result-box">
            Estimated House Price<br>
            <span style="font-size:36px">{formatted}</span>
        </div>
        """, unsafe_allow_html=True)

        # Breakdown expander
        with st.expander("See input summary"):
            summary_df = pd.DataFrame(inputs.items(), columns=["Feature", "Value"])
            st.dataframe(summary_df, use_container_width=True)

    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.info("Make sure all inputs match the features the model was trained on.")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Streamlit · Model: Linear Regression · Data: Affordable Housing Dataset")