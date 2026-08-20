
import streamlit as st
import pandas as pd

st.title("♻️ EXPIRY EXCHANGE")
st.write("Prevent healthcare waste. Reduce unnecessary purchases.")

inventory = pd.DataFrame({
    "Facility": [
        "City Hospital",
        "City Hospital",
        "Medical Center",
        "Community Clinic"
    ],
    "Product": [
        "Gauze",
        "Gloves",
        "Gauze",
        "Gloves"
    ],
    "Quantity": [
        1000,
        5000,
        200,
        3000
    ],
    "Expiry": [
        "2026-11-15",
        "2026-10-20",
        "2026-12-10",
        "2026-09-30"
    ],
    "Unit Price": [
        1.00,
        0.40,
        1.00,
        0.40
    ]
})

st.subheader("Current Inventory")
st.dataframe(inventory)
