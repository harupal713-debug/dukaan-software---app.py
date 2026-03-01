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

# ---------- Load ----------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Date","Item","Qty","Rate","Payment","Type","Total"])

# ---------- ENTRY ----------
st.markdown("## ➕ New Entry")

col1,col2,col3 = st.columns(3)

with col1:
    menu = st.selectbox("Item",[
        "गेहू खरीदा","आटा पिसाई","आटा बेचा",
        "सरसों तेल बेचा","सरसों पिसाई","सरसों खरीदी",
        "चावल खरीदा","सरसों खल बेची","चावल बेचा",
        "⚡ बिजली बिल","🛠 दुकान खर्च","♻ रद्दी बेची","➕ Other Income"
    ])

with col2:
    payment_mode = st.selectbox("Payment",["Cash","Online","Udhar"])

with col3:
    qty = st.text_input("Quantity")

rate = st.text_input("Rate")

qty_float = to_float(qty)
rate_float = to_float(rate)

if qty_float and rate_float:
    total_preview = round(qty_float * rate_float,2)
    if "खरीद" in menu or "बिल" in menu or "खर्च" in menu:
        st.markdown(f"<h3 style='color:red;'>देना है ₹ {total_preview}</h3>",unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color:green;'>लेना है ₹ {total_preview}</h3>",unsafe_allow_html=True)

# ---------- SAVE ----------
if st.button("💾 Save Entry",use_container_width=True):

    if qty_float is None or rate_float is None:
        st.error("Number sahi likho")
    else:
        total = round(qty_float * rate_float,2)

        if "खरीद" in menu or "बिल" in menu or "खर्च" in menu:
            signed_total = -total
            entry_type = "Expense"
        else:
            signed_total = total
            entry_type = "Income"

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": menu,
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved ✅")
        st.rerun()

# ---------- PROCESS ----------
if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"])
    df["Qty"] = pd.to_numeric(df["Qty"])
    df["Total"] = pd.to_numeric(df["Total"])

    st.markdown("---")
    st.markdown("## 🔍 Filter")

    filter_type = st.selectbox("Period",["All","Day","Month","Year"])

    filtered_df = df.copy()

    if filter_type=="Day":
        day = st.date_input("Select Day")
        filtered_df = df[df["Date"].dt.date==day]

    elif filter_type=="Month":
        m = st.selectbox("Month",range(1,13))
        y = st.selectbox("Year",df["Date"].dt.year.unique())
        filtered_df = df[(df["Date"].dt.month==m)&(df["Date"].dt.year==y)]

    elif filter_type=="Year":
        y = st.selectbox("Year",df["Date"].dt.year.unique())
        filtered_df = df[df["Date"].dt.year==y]

    # ---------- SUMMARY ----------
    st.markdown("## 📊 Summary")

    total_income = filtered_df[filtered_df["Total"]>0]["Total"].sum()
    total_expense = abs(filtered_df[filtered_df["Total"]<0]["Total"].sum())
    net = filtered_df["Total"].sum()

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Income",f"₹ {total_income:,.2f}")
    c2.metric("Total Expense",f"₹ {total_expense:,.2f}")
    c3.metric("Net Profit",f"₹ {net:,.2f}")

    # ---------- TIJORI ----------
    st.markdown("## 💰 Daily Tijori")

    cash_income = filtered_df[(filtered_df["Payment"]=="Cash") & (filtered_df["Total"]>0)]["Total"].sum()
    cash_expense = abs(filtered_df[(filtered_df["Payment"]=="Cash") & (filtered_df["Total"]<0)]["Total"].sum())
    closing_cash = cash_income - cash_expense

    c4,c5,c6 = st.columns(3)
    c4.metric("Cash Aaya",f"₹ {cash_income:,.2f}")
    c5.metric("Cash Gaya",f"₹ {cash_expense:,.2f}")
    c6.metric("Tijori Closing",f"₹ {closing_cash:,.2f}")

    # ---------- ITEM WISE ----------
    st.markdown("## 📦 Item Wise Detail")
    st.dataframe(filtered_df.groupby("Item")[["Qty","Total"]].sum().reset_index(),use_container_width=True)

    # ---------- ENTRIES ----------
    st.markdown("## 📋 All Entries")

    for index,row in df.iterrows():

        col1,col2,col3 = st.columns([6,1,1])

        with col1:
            color="green" if row["Total"]>0 else "red"
            st.markdown(f"{row['Date'].date()} | {row['Item']} | ₹ <span style='color:{color}'>{row['Total']}</span>",unsafe_allow_html=True)

        with col2:
            if st.button("✏️",key=f"edit{index}"):
                st.session_state["edit"]=index

        with col3:
            if st.button("❌",key=f"del{index}"):
                df=df.drop(index).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.rerun()

    # ---------- FULL EDIT ----------
    if "edit" in st.session_state:

        st.markdown("## ✏️ Edit Entry")

        i=st.session_state["edit"]
        row=df.loc[i]

        new_date = st.date_input("Date",row["Date"])
        new_item = st.text_input("Item",row["Item"])
        new_qty = st.number_input("Qty",value=float(row["Qty"]))
        new_rate = st.number_input("Rate",value=float(row["Rate"]))
        new_payment = st.selectbox("Payment",["Cash","Online","Udhar"],index=["Cash","Online","Udhar"].index(row["Payment"]))

        if st.button("Update"):

            new_total = new_qty*new_rate

            if row["Total"]<0:
                new_total = -abs(new_total)

            df.at[i,"Date"]=new_date
            df.at[i,"Item"]=new_item
            df.at[i,"Qty"]=new_qty
            df.at[i,"Rate"]=new_rate
            df.at[i,"Payment"]=new_payment
            df.at[i,"Total"]=new_total

            df.to_csv(file_name,index=False)
            del st.session_state["edit"]
            st.success("Updated ✅")
            st.rerun()

    # ---------- DOWNLOAD ----------
    st.download_button("⬇ Download Report",
                       filtered_df.to_csv(index=False),
                       "report.csv",
                       "text/csv",
                       use_container_width=True)
