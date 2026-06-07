import streamlit as st
from bank import Bank
import pandas as pd

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
        "Deposit",
        "withdraw",
        "Transaction History",
        "Update Details",
        "Delete Account",
        "Logout"
       
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
    
elif menu == "withdraw" :
    
    if st.session_state.user is None :
        st.warning("please login first")
    else :

        amount = st.number_input(
           "Enter Amount",
            min_value=1,
            key = "withdraw_amount"
        )

        if st.button("withdraw") :
            
            user = st.session_state.user

            success, result = bank.withdrawMoney(
                user["accountNo"], 
                user["pin"], amount
            )

            if success:
                st.success(result)
            else:
                st.error(result)

elif menu == "Transaction History" :

    if st.session_state.user is None:
        st.warning("please login first")
    else :
        user = st.session_state.user
        st.header("Transaction History")
        transactions = user["transactions"]

        if len(transactions) == 0:
            st.info("No transaction found")
        else:
            df = pd.DataFrame(transactions)
            st.table(df)


elif menu == "Update Details":

    if st.session_state.user is None:
        st.warning("please login first")

    else:
        st.header("update detail")
        user = st.session_state.user
        new_name = st.text_input(
             "Name",
              value = user["name"]
        )
        new_email = st.text_input(
            "Email", 
            value = user["email"]
        )
        new_pin = st.text_input(
            "New pin(leave blank if no change)",
            type = "password"
        )

        if st.button("Update Details"):

            success, result = bank.updateDetails(
                user["accountNo"],
                user["pin"],
                new_name, new_email, new_pin if new_pin else None
            )

            if success:

                st.session_state.user["name"] = new_name
                st.session_state.user["email"] = new_email
                
                if new_pin:
                    st.session_state.user["pin"] = str(new_pin)

                    st.success(result);

            else :
                    st.error(result)

elif menu == "Delete Account":

    if st.session_state.user is None:

        st.warning("please login first")

    else :

        st.header("Delete Account")

        st.error(
            "⚠️ This action cannot be undone!"
        )

        confirm = st.checkbox(
            "I understand that my account will be permanently deleted"
        )

        if confirm:

            st.warning(
                "press delete only if you are sure"
            )

            if st.button("Delete Account"):
                user = st.session_state.user

                sucess, result = bank.deleteAccount(
                    user["accountNo"], 
                    user["pin"]
                )

                if sucess:
                    st.session_state.user = None
                    st.success(
                        "Account deleted sucessfully"
                    )

                else:
                    st.error(result)




elif  menu == "Logout":
    if st.session_state.user is None:
        st.warning("no user is logged in")
    else:
        st.warning("Are you sure you want to logout?")

        if st.button("yes, Logout"):

          st.session_state.user = None
          st.success("Logged out sucessfully!")



