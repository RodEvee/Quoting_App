# app.py
from datetime import date
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from config import PLANTS, MIXES, ADDITIVES, FIBERS, TRUCK_FEES, COUNTY_TAX_RATES
from calculator import estimate_trucks, calculate_quote_totals
from maps_service import rank_plants_by_distance, get_directions_iframe_html

st.set_page_config(page_title="CEMEX Ready-Mix Quoting App", layout="wide")
st.title("CEMEX Ready-Mix Quoting & Plant Dispatch App")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Google Maps API Key",
        type="password",
        help="Requires Distance Matrix API & Maps Embed API enabled.",
    )
    yard_capacity = st.number_input("Max Yards per Truck (CY)", min_value=1.0, max_value=12.0, value=10.0, step=0.5)
    county_label = st.selectbox("County Tax Rate", list(COUNTY_TAX_RATES.keys()), index=0)
    tax_rate = st.number_input("Tax Rate (%)", value=COUNTY_TAX_RATES[county_label] * 100, step=0.05) / 100.0

left_col, right_col = st.columns([1.25, 0.95], gap="large")

# --- LEFT COLUMN: QUOTE INPUTS & LINE ITEMS ---
with left_col:
    st.subheader("1. Customer & Delivery Details")
    c1, c2, c3 = st.columns(3)
    quote_date = c1.date_input("Today's Date", value=date.today())
    delivery_date = c2.date_input("Delivery Date", value=date.today())
    cust_name = c3.text_input("Customer Name", placeholder="Luis Gonzalez")

    c4, c5, c6 = st.columns(3)
    company_name = c4.text_input("Company Name")
    cust_phone = c5.text_input("Phone", placeholder="321-419-7257")
    cust_email = c6.text_input("Email Address")

    delivery_address = st.text_input(
        "Jobsite Delivery Address",
        placeholder="e.g., 1406 Atlanta Ave, Orlando, FL 32806",
    )

    st.subheader("2. Concrete Mixes (Per Yard)")
    line_items = []
    total_yards = 0.0

    for mix in MIXES:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        default_qty = 10.0 if mix["name"] == "4000 PSI REGULAR" else 0.0
        qty = col_q.number_input("Qty", min_value=0.0, step=0.5, value=default_qty, key=f"mix_q_{mix['name']}", label_visibility="collapsed")
        col_n.markdown(f"**{mix['name']}**")
        price = col_p.number_input("Price", min_value=0.0, step=1.0, value=mix["price"], key=f"mix_p_{mix['name']}", label_visibility="collapsed")
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)

        total_yards += qty
        if qty > 0:
            line_items.append({"Item #": "", "Description": mix["name"], "Unit": "CY", "Qty": qty, "Unit Price": price, "Amount": amt})

    st.subheader("3. Additives & Fibers (Per Yard)")
    for add in ADDITIVES:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        qty = col_q.number_input("Qty", min_value=0.0, step=0.5, value=0.0, key=f"add_q_{add['name']}", label_visibility="collapsed")
        col_n.write(add["name"])
        price = col_p.number_input("Price", min_value=0.0, step=0.5, value=add["price"], key=f"add_p_{add['name']}", label_visibility="collapsed")
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)
        if qty > 0:
            line_items.append({"Item #": "", "Description": add["name"], "Unit": "CY", "Qty": qty, "Unit Price": price, "Amount": amt})

    for fib in FIBERS:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        qty = col_q.number_input("Qty", min_value=0.0, step=0.5, value=0.0, key=f"fib_q_{fib['item_no']}", label_visibility="collapsed")
        col_n.write(f"`{fib['item_no']}` {fib['name']}")
        price = col_p.number_input("Price", min_value=0.0, step=0.5, value=fib["price"], key=f"fib_p_{fib['item_no']}", label_visibility="collapsed")
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)
        if qty > 0:
            line_items.append({"Item #": fib["item_no"], "Description": fib["name"], "Unit": "CY", "Qty": qty, "Unit Price": price, "Amount": amt})

    st.subheader("4. Truck / Load Fees (Per Truck)")
    trucks_needed = estimate_trucks(total_yards, yard_capacity)
    st.caption(f"Auto-estimated trucks based on {total_yards:.1f} CY @ {yard_capacity:.1f} CY/truck: **{trucks_needed} truck(s)**")

    for fee in TRUCK_FEES:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        qty = col_q.number_input("Trucks", min_value=0, step=1, value=trucks_needed, key=f"fee_q_{fee['item_no']}", label_visibility="collapsed")
        col_n.write(f"`{fee['item_no']}` {fee['name']}")
        price = col_p.number_input("Price", min_value=0.0, step=5.0, value=fee["price"], key=f"fee_p_{fee['item_no']}", label_visibility="collapsed")
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)
        if qty > 0:
            line_items.append({"Item #": fee["item_no"], "Description": fee["name"], "Unit": "TRUCK", "Qty": qty, "Unit Price": price, "Amount": amt})

# --- RIGHT COLUMN: PLANT DISPATCH, INTERACTIVE MAP & SUMMARY ---
with right_col:
    st.subheader("Interactive Plant Dispatch")

    if delivery_address and api_key:
        try:
            ranked_plants = rank_plants_by_distance(api_key, delivery_address)
            best = ranked_plants[0]
            st.success(
                f"**Recommended Load Plant:** #{best['plant_number']} — {best['name']} ({best['district']})\n\n"
                f"📍 {best['address']} | 🚛 **{best['distance_text']}** ({best['duration_text']})"
            )

            plant_options = [
                f"#{p['plant_number']} - {p['name']} ({p['distance_text']} / {p['duration_text']})"
                for p in ranked_plants
            ]
            chosen_idx = st.selectbox("Override Load Plant", range(len(plant_options)), format_func=lambda i: plant_options[i])
            selected_plant = ranked_plants[chosen_idx]

            iframe_html = get_directions_iframe_html(api_key, selected_plant["address"], delivery_address)
            components.html(iframe_html, height=415)

            with st.expander("View All Plants Ranked by Distance"):
                df_plants = pd.DataFrame(ranked_plants)[["plant_number", "district", "name", "distance_text", "duration_text", "address"]]
                st.dataframe(df_plants, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Google Maps lookup failed: {e}")
    else:
        st.info("Enter your **Google Maps API Key** in the sidebar and a **Jobsite Delivery Address** on the left to auto-rank the closest plant and load the interactive route map.")
        st.dataframe(pd.DataFrame(PLANTS), use_container_width=True, hide_index=True)

    # Quote Summary & Export
    st.subheader("Quote Summary")
    totals = calculate_quote_totals(line_items, tax_rate)

    m1, m2, m3 = st.columns(3)
    m1.metric("Sub Total", f"${totals['sub_total']:,.2f}")
    m2.metric(f"Tax ({tax_rate*100:.2f}%)", f"${totals['tax_amount']:,.2f}")
    m3.metric("Total Quote", f"${totals['grand_total']:,.2f}")

    if line_items:
        summary_df = pd.DataFrame(line_items)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        csv_data = summary_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Quote as CSV",
            data=csv_data,
            file_name=f"CEMEX_Quote_{cust_name or 'Customer'}_{quote_date}.csv",
            mime="text/csv",
        )