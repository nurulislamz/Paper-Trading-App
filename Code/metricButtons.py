import streamlit as st
from metrics import ratings, insider

class metricButtons:
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