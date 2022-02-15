import streamlit as st

from homePage import homePage
from portfolioPage import portfolioPage
from searchPage import searchPage
from statementPage import statementPage

st.set_page_config(layout="wide")

# Multipage class allows the use of multiple apps in one program -- towardDataScience.com
class MultiPage: 

    def __init__(self) -> None:
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        self.pages.append({
                "title": title, # name of page
                "function": func # runs function of that page
            })

    def run(self):
        # Creates a dropdown menu of pages 
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # runs the function associated with that page 
        page['function']()

app = MultiPage()

# Add all your applications (pages) here
app.add_page("Home", homePage)
app.add_page("Portfolio", portfolioPage)
app.add_page("Stock Search", searchPage) 
app.add_page("Financial Statements", statementPage) 

# add.app_page("Mean Reversion", reversion .app)
# app.add_page("Forcasting", machine_learning.app)

app.run()