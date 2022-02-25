import pandas as pd
import streamlit as st

class userTable:
    def __init__(self):
        try:
            usertable = pd.read_csv("usertable.txt") 
        except:
            df = {'username': [], 'password': [], 'deposit': [], 'balance':[]}
            usertable = pd.DataFrame(df)
            usertable.to_csv("usertable.txt", index = False)
        usertable = usertable.set_index("username")
        self.usertable = usertable
            
    def save_usertable(self):
        self.usertable.to_csv("usertable.txt")
    
    def add_user(self, username, password, deposit):
        self.usertable.loc[username] = 0
        self.usertable.loc[username] = password
        self.usertable.loc[username,'deposit'] = deposit
        self.usertable.loc[username,'balance'] = deposit
        self.usertable.to_csv("usertable.txt")
    
    def login_user(self, username, password):
        username_test = username in self.usertable.index
        
        if not username_test:
            st.write("Username does not exist")
            return False
        
        password_test = any(self.usertable.loc[username] == password)
        
        if not password_test:
            st.write("Password is incorrect")
            return False
   
        if username_test and password_test:
            return username 