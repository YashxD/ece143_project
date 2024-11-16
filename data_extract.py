import pandas as pd

# read csv file
df = pd.read_csv('data_transfer.csv')

# pick out lines of 'Incident Type' Including 'theft'
filtered_df = df[df['Incident Type'].str.contains(r'\btheft\b', case=False, na=False)]

# pick out 'Summary' containing scooter, bike,bicycle and skateboard
filtered_df = filtered_df[filtered_df['Summary'].str.contains(r'\bscooter\b|\bbike\b|\bbicycle\b|\bskateboard\b', case=False, na=False)]

# duplicated line removed
filtered_df = filtered_df.drop_duplicates()


filtered_df.to_csv('data_extract.csv', index=False)

# print
row_count = filtered_df.shape[0]
print(f"title including 'theft' and summary including 'scooter', 'bike', 'bicycle', or 'skateboard' lines (unique): {row_count}")
