import pandas as pd 
import datetime as dt # to get dates
import yfinance as yf
import numpy as np 
import streamlit as st
import plotly.graph_objects as go

import news
from portfolioPage import validticker
from metrics import finvizmetrics, yfmetrics, ratings, insider
from twitter import dfTweets

# Used to display news dataframe
def displayNews(df):
    fig = go.Figure(data=[go.Table(      
        columnwidth = [80,400],
        header=dict(values=['Date', 'Headlines'], height = 50,
                    align='left', fill_color='white', font=dict(color='black', size=25)),
        cells=dict(values=[df.Date, df.Headlines], height = 50,
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
        cells=dict(values=[df.date, df.username, df.tweet, df.nlikes], height = 50,
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

    if profitMet: profitMetrics(metrics2) # Performance Metrics
    if performanceMet: performanceMetrics(metrics2)  # Performance Metrics
    if analystMet: analystMetrics(metrics2, ticker) # Analyst Rating Metrics
    if insiderMet: insiderMetrics(metrics2, ticker) # Insider Metrics
    if shortMet: shortMetrics(metrics2) # Short Metrics
    if technicalMet: technicalMetrics(metrics2) # Technical Trading Metrics

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



def profitMetrics(df):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "ROA", value = df['52 Week High abs'], delta = df["52W High"])
    col2.metric(label = "ROE", value = df['52 Week High abs'], delta = df["52W High"])
    col3.metric(label = "ROI", value = df['52 Week High abs'], delta = df["52W High"])
    col4.metric(label = "Gross Margin", value = df['52 Week High abs'], delta = df["52W High"])
    col5.metric(label = "Oper. Margin", value = df['52 Week High abs'], delta = df["52W High"])
    col6.metric(label = "Profit Margin", value = df['52 Week High abs'], delta = df["52W High"])

def performanceMetrics(df):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "52 Week High", value = df['52 Week High abs'], delta = df["52W High"])
    col2.metric(label = "52 Week Low", value = df['52 Week Low abs'], delta = df["52W Low"])
    col3.metric(label = "Weekly Performance", value = df['Perf Week'])
    col4.metric(label = "Monthly Performance", value = df['Perf Month'])
    col5.metric(label = "Quarter Performance", value = df['Perf Quarter'])
    col6.metric(label = "Yearly Performance", value = df['Perf Year'])

def analystMetrics(df, ticker):
    rating = ratings(ticker)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "Mean Target Price", value = df['Target Price'], delta = float(df["Target Price"]) - float(df["Price"]))
    col2.metric(label = "Analyst Recommendation (1 = Buy, 5 = Sell)", value = df['Recom'])
    col3.metric(label = "Positive Analyst Ratings", value = rating[0])
    col4.metric(label = "Neutral Analyst Ratings", value = rating[1])
    col5.metric(label = "Negative Analyst Ratings", value = rating[2])
    col6.metric(label = "", value = " ") # empty metrics for formatting purposes

def insiderMetrics(df, ticker):
    inside = insider(ticker)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "Insider Sell", value = inside[0])
    col2.metric(label = "Insider Buy", value = inside[1])
    col3.metric(label = "Insider Ownership", value = df['Insider Own'], delta = df["Insider Trans"])
    col4.metric(label = "Institutional Ownership", value = df['Inst Own'], delta = df["Inst Trans"])
    col5.metric(label = "", value = " ")
    col6.metric(label = "", value = " ")

def shortMetrics(df):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric(label = "Short Float", value = df['Short Float'])
    col2.metric(label = "Short Ratio", value = df['Short Ratio'])
    col3.metric(label = "", value = "")
    col4.metric(label = "", value = "")
    col5.metric(label = "", value = "")
    col6.metric(label = "", value = "")

def technicalMetrics(df):
    col1, col2, col3, col4, col5, col6 = st.columns(6) 
    col1.metric(label = "SMA20", value = df['SMA20'])
    col2.metric(label = "SMA50", value = df['SMA50'])
    col3.metric(label = "SMA200", value = df['SMA200'])
    col4.metric(label = "RSI (14)", value = df['RSI (14)'])
    col5.metric(label = "Volatility", value = df['Volatility'])
    col6.metric(label = "", value = "")