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

qty = st.text_input("Quantity (kg)")
rate = st.text_input("Rate per kg")

if qty and rate:
    total = float(qty) * float(rate)
    total = round(total, 2)
    st.write("Total Amount: ₹", total)
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
