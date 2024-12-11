import pandas as pd
import matplotlib.pyplot as plt

pfizer_df = pd.read_csv("maybeData/Pfizer_stock.csv", usecols=['Date', 'Close'])
index_df = pd.read_csv("maybeData/SP500_index.csv", usecols=['Date', 'SP500'])

pfizer_df['Date'] = pd.to_datetime(pfizer_df['Date'])
pfizer_df['Date'] = pfizer_df['Date'].dt.to_period('M')
grouped_pfizer_df = pfizer_df.groupby('Date')['Close'].mean().reset_index()

index_df['Date'] = pd.to_datetime(index_df['Date'])
index_df['Date'] = index_df['Date'].dt.to_period('M')

merged_df = pd.merge(grouped_pfizer_df, index_df, on='Date', how='inner')
merged_df['Normalized'] = (merged_df['Close'] / merged_df['SP500']) * 100
merged_df['Date'] = merged_df['Date'].dt.to_timestamp()

merged_df['year'] = merged_df['Date'].dt.to_period('Y')
merged_df = merged_df.groupby('year')['Normalized'].mean()

###########################################################

dem = pd.read_csv("./maybeData/democracy-index-eiu.csv")
dem_usa = dem[dem['Entity'] == 'United States']
dem_usa = dem_usa.rename(columns={'Year': 'year', 'Democracy score': 'score'})
dem_usa = dem_usa.drop(['Code', 'Entity'], axis=1)
dem_usa['year'] = pd.to_datetime(dem_usa['year'], format='%Y').dt.to_period('Y')

print(dem_usa.head())
print(merged_df.head())

df = pd.merge(dem_usa, merged_df, how='outer', on='year')
df['year'] = df['year'].dt.start_time
print(df)

plt.figure(figsize=(10, 6))
plt.plot(df['year'], df['score'], color='orange')
plt.plot(df['year'], df['Normalized'], color='blue')

plt.xlabel('Year')
plt.ylabel('Index Score')
plt.savefig("./graphs/prizer_demindex.png")
