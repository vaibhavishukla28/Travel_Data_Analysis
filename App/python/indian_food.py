import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
# from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")

# st.set_page_config(page_title="Must visit  places in India",page_icon=":bar_chart:", layout='wide')

def app():
    st.title("Indian Foods")
    st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
    df = pd.read_csv("Datasets/indian_food-reshaped.csv")
    
    # Number of dishes based on region
    
    st.subheader("Number of dishes based on region")
    reg_df = df.region.value_counts().reset_index()
    reg_df.columns = ["region", "count"]
    reg_df = reg_df.sample(frac=1)
    fig = px.bar(reg_df,x='region',y='count',title='Number of dishes based on regions', color_discrete_sequence=[
        'red', 'greenyellow', "blue", "darkorange", "deeppink", "gold", "cyan"], color="region")
    st.plotly_chart(fig, use_container_width=True, height= 200)
    
    # relation between preperation time and cooking time
    
    fig = px.scatter(df,x='cook_time',y='prep_time',color='diet', color_discrete_sequence=['green','red'], hover_data = ['name'], 
                     labels={'cook_time': 'Cooking time (minutes)','prep_time': 'Preparation time (minutes)'})
    st.plotly_chart(fig, use_container_width=True)
        
    
    col1, col2 = st.columns((2))
    
    with st.sidebar:
        st.title("Indian Food")
        
        region = st.sidebar.multiselect("Pick your Region", df["region"].unique())
        if not region:
            df2 = df.copy()
        else:
            df2 = df[df["region"].isin(region)]
        
        state = st.sidebar.multiselect("Pick your State", df2["state"].unique())
        if not state:
            df3 = df2.copy()
        else:
            df3 = df2[df2["state"].isin(state)]
            
        # data filtering
        
        if not region and not state:
            filtered_df = df
        elif not state:
            filtered_df = df[df["region"].isin(region)]
        # elif region:
        #     filtered_df = df3[df3["region"].isin(region)]
        elif state:
            filtered_df = df3[df3["state"].isin(state)]
        else:
            filtered_df = df3[df3["region"].isin(region) & df3["state"].isin(state)]
            
        with col1:
            st.subheader("food category")
            fig = px.sunburst(filtered_df, path=['diet', 'course', 'name'], color="course")
            st.plotly_chart(fig, use_container_width= True, height = 200)
        
        with col2:
            st.subheader("Cooking time")
            fig = px.bar(filtered_df, x="name", y="cook_time")
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        with col1:
            st.subheader("Preperation time")
            fig = px.scatter(filtered_df, x="name", y="prep_time")
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        with col2:
            st.subheader("Diet")
            fig = px.pie(filtered_df, names="diet", color_discrete_sequence=["lawngreen", "orangered"], color="diet")
            st.plotly_chart(fig, use_container_width=True, height= 200)
            
        