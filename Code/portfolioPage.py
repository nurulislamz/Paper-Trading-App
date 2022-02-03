import streamlit as st
import datetime as dt
import yfinance as yf

def validticker(ticker): # checks if a ticker is valid
    if yf.Ticker(ticker).info['regularMarketPrice'] == None:
        return False
    else:
        return True

def portfolioPage():
    st.title("Portfolio Page")



    



