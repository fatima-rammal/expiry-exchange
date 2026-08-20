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
# PRODUCT PRICES
# ============================================================

product_prices = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50
}

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
# DEMAND DATA
# ============================================================

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

# ============================================================
# INVENTORY DATA
# ============================================================

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

inventory["Expiry"] = pd.to_datetime(inventory["Expiry"])

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
        "List unused healthcare supplies "
        "that may expire before they are used."
    )

    product = st.selectbox(
        "What product do you have?",
        ["Gauze", "Gloves", "IV Sets"],
        key="surplus_product"
    )

    quantity = st.number_input(
        "Quantity available",
        min_value=1,
        value=100,
        key="surplus_quantity"
    )

    expiry_date = st.date_input(
        "Expiry date",
        key="surplus_expiry"
    )

    if st.button("🔎 Find a Match"):

        today = pd.Timestamp.today().normalize()
        expiry = pd.Timestamp(expiry_date)

        days_left = (expiry - today).days

        # Expiry risk

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

        # Find potential buyers

        matches = demand[
            (demand["Product"] == product) &
            (demand["Quantity Needed"] <= quantity)
        ]

        if len(matches) > 0:

            st.subheader("🎯 Potential Match Found!")

            for _, match in matches.iterrows():

                st.write(
                    f"🏥 **{match['Facility']}**"
                )

                st.write(
                    f"Needs **{match['Quantity Needed']:,} "
                    f"{product}**"
                )

                st.write(
                    f"You have **{quantity:,} {product}**"
                )

                st.success(
                    "✅ Quantity requirement satisfied!"
                )

                # Financial calculation

                unit_price = product_prices[product]

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
                    f"♻️ **{matched_quantity:,} units** "
                    f"could be redirected instead of "
                    f"requiring a new purchase."
                )

                if st.button(
                    "🤝 Propose Exchange",
                    key=f"proposal_{match['Facility']}"
                ):

                    st.success(
                        f"🎉 Exchange proposal created "
                        f"for {match['Facility']}!"
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

    needed_product = st.selectbox(
        "What do you need?",
        ["Gauze", "Gloves", "IV Sets"],
        key="needed_product"
    )

    needed_quantity = st.number_input(
        "Quantity needed",
        min_value=1,
        value=500,
        key="needed_quantity"
    )

    if st.button("🔎 Search Surplus"):

        available = inventory[
            (inventory["Product"] == needed_product) &
            (inventory["Quantity"] >= needed_quantity)
        ]

        if len(available) > 0:

            st.subheader("🎯 Surplus Available!")

            for _, supply in available.iterrows():

                days_left = (
                    supply["Expiry"] -
                    pd.Timestamp.today().normalize()
                ).days

                unit_price = product_prices[needed_product]

                normal_cost = (
                    needed_quantity * unit_price
                )

                exchange_cost = (
                    normal_cost * 0.80
                )

                savings = (
                    normal_cost - exchange_cost
                )

                st.write(
                    f"🏥 **{supply['Facility']}**"
                )

                st.write(
                    f"📦 Available: "
                    f"**{supply['Quantity']:,} {needed_product}**"
                )

                st.write(
                    f"⏳ Days until expiry: "
                    f"**{days_left}**"
                )

                st.metric(
                    "Estimated Saving",
                    f"${savings:,.2f}"
                )

                if st.button(
                    "🤝 Request Exchange",
                    key=f"request_{supply['Facility']}_{needed_product}"
                ):

                    st.success(
                        f"🎉 Exchange request sent to "
                        f"{supply['Facility']}!"
                    )

                st.divider()

        else:

            st.warning(
                "No suitable surplus was found."
            )

# ============================================================
# EXAMPLE INVENTORY
# ============================================================

st.divider()

st.subheader("📦 Example Inventory")

display_inventory = inventory.copy()

display_inventory["Expiry"] = (
    display_inventory["Expiry"].dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_inventory,
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
        "Facilities list surplus supplies "
        "before they expire."
    )

with step2:

    st.write("### 2️⃣ Match")

    st.write(
        "The platform finds facilities "
        "that need those supplies."
    )

with step3:

    st.write("### 3️⃣ Exchange")

    st.write(
        "The buyer saves money, surplus is reused, "
        "and Expiry Exchange earns a small transaction fee."
    )
