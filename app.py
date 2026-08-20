import streamlit as st
import pandas as pd


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Expiry Exchange",
    page_icon="♻",
    layout="wide"
)


# ============================================================
# CUSTOM STYLE
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0A0A0A;
    color: #F5F5F5;
}

.block-container {
    max-width: 1100px;
    padding-top: 40px;
    padding-bottom: 50px;
}

/* Headings */

h1, h2, h3 {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

h1 {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

/* Text */

p {
    color: #B8B8B8;
}

/* Brand */

.brand {
    color: #D94A3A;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.12em;
}

/* Hero */

.hero-subtitle {
    color: #999999;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 650px;
}

/* Panels */

.panel {
    background-color: #111111;
    border: 1px solid #252525;
    border-radius: 8px;
    padding: 24px;
}

/* Section label */

.section-label {
    color: #777777;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Buttons */

.stButton > button {
    background-color: #D94A3A;
    color: white;
    border: 1px solid #D94A3A;
    border-radius: 6px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #B83B2E;
    border-color: #B83B2E;
    color: white;
}

/* Inputs */

.stSelectbox > div > div,
.stNumberInput > div > div,
.stDateInput > div > div {
    background-color: #111111 !important;
}

input {
    color: #FFFFFF !important;
}

/* Metrics */

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

[data-testid="stMetricLabel"] {
    color: #888888 !important;
}

/* Dividers */

hr {
    border-color: #252525 !important;
}

/* Footer */

.footer {
    color: #666666;
    font-size: 0.75rem;
    text-align: center;
    padding-top: 30px;
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


# Facilities that need supplies

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


# Facilities with surplus

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

st.title("Healthcare surplus, before it expires.")

st.markdown(
    '<div class="hero-subtitle">'
    'Connect healthcare facilities with unused supplies '
    'before they expire — reducing waste and unnecessary purchases.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# MAIN INTERFACE
# ============================================================

left, right = st.columns(2, gap="large")


# ============================================================
# I HAVE SURPLUS
# ============================================================

with left:

    st.markdown(
        '<div class="section-label">SURPLUS</div>',
        unsafe_allow_html=True
    )

    st.subheader("I have surplus")

    st.write(
        "List supplies that your facility no longer needs."
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

    st.write("")

    find_button = st.button(
        "Find a facility",
        use_container_width=True,
        key="find_match"
    )


# ============================================================
# I NEED SUPPLIES
# ============================================================

with right:

    st.markdown(
        '<div class="section-label">DEMAND</div>',
        unsafe_allow_html=True
    )

    st.subheader("I need supplies")

    st.write(
        "Search existing surplus before buying new stock."
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

    st.write("")

    search_button = st.button(
        "Search surplus",
        use_container_width=True,
        key="search_surplus"
    )


# ============================================================
# SURPLUS MATCHING
# ============================================================

if find_button:

    st.divider()

    st.markdown(
        '<div class="section-label">MATCH RESULTS</div>',
        unsafe_allow_html=True
    )

    today = pd.Timestamp.today().normalize()
    expiry = pd.Timestamp(surplus_expiry)

    days_left = (expiry - today).days

    matches = demand[
        (demand["Product"] == surplus_product) &
        (demand["Quantity Needed"] <= surplus_quantity)
    ]

    if len(matches) > 0:

        st.subheader("Facilities that may need this supply")

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

            st.write("")

            st.write(
                f"### {match['Facility']}"
            )

            st.caption(
                f"Needs {match['Quantity Needed']:,} "
                f"{surplus_product} · "
                f"You have {surplus_quantity:,}"
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:

                st.metric(
                    "Available",
                    f"{surplus_quantity:,}"
                )

            with result_col2:

                st.metric(
                    "Days to expiry",
                    days_left
                )

            with result_col3:

                st.metric(
                    "Estimated saving",
                    f"${savings:,.2f}"
                )

            if st.button(
                "Propose exchange",
                key=f"propose_{match['Facility']}",
                use_container_width=True
            ):

                st.success(
                    f"Exchange proposal sent to "
                    f"{match['Facility']}."
                )

            st.divider()

    else:

        st.warning(
            "No facility currently matches this supply."
        )


# ============================================================
# SURPLUS SEARCH
# ============================================================

if search_button:

    st.divider()

    st.markdown(
        '<div class="section-label">AVAILABLE SURPLUS</div>',
        unsafe_allow_html=True
    )

    available = inventory[
        (inventory["Product"] == needed_product) &
        (inventory["Quantity"] >= needed_quantity)
    ]

    if len(available) > 0:

        st.subheader("Available inventory")

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

            st.write("")

            st.write(
                f"### {supply['Facility']}"
            )

            st.caption(
                f"{supply['Quantity']:,} "
                f"{needed_product} available"
            )

            result_col1, result_col2, result_col3 = st.columns(3)

            with result_col1:

                st.metric(
                    "Available",
                    f"{supply['Quantity']:,}"
                )

            with result_col2:

                st.metric(
                    "Days to expiry",
                    days_left
                )

            with result_col3:

                st.metric(
                    "Estimated saving",
                    f"${savings:,.2f}"
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

            st.divider()

    else:

        st.warning(
            "No suitable surplus is currently available."
        )


# ============================================================
# BUSINESS MODEL
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">BUSINESS MODEL</div>',
    unsafe_allow_html=True
)

st.subheader("We make money when facilities save money.")

business_col1, business_col2 = st.columns(2)

with business_col1:

    st.write(
        "Expiry Exchange takes a small transaction fee "
        "when a successful exchange is completed."
    )

with business_col2:

    st.metric(
        "Example transaction fee",
        "5%"
    )

    st.caption(
        "Illustrative rate for the prototype."
    )


# ============================================================
# DEMO INVENTORY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">DEMO INVENTORY</div>',
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
    '<div class="footer">'
    'EXPIRY EXCHANGE · Prototype'
    '</div>',
    unsafe_allow_html=True
)
