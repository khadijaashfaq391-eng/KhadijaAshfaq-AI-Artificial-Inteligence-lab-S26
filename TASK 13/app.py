import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Flight Fare Predictor", layout="centered")

# -------------------------------
# Custom CSS Styling
# -------------------------------
st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background-color: #E6D5F7;
    }

    /* Title */
    h1 {
        color: #6A0DAD;
        text-align: center;
        font-weight: bold;
    }

    /* Subheaders */
    h2, h3 {
        color: #7B1FA2;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(to right, #ff66c4, #c77dff);
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #ff1493, #9d4edd);
        transform: scale(1.03);
        box-shadow: 0px 0px 15px #ff66c4;
    }

    /* Info Box */
    .stAlert {
        border-radius: 10px;
    }

    /* Success Message */
    .stSuccess {
        background-color: #ffd6f6;
        color: #c2185b;
        border-radius: 10px;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.title("✈️ Flight Fare Prediction System")
st.markdown("### Predict flight ticket prices using Machine Learning")

# -------------------------------
# Load Model & Files
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
encoders = joblib.load("encoders.pkl")
columns = joblib.load("columns.pkl")

# -------------------------------
# User Inputs (UI Section)
# -------------------------------
st.subheader("📝 Enter Flight Details")

col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("Airline", encoders['Airline'].classes_)
    source = st.selectbox("Source", encoders['Source'].classes_)
    total_stops = st.selectbox("Total Stops", encoders['Total_Stops'].classes_)

with col2:
    destination = st.selectbox("Destination", encoders['Destination'].classes_)
    additional_info = st.selectbox("Additional Info", encoders['Additional_Info'].classes_)

# Date
st.subheader("📅 Journey Date")
journey_day = st.slider("Day", 1, 31, 10)
journey_month = st.slider("Month", 1, 12, 5)

# Time
st.subheader("⏰ Time Details")

col3, col4 = st.columns(2)

with col3:
    dep_hour = st.slider("Departure Hour", 0, 23, 10)
    dep_min = st.slider("Departure Minute", 0, 59, 0)

with col4:
    arrival_hour = st.slider("Arrival Hour", 0, 23, 12)
    arrival_min = st.slider("Arrival Minute", 0, 59, 0)

# -------------------------------
# Auto Duration Calculation
# -------------------------------
dep_total = dep_hour * 60 + dep_min
arr_total = arrival_hour * 60 + arrival_min

if arr_total < dep_total:
    duration = (24 * 60 - dep_total) + arr_total
else:
    duration = arr_total - dep_total

st.info(f"⏱️ Duration: {duration//60}h {duration%60}m ({duration} minutes)")

# -------------------------------
# Encoding Function
# -------------------------------
def encode(col, val):
    return encoders[col].transform([val])[0]

# -------------------------------
# Prediction
# -------------------------------
if st.button("✨ Predict Fare ✨"):

    data = {
        'Airline': encode('Airline', airline),
        'Source': encode('Source', source),
        'Destination': encode('Destination', destination),
        'Total_Stops': encode('Total_Stops', total_stops),
        'Additional_Info': encode('Additional_Info', additional_info),
        'Journey_Day': journey_day,
        'Journey_Month': journey_month,
        'Duration': duration,
        'Dep_Hour': dep_hour,
        'Dep_Min': dep_min,
        'Arrival_Hour': arrival_hour,
        'Arrival_Min': arrival_min
    }

    input_df = pd.DataFrame([data])

    # Match training columns exactly
    input_df = input_df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(input_df)

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(to right, #ff66c4, #c77dff);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0px 0px 20px #ff66c4;
        ">
            ✨💖 Estimated Flight Price: Rs {round(prediction[0], 2)} 💖✨
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("🌸 Developed as AI Project | Flight Fare Prediction System 🌸")