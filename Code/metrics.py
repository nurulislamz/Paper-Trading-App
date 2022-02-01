import yfinance as yf
import datetime as dt
from bs4 import BeautifulSoup
import requests
import pandas as pd

def finvizmetrics(ticker):
    metrics = ['52W High', '52W Low', '52W Range', 'Beta', 'Change', 'Current Ratio', 'Recom',
                 'Debt/Eq', 'Dividend %', 'EPS next 5Y', 'EPS this Y', 'EPS (ttm)', 'Earnings',
                 'Forward P/E', 'Gross Margin', 'Income', 'Insider Own', 'Insider Trans', 'Inst Own',
               'Inst Trans', 'Market Cap', 'Oper. Margin', 'P/B', 'P/E', 'P/FCF', 'P/S', 'PEG', 'Perf Month',
                 'Perf Quarter', 'Perf Week', 'Perf Year', 'Price', 'Profit Margin', 'Quick Ratio', 
                 'ROA', 'ROE', 'ROI', 'RSI (14)', 'SMA20', 'SMA200', 'SMA50', 'Sales', 'Short Float',
                 'Short Ratio', 'Shs Outstand', 'Target Price', 'Volatility', 'Volume']


    metric_table = pd.Series(index=metrics, dtype='float64')

    finwiz_url = 'https://finviz.com/quote.ashx?t=' + "aapl"

    r = requests.get(url=finwiz_url,headers={'user-agent': 'my-app/0.0.1'}).text
    html = BeautifulSoup(r, features="lxml")

    for metric in metrics:
        metric_label = html.find(text=metric)
        metric_value = metric_label.find_next('td',{'class':'snapshot-td2'}).text
        metric_table[metric_label] = metric_value    

    metric_table.loc["52 Week High abs"] = metric_table["52W Range"].split()[0]
    metric_table.loc["52 Week Low abs"]  = metric_table["52W Range"].split()[2]

    return metric_table

def ratings(ticker):
    finwiz_url = 'https://finviz.com/quote.ashx?t=' + ticker

    r = requests.get(url=finwiz_url,headers={'user-agent': 'my-app/0.0.1'}).text
    html = BeautifulSoup(r, features="lxml")
    ratings_table = html.find('table', {'class',"fullview-ratings-outer"})

    positive_ratings = len(ratings_table.find_all(text="Outperform")) + len(ratings_table.find_all(text="Buy")) + len(ratings_table.find_all(text="Overweight")) + len(ratings_table.find_all(text="Strong Buy"))
    negative_ratings = len(ratings_table.find_all(text="Sell")) + len(ratings_table.find_all(text="Underperform")) + len(ratings_table.find_all(text="Underweight")) + len(ratings_table.find_all(text="Strong Sell"))
    neutral_ratings = len(ratings_table.find_all(text="Neutral")) + len(ratings_table.find_all(text="Hold"))

    return (positive_ratings, negative_ratings, neutral_ratings)

def insider(ticker):
    finwiz_url = 'https://finviz.com/quote.ashx?t=' + ticker

    table = pd.DataFrame()

    r = requests.get(url=finwiz_url,headers={'user-agent': 'my-app/0.0.1'}).text
    html = BeautifulSoup(r, features="lxml")
    insider_table = html.find('table', {'class',"body-table"})

    insider_sell = len(insider_table.find_all(text = 'Sale'))
    insider_buy = len(insider_table.find_all(text = 'Buy'))

    return (insider_sell, insider_buy)
class yfmetrics:
    def __init__(self,ticker):
        self.ticker = ticker
        self.data = yf.Ticker(ticker)
        self.history = self.data.history(start = dt.date.today()-dt.timedelta(days=5))
        
    def currvolume(self):
        return str(round((self.history['Volume'][-1]/1000000),2)) + "M"
                    
    def currprice(self):
        return str(round((self.history['Close'][-1]),2)) + "USD"

    def deltaprice(self):
        data = self.history['Close']
        delta = str(round(data[-1]-data[-2],2))
        percentage = str(round((((data[-1]/data[-2])-1)*100),2)) + "%"
        return delta + " (" + percentage +")"
    
    def deltaprice(self):
        data = self.history['Close']
        delta = str(round(data[-1]-data[-2],2)) + "M"
        percentage = str(round((((data[-1]/data[-2])-1)*100),2)) + "%"
        return delta + " (" + percentage +")"

    def deltavolume(self):
        data = self.history['Volume']
        delta = str(round((data[-1]-data[-2])/1000000,2))
        percentage = str(round((((data[-1]/data[-2])-1)*100),2)) + "%"
        return delta + " (" + percentage +")"
    
    def summary(self):
        return self.data.info['longBusinessSummary']

    def tickerTocompany(self):
        return self.data.info['longName']
