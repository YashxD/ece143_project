import pandas as pd
from datetime import datetime, time
import ast
import random

def mapPlot(start_date, end_date, start_time, end_time, types):
  df = pd.read_csv('mingextract.csv')
  filtered_df = df[df['type'].isin(types)] # filtered by type of vehicle
  
  filtered_df = filtered_df[(pd.to_datetime(filtered_df['date'])>= start_date) & (pd.to_datetime(filtered_df['date']) <= end_date)] # filtered by date
  if (start_time < end_time):
    filtered_df = filtered_df[(pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time >= start_time) & (pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time <= end_time)] # filtered by time
  else: # Handle time wrap around case
    filtered_df = filtered_df[
                              (pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time >= start_time) & (pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time <= time(23,59)) |
                              (pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time <= end_time) & (pd.to_datetime(filtered_df['time'], format="%H:%M").dt.time >= time(0,0))  
                              ]
  mapping_list = {}
  
  with open("mapping/locations.txt", 'r') as file:
    for line in file:
      key, value = map(str.strip, line.split(':', 1))
      mapping_list[key] = value

  filtered_df['coordinates'] = filtered_df['location'].map(mapping_list) # Add a new column called "coordinates"
  filtered_df = filtered_df[filtered_df['coordinates'] != "None"] # Only get the ones where the coordinates exist
  filtered_df = filtered_df[filtered_df['coordinates'].notna()]
  
  coordinates_df = filtered_df[['coordinates']]
  
  coordinates_df_2 = coordinates_df.copy()  # Create an explicit copy
  
  coordinates_df_2['coordinates'] = coordinates_df_2['coordinates'].apply( # Convert from String to Tuple
    lambda x: ast.literal_eval(x) if x != "None" else None 
  )
  
  spread = 0.0002
  
  if not coordinates_df_2.empty:
    
    min_lat, max_lat = 32.846263, 32.897726
    min_lon, max_lon = -117.270637, -117.184645
    
    # Filter the DataFrame to include only points within the boundaries
    coordinates_df_2 = coordinates_df_2[
        (coordinates_df_2['coordinates'].apply(lambda x: x[0] if x else None) >= min_lat) &
        (coordinates_df_2['coordinates'].apply(lambda x: x[0] if x else None) <= max_lat) &
        (coordinates_df_2['coordinates'].apply(lambda x: x[1] if x else None) >= min_lon) &
        (coordinates_df_2['coordinates'].apply(lambda x: x[1] if x else None) <= max_lon)
    ]
    
    # Add unique random noise to 'lat' and 'lon' using apply
    coordinates_df_2['lat'] = coordinates_df_2['coordinates'].apply(
        lambda x: x[0] + random.uniform(-spread, spread) if x else None
    )
    coordinates_df_2['lon'] = coordinates_df_2['coordinates'].apply(
        lambda x: x[1] + random.uniform(-spread, spread) if x else None
    )

  # print(coordinates_df_2)
  return coordinates_df_2
  # return pd.DataFrame(np.random.randn(1000, 2) / [300, 300] + [32.8812, -117.2344], columns=["lat", "lon"])
  
def getWorstDay():
  df = pd.read_csv('mingextract.csv')
  df['price'] = pd.to_numeric(df['price'], errors='coerce')
  max_price_row = df.loc[df['price'].idxmax()]
  return max_price_row

def bicyclesVersusScooters():
  df = pd.read_csv('mingextract.csv')
  df_bike = df[df['type'] == 'bicycle']
  df_bike = df_bike.copy()
  df_scoot = df[df['type'] == 'scooter']
  df_scoot = df_scoot.copy()
  
  df_bike['date'] = pd.to_datetime(df_bike['date'])
  df_bike['year_month'] = df_bike['date'].dt.to_period('M').astype('datetime64[ns]')
  df_bike_counts = df_bike.groupby('year_month').size()
  
  df_scoot['date'] = pd.to_datetime(df_scoot['date'])
  df_scoot['year_month'] = df_scoot['date'].dt.to_period('M').astype('datetime64[ns]')  # Year-Month format (e.g., '2024-01')
  df_scoot_counts = df_scoot.groupby('year_month').size()
  
  df_bike_counts = df_bike_counts.reset_index(name='Bike_Count')
  df_scoot_counts = df_scoot_counts.reset_index(name='Scooter_Count')
  df_combined = pd.merge(df_bike_counts, df_scoot_counts, on='year_month', how ='outer')
  print(df_combined)
  return df_combined

# bicyclesVersusScooters()
# worstDay()
# mapPlot(datetime(2019, 9, 18, 15, 30, 45), datetime(2024, 11, 18, 15, 30, 45), time(0, 00), time(23, 59),  ['bicycle'])