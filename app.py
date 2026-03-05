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

# ---------------- LOAD DATA SAFELY ----------------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["Date","Item","Qty","Rate","Payment","Type","Total"])

# Ensure columns exist
required_cols = ["Date","Item","Qty","Rate","Payment","Type","Total"]
for col in required_cols:
    if col not in df.columns:
        df[col] = None

# ---------------- ENTRY TYPE ----------------
st.subheader("➕ New Entry")

entry_category = st.selectbox("Select Entry Type",[
    "Sale / Purchase",
    "Other Income / Expense",
    "Electricity Bill",
    "Shop Expense",
    "Tijori Entry"
])

# ====================================================
# 1️⃣ SALE / PURCHASE
# ====================================================
if entry_category == "Sale / Purchase":

    col1,col2,col3 = st.columns(3)

    with col1:
        item = st.selectbox("Item",[
            "गेहू खरीदा","आटा बेचा",
            "चावल खरीदा","चावल बेचा",
            "सरसों खरीदी","सरसों तेल बेचा"
        ])

    with col2:
        payment = st.selectbox("Payment Mode",["Cash","Online","Udhar"])

    with col3:
        qty = st.text_input("Quantity")

    rate = st.text_input("Rate")

    qty_f = to_float(qty)
    rate_f = to_float(rate)

    if qty_f is not None and rate_f is not None:
        preview = round(qty_f * rate_f,2)
        if "खरीद" in item:
            st.markdown(f"### 🔴 Expense: ₹ {preview}")
        else:
            st.markdown(f"### 🟢 Income: ₹ {preview}")

    if st.button("💾 Save Entry"):

        if qty_f is None or rate_f is None:
            st.error("Number sahi likho")
        else:
            total = qty_f * rate_f
            if "खरीद" in item:
                total = -abs(total)
                ttype="Expense"
            else:
                total = abs(total)
                ttype="Income"

            new_row = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Item": item,
                "Qty": qty_f,
                "Rate": rate_f,
                "Payment": payment,
                "Type": ttype,
                "Total": total
            }

            df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
            df.to_csv(file_name,index=False)
            st.success("Saved Successfully")
            st.rerun()

# ====================================================
# 2️⃣ OTHER INCOME / EXPENSE
# ====================================================
elif entry_category == "Other Income / Expense":

    custom_item = st.text_input("Write Item Name")
    amount = st.number_input("Amount",min_value=0.0)
    entry_type = st.selectbox("Income or Expense",["Income","Expense"])
    payment = st.selectbox("Payment Mode",["Cash","Online","Udhar"])

    if st.button("💾 Save Entry"):

        total = amount if entry_type=="Income" else -amount

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": custom_item,
            "Qty": 0,
            "Rate": 0,
            "Payment": payment,
            "Type": entry_type,
            "Total": total
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved Successfully")
        st.rerun()

# ====================================================
# 3️⃣ ELECTRICITY BILL
# ====================================================
elif entry_category == "Electricity Bill":

    bill_month = st.selectbox("Bill Month",[
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])

    bill_year = st.number_input("Bill Year",min_value=2020,max_value=2100,value=datetime.now().year)

    amount = st.number_input("Bill Amount",min_value=0.0)

    if st.button("💾 Save Entry"):

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": f"Electricity Bill - {bill_month} {bill_year}",
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Expense",
            "Total": -amount
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved Successfully")
        st.rerun()

# ====================================================
# 4️⃣ SHOP EXPENSE
# ====================================================
elif entry_category == "Shop Expense":

    expense_name = st.text_input("Expense Name")
    amount = st.number_input("Amount",min_value=0.0)
    payment = st.selectbox("Payment Mode",["Cash","Online"])

    if st.button("💾 Save Entry"):

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": expense_name,
            "Qty": 0,
            "Rate": 0,
            "Payment": payment,
            "Type": "Expense",
            "Total": -amount
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved Successfully")
        st.rerun()

# ====================================================
# 5️⃣ TIJORI ENTRY
# ====================================================
elif entry_category == "Tijori Entry":

    tijori_type = st.selectbox("Select",["Cash Dala","Cash Nikala"])
    amount = st.number_input("Amount",min_value=0.0)

    if st.button("💾 Save Entry"):

        total = amount if tijori_type=="Cash Dala" else -amount

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": tijori_type,
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Tijori",
            "Total": total
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved Successfully")
        st.rerun()

# ====================================================
# SUMMARY + SAFE DATE CONVERSION
# ====================================================
if not df.empty:

    df["Date"]=pd.to_datetime(df["Date"], errors="coerce")
    df=df.dropna(subset=["Date"])  # remove bad rows safely
    df["Total"]=pd.to_numeric(df["Total"], errors="coerce")

    st.markdown("---")
    st.subheader("📊 Summary")

    filter_type = st.selectbox("Select Period",["All","Day","Month","Year"])

    filtered=df.copy()

    if filter_type=="Day":
        d=st.date_input("Select Day")
        filtered=df[df["Date"].dt.date==d]

    elif filter_type=="Month":
        m=st.selectbox("Month",range(1,13))
        y=st.selectbox("Year",sorted(df["Date"].dt.year.unique()))
        filtered=df[(df["Date"].dt.month==m)&(df["Date"].dt.year==y)]

    elif filter_type=="Year":
        y=st.selectbox("Year",sorted(df["Date"].dt.year.unique()))
        filtered=df[df["Date"].dt.year==y]

    total_income=filtered[filtered["Total"]>0]["Total"].sum()
    total_expense=abs(filtered[filtered["Total"]<0]["Total"].sum())
    net=filtered["Total"].sum()

    c1,c2,c3=st.columns(3)
    c1.metric("Total Income",f"₹ {total_income:,.2f}")
    c2.metric("Total Expense",f"₹ {total_expense:,.2f}")
    c3.metric("Net Balance",f"₹ {net:,.2f}")

    st.dataframe(filtered)

    st.download_button(
        "⬇ Download Report",
        filtered.to_csv(index=False),
        "report.csv",
        "text/csv"
    )
