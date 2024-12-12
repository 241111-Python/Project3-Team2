# jesper's analysis program 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns


PATH1 = r'C:\Revature\Project3-Team2\maybeData\NASA_Close_Approach_Data_1960_2060.csv'
PATH2 = r'C:\Revature\Project3-Team2\maybeData\imdb_top_1000.csv'

nasa_df = pd.read_csv(PATH1)
# imdb_df = pd.read_csv(PATH2)
imdb_df = pd.read_csv(PATH2, usecols=['Released_Year', 'Runtime', 'IMDB_Rating', 
                                      'Meta_score', 'No_of_Votes', 'Gross'])


nasa_df['Year'] = pd.to_datetime(nasa_df['cd']).dt.year

print(nasa_df)
print(imdb_df)

nasa_agg = nasa_df.groupby('Year').agg({
    'dist': 'mean',
    'dist_min': 'mean',
    'dist_max': 'mean',
    'v_rel': 'mean',
    'v_inf': 'mean',
    'h': 'mean'
}).reset_index()


print(nasa_agg)


# Convert Released_Year to numeric
imdb_df['Released_Year'] = pd.to_numeric(imdb_df['Released_Year'], errors='coerce')
imdb_df['Gross'] = imdb_df['Gross'].str.replace('[\$,]', '', regex=True)
imdb_df['Gross'] = pd.to_numeric(imdb_df['Gross'], errors='coerce')
imdb_df.dropna(inplace=True)
imdb_df['Runtime'] = imdb_df['Runtime'].str.extract('(\d+)').astype(int)

# imdb_df = pd.to_numeric(imdb_df, errors='coerce')

imdb_agg = imdb_df.groupby('Released_Year').agg({
    'Runtime': 'mean',
    'IMDB_Rating': 'mean',
    'Meta_score': 'mean',
    'No_of_Votes': 'sum',
    'Gross': 'sum'
}).reset_index()

print(imdb_df)
# Merge datasets on Year
merged_data = pd.merge(nasa_agg, imdb_agg, left_on='Year', right_on='Released_Year', how='inner')
# merged_data['Runtime'] = merged_data['Runtime'].str.extract('(\d+)').astype(int)

print(merged_data)

plt.figure(figsize=(10, 8))
sns.heatmap(merged_data.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()


# Assuming 'merged_data' is your DataFrame with 'Year', 'v_rel', and 'No_of_Votes' columns

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot v_rel on the primary y-axis
ax1.set_xlabel('Year')
ax1.set_ylabel('Nominal Distance between NEO and Earth', color='tab:blue')
ax1.plot(merged_data['Year'], merged_data['dist'], color='tab:blue', label='dist')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Gross', color='tab:red')
ax2.plot(merged_data['Year'], merged_data['Gross'], color='tab:red', label='Gross')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Add title and grid
plt.title('NEO Nominal Distance and Movie Gross over the Years')
fig.tight_layout()
plt.grid(True)
plt.show()



# # Assuming 'merged_data' is your DataFrame with 'Year', 'v_rel', and 'Prevalence Rate (%)' columns

# # Create a figure and a set of subplots
# fig, ax1 = plt.subplots(figsize=(12, 6))

# # Plot v_rel on the primary y-axis
# ax1.set_xlabel('Year')
# ax1.set_ylabel('Relative Velocity (v_rel) km/s', color='tab:blue')
# ax1.plot(merged_data['Year'], merged_data['v_rel'], color='tab:blue', label='v_rel')
# ax1.tick_params(axis='y', labelcolor='tab:blue')

# # Create a secondary y-axis
# ax2 = ax1.twinx()
# ax2.set_ylabel('Prevalence Rate (%)', color='tab:red')
# ax2.plot(merged_data['Year'], merged_data['Prevalence Rate (%)'], color='tab:red', label='Prevalence Rate (%)')
# ax2.tick_params(axis='y', labelcolor='tab:red')

# # Add title and grid
# plt.title('NEO Relative Velocity and Disease Prevalence Rate Over the Years')
# fig.tight_layout()
# plt.grid(True)
# plt.show()
