# jesper's analysis program 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns

PATH1 = r'C:\Revature\Project3-Team2\maybeData\imdb_top_1000.csv'
PATH2 = r'C:\Revature\Project3-Team2\maybeData\boxoffice_data_2024.csv'

imdb_data = pd.read_csv(PATH1, usecols=['Series_Title', 'Released_Year', 'Runtime', 
                                        'IMDB_Rating', 'Meta_score', 'No_of_Votes'])
box_office_data = pd.read_csv(PATH2)

imdb_data['Released_Year'] = imdb_data['Released_Year'].astype(str)
box_office_data['Year'] = box_office_data['Year'].astype(str)


print(imdb_data)
print(box_office_data)

merged_data = pd.merge(imdb_data, box_office_data, 
                       left_on=['Series_Title', 'Released_Year'], 
                       right_on=['Title', 'Year'], 
                       how='inner')
print(merged_data) 
# merged_data.fillna(value=0, inplace=True)
# merged_data.drop['Series_Title', 'Title']
merged_data['Runtime'] = merged_data['Runtime'].str.extract('(\d+)').astype(int)
merged_data['Gross'] = merged_data['Gross'].str.extract('(\d+)').astype(int)

numeric_data = merged_data.drop(['Series_Title', 'Title'], axis=1)

numeric_data_agg = numeric_data.groupby('Released_Year').agg({
    'Runtime': 'mean',
    'IMDB_Rating': 'mean',
    'Meta_score': 'mean',
    'No_of_Votes': 'sum',
    'Gross': 'sum'
}).reset_index()

plt.figure(figsize=(10, 8))
sns.heatmap(numeric_data_agg.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()

# plt.figure()
# plt.scatter(numeric_data.index, numeric_data['Gross', 'No_of_Votes'])
# plt.show()
# grouped_data = merged_data.groupby('Released_Year')[['Gross', 'No_of_Votes']].mean()

# Plot grouped data
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Year')
ax1.set_ylabel('Gross Sum (in millions)', color='blue')
ax1.plot(numeric_data_agg.index, numeric_data_agg['Gross'], color='blue', alpha=0.6, label='Avg Gross')

ax2 = ax1.twinx()
ax2.set_ylabel('Sum of Number of Votes', color='green')
ax2.plot(numeric_data_agg.index, numeric_data_agg['No_of_Votes'], color='green', label='Avg Votes', linewidth=2)

# Add title and grid
plt.title('Average Gross and Votes by Year', fontsize=16)
ax1.grid(linestyle='--', alpha=0.5)

plt.show()

