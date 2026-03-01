import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("SACHIN AATA CHHAKI - DUKAAN MANAGEMENT")

file_name = "dukaan_data.csv"

# ===== MENU =====
menu = st.selectbox("Kaunsa kaam?", [
    "गेहू खरीदा",
    "आटा बेचा",
    "सरसों खरीदी",
    "सरसों तेल बेचा",
    "चावल खरीदा",
    "चावल बेचा",
])

qty = st.number_input("Quantity (kg)", min_value=0.0, step=0.01)
rate = st.number_input("Rate per kg", min_value=0.0, step=0.01)

# ===== SAVE ENTRY =====
if st.button("Save Entry"):

    total = round(qty * rate, 2)

    if "खरीद" in menu:
        entry_type = "Dena"
        signed_total = -total
    else:
        entry_type = "Lena"
        signed_total = total

    today = datetime.now().strftime("%d-%m-%Y")

    new_entry = pd.DataFrame([{
        "Date": today,
        "Item": menu,
        "Qty": qty,
        "Rate": rate,
        "Type": entry_type,
        "Total": signed_total
    }])

    if os.path.exists(file_name):
        new_entry.to_csv(file_name, mode="a", header=False, index=False)
    else:
        new_entry.to_csv(file_name, index=False)

    st.success("Entry Saved Successfully!")

# ===== LOAD DATA =====
if os.path.exists(file_name):

    df = pd.read_csv(file_name)

    st.subheader("All Entries")
    st.dataframe(df)

    # ===== FILTER SECTION =====
    st.subheader("Filter Data")

    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    day_filter = st.date_input("Select Date")
    month_filter = st.selectbox("Select Month", ["All"] + list(range(1,13)))
    year_filter = st.selectbox("Select Year", ["All"] + sorted(df["Date"].dt.year.unique()))

    filtered_df = df.copy()

    if day_filter:
        filtered_df = filtered_df[filtered_df["Date"] == pd.to_datetime(day_filter)]

    if month_filter != "All":
        filtered_df = filtered_df[filtered_df["Date"].dt.month == month_filter]

    if year_filter != "All":
        filtered_df = filtered_df[filtered_df["Date"].dt.year == year_filter]

    st.subheader("Filtered Result")
    st.dataframe(filtered_df)

    # ===== SUMMARY =====
    st.subheader("Summary")

    total_qty = filtered_df["Qty"].sum()
    total_lena = filtered_df[filtered_df["Total"] > 0]["Total"].sum()
    total_dena = filtered_df[filtered_df["Total"] < 0]["Total"].sum()
    net_balance = filtered_df["Total"].sum()

    st.write("Total Quantity:", total_qty)
    st.write("Total Lena: ₹", round(total_lena,2))
    st.write("Total Dena: ₹", round(abs(total_dena),2))
    st.write("Net Balance: ₹", round(net_balance,2))

    # ===== ITEM WISE SUMMARY =====
    st.subheader("Item Wise Summary")
    item_summary = filtered_df.groupby("Item")["Total"].sum().reset_index()
    st.dataframe(item_summary)

    # ===== DOWNLOAD BUTTON =====
    st.download_button(
        label="Download Excel",
        data=filtered_df.to_csv(index=False),
        file_name="dukaan_filtered_data.csv",
        mime="text/csv"
    )
