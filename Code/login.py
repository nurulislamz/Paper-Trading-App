import streamlit as st
import datetime as dt
import regex as re

from usertable import userTable


def login():
    st.title("Login")
    username = st.text_input("Enter Username: ", key = "1")
    password = st.text_input("Enter Password: ", type = 'password', key = "2")
    loginButton = st.button("Login", key = "3")

    if loginButton:
        username =  userTable().login_user(username, password)
        if username:
            st.text("Logged in!")
            return username
        else:
            return False
        
def signup():
    username = st.text_input("Enter Username: ", key = "1")    
    password = st.text_input("Enter Password: ", type = 'password', key = "2")

    initial_deposit = st.text_input("Enter Initial Deposit: ", value = 50000, key = "3")
   # date_start = st.text_input("Enter Date Start: ", value = dt.date.today(), key = "4")

    signup = st.button("Sign Up", key = "4")
    if signup and valid_username(username) and valid_password(password): 
        # add these data into a dictionary
        if username in userTable().usertable.index:
            st.text("Username already exists!")
        else:
            userTable().add_user(username, password, initial_deposit)
            st.text("Sign Up complete")


def valid_username(username):
    # check if password has a digit
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', username) is not None

    length_error = len(username) < 8

    if symbol_error:
        st.text("Username must have no symbols")
    if length_error:
        st.text("Username must be at least 8 characters long")

    username_ok = not( symbol_error or length_error)

    if username_ok:
        st.text("Username Accepted")
        return True

def valid_password(password):
    # check if password is correct length
    length_error = len(password) < 8

    # check if password has a digit
    digit_error = re.search(r"\d", password) is None

    # check if password has an uppercase letter
    uppercase_error = re.search(r"[A-Z]", password) is None

    if length_error:
        st.text("Password must be at least 8 characters long")
    if digit_error:
        st.text("Password must have at least 1 digit")
    if uppercase_error:
        st.text("Password must have at least 1 uppercase letter")

    if not(length_error or digit_error or uppercase_error):
        st.text("Password Accepted")
        return True

def loginPage():
    option = st.selectbox(label = "Do you have an account?", options = ["Login", "Sign Up"])
    if option == "Login":
        user = login()
        if user:
            return user
    else:
        signup()