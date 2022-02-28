from turtle import width
import pandas as pd 
import datetime as dt # to get dates
import yfinance as yf
import numpy as np 
import streamlit as st
import plotly.graph_objects as go

import news
from portfolioPage import validticker
from metrics import finvizmetrics, yfmetrics
from twitter import dfTweets
from metricButtons import metricButtons

# runs when searchPage is chosen
def searchPage():
    
    st.title("Search Page")
    st.header("Stock Graph and Metrics")
    
    a, b = st.columns(2)

    # Search stocks
    ticker = a.text_input("Enter ticker: ", value = 'AAPL',key = "1",) # Search ticker
    n = b.number_input('Days:', min_value=7, max_value=9999, value=999, step=1) # Used for changing plot time scale in days

    # Select which news/twitter source
    news_source = st.sidebar.selectbox(label = "News Source", options = ["Finviz", "Wall Street Journal", "Market Watch", "Forbes"])
    tweets_source = st.sidebar.selectbox(label = "Tweets Source: ", options = ["General Tweets", "Stock-ticker Tweets", "Verified Tweets", "News Tweets"])
    time_scale = None
    tweets_news = None

    if tweets_source == "News Tweets":
        tweets_news = st.sidebar.selectbox(label = "Tweet News: ", options =  ['CNBC','Benzinga', 'Stocktwits', '@MorningstarInc', 'FinancialTimes','WSJMarkets','MarketWatch', 'YahooFinance'])
    if tweets_source == "Stock-ticker Tweets":
        time_scale = st.sidebar.selectbox(label = "Type: ", options = ["Recent Tweets", 'Popular Tweets'])

    # Checks if the ticker is valid
    c,d = st.columns([4,1])
    if validticker(ticker):
        metrics1 = yfmetrics(ticker)  # Creates yahoo metrics 
        metrics2 = finvizmetrics(ticker) # Creates finviz metrics
        c.plotly_chart(stockplot(ticker, n), use_container_width = True) # Creates plot
    else: # Exits out of function if invalid
        st.write("Invalid ticker, try again.")
        st.image("stock image.png", caption="stonk")
        return 0
    
    
    d.metric(label = "", value = " ")
    d.metric(label = "", value = " ")
    d.metric(label = "Current Price", value = (str(metrics1.currprice())), delta = metrics1.deltaprice())
    d.metric(label = "Volume", value = metrics1.currvolume(), delta = metrics1.deltavolume())
    d.metric(label = "Earnings Date", value = metrics2['Earnings'])
    d.metric(label = "Market Cap", value = metrics2['Market Cap'])
    d.metric(label = "52 Week Range", value = metrics2['52W Range'])
    d.metric(label = "Insider Ownership", value = metrics2['Insider Own'], delta = metrics2["Insider Trans"])
    
    metrics = ['52W High', '52W Low', '52W Range', 'Beta', 'Change', 'Current Ratio',
             'Debt/Eq', 'Dividend %', 'EPS next 5Y', 'EPS this Y', 'EPS (ttm)', 'Earnings'
             'Forward P/E', 'Gross Margin', 'Income', 'Insider Own', 'Insider Trans',
             'Market Cap', 'Oper. Margin', 'P/B', 'P/E', 'P/FCF', 'P/S', 'PEG', 'Perf Month',
             'Perf Quarter', 'Perf Week', 'Perf YTD', 'Price', 'Profit Margin', 'Quick Ratio', 
             'ROA', 'ROE', 'ROI', 'RSI (14)', 'SMA20', 'SMA200', 'SMA50', 'Sales', 'Short Float',
             'Short Ratio', 'Shs Outstand', 'Target Price', 'Volatility', 'Volume', 'RSI (14)']

    selectmetric = d.selectbox("Get specific metrics here: ", metrics)
    d.metric(selectmetric, metrics2[selectmetric])
     
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    profitMet = col1.checkbox("Profit Metrics")
    performanceMet = col2.checkbox("Performance Metrics")
    analystMet = col3.checkbox("Analyst Metrics")
    insiderMet = col4.checkbox("Insider Trading")
    shortMet = col5.checkbox("Short Metrics")
    technicalMet = col6.checkbox("Technical Trading Metrics")

    if profitMet: metricButtons.profitMetrics(metrics2, value=True) # Performance Metrics
    if performanceMet: metricButtons.performanceMetrics(metrics2)  # Performance Metrics
    if analystMet: metricButtons.analystMetrics(metrics2, ticker,value=True) # Analyst Rating Metrics
    if insiderMet: metricButtons.insiderMetrics(metrics2, ticker,value=True) # Insider Metrics
    if shortMet: metricButtons.shortMetrics(metrics2) # Short Metrics
    if technicalMet: metricButtons.technicalMetrics(metrics2) # Technical Trading Metrics

    col1, col2 = st.columns(2)

    if news_source == "Finviz":
        col1.title("Recent Headlines from " + news_source)
        newsdata = news.finviz(ticker)
        col1.plotly_chart(displayNews(newsdata.df), use_container_width = True)
        col1.header("Mean sentiment score: " + str(newsdata.meanScore()))

    elif news_source == "Wall Street Journal":
        col1.title("Recent Headlines from " + news_source)
        newsdata = news.wsj(ticker)
        col1.plotly_chart(displayNews(newsdata.df), use_container_width = True)
        col1.header("Mean sentiment score: " + str(newsdata.meanScore()))

    elif news_source == "Market Watch":
        col1.title("Recent Headlines from " + news_source)
        newsdata = news.MarketWatch(ticker)
        col1.plotly_chart(displayNews(newsdata.df), use_container_width = True)
        col1.header("Mean sentiment score: " + str(newsdata.meanScore()))

    elif news_source == "Forbes":
        col1.title("Recent Headlines from " + news_source)
        company = yfmetrics(ticker).tickerTocompany()
        newsdata = news.Forbes(company)
        col1.plotly_chart(displayNews(newsdata.df), use_container_width = True)
        col1.header("Mean sentiment score: " + str(newsdata.meanScore()))
    
    if tweets_source == "General Tweets":
        col2.title("General Tweets about " + ticker)
        tweetdata = dfTweets(ticker, "general")
        col2.plotly_chart(displayTweets(tweetdata.df), use_container_width = True)
        col2.header("Mean sentiment score: " + str(tweetdata.meanScore()))

    if tweets_source == "Verified Tweets":
        col2.title("Tweets from Verified Accounts: " + ticker)
        tweetdata = dfTweets(ticker, "verified")
        col2.plotly_chart(displayTweets(tweetdata.df), use_containter_width = True)
        col2.header("Mean sentiment score: " + str(tweetdata.meanScore()))

    if time_scale == "Recent Tweets":
        col2.title("Recent Tweets about " + ticker)
        tweetdata = dfTweets(ticker, "recent")
        col2.plotly_chart(displayTweets(tweetdata.df), use_container_width = True)
        col2.header("Mean sentiment score: " + str(tweetdata.meanScore()))

    if time_scale == "Popular Tweets":
        col2.title("Popular Tweets about " + ticker)
        tweetdata = dfTweets(ticker, "popular")
        col2.plotly_chart(displayTweets(tweetdata.df), use_container_width = True)
        col2.header("Mean sentiment score: " + str(tweetdata.meanScore()))

    if tweets_news:
        col2.title("Tweets from " + ticker)
        tweetdata = dfTweets(ticker, tweets_news)
        col2.plotly_chart(displayTweets(dfTweets(ticker, tweets_news).df), use_container_width = True)
        col2.header("Mean sentiment score: " + str(tweetdata.meanScore()))


