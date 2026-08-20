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

# -----------------------------
# I HAVE SURPLUS
# -----------------------------

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

    if st.button("🔎 Find a Match"):

        # -----------------------------
        # Calculate expiry risk
        # -----------------------------

        today = pd.Timestamp.today().normalize()
        expiry = pd.Timestamp(expiry_date)

        days_left = (expiry - today).days

        if days_left <= 30:
            risk = "🔴 High"
        elif days_left <= 60:
            risk = "🟠 Medium"
        else:
            risk = "🟢 Low"

        st.success("Inventory analyzed!")

        st.metric(
            "Days until expiry",
            days_left
        )

        st.write("### Expiry Risk:", risk)

        # -----------------------------
        # Demand data
        # -----------------------------

        demand = pd.DataFrame({
            "Facility": [
                "Medical Center",
                "Community Clinic",
                "University Hospital"
            ],
            "Product": [
                "Gloves",
                "Gauze",
                "Gloves"
            ],
            "Quantity Needed": [
                2000,
                500,
                1500
            ]
        })

        # -----------------------------
        # Find matches
        # -----------------------------

        matches = demand[
            (demand["Product"] == product) &
            (demand["Quantity Needed"] <= quantity)
        ]

        if len(matches) > 0:

            st.subheader("🎯 Potential Match Found!")

            for _, match in matches.iterrows():

                st.write(
                    f"🏥 **{match['Facility']}** needs "
                    f"**{match['Quantity Needed']:,} {product}**"
                )

                st.write(
                    f"Your available quantity: "
                    f"**{quantity:,}**"
                )

                st.success(
                    "✅ Quantity requirement satisfied!"
                )

                # -----------------------------
                # Financial impact
                # -----------------------------

                unit_price = 0.40

                matched_quantity = min(
                    quantity,
                    match["Quantity Needed"]
                )

                normal_cost = (
                    matched_quantity * unit_price
                )

                exchange_cost = (
                    normal_cost * 0.80
                )

                buyer_savings = (
                    normal_cost - exchange_cost
                )

                platform_fee = (
                    exchange_cost * 0.05
                )

                st.subheader("💰 Financial Impact")

                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    st.metric(
                        "Normal Purchase",
                        f"${normal_cost:,.2f}"
                    )

                with col_b:
                    st.metric(
                        "Buyer Saves",
                        f"${buyer_savings:,.2f}"
                    )

                with col_c:
                    st.metric(
                        "Platform Revenue",
                        f"${platform_fee:,.2f}"
                    )

                st.info(
                    f"♻️ {matched_quantity:,} units could be "
                    f"redirected instead of requiring a new purchase."
                )

        else:

            st.warning(
                "No suitable facility was found "
                "for this supply."
            )


# -----------------------------
# I NEED SUPPLIES
# -----------------------------

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
# Example inventory
# -----------------------------

st.divider()

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
    ],
    "Unit Price": [
        1.00,
        0.40,
        1.00,
        0.40
    ]
})

st.dataframe(
    inventory,
    use_container_width=True
)
