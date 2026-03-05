import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

# SAFE CONVERT
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce").fillna(0)
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce").fillna(0)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)

# ---------------- NEW ENTRY FORM ----------------
st.subheader("➕ New Entry")

with st.form("entry_form", clear_on_submit=True):

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

    submit = st.form_submit_button("💾 Save Entry")

    if submit:

        if payment=="Udhar" and customer=="":
            st.error("Udhar me customer naam jaruri hai")
        else:
            total = qty * rate

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

# ---------------- STOCK ----------------
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

# ---------------- UDhar Ledger FULL DETAIL ----------------
st.subheader("📒 Udhar Ledger Full Detail")

udhar_df = df[df["Payment"]=="Udhar"]

if not udhar_df.empty:

    for i,row in udhar_df.iterrows():

        col1,col2,col3 = st.columns([6,1,1])

        col1.write(
            f"{row['Date']} | {row['Customer']} | {row['Item']} | "
            f"Qty: {row['Qty']} | Rate: {row['Rate']} | ₹ {row['Total']}"
        )

        if col2.button("✏ Edit",key=f"uedit{i}"):

            df.at[i,"Rate"] = row["Rate"]
            df.at[i,"Total"] = row["Qty"] * row["Rate"]
            df.to_csv(file_name,index=False)
            st.rerun()

        if col3.button("🗑 Delete",key=f"udel{i}"):

            df = df.drop(i).reset_index(drop=True)
            df.to_csv(file_name,index=False)
            st.rerun()

# ---------------- ALL ENTRIES ----------------
st.subheader("📝 All Entries")

for i,row in df.iterrows():

    with st.expander(f"{row['Date']} | {row['Item']} | ₹ {row['Total']}"):

        new_customer = st.text_input("Customer",value=row["Customer"],key=f"cust{i}")
        new_qty = st.number_input("Qty",value=float(row["Qty"]),key=f"qty{i}")
        new_rate = st.number_input("Rate",value=float(row["Rate"]),key=f"rate{i}")
        new_payment = st.selectbox("Payment",
                                   ["Cash","Online","Udhar"],
                                   index=["Cash","Online","Udhar"].index(row["Payment"]),
                                   key=f"pay{i}")

        if st.button("💾 Update",key=f"update{i}"):

            new_total = new_qty * new_rate

            if "खरीद" in row["Item"]:
                new_total = -abs(new_total)
            else:
                new_total = abs(new_total)

            df.at[i,"Customer"]=new_customer
            df.at[i,"Qty"]=new_qty
            df.at[i,"Rate"]=new_rate
            df.at[i,"Payment"]=new_payment
            df.at[i,"Total"]=new_total

            df.to_csv(file_name,index=False)
            st.success("Updated")
            st.rerun()

        if st.button("🗑 Delete",key=f"delete{i}"):

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
