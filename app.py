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

        formatted_total = f"{total:,.2f}"

        if "खरीद" in menu:
            st.markdown(
                f"<h2 style='color:red;'>देना है: ₹ {formatted_total}</h2>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<h2 style='color:green;'>लेना है: ₹ {formatted_total}</h2>",
                unsafe_allow_html=True
            )

    except:
        st.error("सही नंबर लिखें")
