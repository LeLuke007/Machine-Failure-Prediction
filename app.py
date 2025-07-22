import streamlit as st
import numpy as np
import joblib

lr = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(page_title="Machine Failure Predictor", page_icon="🛠️", layout="centered")

st.title("Machine Failure Prediction")

st.markdown("### 📊 Input Sensor Parameters")
col1, col2 = st.columns(2)

with col1:
    type_input = st.selectbox("Type", options=["H", "L", "M"])
    air_temp = st.text_input("Air Temperature [K]", value="298.0")
    proc_temp = st.text_input("Process Temperature [K]", value="310.0")

with col2:
    speed = st.text_input("Rotational Speed [rpm]", value="1600")
    torque = st.text_input("Torque [Nm]", value="35.0")
    tool_wear = st.text_input("Tool Wear [min]", value="90")

try:
    air_temp = float(air_temp)
    proc_temp = float(proc_temp)
    speed = int(speed)
    torque = float(torque)
    tool_wear = int(tool_wear)
    type_input = 1 if type_input == 'L' else (2 if type_input == 'M' else 0)

    valid = True
    if not (1000 <= speed <= 3000):
        st.warning("Rotational Speed should be between 1000 and 3000 rpm.")
        valid = False
    if not (290 <= air_temp <= 320):
        st.warning("Air Temperature should be between 290 and 320 K.")
        valid = False
    if not (300 <= proc_temp <= 340):
        st.warning("Process Temperature should be between 300 and 340 K.")
        valid = False
    if not (0 <= torque <= 100):
        st.warning("Torque should be between 0 and 100 Nm.")
        valid = False
    if not (0 <= tool_wear <= 250):
        st.warning("Tool Wear should be between 0 and 250 min.")
        valid = False

    if st.button("🔍 Predict"):
        if valid:
            input_vector = np.array([type_input, air_temp, proc_temp, speed, torque, tool_wear]).reshape(1, -1)
            input_scaled = scaler.transform(input_vector)
            fail_pred = lr.predict(input_scaled)[0]
            if fail_pred == 1:
                st.error("⚠️ Machine is likely to FAIL")
            else:
                st.success("✅ Machine is NOT likely to FAIL")
        else:
            st.info("Please correct the input values above.")
except ValueError:
    st.warning("Please enter valid numeric values for all fields")