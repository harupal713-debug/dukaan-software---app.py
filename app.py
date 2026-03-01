import streamlit as st

st.title("SACHIN AATA CHHAKI")

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

qty = st.text_input("Quantity (kg)", placeholder="kg likhe")
rate = st.text_input("Rate per kg", placeholder="rate likhe")

if qty != "" and rate != "":
    try:
        total = float(qty) * float(rate)
        total = round(total, 2)

        if "खरीद" in menu:
            st.error(f"देना है: ₹{total}")
        else:
            st.success(f"लेना है: ₹{total}")

    except:
        st.error("सही नंबर लिखें")
