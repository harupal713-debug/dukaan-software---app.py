import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("SACHIN AATA CHHAKI - SMART MANAGEMENT")

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
if qty_float is not None and rate_float is not None:
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
        st.rerun()

# ========= FORMAT =========
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

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

    # ========= SHOW TABLE WITH EDIT DELETE =========
    st.subheader("Entries")

    for index, row in filtered.iterrows():

        col1, col2, col3 = st.columns([6,1,1])

        with col1:
            st.write(f"{row['Date'].date()} | {row['Item']} | ₹{row['Total']:,.2f}")

        with col2:
            if st.button("✏ Edit", key=f"edit{index}"):
                st.session_state["edit_id"] = index

        with col3:
            if st.button("❌ Delete", key=f"del{index}"):
                df = df.drop(index).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.success("Deleted ✅")
                st.rerun()

    # ========= EDIT SECTION =========
    if "edit_id" in st.session_state:

        edit_row = df.loc[st.session_state["edit_id"]]

        st.subheader("Edit Entry")

        new_qty = st.text_input("New Qty", value=str(edit_row["Qty"]))
        new_rate = st.text_input("New Rate", value=str(edit_row["Rate"]))

        if st.button("Update Entry"):

            new_total = round(float(new_qty)*float(new_rate),2)

            if "Purchase" in edit_row["Type"]:
                new_total = -new_total

            df.loc[st.session_state["edit_id"],"Qty"] = float(new_qty)
            df.loc[st.session_state["edit_id"],"Rate"] = float(new_rate)
            df.loc[st.session_state["edit_id"],"Total"] = new_total

            df.to_csv(file_name,index=False)

            st.success("Updated ✅")
            del st.session_state["edit_id"]
            st.rerun()

    # ========= MERGED SUMMARY =========
    st.subheader("Combined Summary")

    summary = filtered.groupby(["Item","Payment"])["Total"].sum().reset_index()
    st.dataframe(summary)

    # ========= FINAL TOTAL =========
    st.markdown("---")
    total_sale = filtered[filtered["Total"] > 0]["Total"].sum()
    total_purchase = abs(filtered[filtered["Total"] < 0]["Total"].sum())
    net = filtered["Total"].sum()

    st.markdown(f"### 🟢 Total Sale: ₹ {total_sale:,.2f}")
    st.markdown(f"### 🔴 Total Purchase: ₹ {total_purchase:,.2f}")
    st.markdown(f"## 💰 Net Balance: ₹ {net:,.2f}")

    # ========= DOWNLOAD =========
    st.download_button(
        "Download Excel",
        filtered.to_csv(index=False),
        "dukaan_report.csv",
        "text/csv"
    )
