import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
from functions import *

# Configure the page
st.set_page_config(page_title="UCSD Bike Theft Analyzer", page_icon="📚", layout="wide")

# Sidebar navigation
st.sidebar.title("Pages")

# Define available pages
pages = {
    "Theft_Map": "Theft Map",
    "HoursVsTypes": "Hours Vs Bicycles and Scooters",
    "BicyclesVsScooters" : "Time Vs Bicycles and Scooters",
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
    selected_options = st.multiselect('Type of Vehicle:', options, default = options)
    coordinates = mapPlot(dateRange[0], dateRange[1], FromTOD, ToTOD,  selected_options)
    st.write(f"Number of mappable thefts: {len(coordinates)}")
    st.map(coordinates, size=3, height=700)
    

elif selected_page == "HoursVsTypes":
    df = pd.read_csv("time_type_proportions.csv")
    df['start'] = df['time_range'].str.extract(r'\[(\d+)')[0].astype(int)
    df_sorted = df.sort_values(by='start').drop(columns='start')
    st.bar_chart(df, x = 'start', x_label= 'Hour of Day', y_label = 'Percent Thefts', y = ['bicycle', 'scooter'] ,horizontal=False, height=700)
    
elif selected_page == "BicyclesVsScooters":
    result = bicyclesVersusScooters()
    st.bar_chart(result, height = 1000, x='year_month', y=['Bike_Count', 'Scooter_Count'], x_label='Year - Month', y_label='# of Thefts', color = ['#FF0000', '#0000FF'])
    
elif selected_page == "Worstday":
    result = getWorstDay()
    st.title("Think you are having a bad day?")
    st.write(f"On {result['date']} at {result['time']}, someone had their {result['type']} stolen from the {result['location']}. It was valued at")
    st.subheader(f"$ {result['price']}")
    st.header("")
    st.header("ouch")