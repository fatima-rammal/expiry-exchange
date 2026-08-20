import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Expiry Exchange",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0A0A0A;
    color: #F5F5F5;
}

/* Main content width */
.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Inter', sans-serif !important;
    color: #F5F5F5 !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.35rem !important;
    font-weight: 600 !important;
}

h3 {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
}

/* Body text */
p {
    color: #B8B8B8;
}

/* Top brand */
.brand {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #D94A3A;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* Hero */
.hero-title {
    font-size: 2.6rem;
    line-height: 1.1;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.6rem;
}

.hero-subtitle {
    font-size: 1rem;
    color: #999999;
    max-width: 650px;
    line-height: 1.6;
    margin-bottom: 2rem;
}

/* Section labels */
.section-label {
    color: #888888;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}

/* Cards */
.panel {
    background: #111111;
    border: 1px solid #242424;
    border-radius: 8px;
    padding: 1.4rem;
    margin-bottom: 1rem;
}

/* Match card */
.result-card {
    background: #111111;
    border: 1px solid #292929;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 0.7rem 0;
}

.result-title {
    color: #FFFFFF;
    font-weight: 600;
    font-size: 1rem;
}

.result-detail {
    color: #999999;
    font-size: 0.85rem;
    margin-top: 0.35rem;
}

/* Small status */
.status {
    display: inline-block;
    padding: 0.25rem 0.55rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    background: #172217;
    color: #7FC47F;
}

/* Financial information */
.savings {
    color: #7FC47F;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background: #D94A3A;
    color: white;
    border: 1px solid #D94A3A;
    border-radius: 6px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    background: #B83B2E;
    border-color: #B83B2E;
    color: white;
}

/* Inputs */
.stSelectbox > div > div,
.stNumberInput > div > div,
.stDateInput > div > div {
    background: #111111 !important;
}

/* Input text */
input {
    color: #FFFFFF !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.25rem;
}

[data-testid="stMetricLabel"] {
    color: #888888 !important;
}

/* Divider */
hr {
    border-color: #222222 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 6px;
}

/* Footer */
.footer {
    border-top: 1px solid #222222;
    margin-top: 3rem;
    padding-top: 1.2rem;
    color: #666666;
    font-size: 0.75rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

product_prices = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50
}

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
    '<div class="brand">EXPIRY EXCHANGE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Healthcare surplus,<br>before it expires.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'A marketplace connecting healthcare facilities with unused '
    'supplies — helping organizations reduce waste and purchase costs.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TWO MAIN OPTIONS
# ============================================================

left, right = st.columns(2, gap="large")


# ============================================================
# SURPLUS SIDE
# ============================================================

with left:

    st.markdown(
        '<div class="section-label">For facilities with surplus</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.subheader("List surplus inventory")

    st.write(
        "Tell us what you have and we'll check whether "
        "another facility needs it."
    )

    surplus_product = st.selectbox(
        "Supply",
        ["Gauze", "Gloves", "IV Sets"],
        key="surplus_product"
    )

    surplus_quantity = st.number_input(
        "Quantity available",
        min_value=1,
        value=100,
        step=50,
        key="surplus_quantity"
    )

    surplus_expiry = st.date_input(
        "Expiry date",
        key="surplus_expiry"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "Find facilities that need this",
        use_container_width=True,
        key="find_match"
    ):

        today = pd.Timestamp.today().normalize()
        expiry = pd.Timestamp(surplus_expiry)
        days_left = (expiry - today).days

        matches = demand[
            (demand["Product"] == surplus_product) &
            (demand["Quantity Needed"] <= surplus_quantity)
        ]

        if len(matches) > 0:

            st.markdown(
                '<div class="section-label">Available matches</div>',
                unsafe_allow_html=True
            )

            for _, match in matches.iterrows():

                matched_quantity = min(
                    surplus_quantity,
                    match["Quantity Needed"]
                )

                normal_cost = (
                    matched_quantity *
                    product_prices[surplus_product]
                )

                exchange_cost = normal_cost * 0.80

                savings = normal_cost - exchange_cost

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-title">
                            {match['Facility']}
                        </div>

                        <div class="result-detail">
                            Looking for {match['Quantity Needed']:,}
                            {surplus_product}
                        </div>

                        <div class="result-detail">
                            Your available quantity:
                            {surplus_quantity:,}
                        </div>

                        <br>

                        <span class="status">
                            MATCH
                        </span>

                        &nbsp;&nbsp;

                        <span class="savings">
                            Estimated buyer saving: ${savings:,.2f}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Propose exchange",
                    key=f"propose_{match['Facility']}",
                    use_container_width=True
                ):
                    st.success(
                        f"Exchange proposal sent to {match['Facility']}."
                    )

        else:

            st.warning(
                "No matching facility was found for this supply."
            )


# ============================================================
# DEMAND SIDE
# ============================================================

with right:

    st.markdown(
        '<div class="section-label">For facilities that need supplies</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.subheader("Search available surplus")

    st.write(
        "Check whether another facility has the supplies "
        "you need before purchasing new stock."
    )

    needed_product = st.selectbox(
        "Supply needed",
        ["Gauze", "Gloves", "IV Sets"],
        key="needed_product"
    )

    needed_quantity = st.number_input(
        "Quantity required",
        min_value=1,
        value=500,
        step=50,
        key="needed_quantity"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "Search available surplus",
        use_container_width=True,
        key="search_surplus"
    ):

        available = inventory[
            (inventory["Product"] == needed_product) &
            (inventory["Quantity"] >= needed_quantity)
        ]

        if len(available) > 0:

            st.markdown(
                '<div class="section-label">Available inventory</div>',
                unsafe_allow_html=True
            )

            for _, supply in available.iterrows():

                days_left = (
                    supply["Expiry"]
                    - pd.Timestamp.today().normalize()
                ).days

                normal_cost = (
                    needed_quantity *
                    product_prices[needed_product]
                )

                exchange_cost = normal_cost * 0.80

                savings = normal_cost - exchange_cost

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-title">
                            {supply['Facility']}
                        </div>

                        <div class="result-detail">
                            {supply['Quantity']:,}
                            {needed_product} available
                        </div>

                        <div class="result-detail">
                            Expires in approximately
                            {days_left} days
                        </div>

                        <br>

                        <span class="status">
                            AVAILABLE
                        </span>

                        &nbsp;&nbsp;

                        <span class="savings">
                            Estimated saving: ${savings:,.2f}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Request exchange",
                    key=(
                        f"request_"
                        f"{supply['Facility']}_"
                        f"{needed_product}"
                    ),
                    use_container_width=True
                ):
                    st.success(
                        f"Request sent to {supply['Facility']}."
                    )

        else:

            st.warning(
                "No suitable surplus is currently available."
            )


# ============================================================
# BUSINESS MODEL
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">Business model</div>',
    unsafe_allow_html=True
)

st.markdown(
    "### We make money when facilities save money."
)

business_left, business_right = st.columns(2)

with business_left:

    st.write(
        "Expiry Exchange charges a small transaction fee "
        "when a surplus-to-demand exchange is completed."
    )

with business_right:

    st.markdown(
        """
        **Example**

        A facility avoids a $800 purchase.

        The exchange costs $640.

        **Buyer saves $160.**

        Expiry Exchange receives a **5% transaction fee**
        on the exchange value.
        """
    )


# ============================================================
# DEMO INVENTORY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">Demo inventory</div>',
    unsafe_allow_html=True
)

display_inventory = inventory.copy()

display_inventory["Expiry"] = (
    display_inventory["Expiry"]
    .dt.strftime("%d %b %Y")
)

st.dataframe(
    display_inventory,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'EXPIRY EXCHANGE · Prototype'
    '</div>',
    unsafe_allow_html=True
)
