
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

if menu == "Pisai / Oil Charge (₹60 per kg)":
    %%writefile app.py
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

if menu == "Pisai / Oil Charge (₹60 per kg)":
    total = qty * 60
else:
    %%writefile app.py
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

if menu == "Pisai / Oil Charge (₹60 per kg)":
    total = qty * 60
else:
    total = qty * rate

if "खरीद" in menu or "kharid" in menu:
    st.error(f"Dena hai: ₹{total}")
else:
    st.success(f"Lena hai: ₹{total}")

if "खरीद" in menu or "kharid" in menu:
    st.error(f"Dena hai: ₹{total}")
else:
    st.success(f"Lena hai: ₹{total}")
else:
    total = rate*price

if "खरीद" in menu or "kharid" in menu:
    st.error(f"Dena hai: ₹{total}")
else:
    st.success(f"लेना है/देना है : ₹{total}")
