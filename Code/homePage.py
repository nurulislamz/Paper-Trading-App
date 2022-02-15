import streamlit as st
import datetime as dt # to get dates
import plotly.graph_objects as go  # used to plot data
from plotly.subplots import make_subplots
import streamlit as st
import yfinance as yf

def marketgraph(timescale):
    SP500 = yf.Ticker("^GSPC").history(start = dt.date.today()-dt.timedelta(days = timescale))
    SP500.dropna(inplace = True)
    
    fig = make_subplots(rows=2, cols=1, subplot_titles = ("Price", "Volume"))
    
    fig.append_trace(
    go.Scatter(
        x=SP500.index,
        y=SP500["Close"],
        name = "sp500",
    ),row = 1, col = 1)
    

    fig.append_trace(
    go.Bar(
        x=SP500.index,
        y=SP500['Volume']/100000,
        name = "volume"
    ),row = 2, col = 1)
        
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    fig.update_layout(title = "SP500", height = 1000)
    
    return fig

def marketreturngraph(timescale):
    SP500 = yf.Ticker("^GSPC").history(start = dt.date.today()-dt.timedelta(days = timescale))
    SP500['daily_return'] = (SP500['Close']/ SP500['Close'].shift(1)) - 1
    SP500['daily_volume'] = (SP500['Volume']/ SP500['Volume'].shift(1)) - 1
    SP500.dropna(inplace=True)

    fig = make_subplots(rows=2, cols=1, subplot_titles = ("Daily Return", "Daily % Volume"))
    
    fig.append_trace(
    go.Scatter(
        x=SP500.index,
        y=SP500["daily_return"],
        name = "sp500",
    ),row = 1, col = 1)
    

    fig.append_trace(
    go.Bar(
        x=SP500.index,
        y=SP500['daily_volume']/100000,
        name = "volume"
    ),row = 2, col = 1)
        
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    fig.update_layout(title = "SP500", height = 1000)
    
    return fig

def homePage():
    st.title("Nurul's DataScience Stonks Project")
    st.write("Use the buttons on the left hand side to navigate to the relevant sections.")
   
    st.plotly_chart(marketgraph(150))
    st.plotly_chart(marketreturngraph(150))
