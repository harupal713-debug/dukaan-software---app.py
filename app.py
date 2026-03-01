import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("SACHIN AATA CHHAKI - DUKAAN MANAGEMENT")

file_name = "dukaan_data.csv"

# ===== MENU =====
menu = st.selectbox("Kaunsa kaam?", [
    "गेहू खरीदा",
    "आटा पिसाई",
    "आटा बेचा",
    "सरसों तेल बेचा",
    "सरसों पिसाई",
    "सरसों खरीदी",
    "चावल खरीदा",
    "सरसों खल बेची",
    "चावल बेचा",
])

# ===== PAYMENT MODE =====
payment_mode = st.selectbox("Payment Mode", [
    "Cash",
    "Online",
    "Udhar"
])

# ===== INPUT =====
qty = st.text_input("Quantity (kg)", placeholder="कितना वजन")
rate = st.text_input("Rate per kg", placeholder="कितने रु")

# ===== LIVE CALCULATION =====
if qty != "" and rate != "":
    try:
        qty_float = float(qty)
        rate_float = float(rate)

        total = round(qty_float * rate_float, 2)
        formatted_total = f"{total:,.2f}"

        if "खरीद" in menu:
            st.markdown(f"<h2 style='color:red;'>देना है: ₹ {formatted_total}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:green;'>लेना है: ₹ {formatted_total}</h2>", unsafe_allow_html=True)

    except:
        st.error("सही नंबर लिखें")

# ===== SAVE ENTRY =====
if st.button("Save Entry") and qty != "" and rate != "":
    try:
        qty_float = float(qty)
        rate_float = float(rate)
        total = round(qty_float * rate_float, 2)

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
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }])

        if os.path.exists(file_name):
            new_entry.to_csv(file_name, mode="a", header=False, index=False)
        else:
            new_entry.to_csv(file_name, index=False)

        st.success("Entry Saved Successfully!")
        st.rerun()

    except:
        st.error("Save नहीं हुआ")

# ===== LOAD DATA =====
if os.path.exists(file_name):

    df = pd.read_csv(file_name)

    # DATE SAFE CONVERSION (CRASH FIX)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    st.subheader("All Entries")
    st.dataframe(df)

    # ===== DELETE ENTRY =====
    st.subheader("Delete Entry")

    if len(df) > 0:
        delete_index = st.number_input("Row Number to Delete", min_value=0, max_value=len(df)-1, step=1)

        if st.button("Delete Selected Entry"):
            df = df.drop(delete_index).reset_index(drop=True)
            df.to_csv(file_name, index=False)
            st.success("Entry Deleted Successfully!")
            st.rerun()

    # ===== FILTER SECTION =====
    st.subheader("Filter Data")

    day_filter = st.date_input("Select Date", value=None)
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

    st.write("Total Quantity:", round(total_qty,2))
    st.write("Total Lena: ₹", round(total_lena,2))
    st.write("Total Dena: ₹", round(abs(total_dena),2))
    st.write("Net Balance: ₹", round(net_balance,2))

    # ===== ITEM WISE SUMMARY =====
    st.subheader("Item Wise Summary")
    item_summary = filtered_df.groupby("Item")["Total"].sum().reset_index()
    st.dataframe(item_summary)

    # ===== PAYMENT SUMMARY =====
    st.subheader("Payment Mode Summary")
    payment_summary = filtered_df.groupby("Payment")["Total"].sum().reset_index()
    st.dataframe(payment_summary)

    # ===== DOWNLOAD BUTTON =====
    st.download_button(
        label="Download Excel",
        data=filtered_df.to_csv(index=False),
        file_name="dukaan_filtered_data.csv",
        mime="text/csv"
    )
