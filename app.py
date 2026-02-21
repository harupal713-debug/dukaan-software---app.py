
import streamlit as st

st.title("SACHIN AATA CHHAKI")

menu = st.selectbox("Kaunsa kaam?", [
    "गेहू खरीदा ",
    "आटा pisai ",
    "आटा सैल ",  
    "sarso तेल सैल ",
    "sars pisai",
    "sarso खरीद ",])

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
