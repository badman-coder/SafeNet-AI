# app.py
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os

# Load the trained model
model = joblib.load("classifier.pkl")

st.set_page_config(page_title="SafeNet AI", page_icon="🧠", layout="centered")
st.title("🧠 SafeNet AI — Scam & Harmful Message Detector")
st.write("Analyze any text message to check if it’s **safe or suspicious**. 🚨")

# Text input
message = st.text_area("✉️ Paste or type the message here:")

if st.button("Analyze Message"):
    if message.strip() == "":
        st.warning("Please enter a message first.")
    else:
        prediction = model.predict([message])[0]
        if prediction == 1:
            st.error("⚠️ This message looks **suspicious or harmful**.")
        else:
            st.success("✅ This message seems safe.")

# --- REPORT MESSAGE SECTION ---
st.subheader("🚨 Report a Message")
st.write("If you think a message is harmful or scammy, help improve SafeNet by reporting it.")

if st.button("Report Message"):
    if message.strip() == "":
        st.warning("Please enter a message before reporting.")
    else:
        report_data = pd.DataFrame({
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "message": [message]
        })
        file_exists = os.path.isfile("reports.csv")
        report_data.to_csv("reports.csv", mode="a", header=not file_exists, index=False)
        st.info("✅ Message reported successfully! Thank you for helping improve SafeNet AI.")

# --- ADMIN DASHBOARD (Password Protected) ---
st.markdown("---")
st.header("📊 Admin Access — SafeNet Reports Dashboard")

password = st.text_input("🔑 Enter admin password to view reports:", type="password")

# You can change this password anytime
ADMIN_PASSWORD = "safenetadmin2025"

if password == ADMIN_PASSWORD:
    if os.path.exists("reports.csv"):
        df = pd.read_csv("reports.csv", names=["timestamp", "message"], header=0)
        st.success(f"✅ Access granted. Total reports: {len(df)}")
        st.dataframe(df.tail(10))
    else:
        st.info("No reports have been submitted yet.")
elif password != "":
    st.error("❌ Wrong password. Access denied.")
