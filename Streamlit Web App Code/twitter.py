import twint 
import yfinance as yf
import pandas as pd
import datetime as dt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from scipy.stats import norm

from metrics import yfmetrics

# creates a general query for twitter
def general_query(ticker):
    company_name = yfmetrics(ticker).tickerTocompany()
    query = "({company_name} OR #{company_name})".format(company_name = company_name)
    return query

# creates a stock twitter query for twitter
def stock_query(ticker):
    query = "(${ticker} OR {ticker})".format(ticker = ticker)
    return query

analyst  = ['CathieDWood']
politicians = ['10DowningStreet', 'JoeBiden']
        
# used to obtain twitter data    
class tweets:
    def __init__(self, ticker, source = None):
        self.ticker = ticker
        self.query = stock_query(ticker)
        self.source = source
            
    # tweets about the company (not the stock)!!!
    def generalTweets(self): 
        query = general_query(self.ticker) + " min_faves:5000" # uses company name/hashtag
        c = twint.Config()
        c.Search = query
        c.Lang = 'en'
        c.Hide_output = True
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 90)) 
        twint.run.Search(c)
        data = twint.storage.panda.Tweets_df
        
        return data # returns (roughly 1500 data points) 
    
    # ---  tweets about the company from here one  ---
    
    # tweets selected from popular news twitter accounts
    def newsTweets(self): # about a week of data
        c = twint.Config()
        news = ['CNBC','Benzinga', 'Stocktwits', '@MorningstarInc', 'FinancialTimes','WSJMarkets','MarketWatch', 'YahooFinance']

        if self.source in news:
            c.Username = self.source 
            c.Search = self.query + " OR " + general_query(self.ticker) 
            c.Lang = 'en'
            c.Hide_output = True
            c.Pandas = True
            c.Since = str(dt.date.today() - dt.timedelta(days = 180)) 
            twint.run.Search(c)
            data = twint.storage.panda.Tweets_df

            return data # returns about a week of data (roughly 100 points for popular tickers)

    # tweets from verified accounts only        
    def verifiedTweets(self): # 3 weeks of data
        c = twint.Config()
        query = self.query + " min_faves:500" + " filter:verified"
        c.Search = query
        c.Lang = 'en'
        c.Hide_output = True
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 40))
        twint.run.Search(c)
        data = twint.storage.panda.Tweets_df
        
        return data # roughly 3 weeks of data (500 data points)
    
    # Popular tweets with over 500 likes 
    def popularTweets(self): # 2 weeks of data # 200 data points roughly
        c = twint.Config()
        query = self.query + " min_faves:500"
        c.Search = query
        c.Lang = 'en'
        c.Hide_output = True
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 15)) 
        twint.run.Search(c)
        data = twint.storage.panda.Tweets_df
        
        return data # returns 1 week of data (roughly 200 data points)
    
    # display most recent tweets
    def recentTweets(self): # within two days 
        c = twint.Config()
        query = self.query + " min_faves:100"
        c.Search = query
        c.Lang = 'en'
        c.Hide_output = True
        c.Output = "recentTweets.json"
        c.Pandas = True
        c.Since = str(dt.date.today() - dt.timedelta(days = 3)) 
        twint.run.Search(c)
        data = twint.storage.panda.Tweets_df
        
        return data # returns tweets from last two days (roughly 300 data points)

# works with tweet function to create dataframe from extracted JSON file
class dfTweets:
    def __init__(self, ticker, source):
        self.ticker = ticker
        self.source = source
        
        news = ['CNBC','Benzinga', 'Stocktwits', 'MorningstarInc', 'FinancialTimes','WSJMarkets','MarketWatch', 'YahooFinance']
        self.ticker = ticker
        if source == "recent":
            data = tweets(ticker).recentTweets()
        elif source == "popular":
            data = tweets(ticker).popularTweets()
        elif source == "verified":
            data = tweets(ticker).verifiedTweets()
        elif source == "general":
            data = tweets(ticker).generalTweets()
        elif source in news:
            data = tweets(ticker, source).newsTweets()
        else:
            return ("invalid scale")
          
        # saves data as a dataframe to display
        if {'date', 'time'}.issubset(data.columns):
            data["date"] = data["date"].astype(str) + " " + data["time"]
        
        data['date'] = data.date.astype({'date': 'datetime64[ns]'}) # converts date to dt.date type
        data = data[["date", "username", "tweet", "nlikes"]]
        self.df = data

        # Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        scores = data['tweet'].apply(analyzer.polarity_scores).tolist()  
        scores = pd.DataFrame(scores)
        df_scores = data.join(scores, rsuffix='_right')
        # weighted scores by using log transformation of likes multiplied by sentiment scores
        df_scores['scores'] = df_scores['compound']*np.log(df_scores['nlikes'])
        
        # applying normal distribution
        standard_scores = (df_scores['scores']-df_scores['scores'].mean())/df_scores['scores'].std()
        df_scores['scores'] = standard_scores.apply(lambda x: norm.cdf(x) if x>0 else -(1-norm.cdf(x)))
        
        # gets the mean sentiment score of that days tweets
        df_scores = df_scores.groupby(df_scores.date.dt.date).mean()   

        self.df_scores = df_scores

    def meanScore(self):
        return self.df_scores['scores'].median()    

    def recentTweets(self):
        # Recent Headlines
        print("Recent tweets from " + self.source)
        for i in range(5):
            print(self.df.tweet[i] + " (" + str(self.df.dates[i]) + ")")
            