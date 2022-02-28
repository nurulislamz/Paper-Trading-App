https://share.streamlit.io/nurulislamz/paper-trading-app/main/app/dashboard.py
# Use this to access the site! Feel free to register with your own login and password, everything is current and working!
Also, I am finally going to integrate this app into a full web application using javascript and the django framework! Should be done by the end of the 5/3/2022!

# SentimentAnalysisofStock
Sentiment Analysis of any searched stocks using data scraped from twitter and popular news websites such as CNBC.

# Reports
- Twitter sentiment analysis report 
- Twitter correlation report

# Login Page
- Allows you to login and store your individual portfolio using a relational database

# Search Page
Functionality includes:
- Get current prices, volume and popular metrics
- Plots the pricing data and volume data
- Uses web scraping to obtain news data from CNBC, WallStreetJournal, Forbes and MarketWatch
- - Sentiment analysis of news headlines with average produced.
- Uses web scraping to obtain tweets from twitter
- - Includes functionality to obtain data from specific twitter news accounts.
- - Sentiment analysis of tweets with average produced.
- Display all data using streamlit in a web app.
- Machine learning classifier using logistic regression (60% average rate)

# Portfolio Page
- Allows you to keep track of your portfolio by uploading JSON/txt file. 
- Allows for paper-trading functionality with current stock prices and volume information. 
- Returns performance analysis, ROI and stock portfolio weightings. 

# Financial Statement Page 
- Utilises web scraping to display financial statement data from last 4 quarters for any ticker.

# Upcoming Pages
- Market Analysis
- Improved machine learning classifier utilising cross-validation testings of multiple different classification algorithms.
