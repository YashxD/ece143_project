import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
from functions import *

# Configure the page
st.set_page_config(page_title="Multi-Page App", page_icon="📚", layout="wide")

# Sidebar navigation
st.sidebar.title("Pages")

# Define available pages
pages = {
    "Theft_Map": "Theft Map",
    "PricevsTOD": "Price Versus Time of Day",
    "WeathervsTheft": "Weather Versus Theft",
    "BicyclesVsScooters" : "Bicycles Versus Scooters",
    "Worstday" : " Who had the worst day?"
}

# Initialize session state to remember the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Theft_Map"

# Create clickable buttons for each page
for page_name, page_display_name in pages.items():
    if st.sidebar.button(page_display_name, key=page_name, use_container_width = True):
        st.session_state.current_page = page_name

# Display the selected page content
selected_page = st.session_state.current_page

if selected_page == "Theft_Map":
    st.title("Theft Map")
    
    end_date = datetime(2024,11,12)
    start_date = end_date - timedelta(days=5 * 365)  # Approximate 5 years back
    dateRange = st.slider('Dates From', min_value= start_date, max_value=end_date, value=(start_date, end_date), format="MM/DD/YYYY") 
    FromTOD = st.slider('From (Time of day)', min_value=time(0,0), max_value=time(23,59), value = (time(0,0)))
    ToTOD = st.slider('To (Time of day)', min_value=time(0,0), max_value=time(23,59), value = (time(23,59)))
    options = ['bicycle', 'scooter', 'skateboard']
    selected_options = st.multiselect('Type of PEV:', options)
    coordinates = mapPlot(dateRange[0], dateRange[1], FromTOD, ToTOD,  selected_options)
    st.map(coordinates, size="0.5")
    

elif selected_page == "PricevsTOD":
    st.title("Map Page")
    st.write("Here is where you can view the map.")
    # Add code to display your map, e.g., using Folium or Pydeck

elif selected_page == "WeathervsTheft":
    st.title("Data Analysis Page")
    st.write("Analyze your data here.")
    # Add code for data analysis features, e.g., charts or tables
