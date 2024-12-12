# jesper's analysis program 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns


PATH1 = r'C:\Revature\Project3-Team2\maybeData\NASA_Close_Approach_Data_1960_2060.csv'
PATH2 = r'C:\Revature\Project3-Team2\maybeData\Global Health Statistics.zip'

nasa_df = pd.read_csv(PATH1)
health_df = pd.read_csv(PATH2)

nasa_df['Year'] = pd.to_datetime(nasa_df['cd']).dt.year

print(nasa_df)
print(health_df)

nasa_agg = nasa_df.groupby('Year').agg({
    'dist': 'mean',
    'dist_min': 'mean',
    'dist_max': 'mean',
    'v_rel': 'mean',
    'v_inf': 'mean',
    'h': 'mean'
}).reset_index()

health_agg = health_df.groupby('Year').agg({
    'Prevalence Rate (%)': 'mean',
    'Incidence Rate (%)': 'mean',
    'Mortality Rate (%)': 'mean',
    'DALYs': 'mean',
    'Recovery Rate (%)': 'mean',
    'Per Capita Income (USD)': 'mean',
    'Urbanization Rate (%)': 'mean'
}).reset_index()

print(nasa_agg)
print(health_agg)

merged_data = pd.merge(nasa_agg, health_agg, on='Year', how='inner')

print(merged_data)

plt.figure(figsize=(10, 8))
sns.heatmap(merged_data.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()


# Assuming 'merged_data' is your DataFrame with 'Year', 'v_rel', and 'Prevalence Rate (%)' columns

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot v_rel on the primary y-axis
ax1.set_xlabel('Year')
ax1.set_ylabel('Relative Velocity (v_rel) km/s', color='tab:blue')
ax1.plot(merged_data['Year'], merged_data['v_rel'], color='tab:blue', label='v_rel')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Prevalence Rate (%)', color='tab:red')
ax2.plot(merged_data['Year'], merged_data['Prevalence Rate (%)'], color='tab:red', label='Prevalence Rate (%)')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Add title and grid
plt.title('NEO Relative Velocity and Disease Prevalence Rate Over the Years')
fig.tight_layout()
plt.grid(True)
plt.show()
