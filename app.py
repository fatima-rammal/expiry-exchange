import streamlit as st
import pandas as pd

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Expiry Exchange",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# Title
# -----------------------------
st.title("♻️ EXPIRY EXCHANGE")

st.subheader("Don't buy new. Exchange what already exists.")

st.write(
    "A smart platform that connects healthcare facilities "
    "with surplus supplies before they expire."
)

st.divider()

# -----------------------------
# Main choices
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏥 I HAVE SURPLUS")
    st.write(
        "Tell us about supplies you have available."
    )

    product = st.selectbox(
        "What product do you have?",
        ["Gauze", "Gloves", "IV Sets"]
    )

    quantity = st.number_input(
        "Quantity available",
        min_value=1,
        value=100
    )

    expiry_date = st.date_input(
        "Expiry date"
    )

    if st.button("🔎 Check expiry risk"):

        today = pd.Timestamp.today().normalize()
        expiry = pd.Timestamp(expiry_date)

        days_left = (expiry - today).days

        if days_left <= 30:
            risk = "🔴 High"
        elif days_left <= 60:
            risk = "🟠 Medium"
        else:
            risk = "🟢 Low"

        st.success("Inventory checked!")

        st.metric(
            "Days until expiry",
            days_left
        )

        st.write("### Expiry Risk:", risk)

with col2:
    st.subheader("🔎 I NEED SUPPLIES")
    st.write(
        "Search for available surplus "
        "instead of buying new."
    )

    st.info(
        "The matching system will be available here."
    )

# -----------------------------
# Simple inventory
# -----------------------------
st.subheader("📦 Example Inventory")

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
    ]
})

st.dataframe(inventory, use_container_width=True)
