import streamlit as st
import datetime as dt # to get dates
import pandas_datareader.data as web # to get yahoo finance data
import plotly.graph_objects as go  # used to plot data

def marketgraph(n):
    SP500 = web.DataReader(['sp500'], 'fred',  start = dt.date.today()-dt.timedelta(days = n), end = dt.date.today())
    SP500.dropna(inplace = True)
    
    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=SP500.index,
        y=SP500["sp500"],
        name = "sp500",
    ))
    
    fig.update_layout(title = "SP500 Price", xaxis_title="Date", yaxis_title="Price")
    
    return fig

def marketreturngraph(n):
    SP500 = web.DataReader(['sp500'], 'fred',  start = dt.date.today()-dt.timedelta(days = n), end = dt.date.today())
    SP500['daily_return'] = (SP500['sp500']/ SP500['sp500'].shift(1)) -1
    SP500.dropna(inplace=True)

    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=SP500.index,
        y=SP500["daily_return"],
        name = "sp500"
    ))
    
    fig.update_layout(title = "SP500 Return", xaxis_title="Date", yaxis_title="Price")

    return fig

def homePage():
    st.title("Nurul's DataScience Stonks Project")
    st.write("Use the buttons on the left hand side to navigate to the relevant sections.")
   
    st.plotly_chart(marketgraph(150))
    st.plotly_chart(marketreturngraph(150))

