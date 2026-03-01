import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("SACHIN AATA CHHAKI - DUKAAN MANAGEMENT")

file_name = "dukaan_data.csv"

# ===== SAFE FLOAT FUNCTION =====
def to_float(value):
    try:
        return float(value)
    except:
        return None

# ===== MENU =====
menu = st.selectbox("Kaunsa kaam?", [
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

# ===== PAYMENT MODE =====
payment_mode = st.selectbox("Payment Mode", [
    "Cash",
    "Online",
    "Udhar"
])

# ===== INPUT =====
qty = st.text_input("Quantity (kg)")
rate = st.text_input("Rate per kg")

qty_float = to_float(qty)
rate_float = to_float(rate)

# ===== LIVE TOTAL =====
if qty_float is not None and rate_float is not None:
    total = round(qty_float * rate_float, 2)

    if "खरीद" in menu:
        st.markdown(f"<h3 style='color:red;'>देना है: ₹ {total}</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3 style='color:green;'>लेना है: ₹ {total}</h3>", unsafe_allow_html=True)

# ===== SAVE BUTTON =====
if st.button("Save Entry"):

    st.write("Button Clicked ✅")   # Debug line

    if qty_float is None or rate_float is None:
        st.error("❌ Quantity aur Rate sahi number me likho")
    else:

        total = round(qty_float * rate_float, 2)

        if "खरीद" in menu:
            entry_type = "Dena"
            signed_total = -total
        else:
            entry_type = "Lena"
            signed_total = total

        today = datetime.now().strftime("%d-%m-%Y")

        new_entry = pd.DataFrame([{
            "Date": today,
            "Item": menu,
            "Qty": qty_float,
            "Rate": rate_float,
            "Payment": payment_mode,
            "Type": entry_type,
            "Total": signed_total
        }])

        # Force proper columns
        columns = ["Date","Item","Qty","Rate","Payment","Type","Total"]
        new_entry = new_entry[columns]

        try:
            if os.path.exists(file_name):
                new_entry.to_csv(file_name, mode="a", header=False, index=False)
            else:
                new_entry.to_csv(file_name, index=False)

            st.success("✅ Entry Saved Successfully!")

        except Exception as e:
            st.error(f"Save error: {e}")

# ===== SHOW DATA =====
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
    st.subheader("All Entries")
    st.dataframe(df)
