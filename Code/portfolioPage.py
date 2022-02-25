import streamlit as st
import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from metrics import yfmetrics
from userportfolio import userPortfolio, userData
def portfolioPage():
    st.title("Portfolio Page")
    st.header("Stock Portfolio")

    a, b, c = st.columns(3)
    
    # Search stocks
    ticker = a.text_input("Enter ticker: ", value = 'AAPL',key = "1",) # Search ticker
    price = b.text_input("Enter price: ", value = float(yfmetrics(ticker).currprice().strip("USD")),key = "1",) # Search ticker
    quantity = c.text_input("Enter quantity: ", value = 1,key = "1",) # Search ticker

    d, e = st.columns(2)
    buy = d.button("Buy")
    sell = e.button("Sell")

    portfolio = userPortfolio("nurul123")
    balance = userData("nurul123")

    if validticker(ticker):
        if buy:
            portfolio.buyStock(ticker, float(price), float(quantity))
            portfolio.updateStocks()
        if sell:
            portfolio.sellStock(ticker, float(price), float(quantity))
            portfolio.updateStocks()
    else: 
        st.write("Invalid ticker")
    
    f,g = st.columns([4,1])
    f.plotly_chart(allstocks(portfolio.portfolio), use_container_width=True)
    
    g.metric(label = "", value = " ")
    g.metric(label = "", value = " ")
    g.metric(label = "Deposit", value = "£" + (str(balance.view_user_deposit())))
    g.metric(label = "Balance", value = "£" + (str(balance.view_user_balance())))
    g.metric(label = "Portfolio Value", value = "£" + (str(balance.portfolio_assets())))    
    g.metric(label = "Return on Investment", value = (str(balance.roi())))
    deposit = g.number_input('Deposit Money:', min_value=10, value=500, step=50) # Used for changing plot time scale in days
    balance.add_deposit(deposit)
    g.subheader("Recent Transactions: ")
    for i in balance.transaction_history()[::-1]:
        g.text(i)
    
    f,g = st.columns([3 ,2])
    f.plotly_chart(portratio(portfolio.portfolio), use_container_width=True)
    g.write(portfolio.portfolio)
   # g.plotly_chart(displayPortfolio(portfolio.portfolio), use_container_width=True)

def validticker(ticker): # checks if a ticker is valid
    if yf.Ticker(ticker).info['regularMarketPrice'] == None:
        return False
    else:
        return True

def displayPortfolio(df):
    fig = go.Figure(data=[go.Table(      
        columnwidth = [80,400],
        header=dict(values=['Ticker', 'Invested', 'Average Price', 'Quantity', 'Current Price', 'Net Gain/Loss', 'Change'], height = 50,
                    align='left', fill_color='white', font=dict(color='black', size=25)),
        cells=dict(values=[df.index, df.invested, df.average_price, df.quantity, df.currprice, df['net+-'], df.change], height = 30,
                align='left', fill_color='white', font=dict(color='black', size=20)))
    ])
    fig.update_layout(height = 400)
    return fig  

def allstocks(portfolio, timescale = 999):
    fig = go.Figure()

    for ticker in portfolio.index:
        price = yf.Ticker(ticker).history(start = dt.date.today()-dt.timedelta(days = timescale))["Close"]
        volume = yf.Ticker(ticker).history(start = dt.date.today()-dt.timedelta(days = timescale))["Volume"]
        price.dropna(inplace = True)
        fig.add_trace(
        go.Scatter(
                x=price.index,
                y=price, 
                name = ticker
            ))
        
        fig.add_trace(
        go.Bar(
            x=volume.index,
            y=volume/100000,
            name = ticker
        ))
        
        fig.add_hline(y=portfolio.at[ticker, "average_price"], line_dash = "dot", annotation_text = ticker)
    
    fig.update_layout(xaxis_title="Date", yaxis_title="Price", height = 1000)
    return fig

def portratio(portfolio):
    labels = portfolio.index
    values = portfolio.quantity*portfolio.average_price
    fig = px.pie(labels, values = values, names = labels)
    fig.update_layout(xaxis_title="Date", yaxis_title="Price", height = 1000)
    return fig