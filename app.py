import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SACHIN AATA CHHAKI", layout="wide")

DATA_FILE = "dukaan_data.csv"
USER_FILE = "users.csv"

# ---------------- INIT ----------------
if not os.path.exists(USER_FILE):
    users = pd.DataFrame({
        "username": ["admin"],
        "password": ["1234"],
        "role": ["Admin"]
    })
    users.to_csv(USER_FILE, index=False)

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Date","Customer","Category","Item",
        "Qty","Rate","Payment","Type","Total"
    ])
    df.to_csv(DATA_FILE, index=False)

users = pd.read_csv(USER_FILE)
df = pd.read_csv(DATA_FILE)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.login:

    st.title("🔐 Login System")

    menu = st.selectbox("Select", ["Login", "Signup", "Forgot Password"])

    if menu == "Login":
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = users[(users.username == u) & (users.password == p)]
            if not user.empty:
                st.session_state.login = True
                st.session_state.username = u
                st.session_state.role = user.iloc[0]["role"]
                st.success("Login Success")
                st.rerun()
            else:
                st.error("Wrong Credentials")

    elif menu == "Signup":
        new_u = st.text_input("Username")
        new_p = st.text_input("Password", type="password")

        if st.button("Create Account"):
            if new_u in users.username.values:
                st.warning("User Exists")
            else:
                users.loc[len(users)] = [new_u, new_p, "User"]
                users.to_csv(USER_FILE, index=False)
                st.success("Account Created")

    elif menu == "Forgot Password":
        u = st.text_input("Username")
        new_p = st.text_input("New Password", type="password")

        if st.button("Reset"):
            if u in users.username.values:
                users.loc[users.username == u, "password"] = new_p
                users.to_csv(USER_FILE, index=False)
                st.success("Password Reset")
            else:
                st.error("User not found")

    st.stop()

# ---------------- MAIN ----------------
st.title("🛒 SACHIN AATA CHHAKI MANAGEMENT")
st.write(f"👤 {st.session_state.username} ({st.session_state.role})")

if st.button("Logout"):
    st.session_state.login = False
    st.rerun()

# ---------------- CHANGE PASSWORD ----------------
with st.expander("Change Password"):
    old = st.text_input("Old Password", type="password")
    new = st.text_input("New Password", type="password")

    if st.button("Update Password"):
        idx = users[users.username == st.session_state.username].index[0]
        if users.at[idx, "password"] == old:
            users.at[idx, "password"] = new
            users.to_csv(USER_FILE, index=False)
            st.success("Updated")
        else:
            st.error("Wrong old password")

# ---------------- NEW ENTRY ----------------
st.subheader("➕ New Entry")

with st.form("entry", clear_on_submit=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        category = st.selectbox("Category", ["Sale","Purchase","Income","Expense"])
        item = st.selectbox("Item", ["गेहूं","आटा","तेल"])
        customer = st.text_input("Customer (Udhar Only)")

    with col2:
        payment = st.selectbox("Payment", ["Cash","Online","Udhar"])
        qty = st.number_input("Qty", min_value=0.0)
        rate = st.number_input("Rate", min_value=0.0)

    total = qty * rate

    if st.form_submit_button("Save"):

        if payment == "Udhar" and customer == "":
            st.error("Customer required for Udhar")
        else:
            if category in ["Purchase","Expense"]:
                total = -abs(total)
                ttype = "Expense"
            else:
                total = abs(total)
                ttype = "Income"

            new_row = {
                "Date": datetime.now(),
                "Customer": customer,
                "Category": category,
                "Item": item,
                "Qty": qty,
                "Rate": rate,
                "Payment": payment,
                "Type": ttype,
                "Total": total
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("Saved")
            st.rerun()

# ---------------- ITEM STOCK ----------------
st.subheader("📦 Item Wise Stock")

stock = {}

for _, row in df.iterrows():
    item = row["Item"]

    if row["Category"] == "Purchase":
        stock[item] = stock.get(item, 0) + row["Qty"]
    elif row["Category"] == "Sale":
        stock[item] = stock.get(item, 0) - row["Qty"]

stock_df = pd.DataFrame(stock.items(), columns=["Item","Stock"])
st.dataframe(stock_df, use_container_width=True)

# ---------------- UDHAR LEDGER ----------------
st.subheader("📒 Udhar Ledger")

udhar = df[df["Payment"] == "Udhar"]

for i, row in udhar.iterrows():

    with st.expander(f"{row['Date']} | {row['Customer']} | ₹{row['Total']}"):

        new_qty = st.number_input("Qty", value=float(row["Qty"]), key=f"uq{i}")
        new_rate = st.number_input("Rate", value=float(row["Rate"]), key=f"ur{i}")

        if st.button("Update", key=f"u{i}"):

            total = new_qty * new_rate

            if row["Category"] in ["Purchase","Expense"]:
                total = -abs(total)
            else:
                total = abs(total)

            df.at[i,"Qty"] = new_qty
            df.at[i,"Rate"] = new_rate
            df.at[i,"Total"] = total

            df.to_csv(DATA_FILE, index=False)
            st.rerun()

        if st.button("Delete", key=f"d{i}"):

            df = df.drop(i).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

# ---------------- ALL ENTRIES ----------------
st.subheader("📝 All Entries")

for i, row in df.iterrows():

    with st.expander(f"{row['Date']} | {row['Item']} | ₹{row['Total']}"):

        new_qty = st.number_input("Qty", value=float(row["Qty"]), key=f"q{i}")
        new_rate = st.number_input("Rate", value=float(row["Rate"]), key=f"r{i}")
        new_payment = st.selectbox(
            "Payment",
            ["Cash","Online","Udhar"],
            index=["Cash","Online","Udhar"].index(row["Payment"]),
            key=f"p{i}"
        )

        if st.button("Update", key=f"up{i}"):

            total = new_qty * new_rate

            if row["Category"] in ["Purchase","Expense"]:
                total = -abs(total)
            else:
                total = abs(total)

            df.at[i,"Qty"] = new_qty
            df.at[i,"Rate"] = new_rate
            df.at[i,"Payment"] = new_payment
            df.at[i,"Total"] = total

            df.to_csv(DATA_FILE, index=False)
            st.rerun()

        if st.button("Delete", key=f"del{i}"):

            df = df.drop(i).reset_index(drop=True)
            df.to_csv(DATA_FILE, index=False)
            st.rerun()

# ---------------- DOWNLOAD ----------------
st.download_button(
    "⬇ Download Report",
    df.to_csv(index=False),
    "dukaan_report.csv",
    "text/csv"
)
