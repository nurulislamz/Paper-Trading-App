# data cleaning
import numpy as np 
import pandas as pd 
import datetime as dt # to get dates
import streamlit as st
# import re # regex patterns

# data scraping
from bs4 import BeautifulSoup # parsses html/xml web data
import requests

# sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class MarketWatch:
    def __init__(self, ticker):
        # Market watch 
        self.ticker = ticker
        marketwatch_url = "https://www.marketwatch.com/investing/stock/" + ticker
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

        r = requests.get(url = marketwatch_url, headers = header)
        soup2 = BeautifulSoup(r.text, features = "lxml")

        data = soup2.find('div',{'class', "column column--primary j-moreHeadlineWrapper"})

        # data cleaning
        data = data.text
        data = data.strip().split("\n")    
        data = pd.Series(data)

        # Headlines
        news = data.apply(lambda x: x.strip())
        news.replace('',np.nan, inplace = True)
        news = news.dropna()

        searchfor = ["Barron", "MarketWatch Automation", "p.m.", "a.m.", "by"] # out of 20, lost 2 articles because of "by"
        news[news.str.contains('|'.join(searchfor))] = np.nan
        news_data = news.dropna()
        news_data.index = np.arange(0,len(news_data))

        # Dates
        searchfor2 = ["p.m. ET", "a.m. ET"] # out of 20, lost 2 articles because of "by"
        news_date = data[data.str.contains('|'.join(searchfor2))]
        news_date.index = np.arange(0,len(news_date))

        # dataframe
        df = pd.DataFrame({'Headlines': news_data, 'Date': news_date})
        df = df.dropna()

        self.df = df
        
        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = df['Headlines'].apply(analyzer.polarity_scores).tolist()  

        df_scores = pd.DataFrame(scores)
        df_scores = df.join(df_scores, rsuffix='_right')
        
        self.df_scores = df_scores        
        
    def recentHeadlines(self):
        # Recent Headlines
        st.subheader("Recent Headlines from Market Watch: " + self.ticker)
        for i in range(10):
            st.write(self.df.Headlines[i] + " (" + self.df.Date[i] + ")")

    # returns mean score of sentiment analysis
    def meanScore(self):
        mean = round(self.df_scores['compound'].mean(), 2)
        return mean

class Forbes:
    def __init__(self, company):
        # company name
        self.company = company

        # data fetch
        forbes_url = "https://www.forbes.com/companies/" + self.company
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

        r = requests.get(url = forbes_url, headers = header)
        soup = BeautifulSoup(r.text, features = "lxml")

        news_data = soup.findAll('a',{'class', "stream-item__title"})
        news_date = soup.findAll('div', {'class', 'stream-item__date'})

        # data cleaning
        news_data = [news.text for news in news_data]
        news_date = [news.text for news in news_date]

        df = pd.DataFrame({'Headlines': news_data, 'Date': news_date})
        
        # dataframe
        self.df = df
        
        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = df['Headlines'].apply(analyzer.polarity_scores).tolist()

        df_scores = pd.DataFrame(scores)
        df_scores = df.join(df_scores, rsuffix='_right')
        
        # dataframe with scores
        self.df_scores = df_scores

    def recentHeadlines(self):
        # Recent Headlines
        st.subheader("Recent Headlines from Forbes: " + self.company)
        for i in range(10):
            st.write(self.df.Headlines[i] + " (" + self.df.Date[i] + ")")

    # returns mean score of sentiment analysis
    def meanScore(self):
        mean = round(self.df_scores['compound'].mean(), 2)
        return mean
        
class wsj:
    def __init__(self, ticker):
        # ticker
        self.ticker = ticker

        # data fetch
        wsj_url = "https://www.wsj.com/market-data/quotes/" + self.ticker
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

        r = requests.get(url = wsj_url, headers = header)
        soup = BeautifulSoup(r.text, features = "html.parser")

        # data cleaning
        news_data = soup.findAll(target = "_blank")
        news_date = soup.findAll('li', {'class': "WSJTheme--cr_dateStamp--13KIPpOo"})

        news_data = [news.text for news in news_data[:10]]
        news_date = [date.text for date in news_date]

        df = pd.DataFrame({'Headlines': news_data, 'Date': news_date})

        # dataframe
        self.df = df
        
        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = df['Headlines'].apply(analyzer.polarity_scores).tolist()

        df_scores = pd.DataFrame(scores)
        df_scores = df.join(df_scores, rsuffix='_right')
        df_scores

        self.df_scores = df_scores

    def recentHeadlines(self):
        # Recent Headlines
        st.subheader("Recent Headlines from Wall Street Journal: " + self.ticker)
        for i in range(10):
            st.write(self.df.Headlines[i] + " (" + self.df.Date[i] + ")")

    # returns mean score of sentiment analysis
    def meanScore(self):
        mean = round(self.df_scores['compound'].mean(), 2)
        return mean

class finviz:
    def __init__(self, ticker = "aapl"):
        # ticker
        self.ticker = ticker 
        
        finwiz_url = 'https://finviz.com/quote.ashx?t=' + self.ticker
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

        # data fetch
        r = requests.get(url=finwiz_url,headers=header) 
        html = BeautifulSoup(r.text, features="lxml")
        news_table = html.find(id='news-table')
        df_tr = news_table.findAll('tr')

        # data cleaning
        news_data = [news.a.text for news in df_tr]
        news_date = [news.td.text.split() for news in df_tr]
        news_time = [time[0] if len(time) == 1 else time[1] for time in news_date]
        news_date = [date[0] if len(date) != 1 else np.nan for date in news_date ]

        # dataframe
        df = pd.DataFrame({'Headlines': news_data, 'Date': news_date, 'Time': news_time})
        df = df.ffill(axis=0)
        
        self.df = df
        
        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = df['Headlines'].apply(analyzer.polarity_scores).tolist()

        df_scores = pd.DataFrame(scores)
        df_scores = df.join(df_scores, rsuffix='_right')
        
        self.df_scores = df_scores
        
    def recentHeadlines(self):
        # Recent Headlines
        st.subheader("Recent Headlines from Finviz: " + self.ticker)
        for i in range(10):
            st.write(self.df.Headlines[i] + " (" + self.df.Date[i] + ")")
    
    # returns mean score of sentiment analysis
    def meanScore(self):
        mean = round(self.df_scores['compound'].mean(), 2)
        return mean