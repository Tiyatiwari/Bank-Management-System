import streamlit as st
from bank import Bank

bank = Bank()

st.title("🏦 Bank Management System")

st.header("Create Account")

name = st.text_input("Name")

age = st.number_input(
    "Age",
    min_value=18,
    step=1
)

email = st.text_input("Email")

pin = st.text_input(
    "PIN",
    type="password"
)

if st.button("Create Account"):

    success, result = bank.createAccount(
        name,
        age,
        email,
        pin
    )

    if success:

        st.success("Account Created Successfully")

        st.write("Your Account Details")

        st.json(result)

    else:

        st.error(result)