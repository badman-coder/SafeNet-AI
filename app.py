# app.py
import streamlit as st
import joblib
from sentence_transformers import SentenceTransformer

# Load model and classifier
@st.cache_resource
def load_models():
    clf = joblib.load("classifier.pkl")
    embedder = SentenceTransformer("text_encoder")
    return clf, embedder

clf, embedder = load_models()

# Streamlit interface
st.set_page_config(page_title="SafeNet AI", page_icon="🧠")
st.title("🧠 SafeNet AI")
st.write("### Detect harmful or safe messages instantly")

user_input = st.text_area("Enter a message to analyze:")

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please type something first.")
    else:
        embedding = embedder.encode([user_input])
        prediction = clf.predict(embedding)[0]

        if prediction == "harmful":
            st.error("🚨 This message appears **HARMFUL**.")
        else:
            st.success("✅ This message appears **SAFE**.")
