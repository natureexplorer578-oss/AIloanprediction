import streamlit as st
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
from google import genai

# ===============================
# ENV & GEMINI
# ===============================
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ===============================
# LOAD MODELS
# ===============================
amount_model = joblib.load("loan_model.pkl")
amount_columns = joblib.load("columns.pkl")

approval_model = joblib.load("random_forest_model.pkl")
approval_columns = joblib.load("feature_columns.pkl")

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config("AI Loan Prediction", layout="wide")

# ===============================
# GLOBAL CSS
# ===============================
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

.result-card {
    background: rgba(0,0,0,0.45);
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
}

.chatbox {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 380px;
    height: 440px;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 18px;
    box-shadow: 0px 15px 40px rgba(0,0,0,0.5);
    padding: 16px;
    z-index: 9999;
}

.chatbox * {
    color: #f1f5f9 !important;
}

.chat-title {
    font-size: 18px;
    font-weight: 600;
    color: #00ffd5 !important;
    margin-bottom: 10px;
}

.chat-content {
    height: 320px;
    overflow-y: auto;
}

.chat-msg {
    background: rgba(0,0,0,0.35);
    padding: 14px;
    border-radius: 14px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# TITLE
# ===============================
st.markdown("""
<h2 style="
    text-align: center;
    margin: 0 0 20px 0;
    font-size: 34px;
    font-weight: 600;
    color: #e5e7eb;
">
🏦 AI-Driven Credit Scoring and Loan Decision Support System
</h2>
""", unsafe_allow_html=True)
# ===============================
# INPUT CARD
# ===============================


st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    dependents = st.number_input("Dependents", 0, 10, 0)
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_emp = st.selectbox("Self Employed", ["Yes", "No"])
    income = st.number_input("Annual Income", 100000, 10000000, 500000)
    cibil = st.number_input("CIBIL Score", 300, 900, 650)

with col2:
    res_asset = st.number_input("Residential Asset Value", 0)
    com_asset = st.number_input("Commercial Asset Value", 0)
    lux_asset = st.number_input("Luxury Asset Value", 0)
    bank_asset = st.number_input("Bank Asset Value", 0)
    loan_term = st.number_input("Loan Term (Years)", 1, 30, 10)

st.markdown('</div>', unsafe_allow_html=True)

# ===============================
# PREDICT BUTTON
# ===============================
st.markdown('<div style="margin-top:10px;">', unsafe_allow_html=True)
predict = st.button("🔍 Predict Loan Decision")
st.markdown('</div>', unsafe_allow_html=True)

if predict:

    edu = 1 if education == "Graduate" else 0
    self_emp = 1 if self_emp == "Yes" else 0

    # ---------- Loan Amount Prediction ----------
    amt_df = pd.DataFrame([[dependents, edu, self_emp, income, cibil,
                            res_asset, com_asset, lux_asset, bank_asset, loan_term]],
                          columns=amount_columns)

    eligible_amount = int(amount_model.predict(amt_df)[0])

    # ---------- Loan Approval ----------
    loan_income_ratio = eligible_amount / income
    income_per_dep = income / (dependents + 1)

    cibil_risk = 0 if cibil < 500 else 1 if cibil < 650 else 2
    loan_term_risk = loan_term * loan_income_ratio

    approve_df = pd.DataFrame([{
        "no_of_dependents": dependents,
        "education": edu,
        "self_employed": self_emp,
        "income_annum": income,
        "loan_amount": eligible_amount,
        "loan_term": loan_term,
        "cibil_score": cibil,
        "loan_income_ratio": loan_income_ratio,
        "income_per_dependent": income_per_dep,
        "cibil_risk": cibil_risk,
        "loan_term_risk": loan_term_risk
    }])[approval_columns]

    decision = approval_model.predict(approve_df)[0]

    # ---------- RESULT ----------
    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    if decision == 1:
        st.success("✅ Loan Approved")
        st.markdown(f"### 💰 Eligible Loan Amount: ₹ {eligible_amount:,}")
        status = "APPROVED"
    else:
        st.error("❌ Loan Rejected")
        status = "REJECTED"

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- GEMINI EXPLANATION ----------
    prompt = f"""
    Loan Status: {status}
    Income: {income}
    CIBIL: {cibil}
    Dependents: {dependents}
    Loan Term: {loan_term}

    Explain clearly in bullet points.
    If approved, congratulate.
    If rejected, explain reasons.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    st.markdown(f"""
    <div class="chatbox">
        <div class="chat-title">🤖 Loan AI Assistant</div>
        <div class="chat-content">
            <div class="chat-msg">{response.text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
