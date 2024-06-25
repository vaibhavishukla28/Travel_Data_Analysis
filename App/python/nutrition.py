import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")

def app():
    st.title(":fries: Nutriton of MacDonalds Menu")
    st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
    df = pd.read_csv("Datasets/India_Menu-reshaped.csv")
    
    col1, col2 = st.columns((2))
    
    with st.sidebar:
        st.title("MacDonalds menu nutrition")
        
        category = st.sidebar.multiselect("Pick your Category", df["Menu Category"].unique())
        if not category:
            df2 = df.copy()
        else:
            df2 = df[df["Menu Category"].isin(category)]
            
        new_menu = st.sidebar.multiselect("Pick your menu", df2['New Menu'].unique())
        if not new_menu:
            df3 = df2.copy()
        else:
            df3 = df2[df2["New Menu"].isin(new_menu)]
        
        menu_items = st.sidebar.multiselect("Select a menu items", df3['Menu Items'].unique())
        if not menu_items:
            df4 = df3.copy()
        else:
            df4 = df3[df3["Menu Items"].isin(menu_items)]
        
        # data filtering
        
        if not category and not new_menu and not menu_items:
            filtered_df = df
        elif not new_menu and not menu_items:
            filtered_df = df[df["Menu Category"].isin(category)]
        elif not category and not menu_items:
            filtered_df = df[df["New Menu"].isin(new_menu)]
        elif not category and not new_menu:
            filtered_df = df3[df3["Menu Items"].isin(menu_items)]
        elif category and new_menu and menu_items:
            filtered_df = df3[df3["Menu Category"].isin(category) & df3["New Menu"].isin(new_menu) & df3["Menu Items"].isin(menu_items)]
        elif category and new_menu:
            filtered_df = df3[(df3["Menu Category"].isin(category)) & (df3["New Menu"].isin(new_menu))]
        elif category and menu_items:
            filtered_df = df3[df3["Menu Category"].isin(category) & df3["Menu Items"].isin(menu_items)]
        elif new_menu and menu_items:
            filtered_df = df3[(df3["New Menu"].isin(new_menu)) & (df3["Menu Items"].isin(menu_items))]
        elif menu_items:
            filtered_df = df3[df3["Menu Items"].isin(menu_items)]
        else:
            filtered_df = df3[df3["Menu Category"].isin(category) & df3["New Menu"].isin(new_menu) & df3["Menu Items"].isin(menu_items)]
        
    
        with col1:
            st.subheader("Energy vs Category")
            fig = px.scatter(filtered_df, x="Menu Category", y="Energy (kCal)", hover_name="Menu Items", color="Menu Category")
            st.plotly_chart(fig, use_container_width=True, height= 200)
        
        with col2:
            st.subheader("Plotting pie chart")
            fig = px.sunburst(filtered_df, path=['Menu Items', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)', 'Cholesterols (mg)',
                                                 "Total carbohydrate (g)", "Total Sugars (g)", "Added Sugars (g)",
                                                 "Sodium (mg)"], hover_name="Menu Items", hover_data=['Menu Items', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)', 'Cholesterols (mg)',
                                                 "Total carbohydrate (g)", "Total Sugars (g)", "Added Sugars (g)",
                                                 "Sodium (mg)"], color="Menu Items")
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        with col1:
            st.subheader("Energy vs  Sodium")
            fig = px.box(filtered_df, x= "Menu Category", y= "Sodium (mg)", color= "Menu Category")
            st.plotly_chart(fig, use_container_width=True, height= 200)
        
        with col2:
            st.subheader("Relation between Fat, Sugar and Cholesterols")
            fig = px.scatter(filtered_df, x="Total Sugars (g)", y="Total fat (g)", hover_name="Menu Items", size = "Cholesterols (mg)", color="Menu Category")
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        with col1:
            st.subheader("Menu Category")
            fig = px.pie(filtered_df, names= "Menu Category", color= "Menu Category")
            st.plotly_chart(fig, use_container_width=True, height= 200)
        
        with col2:
            st.subheader("Menu Items vs Cholesterols")
            fig = px.bar(filtered_df, x="Menu Items", y="Cholesterols (mg)", hover_name
                         ="Cholesterols (mg)", color="Menu Category", text_auto='-1s')
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        with col1:
            st.subheader("Item Vs All Fats")
            fig = px.bar(filtered_df, x = "Menu Items", y= ["Total fat (g)", "Sat Fat (g)", "Trans fat (g)"], text_auto='-1s')
            st.plotly_chart(fig, use_container_width=True)