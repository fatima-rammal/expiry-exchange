import streamlit as st
import pandas as pd


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Expiry Exchange",
    page_icon="♻",
    layout="wide"
)


# ============================================================
# DESIGN
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
    padding-bottom: 40px;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

p {
    color: #B8B8B8;
}

.brand {
    color: #D94A3A;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
}

.subtitle {
    color: #999999;
    font-size: 16px;
    max-width: 650px;
    line-height: 1.6;
}

.section-label {
    color: #777777;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.stButton > button {
    background-color: #D94A3A;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #B83B2E;
    color: white;
}

.stSelectbox > div > div,
.stNumberInput > div > div,
.stDateInput > div > div {
    background-color: #111111 !important;
}

input {
    color: white !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

[data-testid="stMetricLabel"] {
    color: #888888 !important;
}

hr {
    border-color: #252525 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

prices = {
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

st.title("Healthcare surplus, before it expires.")

st.markdown(
    '<div class="subtitle">'
    "Connect healthcare facilities with unused supplies "
    "before they expire, reducing waste and unnecessary purchases."
    "</div>",
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# TWO SIDES
# ============================================================

left, right = st.columns(2)


# ============================================================
# I HAVE SURPLUS
# ============================================================

with left:

    st.markdown(
        '<div class="section-label">SURPLUS</div>',
        unsafe_allow_html=True
    )

    st.header("I have surplus")

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

    find_match = st.button(
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

    st.header("I need supplies")

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

    search_surplus = st.button(
        "Search surplus",
        use_container_width=True,
        key="search_surplus"
    )


# ============================================================
# FIND A FACILITY
# ============================================================

if find_match:

    st.divider()

    st.markdown(
        '<div class="section-label">MATCH RESULTS</div>',
        unsafe_allow_html=True
    )

    matches = demand[
        (demand["Product"] == surplus_product)
        &
        (demand["Quantity Needed"] <= surplus_quantity)
    ]

    if len(matches) == 0:

        st.warning(
            "No facility currently needs this quantity."
        )

    else:

        st.subheader("Facilities that may need this supply")

        today = pd.Timestamp.today().normalize()
        expiry = pd.Timestamp(surplus_expiry)
        days_left = (expiry - today).days

        for _, match in matches.iterrows():

            quantity = min(
                surplus_quantity,
                match["Quantity Needed"]
            )

            normal_cost = quantity * prices[surplus_product]

            exchange_cost = normal_cost * 0.80

            savings = normal_cost - exchange_cost

            st.write("")
            st.write(f"**{match['Facility']}**")

            st.caption(
                f"Needs {match['Quantity Needed']:,} "
                f"{surplus_product} | "
                f"You have {surplus_quantity:,}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Available",
                    f"{surplus_quantity:,}"
                )

            with col2:
                st.metric(
                    "Days to expiry",
                    days_left
                )

            with col3:
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
                    f"Proposal sent to {match['Facility']}."
                )

            st.divider()


# ============================================================
# SEARCH SURPLUS
# ============================================================

if search_surplus:

    st.divider()

    st.markdown(
        '<div class="section-label">AVAILABLE SURPLUS</div>',
        unsafe_allow_html=True
    )

    available = inventory[
        (inventory["Product"] == needed_product)
        &
        (inventory["Quantity"] >= needed_quantity)
    ]

    if len(available) == 0:

        st.warning(
            "No suitable surplus is currently available."
        )

    else:

        st.subheader("Available inventory")

        for _, supply in available.iterrows():

            today = pd.Timestamp.today().normalize()

            days_left = (
                supply["Expiry"] - today
            ).days

            normal_cost = (
                needed_quantity
                * prices[needed_product]
            )

            exchange_cost = normal_cost * 0.80

            savings = normal_cost - exchange_cost

            st.write("")
            st.write(f"**{supply['Facility']}**")

            st.caption(
                f"{supply['Quantity']:,} "
                f"{needed_product} available"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Available",
                    f"{supply['Quantity']:,}"
                )

            with col2:
                st.metric(
                    "Days to expiry",
                    days_left
                )

            with col3:
                st.metric(
                    "Estimated saving",
                    f"${savings:,.2f}"
                )

            if st.button(
                "Request exchange",
                key=f"request_{supply['Facility']}_{needed_product}",
                use_container_width=True
            ):

                st.success(
                    f"Request sent to {supply['Facility']}."
                )

            st.divider()


# ============================================================
# BUSINESS MODEL
# ============================================================

st.markdown(
    '<div class="section-label">BUSINESS MODEL</div>',
    unsafe_allow_html=True
)

st.header("We make money when facilities save money.")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "Expiry Exchange charges a small transaction fee "
        "when a successful exchange is completed."
    )

with col2:

    st.metric(
        "Illustrative transaction fee",
        "5%"
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
    display_inventory["Expiry"].dt.strftime("%d %b %Y")
)

st.dataframe(
    display_inventory,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("EXPIRY EXCHANGE · Prototype")
