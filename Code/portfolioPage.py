from matplotlib import ticker
from matplotlib.style import use
import streamlit as st
import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from metrics import yfmetrics

def displayPortfolio(df):
    fig = go.Figure(data=[go.Table(      
        columnwidth = [80,400],
        header=dict(values=['Ticker', 'Invested', 'Average Price', 'Quantity'], height = 50,
                    align='left', fill_color='white', font=dict(color='black', size=25)),
        cells=dict(values=[df.index, df.invested, df.average_price, df.quantity], height = 50,
                align='left', fill_color='white', font=dict(color='black', size=20)))
    ])
    fig.update_layout(height = 1000)

    return fig  

def portfolioPage():
    st.title("Portfolio Page")
    st.header("Stock Portfolio")
    
    portfolio = readPortfolio()

    a, b, c = st.columns(3)
    
    # Search stocks
    ticker = a.text_input("Enter ticker: ", value = 'AAPL',key = "1",) # Search ticker
    price = b.text_input("Enter price: ", value = float(yfmetrics(ticker).currprice().strip("USD")),key = "1",) # Search ticker
    quantity = c.text_input("Enter price: ", value = 1,key = "1",) # Search ticker

    d, e = st.columns(2)
    buy = d.button("Buy")
    sell = e.button("Sell")

    st.plotly_chart(allstocks(999,portfolio), use_container_width=True)
    st.plotly_chart(portratio(portfolio), use_container_width=True)
    st.plotly_chart(displayPortfolio(portfolio), use_container_width=True)

    if validticker(ticker):
        if buy:
            buyPortfolio(ticker, float(price), float(quantity))
            update_port(portfolio)
            save_port(portfolio)
        elif sell:
            sellPortfolio(ticker, float(price), float(quantity))
            update_port(portfolio)
            save_port(portfolio)
        else: 
            return

def balance():
    pass

def validticker(ticker): # checks if a ticker is valid
    if yf.Ticker(ticker).info['regularMarketPrice'] == None:
        return False
    else:
        return True

# reads portfolio file if it doesnt exist, else creates one
def readPortfolio():
    try:
        portfolio = pd.read_csv("portfolio.txt") 
    except FileNotFoundError:  
        df = {'ticker': [],
               'invested': [], 
              'average_price': [],
               'quantity': []}
        portfolio = pd.DataFrame(df)
        portfolio.to_csv("portfolio.txt", index = False)
    portfolio = portfolio.set_index("ticker")
    return portfolio

portfolio = readPortfolio()

def buyPortfolio(ticker, quantity, price, portfolio = portfolio):
    if ticker not in portfolio.index:
        portfolio.loc[ticker] = 0
    investment = price*quantity
    portfolio.loc[ticker]['quantity'] += quantity
    portfolio.loc[ticker]['invested'] += investment
    portfolio.loc[ticker]['average_price'] = portfolio.loc[ticker]['invested']/portfolio.loc[ticker]['quantity']

def sellPortfolio(ticker, quantity, price, portfolio = portfolio):
    if ticker not in portfolio.index:
        print("do not own stock")
        return 
    withdrawal = price*quantity
    portfolio.loc[ticker]['quantity'] -= quantity        
    portfolio.loc[ticker]['invested'] -= withdrawal
    if portfolio.loc[ticker]['quantity'] <= 0:
          portfolio.loc[ticker] = 0
    else:
        portfolio.loc[ticker]['average_price'] = portfolio.loc[ticker]['invested']/portfolio.loc[ticker]['quantity']

def update_port(portfolio = portfolio): # updates the portfolio with data
    portfolio["currprice"] = portfolio.index.map(lambda x: float(yfmetrics(ticker).currprice().strip("USD")))
    portfolio["net+-"] = round(((portfolio.currprice/portfolio.average_price)-1)*100,2).astype(str) + "%"
    portfolio["change"] = portfolio.index.map(lambda x: yfmetrics(ticker).deltaprice())

def save_port(portfolio = portfolio): # saves portfolio data back to csv
    portfolio.to_csv("portfolio.txt")

def allstocks(timescale = 999,portfolio = portfolio):
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


def portratio(portfolio=portfolio):
    labels = portfolio.index
    values = portfolio.quantity*portfolio.average_price
    fig = px.pie(labels, values = values, names = labels)
    fig.update_layout(xaxis_title="Date", yaxis_title="Price", height = 1000)
    return fig