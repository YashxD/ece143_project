import requests
from datetime import datetime
import pytz

def get_ucsd_weather(date_time):
    """
    Purpose: Get weather at UCSD at given time and date
    
    Args: Date and time to get weather for
        
    Returns: dictionary of weather data including temperature and precipitation
    """
    UCSD_LAT = 32.8801
    UCSD_LON = -117.2340
    assert isinstance(date_time, datetime), "date_time must be a datetime object"
        
    if date_time.tzinfo is None:
        pacific = pytz.timezone('America/Los_Angeles')
        date_time = pacific.localize(date_time)
    utc_time = date_time.astimezone(pytz.UTC)
    
    formatted_date = utc_time.strftime("%Y-%m-%d")
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={UCSD_LAT}&longitude={UCSD_LON}&"
        f"hourly=temperature_2m,precipitation&"
        f"temperature_unit=fahrenheit&"
        f"start_date={formatted_date}&"
        f"end_date={formatted_date}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        target_hour = utc_time.hour
        hourly_data = data['hourly']
        
        temp = hourly_data['temperature_2m'][target_hour]
        precip = hourly_data['precipitation'][target_hour]
        
        return {
            'temperature_f': round(temp, 1),
            'precipitation_mm': round(precip, 2),
            'location': 'UC San Diego',
            'timestamp': date_time.isoformat()
        }
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch weather data: {str(e)}")
