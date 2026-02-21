app.py
import streamlit as st

st.title("DUKAAN MANAGEMENT SOFTWARE")

menu = st.selectbox("Kaunsa kaam?", [
    "Gehun kharidna",
    "Aata bechna",
    "Sarso kharidna",
    "Oil bechna",
    "Pisai / Oil Charge (₹60 per kg)"
])

qty = st.number_input("Quantity (kg)", min_value=0.0)
rate = st.number_input("Rate per kg", min_value=0.0)

if st.button("Calculate"):

    if menu == "Pisai / Oil Charge (₹60 per kg)":
        total = qty * 60
        st.success(f"Lena hai: ₹{total}")
    else:
        total = qty * rate
        if "kharid" in menu:
            st.error(f"Dena hai: ₹{total}")
        else:
            st.success(f"Lena hai: ₹{total}")
