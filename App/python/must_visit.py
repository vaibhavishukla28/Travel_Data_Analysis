import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# defining app

def app():
    st.title(":bar_chart: Must Visit Places of India")
    st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
    
# reading data

    df = pd.read_csv("indian places-reshaped.csv")
    
    col1, col2 = st.columns((2))

    with st.sidebar:
        st.title('🏂 Indian Data')
        
        zone = st.sidebar.multiselect("Pick your Zone", df["Zone"].unique())
        if not zone:
            df2 = df.copy()
        else:
            df2 = df[df["Zone"].isin(zone)]
        
        state = st.sidebar.multiselect("Pick your State", df2["State"].unique())
        if not state:
            df3 = df2.copy()
        else:
            df3 = df2[df2["State"].isin(state)]
        
        city = st.sidebar.multiselect("Pick your City", df3["City"].unique())
        if not city:
            df4 = df3.copy()
        else:
            df4 = df3[df3["City"].isin(city)]
        
        type = st.sidebar.multiselect("Pick your Type", df4["Type"].unique())
        if not type:
            df5 = df4.copy()
        else:
            df5 = df4[df4["Type"].isin(type)]
            
        # filtering data based on zone, state, city and type
        
        if not zone and not state and not city and not type:
            filtered_df = df
        elif not state and not city and not type:
            filtered_df = df[df["Zone"].isin(zone)]
        elif not zone and not city and not type:
            filtered_df = df[df["State"].isin(state)]
        elif not zone and not state and not type:
            filtered_df = df[df["City"].isin(city)]
        elif not zone and not state and not city:
            filtered_df = df[df["Type"].isin(type)]
            
        elif state and city and type:
            filtered_df = df3[df3["State"].isin(state) & df3["City"].isin(city) & df3["Type"].isin(type)]
        elif zone and state and type:
            filtered_df = df3[df3["Zone"].isin(zone) & df3["State"].isin(state) & df3["Type"].isin(type)]
        elif zone and state and city:
            filtered_df = df3[df3["Zone"].isin(zone) & df3["State"].isin(state) & df3["City"].isin(city)]
        elif zone and city and type:
            filtered_df = df3[df3["Zone"].isin(zone) & df3["City"].isin(city) & df3["Type"].isin(type)]
        elif type:
            filtered_df = df3[df3["Type"].isin(type)]
        else:
            filtered_df = df3[df3["Zone"].isin(zone) & df3["State"].isin(state) & df3["City"].isin(city) & df3["Type"].isin(type)]
            
        # column chart
        
        with col1:
            st.subheader("Indian Places and their google review")    
            fig = px.bar(filtered_df, x = "Name", y = "Google review rating", template="plotly_dark", color_discrete_sequence= ["goldenrod"])
            st.plotly_chart(fig, use_container_width=True, height = 200)
        
        with col2:
            st.subheader("Best time to visit")   
            fig = px.scatter(filtered_df, x = "Name", y= "Best Time to visit", color = "Best Time to visit", hover_name= "Name")
            st.plotly_chart(fig, use_container_width=True, height = 200)
        
        with col1:
            st.subheader("DSLR allowed or not")    
            fig = px.treemap(filtered_df, path = ["Name", "DSLR Allowed"], color = "DSLR Allowed", color_discrete_sequence= ["springgreen", "paleturquoise"],)
            st.plotly_chart(fig, use_container_width=True, height = 200)
        
        with col2:
            st.subheader("Weekly Off")   
            fig = px.line(filtered_df, x = "Name", y = "Weekly Off", hover_name = "Name")
            st.plotly_chart(fig, use_container_width=True, height = 200)
            
        
        # df_review = df.sort_values(by= "Number of google review in lakhs", ascending= False)