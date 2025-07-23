import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
from io import BytesIO
import base64

# --- Page Config ---
st.set_page_config(page_title="Equiscope - AI Startup Valuation", layout="wide")

# --- Custom Theme Styling ---
st.markdown('''
    <style>
    html, body, .main, .block-container {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton > button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6em 1.4em;
        font-weight: 600;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #f5f5f5;
        color: black;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 0.5em;
    }
    .stSlider > div > div > div {
        background: #ff4b4b;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h4, p, li {
        font-family: 'Montserrat', sans-serif;
    }
    </style>
''', unsafe_allow_html=True)

# --- Login Logic ---
USER_CREDENTIALS = {"admin": "pass123", "arya": "val2025"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        st.image("https://cdn-icons-png.flaticon.com/512/4052/4052984.png", width=80)
        st.markdown("## 🔐 Login to Equiscope")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if USER_CREDENTIALS.get(username) == password:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4052/4052984.png", width=50)
st.sidebar.title("Equiscope")
page = st.sidebar.radio("📁 Pages", ["Valuation Estimator", "Analytics Dashboard", "Comparable Startups", "Download Report", "About Project"])

# --- Sample Dataset ---
data = {
    "funding": [2, 5, 7, 3, 9],
    "revenue": [1, 6, 5, 2, 8],
    "users": [500, 4000, 3500, 1000, 6000],
    "burn_rate": [10, 20, 15, 12, 25],
    "growth_rate": [15, 30, 40, 18, 50],
    "valuation": [20, 80, 75, 30, 120]
}
df = pd.DataFrame(data)

X = df[["funding", "revenue", "users", "burn_rate", "growth_rate"]]
y = df["valuation"]
model = LinearRegression()
model.fit(X, y)

# --- Valuation Estimator ---
if page == "Valuation Estimator":
    st.markdown("""
        <h1 style='text-align:center;'>📈 <span style='color:#ff4b4b;'>Startup Valuation Estimator</span></h1>
        <p style='text-align:center;color:#666;'>Fill in your startup's details to estimate its valuation.</p>
    """, unsafe_allow_html=True)

    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            funding = st.number_input("💰 Total Funding (₹ Cr)", min_value=0.0, value=2.0)
            revenue = st.number_input("📊 Annual Revenue (₹ Cr)", min_value=0.0, value=1.0)
        with col2:
            users = st.number_input("👥 Active Users (in 1000s)", min_value=0.0, value=500.0)
            burn_rate = st.number_input("🔥 Burn Rate (₹ Lakh/month)", min_value=0.0, value=10.0)
        with col3:
            growth_rate = st.slider("📈 User Growth Rate %", 0, 100, 15)

        submitted = st.form_submit_button("🚀 Estimate Valuation")

    if submitted:
        with st.spinner("Calculating valuation..."):
            user_input = np.array([[funding, revenue, users, burn_rate, growth_rate]])
            pred = model.predict(user_input)[0]

        st.success(f"💸 Estimated Valuation: ₹ {pred:.2f} Crores")
        with st.expander("📁 View Sample Training Dataset"):
            st.dataframe(df)

# --- Analytics Dashboard ---
elif page == "Analytics Dashboard":
    st.markdown("""
        <h1 style='text-align:center;'>📊 <span style='color:#ff4b4b;'>Valuation Analytics</span></h1>
        <p style='text-align:center;color:#666;'>Interactive visualizations to explore startup metrics.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.scatter(df, x="funding", y="valuation", trendline="ols", title="Valuation vs Funding"))
        st.plotly_chart(px.bar(df, x="revenue", y="valuation", title="Revenue vs Valuation"))
    with col2:
        st.plotly_chart(px.pie(df, values="valuation", names="growth_rate", title="Valuation by Growth Rate"))
        st.plotly_chart(px.line(df, x="users", y="valuation", title="Users vs Valuation"))

# --- Comparable Startups ---
elif page == "Comparable Startups":
    st.markdown("""
        <h1 style='text-align:center;'>🔍 <span style='color:#ff4b4b;'>Comparable Startups</span></h1>
        <p style='text-align:center;color:#666;'>Similar startups to benchmark your valuation.</p>
    """, unsafe_allow_html=True)

    st.dataframe(df.style.highlight_max(axis=0).format("{:.2f}"))

# --- Report Download ---
elif page == "Download Report":
    st.markdown("""
        <h1 style='text-align:center;'>📄 <span style='color:#ff4b4b;'>Export Valuation Report</span></h1>
        <p style='text-align:center;color:#666;'>Download your input and estimated valuation for records.</p>
    """, unsafe_allow_html=True)

    report_df = df.copy()
    csv = report_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="valuation_report.csv">📥 Download CSV Report</a>'
    st.markdown(href, unsafe_allow_html=True)

# --- About Page ---
elif page == "About Project":
    st.markdown("""
        <h1 style='text-align:center;'>📘 <span style='color:#ff4b4b;'>About Equiscope</span></h1>
        <p style='text-align:center;color:#666;'>An AI-powered tool built to help estimate startup valuation.</p>
        <hr>
        <h4 style='color:#ff4b4b;'>💡 Features</h4>
        <ul>
            <li>Secure login with user management</li>
            <li>AI-based valuation prediction</li>
            <li>Interactive analytics dashboard</li>
            <li>Comparable startups section</li>
            <li>Export report functionality</li>
            <li>Clean white-red UI for professionalism</li>
        </ul>
        <h4 style='color:#ff4b4b;'>👤 Built By</h4>
        <p>Arya Shinde, 2025</p>
    """, unsafe_allow_html=True)
