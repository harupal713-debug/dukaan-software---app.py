import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="SACHIN AATA CHHAKI", layout="wide")

# ---------------- PASSWORD LOGIN ----------------
PASSWORD = "1234"

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    pwd = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong Password")
    st.stop()

st.title("🛒 SACHIN AATA CHHAKI MANAGEMENT")

file_name = "dukaan_data.csv"

# ---------------- LOAD DATA ----------------
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=[
        "Date","Customer","Item","Qty","Rate",
        "Payment","Type","Total"
    ])

# SAFE CONVERT (ERROR FREE)
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce").fillna(0)
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").fillna(0)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)

# ---------------- NEW ENTRY ----------------
st.subheader("➕ New Entry")

col1,col2,col3 = st.columns(3)

with col1:
    customer = st.text_input("Customer Name (Udhar Only)")
    item = st.selectbox("Item",[
        "गेहू खरीदा","आटा बेचा",
        "चावल खरीदा","चावल बेचा",
        "सरसों खरीदी","सरसों तेल बेचा"
    ])

with col2:
    payment = st.selectbox("Payment Mode",["Cash","Online","Udhar"])

with col3:
    qty = st.number_input("Quantity",min_value=0.0)
    rate = st.number_input("Rate",min_value=0.0)

total = qty * rate

if "खरीद" in item:
    st.markdown(f"🔴 Expense: ₹ {total}")
else:
    st.markdown(f"🟢 Income: ₹ {total}")

if st.button("💾 Save Entry"):

    if payment=="Udhar" and customer=="":
        st.error("Udhar me customer naam jaruri hai")
    else:
        if "खरीद" in item:
            total = -abs(total)
            ttype="Expense"
        else:
            total = abs(total)
            ttype="Income"

        new_row = {
            "Date": datetime.now(),
            "Customer": customer,
            "Item": item,
            "Qty": qty,
            "Rate": rate,
            "Payment": payment,
            "Type": ttype,
            "Total": total
        }

        df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved Successfully")
        st.rerun()

# ---------------- STOCK AUTO ----------------
st.subheader("📦 Stock Status")

stock = {}

for _,row in df.iterrows():
    name = row["Item"]

    if "खरीद" in str(name):
        stock[name] = stock.get(name,0) + row["Qty"]
    elif "बेचा" in str(name):
        buy_name = name.replace("बेचा","खरीदा")
        stock[buy_name] = stock.get(buy_name,0) - row["Qty"]

stock_df = pd.DataFrame(stock.items(),columns=["Item","Stock Qty"])
st.dataframe(stock_df)

# ---------------- REPORT FILTER ----------------
st.subheader("📊 Reports")

filter_type = st.selectbox("Select Period",["All","Day","Month","Year"])

filtered = df.copy()

if not df.empty:

    if filter_type=="Day":
        d = st.date_input("Select Day")
        filtered = df[df["Date"].dt.date==d]

    elif filter_type=="Month":
        m = st.selectbox("Month",range(1,13))
        y = st.selectbox("Year",sorted(df["Date"].dt.year.dropna().unique()))
        filtered = df[(df["Date"].dt.month==m)&(df["Date"].dt.year==y)]

    elif filter_type=="Year":
        y = st.selectbox("Year",sorted(df["Date"].dt.year.dropna().unique()))
        filtered = df[df["Date"].dt.year==y]

# ---------------- SUMMARY ----------------
if not filtered.empty:

    income = filtered[filtered["Total"]>0]["Total"].sum()
    expense = abs(filtered[filtered["Total"]<0]["Total"].sum())
    net = filtered["Total"].sum()

    col1,col2,col3 = st.columns(3)
    col1.metric("Income",f"₹ {income:,.2f}")
    col2.metric("Expense",f"₹ {expense:,.2f}")
    col3.metric("Net Balance",f"₹ {net:,.2f}")

# ---------------- GRAPH ----------------
st.subheader("📈 Daily Graph")

if not filtered.empty:
    daily = filtered.groupby(filtered["Date"].dt.date)["Total"].sum()

    fig, ax = plt.subplots()
    daily.plot(kind="bar", ax=ax)
    st.pyplot(fig)

# ---------------- UDhar LEDGER ----------------
st.subheader("📒 Udhar Ledger")

udhar_df = df[df["Payment"]=="Udhar"]

if not udhar_df.empty:
    ledger = udhar_df.groupby("Customer")["Total"].sum().reset_index()
    st.dataframe(ledger)

# ---------------- EDIT / DELETE ----------------
st.subheader("📝 All Entries")

for i,row in df.iterrows():

    col1,col2,col3 = st.columns([5,1,1])

    col1.write(
        f"{row['Date']} | {row['Item']} | ₹ {row['Total']}"
    )

    if col2.button("✏ Edit",key=f"edit{i}"):

        new_rate = st.number_input("New Rate",value=float(row["Rate"]),key=f"rate{i}")
        new_total = row["Qty"] * new_rate

        df.at[i,"Rate"]=new_rate
        df.at[i,"Total"]=new_total

        df.to_csv(file_name,index=False)
        st.success("Updated")
        st.rerun()

    if col3.button("🗑 Delete",key=f"del{i}"):

        df = df.drop(i).reset_index(drop=True)
        df.to_csv(file_name,index=False)
        st.success("Deleted")
        st.rerun()

# ---------------- DOWNLOAD ----------------
st.download_button(
    "⬇ Download Excel",
    df.to_csv(index=False),
    "dukaan_report.csv",
    "text/csv"
)
