import twint 
import yfinance as yf
import pandas as pd
import datetime as dt
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def tickerTocompany(ticker): # a bit slow 
    company = yf.Ticker(ticker).info['longName']
    return company.split()[0].lower().strip(",")

def general_query(ticker):
    company_name = tickerTocompany(ticker)
    query = "({company_name} OR #{company_name})".format(company_name = company_name)
    return query

def stock_query(ticker):
    query = "(${ticker} OR {ticker})".format(ticker = ticker)
    return query


# note c.since does not work currently, date of data subject to twint but
# to counteract this, i used c.filter and c.likes to remove less relevant data (created by bots or unpopular views)
analyst  = ['CathieDWood']
politicians = ['10DowningStreet', 'JoeBiden']
        
        
# note c.since does not work currently, date of data subject to twint but
# to counteract this, i used c.filter and c.likes to remove less relevant data (created by bots or unpopular views)
class tweets:
    def __init__(self, ticker, source = None):
        self.ticker = ticker
        self.query = stock_query(ticker)
        self.source = source
            
    # tweets about the company (not the stock)!!!
    def generalTweets(self): # about one month of data
        query = general_query(self.ticker) + " min_faves:5000" # uses company name/hashtag
        c = twint.Config()
        c.Search = query
        c.Lang = 'en'
        c.Store_json = True
        c.Hide_output = True
        c.Output = "generalTweets.json"
        c.Pandas = True
        twint.run.Search(c)
        
        return c.Output
    
    # ---  tweets about the company from here one  ---
    def newsTweets(self): # about a week of data
        c = twint.Config()
        news = ['CNBC','Benzinga', 'Stocktwits', '@MorningstarInc', 'FinancialTimes','WSJMarkets','MarketWatch', 'YahooFinance']

        if self.source in news:
            c.Username = self.source 
            c.Search = self.query + " OR " + general_query(self.ticker) 
            c.Lang = 'en'
            c.Store_json = True
            c.Hide_output = True
            c.Output = self.source +".json"
            c.Pandas = True
            c.Since = str(dt.date.today() - dt.timedelta(days = 180)) 
            c.Until = str(dt.date.today())
            twint.run.Search(c)
            print(c.Search)
            return c.Output
        
    def verifiedTweets(self): # 3 weeks of data
        c = twint.Config()
        query = self.query + " min_faves:500" + " filter:verified"
        c.Search = query
        c.Lang = 'en'
        c.Store_json = True
        c.Hide_output = True
        c.Output = "verifiedTweets.json"
        c.Pandas = True
        twint.run.Search(c)
        
        return c.Output
    
    def popularTweets(self): # a week of data roughly # 200 data points
        c = twint.Config()
        query = self.query + " min_faves:500"
        c.Search = query
        c.Lang = 'en'
        c.Store_json = True
        c.Hide_output = True
        c.Output = "weeklyTweets.json"
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 8)) 
        c.Until = str(dt.date.today())
        twint.run.Search(c)
        
        return c.Output
    
    # display most recent tweets # 300 data points
    def recentTweets(self): # within two days 
        c = twint.Config()
        query = self.query + " min_faves:100"
        c.Search = query
        c.Lang = 'en'
        c.Store_json = True
        c.Hide_output = True
        c.Output = "recentTweets.json"
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 3)) 
        c.Until = str(dt.date.today())
        twint.run.Search(c)
        
        return c.Output

class dfTweets:
    def __init__(self, ticker, source):
        self.ticker = ticker
        self.source = source
        
        news = ['CNBC','Benzinga', 'Stocktwits', 'MorningstarInc', 'FinancialTimes','WSJMarkets','MarketWatch', 'YahooFinance']
        self.ticker = ticker
        if source == "recent":
            self.json = tweets(ticker).recentTweets()
        elif source == "popular":
            self.json = tweets(ticker).popularTweets()
        elif source == "verified":
            self.json = tweets(ticker).verifiedTweets()
        elif source == "general":
            self.json = tweets(ticker).generalTweets()
        elif source in news:
            self.json = tweets(ticker, source).newsTweets()
        else:
            print("invalid scale")
    
        try:
            data = pd.read_json(self.json, lines = True)
        except:
            print("empty table")
            return
        
        data["date"] = data["date"].astype(str) + " " + data["time"]
        data = data[["date", "username", "tweet", "likes_count"]]
        self.df = data

        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = data['tweet'].apply(analyzer.polarity_scores).tolist()  
        scores = pd.DataFrame(scores)
        data = data.join(scores, rsuffix='_right')
        # weighted scores by using likes and sentiment
        data['scores'] = data['compound']*((data['likes_count'])/(data['likes_count']).mean()) # scews data too much
        self.df_scores = data
        
    def meanScore(self):
        return self.df_scores['scores'].mean()

    def recentTweets(self):
        # Recent Headlines
        print("Recent tweets from " + self.source)
        for i in range(5):
            print(self.df.tweet[i] + " (" + str(self.df.date[i]) + ")")

def clearfiles():
    paths = ['recentTweets.json', 'weeklyTweets.json', 'verifiedTweets.json', 'generalTweets.json', 'CNBC.json',
             'Benzinga.json', 'Stocktwits.json', '@MorningstarInc.json', 'FinancialTimes.json', 'WSJMarkets.json',
             'MarketWatch.json', 'YahooFinance.json'] 

    for path in paths:
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Can not delete the file as it doesn't exists")
