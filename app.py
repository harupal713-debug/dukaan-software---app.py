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

qty = st.number_input("Quantity (kg)", min_value=0.0, step=0.01)
rate = st.number_input("Rate per kg", min_value=0.0, step=0.01)

total = qty * rate
total = round(total, 2)

if "खरीद" in menu:
    st.error(f"देना है: ₹{total}")
else:
    st.success(f"लेना है: ₹{total}")
