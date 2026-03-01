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

# ---------- Entry Section ----------
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

# ---------- Live Total ----------
if qty_float is not None and rate_float is not None:
    total = round(qty_float * rate_float,2)

    if "खरीद" in menu:
        st.markdown(f"<h3 style='color:red;'>देना है: ₹ {total:,.2f}</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color:green;'>लेना है: ₹ {total:,.2f}</h3>", unsafe_allow_html=True)

# ---------- Save ----------
if st.button("💾 Save Entry", use_container_width=True):

    if qty_float is None or rate_float is None:
        st.error("❌ Quantity aur Rate sahi number me likho")
    else:
        total = round(qty_float * rate_float,2)

        if "खरीद" in menu:
            entry_type = "Purchase"
            signed_total = -total
        else:
            entry_type = "Sale"
            signed_total = total

        new_row = {
            "Date": datetime.now().strftime("%d-%m-%Y"),
            "Item": menu,
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_name,index=False)

        st.success("✅ Entry Saved Successfully")
        st.rerun()

# ---------- Show Data ----------
if not df.empty:

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    st.markdown("---")
    st.markdown("## 📋 All Entries")

    for index, row in df.iterrows():

        col1, col2 = st.columns([8,2])

        with col1:
            color = "green" if row["Total"] > 0 else "red"
            st.markdown(
                f"""
                <div style="padding:10px; border-radius:10px; background-color:#f5f5f5; margin-bottom:8px;">
                <b>{row['Date'].date()}</b> | {row['Item']} | {row['Payment']} |
                <span style='color:{color}; font-weight:bold;'>₹ {row['Total']:,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if st.button("❌", key=f"del{index}"):
                df = df.drop(index).reset_index(drop=True)
                df.to_csv(file_name,index=False)
                st.rerun()

    # ---------- Summary ----------
    st.markdown("---")
    st.markdown("## 📊 Summary")

    total_sale = df[df["Total"] > 0]["Total"].sum()
    total_purchase = abs(df[df["Total"] < 0]["Total"].sum())
    net = df["Total"].sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sale", f"₹ {total_sale:,.2f}")
    c2.metric("Total Purchase", f"₹ {total_purchase:,.2f}")
    c3.metric("Net Balance", f"₹ {net:,.2f}")

    # ---------- Download ----------
    st.download_button(
        "⬇ Download Excel",
        df.to_csv(index=False),
        "dukaan_report.csv",
        "text/csv",
        use_container_width=True
    )
