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
        st.markdown(f"<h2 style='color:red;'>देना है: ₹ {total:,.2f}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:green;'>लेना है: ₹ {total:,.2f}</h2>", unsafe_allow_html=True)

elif qty != "" or rate != "":
    st.warning("सही नंबर लिखें")

# ===== SAVE ENTRY =====
if st.button("Save Entry"):

    if qty_float is None or rate_float is None:
        st.error("Quantity aur Rate sahi number me likho")

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

        columns = ["Date","Item","Qty","Rate","Payment","Type","Total"]
        new_entry = new_entry[columns]

        try:
            if os.path.exists(file_name):
                old_df = pd.read_csv(file_name)
                full_df = pd.concat([old_df, new_entry], ignore_index=True)
                full_df.to_csv(file_name, index=False)
            else:
                new_entry.to_csv(file_name, index=False)

            st.success("✅ Entry Saved Successfully!")

        except Exception as e:
            st.error(f"Save Error: {e}")

# ===== LOAD DATA =====
if os.path.exists(file_name):

    df = pd.read_csv(file_name)

    # SAFE NUMERIC CONVERSION
    df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
    df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    st.subheader("All Entries")
    st.dataframe(df)

    # ===== SUMMARY =====
    st.subheader("Summary")

    total_qty = df["Qty"].sum()
    total_lena = df[df["Total"] > 0]["Total"].sum()
    total_dena = df[df["Total"] < 0]["Total"].sum()
    net_balance = df["Total"].sum()

    st.write("Total Quantity:", round(total_qty,2))
    st.write("Total Lena: ₹", round(total_lena,2))
    st.write("Total Dena: ₹", round(abs(total_dena),2))
    st.write("Net Balance: ₹", round(net_balance,2))

    # PAYMENT SUMMARY
    st.subheader("Payment Mode Summary")
    st.dataframe(df.groupby("Payment")["Total"].sum().reset_index())

    # DOWNLOAD
    st.download_button(
        label="Download Excel",
        data=df.to_csv(index=False),
        file_name="dukaan_data.csv",
        mime="text/csv"
    )
