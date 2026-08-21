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
    padding-bottom: 50px;
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
    max-width: 700px;
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
# DEMO PRICES
# ============================================================

prices = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50
}


# ============================================================
# DEMO DEMAND
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
# DEMO SURPLUS INVENTORY
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
        "2026-09-15",
        "2026-09-05",
        "2026-10-20",
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
# IMPACT DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-label">PLATFORM IMPACT</div>',
    unsafe_allow_html=True
)

dashboard1, dashboard2, dashboard3 = st.columns(3)

with dashboard1:
    st.metric(
        "Supplies available",
        "9,200"
    )

with dashboard2:
    st.metric(
        "Potential savings",
        "$3,280"
    )

with dashboard3:
    st.metric(
        "Waste potentially diverted",
        "9,200 units"
    )


st.divider()


# ============================================================
# TWO MAIN FUNCTIONS
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
        "List supplies your facility no longer needs."
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
# FEATURE 1 + 2 + 3
# PARTIAL MATCHING + EXPIRY RISK + SAVINGS
# ============================================================

if find_match:

    st.divider()

    st.markdown(
        '<div class="section-label">MATCH RESULTS</div>',
        unsafe_allow_html=True
    )

    matches = demand[
        demand["Product"] == surplus_product
    ].copy()

    if len(matches) == 0:

        st.warning(
            "No facility currently needs this supply."
        )

    else:

        today = pd.Timestamp.today().normalize()

        expiry = pd.Timestamp(surplus_expiry)

        days_left = (expiry - today).days


        # ----------------------------------------------------
        # EXPIRY RISK
        # ----------------------------------------------------

        if days_left <= 30:

            risk = "HIGH"
            risk_message = "This supply should be exchanged soon."

        elif days_left <= 60:

            risk = "MEDIUM"
            risk_message = "This supply should be considered soon."

        else:

            risk = "LOW"
            risk_message = "There is more time before expiry."


        st.subheader("Facilities that may need this supply")

        st.caption(
            f"Expiry risk: {risk} · {risk_message}"
        )


        # ----------------------------------------------------
        # SORT BY DEMAND
        # ----------------------------------------------------

        matches = matches.sort_values(
            by="Quantity Needed",
            ascending=True
        )


        for _, match in matches.iterrows():

            # ------------------------------------------------
            # PARTIAL MATCH
            # ------------------------------------------------

            matched_quantity = min(
                surplus_quantity,
                match["Quantity Needed"]
            )

            remaining_demand = (
                match["Quantity Needed"]
                - matched_quantity
            )


            # ------------------------------------------------
            # FINANCIAL CALCULATION
            # ------------------------------------------------

            normal_cost = (
                matched_quantity
                * prices[surplus_product]
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


            result1, result2, result3 = st.columns(3)

            with result1:

                st.metric(
                    "Matched",
                    f"{matched_quantity:,}"
                )

            with result2:

                st.metric(
                    "Demand remaining",
                    f"{remaining_demand:,}"
                )

            with result3:

                st.metric(
                    "Buyer saving",
                    f"${savings:,.2f}"
                )


            st.info(
                f"Partial exchange possible: "
                f"{matched_quantity:,} units can be redirected."
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
# SEARCH AVAILABLE SURPLUS
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
        (inventory["Quantity"] > 0)
    ].copy()


    if len(available) == 0:

        st.warning(
            "No suitable surplus is currently available."
        )

    else:

        today = pd.Timestamp.today().normalize()

        available["Days Left"] = (
            available["Expiry"] - today
        ).dt.days


        # ----------------------------------------------------
        # SORT BY EXPIRY
        # MOST URGENT FIRST
        # ----------------------------------------------------

        available = available.sort_values(
            by="Days Left",
            ascending=True
        )


        st.subheader("Available surplus")

        st.caption(
            "Supplies closest to expiry are shown first."
        )


        for _, supply in available.iterrows():

            days_left = supply["Days Left"]


            # ------------------------------------------------
            # EXPIRY RISK
            # ------------------------------------------------

            if days_left <= 30:

                risk = "HIGH"

            elif days_left <= 60:

                risk = "MEDIUM"

            else:

                risk = "LOW"


            # ------------------------------------------------
            # PARTIAL QUANTITY
            # ------------------------------------------------

            matched_quantity = min(
                needed_quantity,
                supply["Quantity"]
            )

            remaining_need = (
                needed_quantity
                - matched_quantity
            )


            # ------------------------------------------------
            # SAVINGS
            # ------------------------------------------------

            normal_cost = (
                matched_quantity
                * prices[needed_product]
            )

            exchange_cost = normal_cost * 0.80

            savings = normal_cost - exchange_cost


            st.write("")

            st.write(
                f"### {supply['Facility']}"
            )

            st.caption(
                f"{supply['Quantity']:,} "
                f"{needed_product} available · "
                f"Expires in {days_left} days · "
                f"Risk: {risk}"
            )


            result1, result2, result3 = st.columns(3)

            with result1:

                st.metric(
                    "Matched",
                    f"{matched_quantity:,}"
                )

            with result2:

                st.metric(
                    "Still needed",
                    f"{remaining_need:,}"
                )

            with result3:

                st.metric(
                    "Your saving",
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
# BUY VS EXCHANGE CALCULATOR
# ============================================================

st.markdown(
    '<div class="section-label">SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.header("Buy new or exchange?")


calc_col1, calc_col2 = st.columns(2)


with calc_col1:

    calculator_product = st.selectbox(
        "Product",
        ["Gauze", "Gloves", "IV Sets"],
        key="calculator_product"
    )

    calculator_quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1000,
        step=100,
        key="calculator_quantity"
    )


with calc_col2:

    normal_price = (
        calculator_quantity
        * prices[calculator_product]
    )

    exchange_price = normal_price * 0.80

    calculator_saving = (
        normal_price
        - exchange_price
    )

    st.metric(
        "Buying new",
        f"${normal_price:,.2f}"
    )

    st.metric(
        "Estimated exchange cost",
        f"${exchange_price:,.2f}"
    )

    st.success(
        f"Estimated saving: ${calculator_saving:,.2f}"
    )


# ============================================================
# BUSINESS MODEL
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">BUSINESS MODEL</div>',
    unsafe_allow_html=True
)

st.header("We make money when facilities save money.")

business_col1, business_col2 = st.columns(2)


with business_col1:

    st.write(
        "Expiry Exchange charges a small transaction fee "
        "when a successful exchange is completed."
    )

    st.write(
        "The buyer spends less, the supplier reduces "
        "waste, and the platform earns from the transaction."
    )


with business_col2:

    st.metric(
        "Illustrative transaction fee",
        "5%"
    )

    st.caption(
        "Example rate used for the prototype."
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

st.divider()

st.caption(
    "EXPIRY EXCHANGE · Prototype"
)
