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

# SAFE FORMAT
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")

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
        st.success("Saved")
        st.rerun()

# ---------------- STOCK AUTO ----------------
st.subheader("📦 Stock Status")

stock_df = df[df["Item"].notna()].copy()

stock = {}

for i,row in stock_df.iterrows():
    name = row["Item"]
    if "खरीद" in name:
        stock[name] = stock.get(name,0) + row["Qty"]
    else:
        buy_item = name.replace("बेचा","खरीदा")
        stock[buy_item] = stock.get(buy_item,0) - row["Qty"]

stock_table = pd.DataFrame(stock.items(),columns=["Item","Stock Qty"])
st.dataframe(stock_table)

# ---------------- FILTER ----------------
st.subheader("📊 Reports")

filter_type = st.selectbox("Select Period",["All","Day","Month","Year"])

filtered = df.copy()

if filter_type=="Day":
    d = st.date_input("Select Day")
    filtered = df[df["Date"].dt.date==d]

elif filter_type=="Month":
    m = st.selectbox("Month",range(1,13))
    y = st.selectbox("Year",df["Date"].dt.year.unique())
    filtered = df[(df["Date"].dt.month==m)&(df["Date"].dt.year==y)]

elif filter_type=="Year":
    y = st.selectbox("Year",df["Date"].dt.year.unique())
    filtered = df[df["Date"].dt.year==y]

# ---------------- SUMMARY ----------------
income = filtered[filtered["Total"]>0]["Total"].sum()
expense = abs(filtered[filtered["Total"]<0]["Total"].sum())
net = filtered["Total"].sum()

col1,col2,col3 = st.columns(3)
col1.metric("Income",f"₹ {income}")
col2.metric("Expense",f"₹ {expense}")
col3.metric("Net",f"₹ {net}")

# ---------------- GRAPH ----------------
st.subheader("📈 Graph")

daily = filtered.groupby(filtered["Date"].dt.date)["Total"].sum()

plt.figure()
daily.plot(kind="bar")
st.pyplot(plt)

# ---------------- UDhar LEDGER ----------------
st.subheader("📒 Udhar Ledger")

udhar_df = df[df["Payment"]=="Udhar"]

if not udhar_df.empty:
    ledger = udhar_df.groupby("Customer")["Total"].sum().reset_index()
    st.dataframe(ledger)

# ---------------- EDIT / DELETE ----------------
st.subheader("📝 All Entries")

for i,row in df.iterrows():

    col1,col2,col3,col4 = st.columns([3,1,1,1])

    col1.write(row["Date"],row["Item"],row["Total"])

    if col2.button("Edit",key=f"edit{i}"):
        df.at[i,"Rate"]=st.number_input("New Rate",value=row["Rate"])
        df.at[i,"Total"]=df.at[i,"Qty"]*df.at[i,"Rate"]
        df.to_csv(file_name,index=False)
        st.rerun()

    if col3.button("Delete",key=f"del{i}"):
        df = df.drop(i)
        df.to_csv(file_name,index=False)
        st.rerun()

# ---------------- DOWNLOAD ----------------
st.download_button(
    "⬇ Download Excel",
    df.to_csv(index=False),
    "dukaan_report.csv",
    "text/csv"
)
