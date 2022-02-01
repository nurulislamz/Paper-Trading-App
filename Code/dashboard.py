import streamlit as st

from homePage import homePage
from portfolioPage import portfolioPage
from searchPage import stocksearcher

st.set_page_config(layout="wide")

# Define the multipage class to manage the multiple apps in our program -- towardDataScience.com
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append({
          
                "title": title, 
                "function": func
            })

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function']()

app = MultiPage()

# Add all your applications (pages) here
app.add_page("Home", homePage)
app.add_page("Portfolio", portfolioPage)
app.add_page("Stock Search", stocksearcher)
# app.add_page("Forcasting", machine_learning.app)
# app.add_page("Technical Analysis ",data_visualize.app)

# app.add_page("Data Analysis",redundant.app)

app.run()