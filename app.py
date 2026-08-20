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
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

    /* ---------- Main background ---------- */

    .stApp {
        background-color: #F3FAF9;
    }

    /* ---------- Main container ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ---------- Main title ---------- */

    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #075E54;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.25rem;
        color: #46736E;
        margin-top: 0.3rem;
        margin-bottom: 1.5rem;
    }

    /* ---------- Healthcare badge ---------- */

    .health-badge {
        display: inline-block;
        background-color: #DDF3EF;
        color: #075E54;
        padding: 0.45rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* ---------- Cards ---------- */

    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #D8EAE7;
        box-shadow: 0 4px 15px rgba(7, 94, 84, 0.06);
        min-height: 250px;
    }

    .card-title {
        color: #075E54;
        font-size: 1.35rem;
        font-weight: 700;
    }

    .card-text {
        color: #5D7370;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* ---------- Section titles ---------- */

    .section-title {
        color: #075E54;
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 1rem;
    }

    /* ---------- Match card ---------- */

    .match-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 18px;
        border-left: 6px solid #19A974;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(7, 94, 84, 0.08);
    }

    .match-title {
        color: #075E54;
        font-size: 1.4rem;
        font-weight: 700;
    }

    /* ---------- Impact banner ---------- */

    .impact-banner {
        background-color: #E3F5ED;
        padding: 1.2rem;
        border-radius: 15px;
        color: #075E54;
        font-weight: 600;
        margin-top: 1rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #6C8581;
        font-size: 0.85rem;
        padding-top: 2rem;
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
# DATA
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

st.markdown(
    '<div class="health-badge">🩺 HEALTHCARE × ♻️ CIRCULAR ECONOMY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">♻️ EXPIRY EXCHANGE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Don\'t buy new. Exchange what already exists.'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "A digital marketplace that connects healthcare facilities "
    "with surplus supplies before they expire."
)

# ============================================================
# HOW IT WORKS MINI VISUAL
# ============================================================

st.markdown(
    """
    <div style="
        background-color:#EAF7F5;
        padding:1rem;
        border-radius:15px;
        text-align:center;
        color:#075E54;
        font-weight:600;
        margin:1.5rem 0;
    ">
    🏥 SURPLUS &nbsp; → &nbsp; 🔎 SMART MATCH &nbsp; → &nbsp; ♻️ REUSE
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# MAIN COLUMNS
# ============================================================

col1, col2 = st.columns(2, gap="large")

# ============================================================
# I HAVE SURPLUS
# ============================================================

with col1:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🏥 I HAVE SURPLUS</div>
            <div class="card-text">
                List unused healthcare supplies that may expire
                before your facility can use them.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

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

        matches = demand[
            (demand["Product"] == product) &
            (demand["Quantity Needed"] <= quantity)
        ]

        if len(matches) > 0:

            st.markdown(
                '<div class="section-title">'
                '🎯 Potential Matches'
                '</div>',
                unsafe_allow_html=True
            )

            for _, match in matches.iterrows():

                st.markdown(
                    f"""
                    <div class="match-card">
                        <div class="match-title">
                            🏥 {match['Facility']}
                        </div>
                        <p>
                            Needs <b>{match['Quantity Needed']:,}
                            {product}</b>
                        </p>
                        <p>
                            Available from your facility:
                            <b>{quantity:,}</b>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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

                st.write("")

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

                st.markdown(
                    f"""
                    <div class="impact-banner">
                        ♻️ {matched_quantity:,} units redirected
                        instead of requiring a new purchase.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                if st.button(
                    "🤝 Propose Exchange",
                    key=f"proposal_{match['Facility']}",
                    use_container_width=True
                ):

                    st.success(
                        f"🎉 Exchange proposal created for "
                        f"{match['Facility']}!"
                    )

        else:

            st.warning(
                "No suitable facility was found for this supply."
            )

# ============================================================
# I NEED SUPPLIES
# ============================================================

with col2:

    st.markdown(
        """
        <div class="card">
            <div class="card-title">🔎 I NEED SUPPLIES</div>
            <div class="card-text">
                Find available surplus and avoid purchasing
                new supplies unnecessarily.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

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

            st.markdown(
                '<div class="section-title">'
                '🎯 Surplus Available'
                '</div>',
                unsafe_allow_html=True
            )

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

                st.markdown(
                    f"""
                    <div class="match-card">
                        <div class="match-title">
                            🏥 {supply['Facility']}
                        </div>
                        <p>
                            📦 Available:
                            <b>{supply['Quantity']:,}
                            {needed_product}</b>
                        </p>
                        <p>
                            ⏳ Days until expiry:
                            <b>{days_left}</b>
                        </p>
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
                    key=f"request_{supply['Facility']}_{needed_product}",
                    use_container_width=True
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
# INVENTORY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📦 Example Inventory</div>',
    unsafe_allow_html=True
)

display_inventory = inventory.copy()

display_inventory["Expiry"] = (
    display_inventory["Expiry"].dt.strftime("%Y-%m-%d")
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

st.markdown(
    '<div class="section-title">💡 How It Works</div>',
    unsafe_allow_html=True
)

step1, step2, step3 = st.columns(3)

with step1:

    st.markdown(
        """
        **1️⃣ LIST**

        Facilities list surplus supplies
        before they expire.
        """
    )

with step2:

    st.markdown(
        """
        **2️⃣ MATCH**

        Expiry Exchange finds facilities
        that need those supplies.
        """
    )

with step3:

    st.markdown(
        """
        **3️⃣ EXCHANGE**

        Buyers save money, supplies are reused,
        and the platform earns a transaction fee.
        """
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ♻️ Consume less. Waste less. Exchange smarter.<br>
        Expiry Exchange — Healthcare Circular Economy
    </div>
    """,
    unsafe_allow_html=True
)
