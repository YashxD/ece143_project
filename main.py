import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time

# Configure the page
st.set_page_config(page_title="Multi-Page App", page_icon="📚", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")

# Define available pages
pages = {
    "Theft_Map": "Theft Map",
    "PricevsTOD": "Price Versus Time of Day",
    "WeathervsTheft": "Weather Versus Theft"
}

# Initialize session state to remember the current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Create clickable buttons for each page
for page_name, page_display_name in pages.items():
    if st.sidebar.button(page_display_name, key=page_name, use_container_width = True):
        st.session_state.current_page = page_name

# Display the selected page content
selected_page = st.session_state.current_page

def examplegetfunction(start_date, end_date, from_TOD, to_TOD):
    return pd.DataFrame(np.random.randn(1000, 2) / [250, 250] + [32.8812, -117.2344], columns=["lat", "lon"])

if selected_page == "Theft_Map":
    st.title("Theft Map")
    
    end_date = datetime(2024,11,12)
    start_date = end_date - timedelta(days=5 * 365)  # Approximate 5 years back
    x = st.slider('Dates From', min_value= start_date, max_value=end_date, value=(start_date, end_date), format="YYYY-MM-DD")  # 👈 this is a widget
    y = st.slider('From (Time of day)', min_value=time(0,0), max_value=time(23,59), value = (time(0,0)))
    z = st.slider('To (Time of day)', min_value=time(0,0), max_value=time(23,59), value = (time(23,59)))
    
    st.map(examplegetfunction(1,1,1,1), size=3)

elif selected_page == "PricevsTOD":
    st.title("Map Page")
    st.write("Here is where you can view the map.")
    # Add code to display your map, e.g., using Folium or Pydeck

elif selected_page == "WeathervsTheft":
    st.title("Data Analysis Page")
    st.write("Analyze your data here.")
    # Add code for data analysis features, e.g., charts or tables
