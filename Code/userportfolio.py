import pandas as pd
from metrics import yfmetrics
from usertable import userTable
import streamlit as st
import datetime as dt

class userPortfolio:
    def __init__(self, user):
        try:
            portfolio = pd.read_csv(user + "_portfolio.txt") 
        except:
            df = {'ticker': [],'invested': [],'average_price': [],'quantity': [],
                'currprice': [], 'net+-': [], 'change': []}
            portfolio = pd.DataFrame(df)
            portfolio.to_csv(user + "_portfolio.txt", index = False)
        portfolio = portfolio.set_index("ticker")
        self.portfolio = portfolio
        self.user = user
        
    def buyStock(self, ticker, price, quantity):
        if ticker not in self.portfolio.index:
            self.portfolio.loc[ticker] = 0
        investment = price*quantity
        
        if (userData(self.user).view_user_balance()) - investment < 0:
            st.write("You cannot afford this transaction. Please deposit more.")
            return self.portfolio
        self.portfolio.loc[ticker,'quantity'] += quantity
        self.portfolio.loc[ticker,'invested'] += investment
        self.portfolio.loc[ticker,'average_price'] = self.portfolio.loc[ticker]['invested']/self.portfolio.loc[ticker]['quantity']
        self.portfolio.to_csv(self.user + "_portfolio.txt")
        userData(self.user).add_transaction("Bought", ticker, price, quantity)
        userData(self.user).subtract_balance(price, quantity)
        
        return self.portfolio
        # # send transaction
    
    def sellStock(self, ticker, price, quantity):
        if ticker not in self.portfolio.index:
            st.write("do not own stock")
            return 
        withdrawal = price*quantity
        self.portfolio.loc[ticker,'quantity'] -= quantity        
        self.portfolio.loc[ticker,'invested'] -= withdrawal
        if self.portfolio.loc[ticker,'quantity'] <= 0:
              self.portfolio.loc[ticker] = 0
        else:
            self.portfolio.loc[ticker,'average_price'] = self.portfolio.loc[ticker]['invested']/self.portfolio.loc[ticker]['quantity']
        self.portfolio.to_csv(self.user + "_portfolio.txt")
        userData(self.user).add_transaction("Sold", ticker, price, quantity)
        userData(self.user).add_balance(price, quantity)
        return self.portfolio
        # send transaction
    
    def updateStocks(self): # updates the portfolio with data
        self.portfolio["currprice"] = self.portfolio.index.map(lambda ticker: float(yfmetrics(ticker).currprice().strip("USD")))
        self.portfolio["net+-"] = (self.portfolio.currprice / self.portfolio.average_price)
      #   self.portfolio["net+-"] = round(((self.portfolio["currprice"]/self.portfolio["average_price"])-1)*100,2).astype(str) + "%"
        self.portfolio["change"] = self.portfolio.index.map(lambda x: yfmetrics(x).deltaprice())
        self.portfolio.to_csv(self.user + "_portfolio.txt")

    def save_port(self, user): # saves portfolio data back to csv
        self.portfolio.to_csv(user + "_portfolio.txt")

class userData(userTable, userPortfolio):
    def __init__(self, user):
        userTable.__init__(self)
        userPortfolio.__init__(self, user)
        self.user = user
        
    def view_user_deposit(self):
        return self.usertable.loc[self.user,'deposit'] 
    
    def view_user_balance(self):
        return self.usertable.loc[self.user,'balance'] 
    
    def add_deposit(self, deposit):
        self.usertable.loc[self.user, 'deposit'] += deposit
        self.usertable.loc[self.user, 'balance'] += deposit
        self.usertable.to_csv("usertable.txt")
        
    def transaction_history(self):
        try:
            open("transaction_history.txt", 'r')
        except FileNotFoundError:
            open("transaction_history.txt", 'w')
            
        with open("transaction_history.txt", 'r') as f:
            transaction = f.readlines()
        if transaction == []:
            return "No transaction history."
        else:
            return [i.strip("\n") for i in transaction]
        
    def add_transaction(self, tr_type, ticker, price, quantity):
        with open("transaction_history.txt", 'a+') as f:
            query = "{date_time}: {tr_type} x{quantity} {ticker} at {price} \n".format(date_time =  dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            tr_type = tr_type, ticker = ticker, price = price, quantity = quantity)
            f.write(query)
            f.close()
            
    def add_balance(self, price, quantity):
        self.usertable.loc[self.user, 'balance'] += (price*quantity)
        self.usertable.to_csv("usertable.txt")

    def subtract_balance(self, price, quantity):
        self.usertable.loc[self.user, 'balance'] -= (price*quantity)
        self.usertable.to_csv("usertable.txt")

    def portfolio_assets(self):
        return sum(self.portfolio.average_price * self.portfolio.quantity)
        
    def roi(self):
        return (sum(self.portfolio.average_price * self.portfolio.quantity) + 
        self.usertable.loc[self.user, 'balance'])/self.usertable.loc[self.user,'deposit']