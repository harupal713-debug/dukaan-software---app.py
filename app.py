import streamlit as st

st.title("SACHIN AATA CHHAKI")

menu = st.selectbox("Kaunsa kaam?", [
    "गेहू खरीदा",
    "आटा पिसाई",
    "आटा सेल",
    "सरसों तेल सेल",
    "सरसों पिसाई",
    "सरसों खरीद"
])

qty = st.text_input("Quantity (kg)")
rate = st.text_input("Rate per kg")

if qty and rate:
    try:
        qty = float(qty)
        rate = float(rate)

        total = qty * rate
        total = round(total, 2)

        if "खरीद" in menu:
            st.error(f"देना है: ₹{total}")
        else:
            st.success(f"लेना है: ₹{total}")

    except:
        st.error("सही नंबर लिखें")
