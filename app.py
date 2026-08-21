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
.stDateInput > div > div,
.stTextInput > div > div {
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
# PRODUCT PRICES
# ============================================================

prices = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50
}


# ============================================================
# INITIAL MARKETPLACE DATA
# ============================================================

initial_inventory = pd.DataFrame({
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

initial_inventory["Expiry"] = pd.to_datetime(
    initial_inventory["Expiry"]
)


# ============================================================
# CREATE LIVE INVENTORY
# ============================================================

if "inventory" not in st.session_state:

    st.session_state.inventory = initial_inventory.copy()


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
    "A marketplace for unused healthcare supplies. "
    "Facilities with surplus can list it, while facilities "
    "in need can find it before buying new."
    "</div>",
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# LIVE IMPACT DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-label">PLATFORM IMPACT</div>',
    unsafe_allow_html=True
)

total_units = int(
    st.session_state.inventory["Quantity"].sum()
)

estimated_value = 0

for _, row in st.session_state.inventory.iterrows():

    estimated_value += (
        row["Quantity"]
        * prices[row["Product"]]
    )


dashboard1, dashboard2, dashboard3 = st.columns(3)

with dashboard1:

    st.metric(
        "Supplies listed",
        f"{total_units:,}"
    )

with dashboard2:

    st.metric(
        "Estimated value",
        f"${estimated_value:,.0f}"
    )

with dashboard3:

    st.metric(
        "Waste potentially diverted",
        f"{total_units:,} units"
    )


st.divider()


# ============================================================
# MAIN FUNCTIONS
# ============================================================

left, right = st.columns(2)


# ============================================================
# I HAVE SURPLUS
# ============================================================

with left:

    st.markdown(
        '<div class="section-label">SUPPLIER</div>',
        unsafe_allow_html=True
    )

    st.header("I have surplus")

    st.write(
        "List extra supplies so another facility can use them."
    )

    facility_name = st.text_input(
        "Facility name",
        placeholder="e.g. City Hospital",
        key="facility_name"
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

    list_surplus = st.button(
        "List Surplus",
        use_container_width=True,
        key="list_surplus"
    )


# ============================================================
# ADD NEW SURPLUS
# ============================================================

if list_surplus:

    if facility_name.strip() == "":

        st.warning(
            "Please enter your facility name."
        )

    else:

        new_supply = pd.DataFrame({
            "Facility": [facility_name],
            "Product": [surplus_product],
            "Quantity": [surplus_quantity],
            "Expiry": [pd.Timestamp(surplus_expiry)]
        })

        st.session_state.inventory = pd.concat(
            [
                st.session_state.inventory,
                new_supply
            ],
            ignore_index=True
        )

        st.success(
            f"✓ {surplus_quantity:,} "
            f"{surplus_product} listed successfully."
        )

        st.info(
            "Your surplus is now visible in the "
            "live marketplace."
        )


# ============================================================
# I NEED SUPPLIES
# ============================================================

with right:

    st.markdown(
        '<div class="section-label">BUYER</div>',
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
        "Search Surplus",
        use_container_width=True,
        key="search_surplus"
    )


# ============================================================
# SEARCH LIVE MARKETPLACE
# ============================================================

if search_surplus:

    st.divider()

    st.markdown(
        '<div class="section-label">MARKETPLACE RESULTS</div>',
        unsafe_allow_html=True
    )

    available = st.session_state.inventory[
        (
            st.session_state.inventory["Product"]
            == needed_product
        )
        &
        (
            st.session_state.inventory["Quantity"]
            > 0
        )
    ].copy()


    if len(available) == 0:

        st.warning(
            "No surplus is currently available "
            "for this supply."
        )

    else:

        today = pd.Timestamp.today().normalize()

        available["Days Left"] = (
            available["Expiry"] - today
        ).dt.days

        available = available.sort_values(
            by="Days Left",
            ascending=True
        )

        st.subheader(
            f"Surplus available for {needed_product}"
        )

        st.caption(
            "Supplies closest to expiry are shown first."
        )


        for index, supply in available.iterrows():

            days_left = int(
                supply["Days Left"]
            )


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
            # PARTIAL MATCH
            # ------------------------------------------------

            matched_quantity = min(
                needed_quantity,
                int(supply["Quantity"])
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

            exchange_cost = (
                normal_cost * 0.80
            )

            savings = (
                normal_cost
                - exchange_cost
            )


            # ------------------------------------------------
            # MATCH SCORE
            # ------------------------------------------------

            score = 50

            if matched_quantity == needed_quantity:

                score += 20

            else:

                score += 10

            if days_left <= 30:

                score += 20

            elif days_left <= 60:

                score += 10

            else:

                score += 5

            if days_left >= 0:

                score += 10

            score = min(score, 100)


            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            st.write("")

            st.write(
                f"### {supply['Facility']}"
            )

            st.caption(
                f"{int(supply['Quantity']):,} "
                f"{needed_product} available"
            )


            result1, result2, result3, result4 = st.columns(4)


            with result1:

                st.metric(
                    "Match",
                    f"{score}%"
                )


            with result2:

                st.metric(
                    "Available",
                    f"{int(supply['Quantity']):,}"
                )


            with result3:

                st.metric(
                    "Expires in",
                    f"{days_left} days"
                )


            with result4:

                st.metric(
                    "Your saving",
                    f"${savings:,.2f}"
                )


            st.write(
                f"**Why this match?** "
                f"Same supply ✓ · "
                f"{matched_quantity:,} units can be matched ✓ · "
                f"Expiry risk: {risk}"
            )


            if remaining_need > 0:

                st.info(
                    f"Partial exchange: "
                    f"{matched_quantity:,} units available. "
                    f"You would still need "
                    f"{remaining_need:,} units."
                )

            else:

                st.success(
                    "This surplus can cover your full request."
                )


            button_key = (
                f"request_"
                f"{supply['Facility']}_"
                f"{needed_product}_"
                f"{index}"
            )


            if st.button(
                "Request Exchange",
                key=button_key,
                use_container_width=True
            ):

                st.success(
                    "✓ Exchange request submitted!"
                )

                st.write(
                    f"**{matched_quantity:,} "
                    f"{needed_product}**"
                )

                st.write(
                    f"From: **{supply['Facility']}**"
                )

                st.write(
                    f"Estimated saving: "
                    f"**${savings:,.2f}**"
                )

                st.write(
                    f"Potential waste diverted: "
                    f"**{matched_quantity:,} units**"
                )


            st.divider()


# ============================================================
# SAVINGS CALCULATOR
# ============================================================

st.markdown(
    '<div class="section-label">SAVINGS CALCULATOR</div>',
    unsafe_allow_html=True
)

st.header("Buy new or exchange?")


calc1, calc2 = st.columns(2)


with calc1:

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


with calc2:

    normal_price = (
        calculator_quantity
        * prices[calculator_product]
    )

    exchange_price = (
        normal_price * 0.80
    )

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
        f"Estimated saving: "
        f"${calculator_saving:,.2f}"
    )


# ============================================================
# BUSINESS MODEL
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">BUSINESS MODEL</div>',
    unsafe_allow_html=True
)

st.header(
    "We make money when facilities save money."
)

business1, business2 = st.columns(2)


with business1:

    st.write(
        "Expiry Exchange charges a small transaction "
        "fee when an exchange is completed."
    )

    st.write(
        "The buyer pays less, the supplier reduces "
        "waste, and the platform earns from the transaction."
    )


with business2:

    st.metric(
        "Illustrative platform fee",
        "5%"
    )

    st.caption(
        "Example rate used for the prototype."
    )


# ============================================================
# LIVE MARKETPLACE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">LIVE MARKETPLACE</div>',
    unsafe_allow_html=True
)

st.write(
    "All currently listed surplus supplies:"
)

display_inventory = st.session_state.inventory.copy()

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
# HOW IT WORKS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-label">HOW IT WORKS</div>',
    unsafe_allow_html=True
)

step1, step2, step3 = st.columns(3)


with step1:

    st.subheader("01 · List")

    st.write(
        "A facility lists unused supplies "
        "before they expire."
    )


with step2:

    st.subheader("02 · Match")

    st.write(
        "Facilities in need search the "
        "available surplus."
    )


with step3:

    st.subheader("03 · Exchange")

    st.write(
        "The buyer saves money while "
        "preventing unnecessary waste."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EXPIRY EXCHANGE · Prototype"
)
st.divider()

st.caption(
    "EXPIRY EXCHANGE · Prototype"
)
