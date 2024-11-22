import pandas as pd

def time_v_price():
    df = pd.read_csv('mingextract.csv')
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
    print(avg_time_dict)

time_v_price()