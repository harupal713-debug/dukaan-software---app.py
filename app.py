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

# ---------- ENTRY TYPE ----------
st.markdown("## ➕ New Entry")

entry_category = st.selectbox("Entry Type", [
    "Product Sale / Purchase",
    "Extra Income",
    "Shop Expense",
    "Tijori In",
    "Tijori Out"
])

# ---------- PRODUCT ENTRY ----------
if entry_category == "Product Sale / Purchase":

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
        qty = st.text_input("Quantity")

    rate = st.text_input("Rate")

    qty_float = to_float(qty)
    rate_float = to_float(rate)

    if qty_float and rate_float:
        preview = qty_float * rate_float
        color = "red" if "खरीद" in menu else "green"
        text = "देना है" if "खरीद" in menu else "लेना है"
        st.markdown(f"<h3 style='color:{color};'>{text}: ₹ {preview:,.2f}</h3>", unsafe_allow_html=True)

    if st.button("💾 Save Entry", use_container_width=True):
        if qty_float is None or rate_float is None:
            st.error("Number sahi likho")
        else:
            total = qty_float * rate_float
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
            st.success("Saved ✅")
            st.rerun()

# ---------- EXTRA INCOME ----------
elif entry_category == "Extra Income":

    desc = st.text_input("Income Description (e.g. रद्दी बेचना)")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("💾 Save Income"):
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": desc,
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Extra Income",
            "Total": amount
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Income Saved ✅")
        st.rerun()

# ---------- SHOP EXPENSE ----------
elif entry_category == "Shop Expense":

    desc = st.text_input("Expense Description (e.g. बिजली बिल)")
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("💾 Save Expense"):
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": desc,
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Expense",
            "Total": -amount
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Expense Saved ✅")
        st.rerun()

# ---------- TIJORI IN ----------
elif entry_category == "Tijori In":

    amount = st.number_input("Amount Put in Tijori", min_value=0.0)

    if st.button("💾 Save"):
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": "Tijori In",
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Tijori In",
            "Total": -amount
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved ✅")
        st.rerun()

# ---------- TIJORI OUT ----------
elif entry_category == "Tijori Out":

    amount = st.number_input("Amount Taken from Tijori", min_value=0.0)

    if st.button("💾 Save"):
        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": "Tijori Out",
            "Qty": 0,
            "Rate": 0,
            "Payment": "Cash",
            "Type": "Tijori Out",
            "Total": amount
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)
        st.success("Saved ✅")
        st.rerun()

# ---------- SHOW DATA ----------
if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"])
    df["Total"] = pd.to_numeric(df["Total"])

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

        with col2:
            if st.button("✏️", key=f"edit{index}"):
                st.session_state["edit_index"] = index

        with col3:
            if st.button("❌", key=f"del{index}"):
                df = df.drop(index).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.rerun()

    # ---------- EDIT FULL ----------
    if "edit_index" in st.session_state:

        st.markdown("---")
        st.markdown("## ✏️ Edit Entry")

        i = st.session_state["edit_index"]
        row = df.loc[i]

        new_date = st.date_input("Date", value=row["Date"])
        new_item = st.text_input("Item", value=row["Item"])
        new_qty = st.number_input("Qty", value=float(row["Qty"]))
        new_rate = st.number_input("Rate", value=float(row["Rate"]))
        new_payment = st.selectbox("Payment", ["Cash","Online","Udhar"], index=0)

        if st.button("Update Entry"):
            new_total = new_qty * new_rate
            if row["Total"] < 0:
                new_total = -abs(new_total)

            df.at[i,"Date"] = new_date
            df.at[i,"Item"] = new_item
            df.at[i,"Qty"] = new_qty
            df.at[i,"Rate"] = new_rate
            df.at[i,"Payment"] = new_payment
            df.at[i,"Total"] = new_total

            df.to_csv(file_name,index=False)
            del st.session_state["edit_index"]
            st.success("Updated ✅")
            st.rerun()

    # ---------- DAILY SUMMARY ----------
    st.markdown("---")
    st.markdown("## 📊 Today Summary")

    today = datetime.now().date()
    today_df = df[df["Date"].dt.date == today]

    st.metric("Today Net", f"₹ {today_df['Total'].sum():,.2f}")
