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
        "I have unused healthcare supplies "
        "that may not be used before expiry."
    )

    if st.button("Find a facility that needs them"):
        st.success("Great! We'll help you find a match.")

with col2:
    st.subheader("🔎 I NEED SUPPLIES")
    st.write(
        "I need a healthcare supply "
        "and want to avoid buying new."
    )

    if st.button("Search available supplies"):
        st.success("Let's find available surplus!")

st.divider()

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
