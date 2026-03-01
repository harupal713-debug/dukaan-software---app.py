import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SACHIN AATA CHHAKI", layout="wide")

st.markdown("<h1 style='text-align:center;'>🛒 SACHIN AATA CHHAKI</h1>", unsafe_allow_html=True)

file_name = "dukaan_data.csv"

# ---------- Safe Float ----------
def to_float(val):
    try:
        return float(val)
    except:
        return None

# ---------- Load Data ----------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Date","Item","Qty","Rate","Payment","Type","Total"])

# ---------- ENTRY SECTION ----------
st.markdown("## ➕ New Entry")

col1, col2, col3 = st.columns(3)

with col1:
    menu = st.selectbox("Item", [
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

with col2:
    payment_mode = st.selectbox("Payment", ["Cash","Online","Udhar"])

with col3:
    qty = st.text_input("Quantity (kg)")

rate = st.text_input("Rate per kg")

qty_float = to_float(qty)
rate_float = to_float(rate)

if qty_float and rate_float:
    total_preview = round(qty_float * rate_float,2)
    color = "red" if "खरीद" in menu else "green"
    text = "देना है" if "खरीद" in menu else "लेना है"
    st.markdown(f"<h3 style='color:{color};'>{text}: ₹ {total_preview:,.2f}</h3>", unsafe_allow_html=True)

# ---------- SAVE ----------
if st.button("💾 Save Entry", use_container_width=True):
    if qty_float is None or rate_float is None:
        st.error("❌ Quantity aur Rate sahi number me likho")
    else:
        total = round(qty_float * rate_float,2)
        signed_total = -total if "खरीद" in menu else total
        entry_type = "Purchase" if "खरीद" in menu else "Sale"

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": menu,
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("✅ Entry Saved")
        st.rerun()

# ---------- PROCESS DATA ----------
if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"])
    df["Qty"] = pd.to_numeric(df["Qty"])
    df["Total"] = pd.to_numeric(df["Total"])

    st.markdown("---")
    st.markdown("## 🔍 Filter Summary")

    filter_type = st.selectbox("Select Period", ["All","Day","Month","Year"])

    filtered_df = df.copy()

    if filter_type == "Day":
        selected_day = st.date_input("Select Day")
        filtered_df = df[df["Date"].dt.date == selected_day]

    elif filter_type == "Month":
        selected_month = st.selectbox("Select Month", range(1,13))
        selected_year = st.selectbox("Select Year", df["Date"].dt.year.unique())
        filtered_df = df[
            (df["Date"].dt.month == selected_month) &
            (df["Date"].dt.year == selected_year)
        ]

    elif filter_type == "Year":
        selected_year = st.selectbox("Select Year", df["Date"].dt.year.unique())
        filtered_df = df[df["Date"].dt.year == selected_year]

    # ---------- ITEM WISE SUMMARY ----------
    st.markdown("### 📦 Item Wise Summary")

    item_summary = filtered_df.groupby("Item").agg({
        "Qty":"sum",
        "Total":"sum"
    }).reset_index()

    st.dataframe(item_summary, use_container_width=True)

    # ---------- OVERALL SUMMARY ----------
    st.markdown("### 📊 Summary")

    total_sale = filtered_df[filtered_df["Total"] > 0]["Total"].sum()
    total_purchase = abs(filtered_df[filtered_df["Total"] < 0]["Total"].sum())
    net = filtered_df["Total"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sale", f"₹ {total_sale:,.2f}")
    c2.metric("Total Purchase", f"₹ {total_purchase:,.2f}")
    c3.metric("Net Balance", f"₹ {net:,.2f}")

    # ---------- ALL ENTRIES ----------
    st.markdown("---")
    st.markdown("## 📋 All Entries")

    for index, row in df.iterrows():

        col1, col2, col3 = st.columns([6,1,1])

        with col1:
            color = "green" if row["Total"] > 0 else "red"
            st.markdown(
                f"<b>{row['Date'].date()}</b> | {row['Item']} | ₹ <span style='color:{color};'>{row['Total']:,.2f}</span>",
                unsafe_allow_html=True
            )

        # EDIT
        with col2:
            if st.button("✏️", key=f"edit{index}"):
                st.session_state["edit_index"] = index

        # DELETE
        with col3:
            if st.button("❌", key=f"del{index}"):
                df = df.drop(index).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.rerun()

    # ---------- EDIT MODE ----------
    if "edit_index" in st.session_state:

        st.markdown("---")
        st.markdown("## ✏️ Edit Entry")

        edit_i = st.session_state["edit_index"]
        edit_row = df.loc[edit_i]

        new_qty = st.number_input("Quantity", value=float(edit_row["Qty"]))
        new_rate = st.number_input("Rate", value=float(edit_row["Rate"]))

        if st.button("Update Entry"):
            new_total = new_qty * new_rate
            if edit_row["Type"] == "Purchase":
                new_total = -new_total

            df.at[edit_i,"Qty"] = new_qty
            df.at[edit_i,"Rate"] = new_rate
            df.at[edit_i,"Total"] = new_total

            df.to_csv(file_name,index=False)
            del st.session_state["edit_index"]
            st.success("✅ Updated Successfully")
            st.rerun()

    # ---------- DOWNLOAD ----------
    st.download_button(
        "⬇ Download Filtered Report",
        filtered_df.to_csv(index=False),
        "filtered_report.csv",
        "text/csv",
        use_container_width=True
    )
