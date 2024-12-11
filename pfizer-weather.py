import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pfizer_df = pd.read_csv("maybeData/Pfizer_stock.csv", usecols=['Date', 'Close'])
index_df = pd.read_csv("maybeData/SP500_index.csv", usecols=['Date', 'SP500'])
weather_df = pd.read_csv("maybeData/Monthly_weather_report.csv", usecols=['Time', 'Monthly Average Temperature', 'Monthly Total Precepitation'])

weather_df.rename(columns={'Time' : 'Date'}, inplace=True)
grouped_weather_df = weather_df.groupby('Date').agg({
    'Monthly Average Temperature': 'mean',
    'Monthly Total Precepitation': 'mean'
}).reset_index()
grouped_weather_df['Date'] = pd.to_datetime(grouped_weather_df['Date'])
grouped_weather_df['Date'] = grouped_weather_df['Date'].dt.to_period('M')

#print(grouped_weather_df.tail())

pfizer_df['Date'] = pd.to_datetime(pfizer_df['Date'])
pfizer_df['Date'] = pfizer_df['Date'].dt.to_period('M')
grouped_pfizer_df = pfizer_df.groupby('Date')['Close'].mean().reset_index()

#print(grouped_pfizer_df.head())

index_df['Date'] = pd.to_datetime(index_df['Date'])
index_df['Date'] = index_df['Date'].dt.to_period('M')

merged_df = pd.merge(grouped_pfizer_df, index_df, on='Date', how='inner')
merged_df = merged_df.merge(grouped_weather_df, on='Date', how='inner')

merged_df['Normalized'] = (merged_df['Close'] / merged_df['SP500']) * 100
merged_df['Date'] = merged_df['Date'].dt.to_timestamp()
print(merged_df)

filtered_df = merged_df[merged_df['Date'] > '2018-01-01']

fig, ax1 = plt.subplots(figsize=(10, 6))
#ax1.plot(filtered_df['Date'], filtered_df['Monthly Average Temperature'], label='Avg Temperature', color='tab:red')
ax1.plot(filtered_df['Date'], filtered_df['Monthly Total Precepitation'], label='Precipitation', color='tab:blue')
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Precipitation', fontsize=12)
ax2 = ax1.twinx()
ax2.plot(filtered_df['Date'], filtered_df['Normalized'], label='Normalized Pfizer Close', color='tab:green')
ax2.set_ylabel('Normalized Pfizer Close', fontsize=12)
plt.title('Monthly Data: Temperature, Precipitation, and Normalized Pfizer Close (After 2020)', fontsize=14)
plt.xticks(rotation=45)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.show()
