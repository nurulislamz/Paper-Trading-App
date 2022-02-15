import pandas as pd 
import datetime as dt # to get dates
import numpy as np 
import streamlit as st
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests

from portfolioPage import validticker
def statementPage():
    # Search stocks
    ticker = st.text_input("Enter ticker: ", value = 'AAPL',key = "1",) # Search ticker

    if validticker(ticker):
        st.table(incomeStatement(ticker))
        st.table(balanceSheet(ticker))
        st.table(cashflowStatement(ticker))

# historical income statements
# DATA MAY NOT LOAD ON THE FIRST TIME, try twice after waiting 3 seconds (server side issue)
def incomeStatement(ticker):
    wsj_url = "https://www.wsj.com/market-data/quotes/" + ticker + "/financials/quarter/income-statement"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    r = requests.get(url=wsj_url,headers=header) 
    html = BeautifulSoup(r.text, features="lxml")

    income_table = html.find("table", {"class", "cr_dataTable"})

    table = pd.read_html(str(income_table))
    table = table[0]
    table.index = table.iloc[:,0]
    table = table.drop(table.columns[0], axis=1)
    table = table.drop('5-qtr trend', axis=1)
    table = table.dropna()
    return table

def balanceSheet(ticker):
    wsj_url = "https://www.wsj.com/market-data/quotes/" + ticker + "/financials/quarter/balance-sheet"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    r = requests.get(url=wsj_url,headers=header) 
    html = BeautifulSoup(r.text, features="lxml")

    balance_sheet_assets = html.find("table", {"class", "cr_dataTable"})
    balance_sheet_liabilities = balance_sheet_assets.find_next("table", {"class", "cr_dataTable"})

    assets = pd.read_html(str(balance_sheet_assets))
    assets = assets[0]
    assets.index = assets.iloc[:,0]
    assets = assets.drop(assets.columns[0], axis=1)
    assets = assets.drop('5-qtr trend', axis=1)
    assets = assets.dropna()

    liabilities = pd.read_html(str(balance_sheet_liabilities))
    liabilities = liabilities[0]
    liabilities.index = liabilities.iloc[:,0]
    liabilities = liabilities.drop(liabilities.columns[0], axis=1)
    liabilities = liabilities.drop('5-qtr trend', axis=1)
    liabilities = liabilities.dropna()

    table = pd.concat([assets, liabilities], keys=['assets','liabilities'])
    return table

def cashflowStatement(ticker):
    wsj_url = "https://www.wsj.com/market-data/quotes/" + ticker + "/financials/quarter/cash-flow"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    r = requests.get(url=wsj_url,headers=header) 
    html = BeautifulSoup(r.text, features="lxml")

    cash_flow_operating = html.find("table", {"class", "cr_dataTable"})
    cash_flow_investing = cash_flow_operating.find_next("table", {"class", "cr_dataTable"})
    cash_flow_financing = cash_flow_investing.find_next("table", {"class", "cr_dataTable"})

    operating = pd.read_html(str(cash_flow_operating))
    operating = operating[0]
    operating.index = operating.iloc[:,0]
    operating = operating.drop(operating.columns[0], axis=1)
    operating = operating.drop('5-qtr trend', axis=1)
    operating = operating.dropna()

    investing = pd.read_html(str(cash_flow_investing))
    investing = investing[0]
    investing.index = investing.iloc[:,0]
    investing = investing.drop(investing.columns[0], axis=1)
    investing = investing.drop('5-qtr trend', axis=1)
    investing = investing.dropna()

    financing = pd.read_html(str(cash_flow_financing))
    financing = financing[0]
    financing.index = financing.iloc[:,0]
    financing = financing.drop(financing.columns[0], axis=1)
    financing = financing.drop('5-qtr trend', axis=1)
    financing = financing.dropna()
    
    table = pd.concat([operating, investing, financing], keys=['operating','investing', 'financing'])
    return table