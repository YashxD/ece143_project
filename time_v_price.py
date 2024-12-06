import pandas as pd

def time_v_price(csv_file):
    '''
    Get the time vs price distribution for the data stored in an extracted
    CSV file.

    @param[in]  csv_file - Extracted CSV file

    @returns    Dictionary of average value of reported loss for each hour of day
    '''
    assert isinstance(csv_file, str)
    assert len(csv_file) > 0

    df = pd.read_csv(csv_file)
    # df = df[['time', 'price']]
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['price'] = df['price'].fillna(0).astype(int)
    df['time'] = pd.to_datetime(df['time'], format='%H:%M')
    df['hour'] = df['time'].dt.hour
    # df = df.sort_values(by='hour')

    time_dict = {}
    for h in range(24):
        time_dict[h] = df[(df['hour'] == h) & (df['price'] != -1)]['price']
    
    avg_time_dict = {h: time_dict[h].mean() for h in time_dict}

    return avg_time_dict