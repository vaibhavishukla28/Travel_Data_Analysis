import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from streamlit_option_menu import option_menu

import home, must_visit, indian_food, nutrition


st.set_page_config(
    page_title = "Travel Data Analysis",
    layout = "wide"
)

class MultiApp:
    
    
    def run():
        
        with st.sidebar:
            app = option_menu(
                menu_title = "Analysis",
                options= ["Home", "Must Visit Places", "Indian Foods", "Nutrition"],
                default_index= 0,
                styles= {
                    "container" : { "padding" : "5!important",
                                   "nav-link" : {"font-size": "20px"}}
                }
            )
            
        if app == 'Home':
            home.app()
        if app == 'Must Visit Places':
            must_visit.app()
        if app == "Indian Foods":
            indian_food.app()
        if app == "Nutrition":
            nutrition.app()
    run()