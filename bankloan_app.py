import streamlit as st
import pickle
import numpy as np

# --- Load model from same folder ---
MODEL_PATH = "bankloan_default.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# --- Dummy credentials for local use ---
USERS = {"vivek": "pass123", "admin": "admin"}

# --- Session state init ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Login UI ---
def login():
    st.title("🏦 Bank Loan Default App - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()  # ✅ Replaces deprecated experimental_rerun
        else:
            st.error("Invalid username or password")

# --- Logout function ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()  # ✅ Replaces deprecated experimental_rerun

# --- Prediction UI ---
def main_app():
    st.title("📈 Bank Loan Default Predictor")

    with st.form("loan_form"):
        age = st.number_input("Age", min_value=18, max_value=100)
        ed = st.selectbox("Education Level (1 to 4)", [1, 2, 3, 4])
        employ = st.number_input("Years Employed", min_value=0)
        address = st.number_input("Years at Address", min_value=0)
        income = st.number_input("Annual Income (₹000)", min_value=0.0)
        debtinc = st.number_input("Debt-to-Income Ratio (%)", min_value=0.0)
        creddebt = st.number_input("Credit Card Debt", min_value=0.0)
        othdebt = st.number_input("Other Debt", min_value=0.0)

        submit = st.form_submit_button("Predict")

    if submit:
        input_data = np.array([[age, ed, employ, address, income, debtinc, creddebt, othdebt]])
        prediction = model.predict(input_data)[0]
        result = "⚠️ High Risk of Default" if prediction == 1.0 else "✅ Low Risk (Likely to Repay)"
        st.success(f"Prediction: {result}")

    st.button("Logout", on_click=logout)

# --- App entry point ---
if st.session_state.logged_in:
    main_app()
else:
    login()
