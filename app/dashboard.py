import streamlit as st
import nltk
nltk.download('vader-lexicon')

from homePage import homePage
from login import loginPage
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

# we set the app state to off initially
if "app_state" not in st.session_state:
    st.session_state.app_state = False

# runs app only if we are in app state
if st.session_state.app_state:
    app = MultiPage()

    # Application pages
    app.add_page("Home", homePage)
    app.add_page("Portfolio", portfolioPage)
    app.add_page("Stock Search", searchPage) 
    app.add_page("Financial Statements", statementPage) 
    # add.app_page("Mean Reversion", reversion .app)
    # app.add_page("Forcasting", machine_learning.app)
    app.run()

# # if we successfully log in, we run the app state
if not st.session_state.app_state:
    user = loginPage()
    if user:
        st.session_state.app_state = True
        st.session_state.user = user
