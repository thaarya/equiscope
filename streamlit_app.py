import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Startup Valuation Estimator", layout="centered")
st.title("📈 AI-powered Startup Valuation Estimator")

st.markdown("""
Enter your startup's key metrics to get an estimated valuation. 
This tool uses a simple regression model based on comparable startups.
""")

# --- User Inputs ---
col1, col2 = st.columns(2)
with col1:
    funding = st.number_input("Total Funding Received (₹ Crores)", min_value=0.0, value=2.0)
    users = st.number_input("Number of Active Users (in thousands)", min_value=0.0, value=500.0)
with col2:
    revenue = st.number_input("Annual Revenue (₹ Crores)", min_value=0.0, value=1.0)
    burn_rate = st.number_input("Monthly Burn Rate (₹ Lakhs)", min_value=0.0, value=10.0)

growth_rate = st.slider("User Growth Rate (Monthly %)", 0, 100, 15)

# --- Simulated Dataset for Training ---
data = {
    "funding": [2, 5, 7, 3, 9],
    "revenue": [1, 6, 5, 2, 8],
    "users": [500, 4000, 3500, 1000, 6000],
    "burn_rate": [10, 20, 15, 12, 25],
    "growth_rate": [15, 30, 40, 18, 50],
    "valuation": [20, 80, 75, 30, 120]
}
df = pd.DataFrame(data)

# --- Model Training ---
X = df[["funding", "revenue", "users", "burn_rate", "growth_rate"]]
y = df["valuation"]
model = LinearRegression()
model.fit(X, y)

# --- Prediction ---
user_input = np.array([[funding, revenue, users, burn_rate, growth_rate]])
pred = model.predict(user_input)[0]

st.subheader("💸 Estimated Valuation")
st.success(f"₹ {pred:.2f} Crores")

with st.expander("📊 View Sample Data Used for Estimation"):
    st.dataframe(df)

st.caption("Built by Arya Shinde | Streamlit AI Project")

