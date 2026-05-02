import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# -------------------- PAGE SETTINGS --------------------
st.set_page_config(page_title="EV AI System", layout="wide")

# -------------------- BIG UI FIX --------------------
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 22px !important;
}
h1 {font-size: 40px !important;}
h2 {font-size: 34px !important;}
h3 {font-size: 28px !important;}
[data-testid="metric-container"] {
    font-size: 24px !important;
}
label {font-size: 22px !important;}
button {font-size: 20px !important;}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("# ⚡ Smart EV Charging System")
st.markdown("### AI-based demand prediction, smart scheduling & predictive maintenance")
st.divider()

# -------------------- LOAD MODEL --------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("Model not found!")
    st.stop()

# -------------------- INPUT --------------------
st.markdown("## 🔍 Demand Prediction")

hour = st.slider("Select Hour", 0, 23)

prediction = model.predict([[hour]])[0]

# -------------------- METRICS --------------------
col1, col2, col3 = st.columns(3)

col1.metric("Predicted Vehicles", int(prediction))
col2.metric("Available Slots", 10)

util = min(int((prediction/10)*100), 100)
col3.metric("Utilization %", f"{util}%")

st.divider()

# -------------------- GRAPHS --------------------
st.markdown("## 📊 Demand Analysis")

hours = np.arange(0, 24)
preds = model.predict(hours.reshape(-1,1))

col1, col2 = st.columns(2)

# Line Graph
with col1:
    st.markdown("### 📈 Demand Curve")
    fig, ax = plt.subplots(figsize=(7,4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    ax.plot(hours, preds, marker='o', color='#00C9A7', linewidth=3)

    ax.set_xlabel("Hour", fontsize=16, color='white')
    ax.set_ylabel("Vehicles", fontsize=16, color='white')
    ax.tick_params(labelsize=14, colors='white')

    for spine in ax.spines.values():
        spine.set_color('white')

    st.pyplot(fig)

# Bar Graph
with col2:
    st.markdown("### 📊 Demand Distribution")
    fig2, ax2 = plt.subplots(figsize=(7,4))
    fig2.patch.set_facecolor('#0E1117')
    ax2.set_facecolor('#0E1117')

    ax2.bar(hours, preds, color='#4D96FF')

    ax2.set_xlabel("Hour", fontsize=16, color='white')
    ax2.set_ylabel("Vehicles", fontsize=16, color='white')
    ax2.tick_params(labelsize=14, colors='white')

    for spine in ax2.spines.values():
        spine.set_color('white')

    st.pyplot(fig2)

st.divider()

# -------------------- SMART CHARGING (NEW) --------------------
st.markdown("## ⚡ Smart Charging Simulation")

slots = 10

if prediction > slots:
    st.warning("High Demand - Queue Formed")

    queue = int(prediction - slots)
    st.write(f"🚗 Vehicles Waiting: {queue}")

    # simple scheduling visualization
    schedule = ["Charging" if i < slots else "Waiting" for i in range(int(prediction))]

    st.write("### Charging Queue Status:")
    st.write(schedule)

else:
    st.success("All Vehicles Charged Successfully")

st.divider()

# -------------------- PREDICTIVE MAINTENANCE (NEW) --------------------
st.markdown("## 🔧 Predictive Maintenance")

# Simulate sensor values
temperature = random.randint(30, 90)
usage = random.randint(50, 120)

col1, col2 = st.columns(2)

col1.metric("Charger Temperature (°C)", temperature)
col2.metric("Usage Load (%)", usage)

# Fault detection logic
if temperature > 70 or usage > 100:
    st.error("⚠️ Potential Charger Failure Detected!")
    st.write("Maintenance Required Soon")
else:
    st.success("Charger Operating Normally")

st.divider()

# -------------------- SYSTEM INSIGHT --------------------
st.markdown("## 📊 System Insight")
st.write(
    "This system integrates AI-based demand prediction, smart charging scheduling, "
    "and predictive maintenance. It improves efficiency, reduces waiting time, "
    "and prevents unexpected charger failures."
)

st.divider()

# -------------------- REAL-TIME SIMULATION --------------------
st.markdown("## ⏱ Real-Time Simulation")

if st.button("Start Simulation"):
    placeholder = st.empty()

    for h in range(24):
        pred = model.predict([[h]])[0]
        placeholder.write(f"Hour {h}: {int(pred)} vehicles")
        time.sleep(0.3)