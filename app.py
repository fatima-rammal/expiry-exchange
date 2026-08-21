import streamlit as st
from datetime import date

# ------------------------------------------------------------------
# This app is a small "marketplace" where hospitals can list unused
# medical supplies (surplus), and other hospitals can search for
# supplies they need. It's built with Streamlit, a library that lets
# you turn a plain Python script into a website.
# ------------------------------------------------------------------

st.set_page_config(page_title="Expiry Exchange", page_icon="♻", layout="wide")

# A little bit of custom styling: lighter background, red headings.
# st.markdown with unsafe_allow_html=True lets us inject raw CSS.
st.markdown("""
<style>
.stApp {
    background-color: #F5F5F5;
    color: #222222;
}
h1, h2, h3 {
    color: #D94A3A !important;
}
p, span, label, div {
    color: #222222;
}
.stSelectbox > div > div,
.stNumberInput > div > div,
.stDateInput > div > div,
.stTextInput > div > div,
[data-baseweb="select"] > div,
[data-baseweb="input"],
[data-baseweb="base-input"] {
    background-color: #D94A3A !important;
    color: white !important;
}
.stSelectbox input,
.stNumberInput input,
.stDateInput input,
.stTextInput input {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# A dictionary is just a lookup table: "product name" -> price per unit
PRICES = {
    "Gauze": 1.00,
    "Gloves": 0.40,
    "IV Sets": 2.50,
}

PLATFORM_FEE = 0.05        # 5% fee (just shown for display, not used in math below)
EXCHANGE_DISCOUNT = 0.20   # exchanging costs 20% less than buying new


# ------------------------------------------------------------------
# STORING DATA
# ------------------------------------------------------------------
# Streamlit re-runs your whole script every time the user clicks
# something. So normal Python variables would reset every time.
# st.session_state is a special dictionary that Streamlit remembers
# between those re-runs -- that's where we keep our data.
#
# Instead of a pandas DataFrame, we're using a plain Python list of
# dictionaries. Each dictionary is one row / one listing.
# ------------------------------------------------------------------

if "inventory" not in st.session_state:
    st.session_state.inventory = [
        {"facility": "City Hospital",   "product": "Gauze",  "quantity": 1000, "expiry": date(2026, 9, 15)},
        {"facility": "City Hospital",   "product": "Gloves", "quantity": 5000, "expiry": date(2026, 9, 5)},
        {"facility": "Medical Center",  "product": "Gauze",  "quantity": 200,  "expiry": date(2026, 10, 20)},
        {"facility": "Community Clinic","product": "Gloves", "quantity": 3000, "expiry": date(2026, 9, 30)},
    ]

inventory = st.session_state.inventory


# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------

st.title("Healthcare surplus, before it expires.")
st.write(
    "A marketplace for unused healthcare supplies. Facilities with surplus "
    "can list it, while facilities in need can find it before buying new."
)
st.write("")


# ------------------------------------------------------------------
# DASHBOARD NUMBERS
# ------------------------------------------------------------------
# A "for loop" here just goes through every listing one at a time
# and adds up the totals, instead of using pandas .sum()

total_units = 0
estimated_value = 0

for item in inventory:
    total_units += item["quantity"]
    estimated_value += item["quantity"] * PRICES[item["product"]]

col1, col2, col3 = st.columns(3)
col1.metric("Supplies listed", f"{total_units:,}")
col2.metric("Estimated value", f"${estimated_value:,.0f}")
col3.metric("Waste potentially diverted", f"{total_units:,} units")

st.divider()


# ------------------------------------------------------------------
# TWO COLUMNS: LIST SURPLUS / SEARCH FOR SUPPLIES
# ------------------------------------------------------------------

left, right = st.columns(2)

with left:
    st.header("I have surplus")
    st.write("List extra supplies so another facility can use them.")

    facility_name = st.text_input("Facility name", placeholder="e.g. City Hospital")
    surplus_product = st.selectbox("Supply", list(PRICES.keys()), key="surplus_product")
    surplus_quantity = st.number_input("Quantity available", min_value=1, value=100, step=50)
    surplus_expiry = st.date_input("Expiry date")
    list_surplus_clicked = st.button("List Surplus", use_container_width=True)

# This block runs only when the "List Surplus" button was clicked.
if list_surplus_clicked:
    if facility_name.strip() == "":
        st.warning("Please enter your facility name.")
    else:
        # Add a new dictionary (row) to our list of listings
        inventory.append({
            "facility": facility_name,
            "product": surplus_product,
            "quantity": surplus_quantity,
            "expiry": surplus_expiry,
        })
        st.success(f"✓ {surplus_quantity:,} {surplus_product} listed successfully.")

with right:
    st.header("I need supplies")
    st.write("Search existing surplus before buying new stock.")

    needed_product = st.selectbox("Supply needed", list(PRICES.keys()), key="needed_product")
    needed_quantity = st.number_input("Quantity required", min_value=1, value=500, step=50)
    search_clicked = st.button("Search Surplus", use_container_width=True)


# ------------------------------------------------------------------
# SEARCH RESULTS
# ------------------------------------------------------------------

if search_clicked:
    st.divider()
    st.subheader(f"Surplus available for {needed_product}")

    # Build a list of only the listings that match what's needed
    matches = []
    for item in inventory:
        if item["product"] == needed_product and item["quantity"] > 0:
            matches.append(item)

    if len(matches) == 0:
        st.warning("No surplus is currently available for this supply.")
    else:
        today = date.today()

        # Add a "days_left" value to each match, then sort so the
        # soonest-to-expire listings show up first.
        for item in matches:
            item["days_left"] = (item["expiry"] - today).days

        matches.sort(key=lambda item: item["days_left"])

        for item in matches:
            days_left = item["days_left"]

            if days_left <= 30:
                risk = "HIGH"
            elif days_left <= 60:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            # How much of the request can this listing cover?
            matched_qty = min(needed_quantity, item["quantity"])
            remaining_need = needed_quantity - matched_qty

            normal_cost = matched_qty * PRICES[needed_product]
            exchange_cost = normal_cost * (1 - EXCHANGE_DISCOUNT)
            savings = normal_cost - exchange_cost

            st.write(f"### {item['facility']}")
            st.caption(f"{item['quantity']:,} {needed_product} available")

            r1, r2, r3 = st.columns(3)
            r1.metric("Available", f"{item['quantity']:,}")
            r2.metric("Expires in", f"{days_left} days")
            r3.metric("Your saving", f"${savings:,.2f}")

            st.write(f"Expiry risk: **{risk}**")

            if remaining_need > 0:
                st.info(
                    f"Partial exchange: {matched_qty:,} units available. "
                    f"You would still need {remaining_need:,} units."
                )
            else:
                st.success("This surplus can cover your full request.")

            st.divider()


# ------------------------------------------------------------------
# SAVINGS CALCULATOR
# ------------------------------------------------------------------

st.header("Buy new or exchange?")

calc1, calc2 = st.columns(2)

with calc1:
    calc_product = st.selectbox("Product", list(PRICES.keys()), key="calc_product")
    calc_quantity = st.number_input("Quantity", min_value=1, value=1000, step=100)

with calc2:
    normal_price = calc_quantity * PRICES[calc_product]
    exchange_price = normal_price * (1 - EXCHANGE_DISCOUNT)
    calc_savings = normal_price - exchange_price

    st.metric("Buying new", f"${normal_price:,.2f}")
    st.metric("Estimated exchange cost", f"${exchange_price:,.2f}")
    st.success(f"Estimated saving: ${calc_savings:,.2f}")


# ------------------------------------------------------------------
# FULL LISTING TABLE
# ------------------------------------------------------------------

st.divider()
st.header("Live marketplace")
st.write("All currently listed surplus supplies:")

# st.table / st.dataframe can display a list of dictionaries directly,
# no pandas needed.
st.dataframe(inventory, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------

st.divider()
st.caption("EXPIRY EXCHANGE · Prototype")
