import streamlit as st
import pandas_datareader as web
import datetime as dt

def validticker(ticker): # checks if a ticker is valid
    try: 
        web.get_data_yahoo(symbols=ticker, start = dt.date.today() - dt.timedelta(days=5))
        return True
    except:
        return False

def portfolioPage():
    st.title("Portfolio Page")



    



