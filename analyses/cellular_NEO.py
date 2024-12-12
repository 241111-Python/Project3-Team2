"""
Analysis program written by Jesper 
links to data: 
https://www.kaggle.com/datasets/justinwilcher/nasa-neoclose-approaches-1960-2060
https://www.kaggle.com/datasets/suraj520/cellular-network-analysis-dataset
"""
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns


PATH1 = r'C:\Revature\Project3-Team2\maybeData\NASA_Close_Approach_Data_1960_2060.csv'
PATH2 = r'C:\Revature\Project3-Team2\maybeData\signal_metrics.csv'

nasa_df = pd.read_csv(PATH1)
cellular_df = pd.read_csv(PATH2)

nasa_df['Date'] = pd.to_datetime(nasa_df['cd']).dt.date
cellular_df['Date'] = pd.to_datetime(cellular_df['Timestamp']).dt.date

print(nasa_df)
print(cellular_df)
# mortality_df.drop(['Sex'], axis=1, inplace=True)
nasa_agg = nasa_df.groupby('Date').agg({
    'dist': 'mean',
    'dist_min': 'mean',
    'dist_max': 'mean',
    'v_rel': 'mean',
    'v_inf': 'mean',
    'h': 'mean'
}).reset_index()

cellular_df.drop(['Locality', 'Network Type', 'Timestamp', 'Signal Quality (%)'], axis=1, inplace=True)
cellular_agg = cellular_df.groupby('Date').mean().reset_index()

print(nasa_agg)
print(cellular_agg)

merged_data = pd.merge(nasa_agg, cellular_agg, on='Date', how='inner')
merged_data.drop(['Date'], axis=1,inplace=True)

print(merged_data)


plt.figure(figsize=(10, 8))
sns.heatmap(merged_data.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot v_rel on the primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('Data Throughput (Mbps)', color='tab:blue')
ax1.plot(merged_data.index, merged_data['Data Throughput (Mbps)'], color='tab:blue', label='v_rel')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Velocity Relative to Earth', color='tab:red')
ax2.plot(merged_data.index, merged_data['v_rel'], color='tab:red', label='Prevalence Rate (%)')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Add title and grid
plt.title('Velocity of NEO and Data Throughput vs date')
fig.tight_layout()
plt.grid(True)
plt.show()

