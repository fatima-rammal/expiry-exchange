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
# DESIGN
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #FDE8E7;
    }

    /* Main headings */
    h1 {
        color: #B42318 !important;
    }

    h2, h3 {
        color: #B42318 !important;
    }

    /* Subtitle */
    .subtitle {
        color: #6B3A37;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    /* Small information section */
    .section-box {
        background-color: #FFF8F7;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #D92D20;
        margin-bottom: 1rem;
    }

    /* Match result */
    .match-box {
        background-color: #FFFFFF;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #F0C8C5;
        margin: 0.8rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #795A57;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# PRODUCT PRICES
# ============================================================

product_prices = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50
}

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
# HEADER
# ============================================================

st.title("♻️ EXPIRY EXCHANGE")

st.markdown(
    '<div class="subtitle">'
    "Don't buy new. Exchange what already exists."
    "</div>",
    unsafe_allow_html=True
)

st.write(
    "A simple platform connecting healthcare facilities "
    "with surplus supplies before they expire."
)

st.divider()

# ============================================================
# QUICK EXPLANATION
# ============================================================

st.markdown(
    """
    <div class="section-box">
        <b>How it works:</b>
        🏥 List surplus &nbsp; → &nbsp;
        🔎 Find a match &nbsp; → &nbsp;
        ♻️ Exchange instead of buying new
    </div>
    """,
    unsafe_allow_html=True
)

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
        "List unused healthcare supplies that may expire."
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

    if st.button(
        "🔎 Find a Match",
        use_container_width=True,
        key="find_match"
    ):

        # ----------------------------------------------------
        # EXPIRY CALCULATION
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

        st.success("Inventory analyzed.")

        metric1, metric2 = st.columns(2)

        with metric1:
            st.metric(
                "Days Until Expiry",
                days_left
            )

        with metric2:
            st.metric(
                "Expiry Risk",
                risk
            )

        # ----------------------------------------------------
        # FIND MATCHES
        # ----------------------------------------------------

        matches = demand[
            (demand["Product"] == product) &
            (demand["Quantity Needed"] <= quantity)
        ]

        if len(matches) > 0:

            st.subheader("🎯 Potential Match Found")

            for _, match in matches.iterrows():

                st.markdown(
                    f"""
                    <div class="match-box">
                        <b>🏥 {match['Facility']}</b><br><br>
                        Needs: <b>{match['Quantity Needed']:,}
                        {product}</b><br>
                        Available: <b>{quantity:,}
                        {product}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.success(
                    "✓ Quantity requirement satisfied."
                )

                # ------------------------------------------------
                # FINANCIAL CALCULATION
                # ------------------------------------------------

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

                st.write("**Financial impact**")

                money1, money2, money3 = st.columns(3)

                with money1:

                    st.metric(
                        "Normal Purchase",
                        f"${normal_cost:,.2f}"
                    )

                with money2:

                    st.metric(
                        "Buyer Saves",
                        f"${buyer_savings:,.2f}"
                    )

                with money3:

                    st.metric(
                        "Platform Revenue",
                        f"${platform_fee:,.2f}"
                    )

                st.info(
                    f"♻️ {matched_quantity:,} units could be "
                    f"redirected instead of requiring a new purchase."
                )

                if st.button(
                    "🤝 Propose Exchange",
                    key=f"proposal_{match['Facility']}",
                    use_container_width=True
                ):

                    st.success(
                        f"Exchange proposal created for "
                        f"{match['Facility']}."
                    )

        else:

            st.warning(
                "No suitable facility was found for this supply."
            )

# ============================================================
# I NEED SUPPLIES
# ============================================================

with col2:

    st.subheader("🔎 I NEED SUPPLIES")

    st.write(
        "Search for available surplus instead of buying new."
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

    if st.button(
        "🔎 Search Surplus",
        use_container_width=True,
        key="search_surplus"
    ):

        available = inventory[
            (inventory["Product"] == needed_product) &
            (inventory["Quantity"] >= needed_quantity)
        ]

        if len(available) > 0:

            st.subheader("🎯 Surplus Available")

            for _, supply in available.iterrows():

                days_left = (
                    supply["Expiry"]
                    - pd.Timestamp.today().normalize()
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

                st.markdown(
                    f"""
                    <div class="match-box">
                        <b>🏥 {supply['Facility']}</b><br><br>
                        Available:
                        <b>{supply['Quantity']:,}
                        {needed_product}</b><br>
                        Days until expiry:
                        <b>{days_left}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.metric(
                    "Estimated Saving",
                    f"${savings:,.2f}"
                )

                if st.button(
                    "🤝 Request Exchange",
                    key=(
                        f"request_"
                        f"{supply['Facility']}_"
                        f"{needed_product}"
                    ),
                    use_container_width=True
                ):

                    st.success(
                        f"Exchange request sent to "
                        f"{supply['Facility']}."
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
    display_inventory["Expiry"]
    .dt.strftime("%Y-%m-%d")
)

st.dataframe(
    display_inventory,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.subheader("💡 How It Works")

step1, step2, step3 = st.columns(3)

with step1:

    st.write("**1️⃣ List**")

    st.write(
        "Facilities list surplus supplies "
        "before they expire."
    )

with step2:

    st.write("**2️⃣ Match**")

    st.write(
        "The platform finds facilities "
        "that need those supplies."
    )

with step3:

    st.write("**3️⃣ Exchange**")

    st.write(
        "Buyers save money, supplies are reused, "
        "and the platform earns a transaction fee."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ♻️ Consume less. Waste less. Exchange smarter.
    </div>
    """,
    unsafe_allow_html=True
)
