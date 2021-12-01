import streamlit as st
import json
import os
import time
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
# from streamlit_player import st_player



# use st.write("") to write output
# vedio path ./temp/1.avi
# brfore returninng the final count delete frames and other in temp folder
def give_count():
    pass



def no_page():
    '''
        404 page
    '''
    st.error("### Oops! 404")

def explore_page():
    '''
        Explore page
    '''
    st.write("""## Overview """)
    

def show_home_page():
    '''
        Home page
    '''
    st.write("## User Input")
    uploaded_file = st.file_uploader("Video", type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
    if uploaded_file is not None:
        with open("temp/1.avi", 'wb') as f:
            f.write(uploaded_file.getbuffer())
    #         components.html(
    # """
    # Project/dip-project-evil_morty/demo/temp/1.avi
    # <iframe width="420" height="315" src="./temp/1.avi"> </iframe>
    # """,
    # height=600,
# )
    run = st.button("Count")
    if run and uploaded_file is not None:
        st.markdown("""---""")
        with st.spinner("Counting ..."):
            ans = give_count()
            if uploaded_file:
                st.write('## Count')
            else:
                st.error("Eror with the file")

st.sidebar.header('Navigation')
page = st.sidebar.selectbox("Select the page you want to see", ["Home","Explore"])
st.sidebar.markdown("---")



st.title("People Counting")
st.write("This app count ...")
if page == "Explore":
    explore_page()
elif page == "Home":
    show_home_page()
else:
    no_page()

