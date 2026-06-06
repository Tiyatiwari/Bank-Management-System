import streamlit as st
from bank import Bank

bank = Bank()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Create Account",
        "Login",
        "Dashboard",
        "Deposit"
    ]
)
st.write(menu)


if menu == "Create Account":
    st.header("Create account")

    name = st.text_input("Name")

    age = st.number_input("age", min_value = 18, step = 1)

    email = st.text_input("Email")

    pin = st.text_input("PIN", type = "password")

    if st.button("Create Account"):
        success , result = bank.createAccount(name, age, email, pin)
        if success :
            st.success("Account created sucessfully")
            st.json(result)

        else :
            st.error(result)

elif menu == "Login":

    st.header("Login")

    accountNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type = "password")

    if st.button("Login"):
        success, result = bank.login(accountNo, pin)

        if success:
            st.session_state.user = result

            st.success(f"welcome {result['name']}")

        else :
            st.error(result)

elif menu == "Dashboard":

    if st.session_state.user is None:

        st.warning("please login first")

    else:

        user = st.session_state.user

        st.header("Dashboard")

        st.success(
            f"Welcome {user['name']}"
        )
        st.write(
            f"Account Number : {user['accountNo']}"
        )

        st.write(
            f"Email : {user['email']}"
        )
        st.write(
            f"Balance : ₹{user['balance']} "
        )

elif menu == "Deposit" :

    if st.session_state.user is None:

        st.warning("please login first")

    else:

        amount = st.number_input(
            "Enter Amount", min_value = 1
        )
        
        if st.button("Deposit"):

            user = st.session_state.user

            success, result = bank.depositMoney(
                user["accountNo"],
                user["pin"],
                amount
            )

            if success :
                

                st.success(result)
                
            else :

                st.error(result)