# Used to display news dataframe
def displayNews(df):
    fig = go.Figure(data=[go.Table(      
        columnwidth = [80,400],
        header=dict(values=['Date', 'Headlines'], height = 50,
                    align='left', fill_color='white', font=dict(color='black', size=25)),
        cells=dict(values=[df.Date, df.Headlines], height = 30,
                align='left', fill_color='white', font=dict(color='black', size=20)))
    ])
    fig.update_layout(height = 1000)

    return fig  

# Used to display tweets dataframe
def displayTweets(df):
    fig = go.Figure(data=[go.Table(      
        columnwidth = [200,200,400,100],
        header=dict(values=['Date', 'UserName', 'Tweet', 'nlikes'], height = 50,
                    align='left', fill_color='white', font=dict(color='black', size=25)),
        cells=dict(values=[df.date, df.username, df.tweet, df.nlikes], height = 30,
                align='left', fill_color='white', font=dict(color='black', size=20)))
    ])
    fig.update_layout(height = 1000)

    return fig  

# Used to plot stock prices and volume
def stockplot(ticker, n):
    stock = yf.Ticker(ticker)
    start = dt.date.today()-dt.timedelta(days = n)
    price = stock.history(start=start)['Close']
    volume = stock.history(start=start)['Volume']

    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=price.index,
        y=price,
        name = 'price'
    ))

    fig.add_trace(
        go.Bar(
        x=volume.index,
        y=volume/1000000,
        name = "volume"
    ))
     
    fig.update_layout(xaxis_title="Date", yaxis_title="Price", height = 1000)
    return fig
