# app.py
from datetime import date
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from config import PLANTS, MIXES, ADDITIVES, FIBERS, TRUCK_FEES, COUNTY_TAX_RATES
from calculator import calculate_truck_breakdown, calculate_quote_totals
from maps_service import rank_plants_by_distance, build_interactive_map

st.set_page_config(page_title="CEMEX Ready-Mix Quoting App", layout="wide")
st.title("CEMEX Ready-Mix Quoting & Plant Dispatch App")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("Dispatch & Tax Settings")
    yard_capacity = st.number_input("Max Yards per Truck (CY)", min_value=1.0, max_value=12.0, value=10.0, step=0.5)
    county_label = st.selectbox("County Tax Rate", list(COUNTY_TAX_RATES.keys()), index=0)
    tax_rate = st.number_input("Tax Rate (%)", value=COUNTY_TAX_RATES[county_label] * 100, step=0.05) / 100.0
    st.caption("Maps & routing powered by OpenStreetMap & OSRM (100% free, no API key needed).")

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
        placeholder="e.g., 5503 E Diana St, Tampa, FL 33610",
    )

    st.subheader("2. Concrete Mixes (Per Yard)")
    line_items = []
    total_yards = 0.0

    for mix in MIXES:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        qty = col_q.number_input(
            "Qty",
            min_value=0.0,
            step=0.5,
            value=0.0,
            key=f"mix_q_{mix['name']}",
            label_visibility="collapsed",
        )
        col_n.markdown(f"**{mix['name']}**")
        price = col_p.number_input(
            "Price",
            min_value=0.0,
            step=1.0,
            value=mix["price"],
            key=f"mix_p_{mix['name']}",
            label_visibility="collapsed",
        )
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)

        total_yards += qty
        if qty > 0:
            line_items.append({"Item #": "", "Description": mix["name"], "Unit": "CY", "Qty": qty, "Unit Price": price, "Amount": amt})

    # Calculate truck breakdown based on total concrete yards
    truck_info = calculate_truck_breakdown(total_yards, yard_capacity)
    trucks_needed = truck_info["total_trucks"]

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
    if trucks_needed > 0:
        st.info(f"🚛 **Truck Calculation:** {total_yards:.1f} CY requires **{trucks_needed} truck(s)** ({truck_info['breakdown_text']}).")
    else:
        st.caption("Enter concrete yards above to automatically calculate required trucks and load fees.")

    for fee in TRUCK_FEES:
        col_q, col_n, col_p, col_a = st.columns([1, 2.5, 1.2, 1.2])
        qty = col_q.number_input(
            "Trucks",
            min_value=0,
            step=1,
            value=trucks_needed,
            key=f"fee_q_{fee['item_no']}",
            label_visibility="collapsed",
        )
        col_n.write(f"`{fee['item_no']}` {fee['name']}")
        price = col_p.number_input("Price", min_value=0.0, step=5.0, value=fee["price"], key=f"fee_p_{fee['item_no']}", label_visibility="collapsed")
        amt = qty * price
        col_a.markdown(f"<div style='text-align:right; padding-top:6px;'>${amt:,.2f}</div>", unsafe_allow_html=True)
        if qty > 0:
            line_items.append({"Item #": fee["item_no"], "Description": fee["name"], "Unit": "TRUCK", "Qty": qty, "Unit Price": price, "Amount": amt})

# --- RIGHT COLUMN: PLANT DISPATCH, INTERACTIVE MAP & SUMMARY ---
with right_col:
    st.subheader("Interactive Plant Dispatch")

    selected_plant_label = "Not Assigned"
    if delivery_address:
        with st.spinner("Locating jobsite and calculating driving distances to all 21 plants..."):
            ranked_plants, dest_coords = rank_plants_by_distance(delivery_address)

        if ranked_plants and dest_coords:
            best = ranked_plants[0]
            st.success(
                f"**Recommended Load Plant:** #{best['plant_number']} — {best['name']} ({best['district']})\n\n"
                f"📍 {best['address']} | 🚛 **{best['distance_text']}** ({best['duration_text']})"
            )

            plant_options = [
                f"#{p['plant_number']} - {p['name']} ({p['distance_text']} / {p['duration_text']})"
                for p in ranked_plants
            ]
            chosen_idx = st.selectbox("Select / Override Load Plant", range(len(plant_options)), format_func=lambda i: plant_options[i])
            selected_plant = ranked_plants[chosen_idx]
            selected_plant_label = f"#{selected_plant['plant_number']} - {selected_plant['name']}"

            folium_map = build_interactive_map(selected_plant, dest_coords, delivery_address)
            st_folium(folium_map, width=None, height=380, returned_objects=[])

            with st.expander("View All 21 Plants Ranked by Proximity"):
                df_plants = pd.DataFrame(ranked_plants)[["plant_number", "district", "name", "distance_text", "duration_text", "address"]]
                st.dataframe(df_plants, use_container_width=True, hide_index=True)
        else:
            st.warning("Could not locate that exact address. Try including street, city, state, and ZIP code.")
    else:
        st.info("Enter a **Jobsite Delivery Address** on the left to find the closest plant and view the interactive route map.")
        st.dataframe(pd.DataFrame(PLANTS), use_container_width=True, hide_index=True)

    # Quote Summary & Export
    st.subheader("Quote Summary")
    totals = calculate_quote_totals(line_items, tax_rate)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Yards", f"{total_yards:.1f} CY")
    m2.metric("Trucks Needed", f"{trucks_needed}", help=truck_info["breakdown_text"])
    m3.metric(f"Tax ({tax_rate*100:.2f}%)", f"${totals['tax_amount']:,.2f}")
    m4.metric("Total Quote", f"${totals['grand_total']:,.2f}")

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
    else:
        st.caption("Quote is currently at **$0.00**. Enter a concrete quantity on the left to build the quote.")