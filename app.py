import streamlit as st
import pandas as pd

# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Expiry Exchange",
    page_icon="♻️",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("♻️ EXPIRY EXCHANGE")

st.subheader("Don't buy new. Exchange what already exists.")

st.write(
    "A smart platform that connects healthcare facilities "
    "with surplus supplies before they expire."
)

st.divider()

# ============================================================
# MAIN COLUMNS
# ============================================================

col1, col2 = st.columns(2)

# ============================================================
# I HAVE SURPLUS
# ============================================================

with col1:

    st.subheader("🏥 I HAVE SURPLUS")

    st.write(
        "Tell us about healthcare supplies "
        "you have available."
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

        # ----------------------------------------------------
        # CALCULATE EXPIRY RISK
        # ----------------------------------------------------

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

        st.write(
            "### Expiry Risk:",
            risk
        )

        # ----------------------------------------------------
        # DEMAND DATA
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # FIND MATCHES
        # ----------------------------------------------------

        matches = demand[
            (demand["Product"] == product) &
            (demand["Quantity Needed"] <= quantity)
        ]

        # ----------------------------------------------------
        # DISPLAY MATCHES
        # ----------------------------------------------------

        if len(matches) > 0:

            st.subheader("🎯 Potential Match Found!")

            for _, match in matches.iterrows():

                st.write(
                    f"🏥 **{match['Facility']}**"
                )

                st.write(
                    f"Needs: **{match['Quantity Needed']:,} "
                    f"{product}**"
                )

                st.write(
                    f"Your available quantity: "
                    f"**{quantity:,}**"
                )

                st.success(
                    "✅ Quantity requirement satisfied!"
                )

                # ------------------------------------------------
                # FINANCIAL IMPACT
                # ------------------------------------------------

                unit_price = 0.40

                matched_quantity = min(
                    quantity,
                    match["Quantity Needed"]
                )

                # Normal purchase cost
                normal_cost = (
                    matched_quantity * unit_price
                )

                # 20% discount through Expiry Exchange
                exchange_cost = (
                    normal_cost * 0.80
                )

                # Buyer savings
                buyer_savings = (
                    normal_cost - exchange_cost
                )

                # 5% platform transaction fee
                platform_fee = (
                    exchange_cost * 0.05
                )

                st.subheader("💰 Financial Impact")

                financial_col1, financial_col2, financial_col3 = (
                    st.columns(3)
                )

                with financial_col1:

                    st.metric(
                        "Normal Purchase",
                        f"${normal_cost:,.2f}"
                    )

                with financial_col2:

                    st.metric(
                        "Buyer Saves",
                        f"${buyer_savings:,.2f}"
                    )

                with financial_col3:

                    st.metric(
                        "Platform Revenue",
                        f"${platform_fee:,.2f}"
                    )

                st.info(
                    f"♻️ **{matched_quantity:,} units** could be "
                    f"redirected instead of requiring a new purchase."
                )

                # ------------------------------------------------
                # PROPOSE EXCHANGE
                # ------------------------------------------------

                if st.button(
                    "🤝 Propose Exchange",
                    key=f"proposal_{match['Facility']}"
                ):

                    st.success(
                        f"🎉 Exchange proposal created for "
                        f"{match['Facility']}!"
                    )

                    st.write(
                        "The receiving facility can review "
                        "the available quantity and proposed exchange."
                    )

        else:

            st.warning(
                "No suitable facility was found "
                "for this supply."
            )


# ============================================================
# I NEED SUPPLIES
# ============================================================

with col2:

    st.subheader("🔎 I NEED SUPPLIES")

    st.write(
        "Search for available surplus "
        "instead of buying new."
    )

    st.info(
        "The demand-side matching system "
        "will be available here."
    )


# ============================================================
# EXAMPLE INVENTORY
# ============================================================

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


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.subheader("💡 How Expiry Exchange Works")

step1, step2, step3 = st.columns(3)

with step1:

    st.write("### 1️⃣ List")

    st.write(
        "Healthcare facilities list surplus "
        "supplies that may expire."
    )

with step2:

    st.write("### 2️⃣ Match")

    st.write(
        "Expiry Exchange identifies facilities "
        "that need those supplies."
    )

with step3:

    st.write("### 3️⃣ Exchange")

    st.write(
        "The buyer saves money, surplus is reused, "
        "and Expiry Exchange earns a small transaction fee."
    )

st.dataframe(
    inventory,
    use_container_width=True
)
