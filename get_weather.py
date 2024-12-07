import requests
from datetime import datetime
import pytz
import pandas as pd
from tqdm import tqdm
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures
from functools import partial
import numpy as np

def get_ucsd_weather(date_time, session):
    """
    Get historical weather at UCSD at given time and date
    Input: datetime object, session 
    Returns: dictionary 
    """

    #THese are the coordinates of UCSD
    UCSD_LAT = 32.8801
    UCSD_LON = -117.2340
    
    if date_time.tzinfo is None:
        pacific = pytz.timezone('America/Los_Angeles')
        date_time = pacific.localize(date_time)
    
    utc_time = date_time.astimezone(pytz.UTC)
    formatted_date = utc_time.strftime("%Y-%m-%d")
    
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={UCSD_LAT}&longitude={UCSD_LON}&"
        f"hourly=temperature_2m,precipitation&"
        f"temperature_unit=fahrenheit&"
        f"start_date={formatted_date}&"
        f"end_date={formatted_date}&"
        f"timezone=America/Los_Angeles"
    )
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        
        target_hour = utc_time.hour
        hourly_data = data['hourly']
        
        if not hourly_data['temperature_2m'] or not hourly_data['precipitation']:
            return None, None
        
        temp = hourly_data['temperature_2m'][target_hour]
        precip = hourly_data['precipitation'][target_hour]
        
        if temp is None or precip is None:
            return None, None
            
        return round(temp, 1), round(precip, 2)
        
    except requests.RequestException:
        return None, None

def process_batch(date_times, session):
    #Processes batch of dates
    results = []
    for dt in date_times:
        temp, precip = get_ucsd_weather(dt, session)
        results.append((temp, precip))
        time.sleep(0.5)  
    return results

def create_session():
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

def main():

    #We process the data in batches to ensure that we do not lose our data if the api gets timed out
    df = pd.read_csv('mingextract.csv')
    
    datetime_objects = []
    for date_str, time_str in zip(df['date'], df['time']):
        datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(datetime_str, '%m/%d/%Y %H:%M')
        datetime_objects.append(dt)
    
    BATCH_SIZE = 10  
    NUM_WORKERS = 4  
    
    batches = [datetime_objects[i:i + BATCH_SIZE] 
              for i in range(0, len(datetime_objects), BATCH_SIZE)]
    
    weather_data = []
    
    with tqdm(total=len(datetime_objects), desc="Fetching weather data") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            sessions = [create_session() for _ in range(NUM_WORKERS)]
            
            batch_processors = [partial(process_batch, session=session) 
                              for session in sessions]
            
            futures = []
            for batch, processor in zip(batches, 
                                      np.tile(batch_processors, 
                                            len(batches) // NUM_WORKERS + 1)):
                future = executor.submit(processor, batch)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                batch_results = future.result()
                weather_data.extend(batch_results)
                pbar.update(len(batch_results))
                
                if len(weather_data) % (BATCH_SIZE * 2) == 0:
                    temp_df = df.copy()
                    temps, precips = zip(*weather_data)
                    temp_df['weather'] = list(temps) + [None] * (len(df) - len(temps))
                    temp_df['rain'] = list(precips) + [None] * (len(df) - len(precips))
                    temp_df.to_csv('mingextract_weather_backup.csv', index=False)
    
    temps, precips = zip(*weather_data)
    df['weather'] = temps
    df['rain'] = precips
    
    df.to_csv('mingextract_with_weather.csv', index=False)

if __name__ == "__main__":
    main()
