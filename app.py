import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SACHIN AATA CHHAKI", layout="wide")

DATA_FILE = "dukaan_data.csv"
USER_FILE = "users.csv"

# ---------------- USER SETUP ----------------
if not os.path.exists(USER_FILE):
    users = pd.DataFrame({
        "username":["admin"],
        "password":["1234"],
        "role":["Admin"]
    })
    users.to_csv(USER_FILE,index=False)

users = pd.read_csv(USER_FILE)

# ---------------- LOGIN SYSTEM ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):
        user_row = users[(users["username"]==username) & (users["password"]==password)]
        if not user_row.empty:
            st.session_state.login = True
            st.session_state.username = username
            st.session_state.role = user_row.iloc[0]["role"]
            st.rerun()
        else:
            st.error("Wrong Username or Password")

    st.stop()

# ---------------- LOAD DATA ----------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Date","Customer","Category","Item",
        "Qty","Rate","Payment","Type","Total"
    ])

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"],errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"],errors="coerce").fillna(0)
    df["Rate"] = pd.to_numeric(df["Rate"],errors="coerce").fillna(0)
    df["Total"] = pd.to_numeric(df["Total"],errors="coerce").fillna(0)

# ---------------- HEADER ----------------
st.title("🛒 SACHIN AATA CHHAKI MANAGEMENT")
st.write(f"👤 Logged in as: {st.session_state.username}")

# ---------------- CHANGE PASSWORD ----------------
with st.expander("🔐 Change Password"):
    old = st.text_input("Old Password",type="password")
    new = st.text_input("New Password",type="password")

    if st.button("Update Password"):
        idx = users[users["username"]==st.session_state.username].index[0]
        if users.at[idx,"password"] == old:
            users.at[idx,"password"] = new
            users.to_csv(USER_FILE,index=False)
            st.success("Password Updated")
        else:
            st.error("Wrong Old Password")

# ---------------- NEW ENTRY ----------------
st.subheader("➕ New Entry")

with st.form("entry",clear_on_submit=True):

    col1,col2,col3 = st.columns(3)

    with col1:
        category = st.selectbox("Category",[
            "Sale","Purchase","Income","Expense"
        ])
        item = st.selectbox("Item",[
            "गेहूं","आटा","तेल"
        ])
        customer = st.text_input("Customer (Udhar Only)")

    with col2:
        payment = st.selectbox("Payment",["Cash","Online","Udhar"])
        qty = st.number_input("Qty",min_value=0.0)
        rate = st.number_input("Rate",min_value=0.0)

    total = qty * rate

    submit = st.form_submit_button("💾 Save")

    if submit:

        if payment=="Udhar" and customer=="":
            st.error("Customer name required for Udhar")
        else:

            if category=="Purchase" or category=="Expense":
                total = -abs(total)
                ttype="Expense"
            else:
                total = abs(total)
                ttype="Income"

            new_row = {
                "Date":datetime.now(),
                "Customer":customer,
                "Category":category,
                "Item":item,
                "Qty":qty,
                "Rate":rate,
                "Payment":payment,
                "Type":ttype,
                "Total":total
            }

            df = pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
            df.to_csv(DATA_FILE,index=False)
            st.success("Saved")
            st.rerun()

# ---------------- ITEM WISE STOCK ----------------
st.subheader("📦 Item Wise Stock")

stock = {}

for _,row in df.iterrows():
    item = row["Item"]

    if row["Category"]=="Purchase":
        stock[item] = stock.get(item,0) + row["Qty"]

    elif row["Category"]=="Sale":
        stock[item] = stock.get(item,0) - row["Qty"]

stock_df = pd.DataFrame(stock.items(),columns=["Item","Stock Qty"])
st.dataframe(stock_df,use_container_width=True)

# ---------------- UDHAR LEDGER ----------------
st.subheader("📒 Udhar Ledger")

udhar = df[df["Payment"]=="Udhar"]

for i,row in udhar.iterrows():

    with st.expander(f"{row['Date']} | {row['Customer']} | ₹ {row['Total']}"):

        new_qty = st.number_input("Qty",value=float(row["Qty"]),key=f"uqty{i}")
        new_rate = st.number_input("Rate",value=float(row["Rate"]),key=f"urate{i}")

        if st.button("Update",key=f"uupdate{i}"):

            new_total = new_qty * new_rate

            if row["Category"] in ["Purchase","Expense"]:
                new_total = -abs(new_total)
            else:
                new_total = abs(new_total)

            df.at[i,"Qty"]=new_qty
            df.at[i,"Rate"]=new_rate
            df.at[i,"Total"]=new_total

            df.to_csv(DATA_FILE,index=False)
            st.rerun()

        if st.button("Delete",key=f"udelete{i}"):

            df = df.drop(i).reset_index(drop=True)
            df.to_csv(DATA_FILE,index=False)
            st.rerun()

# ---------------- ALL ENTRIES ----------------
st.subheader("📝 All Entries")

for i,row in df.iterrows():

    with st.expander(f"{row['Date']} | {row['Item']} | ₹ {row['Total']}"):

        new_qty = st.number_input("Qty",value=float(row["Qty"]),key=f"qty{i}")
        new_rate = st.number_input("Rate",value=float(row["Rate"]),key=f"rate{i}")
        new_payment = st.selectbox("Payment",
            ["Cash","Online","Udhar"],
            index=["Cash","Online","Udhar"].index(row["Payment"]),
            key=f"pay{i}"
        )

        if st.button("Update",key=f"update{i}"):

            new_total = new_qty * new_rate

            if row["Category"] in ["Purchase","Expense"]:
                new_total = -abs(new_total)
            else:
                new_total = abs(new_total)

            df.at[i,"Qty"]=new_qty
            df.at[i,"Rate"]=new_rate
            df.at[i,"Payment"]=new_payment
            df.at[i,"Total"]=new_total

            df.to_csv(DATA_FILE,index=False)
            st.rerun()

        if st.button("Delete",key=f"delete{i}"):

            df = df.drop(i).reset_index(drop=True)
            df.to_csv(DATA_FILE,index=False)
            st.rerun()

# ---------------- DOWNLOAD ----------------
st.download_button(
    "⬇ Download Excel",
    df.to_csv(index=False),
    "dukaan_report.csv",
    "text/csv"
)
