import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SACHIN AATA CHHAKI", layout="wide")
st.title("🛒 SACHIN AATA CHHAKI MANAGEMENT")

file_name = "dukaan_data.csv"

# ---------------- SAFE FLOAT ----------------
def to_float(val):
    try:
        return float(val)
    except:
        return None

# ---------------- LOAD DATA ----------------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Date","Item","Qty","Rate","Payment","Type","Total"])

# ---------------- NEW ENTRY ----------------
st.subheader("➕ New Entry")

col1,col2,col3 = st.columns(3)

with col1:
    item = st.selectbox("Item",[
        "गेहू खरीदा","आटा बेचा","चावल खरीदा","चावल बेचा",
        "सरसों खरीदी","सरसों तेल बेचा",
        "⚡ बिजली बिल","🛠 दुकान खर्च",
        "♻ रद्दी बेची","➕ Other Income"
    ])

with col2:
    payment = st.selectbox("Payment Mode",["Cash","Online","Udhar"])

with col3:
    qty = st.text_input("Quantity")

rate = st.text_input("Rate")

qty_f = to_float(qty)
rate_f = to_float(rate)

# ---------- LIVE TOTAL ----------
if qty_f is not None and rate_f is not None:
    preview = round(qty_f * rate_f,2)

    if "खरीद" in item or "बिल" in item or "खर्च" in item:
        st.markdown(f"### 🔴 Expense: ₹ {preview}")
    else:
        st.markdown(f"### 🟢 Income: ₹ {preview}")

# ---------- SAVE ----------
if st.button("💾 Save Entry", use_container_width=True):

    if qty_f is None or rate_f is None:
        st.error("❌ Quantity aur Rate number me likho")
    else:
        total = round(qty_f * rate_f,2)

        # Decide type automatically
        if "खरीद" in item or "बिल" in item or "खर्च" in item:
            total = -abs(total)
            entry_type = "Expense"
        else:
            total = abs(total)
            entry_type = "Income"

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": item,
            "Qty": qty_f,
            "Rate": rate_f,
            "Payment": payment,
            "Type": entry_type,
            "Total": total
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)

        st.success("✅ Entry Saved")
        st.rerun()

# ---------------- PROCESS DATA ----------------
if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    # ---------------- FILTER ----------------
    st.markdown("---")
    st.subheader("🔍 Filter")

    filter_type = st.selectbox("Select Period",["All","Day","Month","Year"])

    filtered = df.copy()

    if filter_type=="Day":
        d = st.date_input("Select Day")
        filtered = df[df["Date"].dt.date==d]

    elif filter_type=="Month":
        m = st.selectbox("Month",range(1,13))
        y = st.selectbox("Year",sorted(df["Date"].dt.year.unique()))
        filtered = df[(df["Date"].dt.month==m)&(df["Date"].dt.year==y)]

    elif filter_type=="Year":
        y = st.selectbox("Year",sorted(df["Date"].dt.year.unique()))
        filtered = df[df["Date"].dt.year==y]

    # ---------------- SUMMARY ----------------
    st.markdown("---")
    st.subheader("📊 Summary")

    total_income = filtered[filtered["Total"]>0]["Total"].sum()
    total_expense = abs(filtered[filtered["Total"]<0]["Total"].sum())
    net_profit = filtered["Total"].sum()

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Income",f"₹ {total_income:,.2f}")
    c2.metric("Total Expense",f"₹ {total_expense:,.2f}")
    c3.metric("Net Profit",f"₹ {net_profit:,.2f}")

    # ---------------- TIJORI SYSTEM ----------------
    st.subheader("💰 Cash (Tijori) Summary")

    cash_in = filtered[(filtered["Payment"]=="Cash") & (filtered["Total"]>0)]["Total"].sum()
    cash_out = abs(filtered[(filtered["Payment"]=="Cash") & (filtered["Total"]<0)]["Total"].sum())
    closing_cash = cash_in - cash_out

    c4,c5,c6 = st.columns(3)
    c4.metric("Cash Aaya",f"₹ {cash_in:,.2f}")
    c5.metric("Cash Gaya",f"₹ {cash_out:,.2f}")
    c6.metric("Tijori Closing",f"₹ {closing_cash:,.2f}")

    # ---------------- ITEM WISE ----------------
    st.subheader("📦 Item Wise Summary")
    item_summary = filtered.groupby("Item")[["Qty","Total"]].sum().reset_index()
    st.dataframe(item_summary,use_container_width=True)

    # ---------------- ALL ENTRIES ----------------
    st.markdown("---")
    st.subheader("📋 All Entries")

    for i,row in df.iterrows():

        col1,col2,col3 = st.columns([6,1,1])

        with col1:
            color="green" if row["Total"]>0 else "red"
            st.markdown(f"{row['Date'].date()} | {row['Item']} | ₹ <span style='color:{color}'>{row['Total']:,.2f}</span>",unsafe_allow_html=True)

        # EDIT BUTTON
        with col2:
            if st.button("✏️",key=f"edit{i}"):
                st.session_state["edit_index"]=i

        # DELETE BUTTON
        with col3:
            if st.button("❌",key=f"del{i}"):
                df=df.drop(i).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.rerun()

    # ---------------- FULL EDIT MODE ----------------
    if "edit_index" in st.session_state:

        st.markdown("---")
        st.subheader("✏️ Edit Entry")

        idx = st.session_state["edit_index"]
        row = df.loc[idx]

        new_date = st.date_input("Date", row["Date"])
        new_item = st.text_input("Item", row["Item"])
        new_qty = st.number_input("Quantity", value=float(row["Qty"]))
        new_rate = st.number_input("Rate", value=float(row["Rate"]))
        new_payment = st.selectbox("Payment",["Cash","Online","Udhar"],
                                   index=["Cash","Online","Udhar"].index(row["Payment"]))

        if st.button("Update Entry"):

            new_total = new_qty * new_rate

            # auto decide income or expense
            if "खरीद" in new_item or "बिल" in new_item or "खर्च" in new_item:
                new_total = -abs(new_total)
                new_type = "Expense"
            else:
                new_total = abs(new_total)
                new_type = "Income"

            df.at[idx,"Date"]=new_date
            df.at[idx,"Item"]=new_item
            df.at[idx,"Qty"]=new_qty
            df.at[idx,"Rate"]=new_rate
            df.at[idx,"Payment"]=new_payment
            df.at[idx,"Type"]=new_type
            df.at[idx,"Total"]=new_total

            df.to_csv(file_name,index=False)

            del st.session_state["edit_index"]
            st.success("✅ Updated Successfully")
            st.rerun()

    # ---------------- DOWNLOAD ----------------
    st.download_button(
        "⬇ Download Filtered Report",
        filtered.to_csv(index=False),
        "filtered_report.csv",
        "text/csv",
        use_container_width=True
    )
