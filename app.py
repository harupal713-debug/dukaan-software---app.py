import streamlit as st

st.title("SACHIN AATA CHHAKI")

menu = st.selectbox("Kaunsa kaam?", [
    "गेहू खरीदा",
    "आटा पिसाई (₹2.40/kg)",
    "आटा सेल",
    "सरसों तेल सेल",
    "सरसों पिसाई (₹2.40/kg)",
    "सरसों खरीद"
])

qty = st.number_input("Quantity (kg)", min_value=0.000)
rate = st.number_input("Rate per kg", min_value=0)

# Auto calculation
if "पिसाई" in menu:
    total = qty * 60
else:
    total = qty * rate

# Rounding system
total = round(total)

# Lena ya Dena
if "खरीद" in menu:
    st.error(f"देना है: ₹{total}")
else:
    st.success(f"लेना है: ₹{total}")
