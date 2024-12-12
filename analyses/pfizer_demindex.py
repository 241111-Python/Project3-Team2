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

df = pd.merge(dem_usa, merged_df, how='inner', on='year')
df['year'] = df['year'].dt.start_time
print(df)

print(df.corr())

fix, ax1 = plt.subplots()

# plt.figure(figsize=(10, 6))
ax1.plot(df['year'], df['score'], color='orange', label="Democracy Index", marker='x')
ax1.set_xlabel('Time (years)')
ax1.set_ylabel('Democracy Index', color='black')

ax2 = ax1.twinx()
ax2.plot(df['year'], df['Normalized'], color='blue', label="Normalized Pfizer Stock Price", marker='o')
ax2.set_ylabel('Normalized Stock Price', color='black')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Demoracy Index over Time')
plt.savefig("./graphs/pfizer_demindex.png")
