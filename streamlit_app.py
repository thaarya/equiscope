import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Startup Valuation Dashboard", layout="wide")

# --- Hardcoded Login ---
USER_CREDENTIALS = {"admin": "pass123", "arya": "val2025"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login to Access Dashboard")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if USER_CREDENTIALS.get(username) == password:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    st.stop()

# --- Sidebar Navigation ---
st.sidebar.title("📊 Dashboard")
page = st.sidebar.radio("Navigate", ["Estimator", "Graphs", "About"])

# --- Simulated Dataset ---
data = {
    "funding": [2, 5, 7, 3, 9],
    "revenue": [1, 6, 5, 2, 8],
    "users": [500, 4000, 3500, 1000, 6000],
    "burn_rate": [10, 20, 15, 12, 25],
    "growth_rate": [15, 30, 40, 18, 50],
    "valuation": [20, 80, 75, 30, 120]
}
df = pd.DataFrame(data)

# --- Linear Regression Model ---
X = df[["funding", "revenue", "users", "burn_rate", "growth_rate"]]
y = df["valuation"]
model = LinearRegression()
model.fit(X, y)

# --- Estimator Page ---
if page == "Estimator":
    st.title("📈 AI-powered Startup Valuation Estimator")
    st.markdown("""
    Enter your startup's key metrics to get an estimated valuation.
    This tool uses a regression model trained on sample startup data.
    """)

    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            funding = st.number_input("Total Funding (₹ Cr)", min_value=0.0, value=2.0)
            revenue = st.number_input("Annual Revenue (₹ Cr)", min_value=0.0, value=1.0)
        with col2:
            users = st.number_input("Active Users (in 1000s)", min_value=0.0, value=500.0)
            burn_rate = st.number_input("Burn Rate (₹ Lakh/month)", min_value=0.0, value=10.0)
        with col3:
            growth_rate = st.slider("User Growth Rate %", 0, 100, 15)
        submitted = st.form_submit_button("Estimate Valuation")

    if submitted:
        user_input = np.array([[funding, revenue, users, burn_rate, growth_rate]])
        pred = model.predict(user_input)[0]
        st.subheader("💸 Estimated Valuation")
        st.success(f"₹ {pred:.2f} Crores")

        with st.expander("📊 View Training Dataset"):
            st.dataframe(df)

# --- Graphs Page ---
elif page == "Graphs":
    st.title("📉 Visual Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(px.scatter(df, x="funding", y="valuation", trendline="ols", title="Valuation vs Funding"))
        st.plotly_chart(px.bar(df, x="revenue", y="valuation", title="Revenue vs Valuation"))

    with col2:
        st.plotly_chart(px.pie(df, values="valuation", names="growth_rate", title="Valuation by Growth Rate"))
        st.plotly_chart(px.line(df, x="users", y="valuation", title="Users vs Valuation"))

# --- About Page ---
elif page == "About":
    st.title("📘 About This App")
    st.markdown("""
    **Equiscope** is an AI-powered valuation tool built with Streamlit. 

    It lets early-stage startups estimate their worth using a linear regression model trained on simulated startup data.

    **Features:**
    - Login-based dashboard access
    - Input-driven valuation estimator
    - Interactive graphs with Plotly
    - Simple, modern UI

    Built by Arya Shinde 💡
    """)

