import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("SACHIN AATA CHHAKI - ADVANCE MANAGEMENT")

file_name = "dukaan_data.csv"

# ========= SAFE FLOAT =========
def to_float(val):
    try:
        return float(val)
    except:
        return None

# ========= LOAD DATA =========
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Date","Item","Qty","Rate","Payment","Type","Total"])

# ========= MENU =========
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

payment_mode = st.selectbox("Payment Mode", ["Cash","Online","Udhar"])

qty = st.text_input("Quantity (kg)")
rate = st.text_input("Rate per kg")

qty_float = to_float(qty)
rate_float = to_float(rate)

# ========= LIVE TOTAL =========
if qty_float and rate_float:
    total = round(qty_float * rate_float,2)
    if "खरीद" in menu:
        st.markdown(f"### 🔴 देना है: ₹ {total:,.2f}")
    else:
        st.markdown(f"### 🟢 लेना है: ₹ {total:,.2f}")

# ========= SAVE =========
if st.button("Save Entry"):
    if qty_float is None or rate_float is None:
        st.error("Number sahi likho")
    else:
        total = round(qty_float * rate_float,2)

        if "खरीद" in menu:
            entry_type = "Purchase"
            signed_total = -total
        else:
            entry_type = "Sale"
            signed_total = total

        new_row = {
            "Date": datetime.now().strftime("%d-%m-%Y"),
            "Item": menu,
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)

        st.success("Entry Saved ✅")

# ========= FORMAT =========
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

# ========= EDIT DELETE =========
st.subheader("Edit / Delete Entry")

if not df.empty:

    row_id = st.number_input("Row Number", 0, len(df)-1, 0)

    if st.button("Delete Selected"):
        df = df.drop(row_id).reset_index(drop=True)
        df.to_csv(file_name,index=False)
        st.success("Deleted ✅")
        st.rerun()

# ========= FILTER =========
st.subheader("Filter Section")

if not df.empty:

    day = st.date_input("Select Date", value=None)
    month = st.selectbox("Month", ["All"] + list(range(1,13)))
    year = st.selectbox("Year", ["All"] + sorted(df["Date"].dt.year.unique()))

    filtered = df.copy()

    if day:
        filtered = filtered[filtered["Date"] == pd.to_datetime(day)]

    if month != "All":
        filtered = filtered[filtered["Date"].dt.month == month]

    if year != "All":
        filtered = filtered[filtered["Date"].dt.year == year]

    st.dataframe(filtered)

    # ========= SUMMARY =========
    st.subheader("Summary")

    total_sale = filtered[filtered["Total"] > 0]["Total"].sum()
    total_purchase = abs(filtered[filtered["Total"] < 0]["Total"].sum())
    net = filtered["Total"].sum()

    st.write("Total Sale ₹:", round(total_sale,2))
    st.write("Total Purchase ₹:", round(total_purchase,2))
    st.write("Net Balance ₹:", round(net,2))

    # ========= ITEM WISE =========
    st.subheader("Item Wise Summary")
    st.dataframe(filtered.groupby("Item")["Total"].sum().reset_index())

    # ========= PAYMENT WISE =========
    st.subheader("Payment Wise Summary")
    st.dataframe(filtered.groupby("Payment")["Total"].sum().reset_index())

    # ========= DOWNLOAD =========
    st.download_button(
        "Download Excel",
        filtered.to_csv(index=False),
        "dukaan_report.csv",
        "text/csv"
    )
