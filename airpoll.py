import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

pollution_df = pd.read_csv("maybeData/global-air-pollution-dataset.csv")
deaths_df = pd.read_csv("maybeData/cause_of_deaths.csv")
population_df = pd.read_csv("maybeData/world_population.csv")

grouped_poll_df = pollution_df.groupby('Country')['AQI Value'].mean().astype(int).reset_index()
print(grouped_poll_df.sort_values(by='AQI Value', ascending=False).head())
print()

deaths_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
deaths_year_df = deaths_df[deaths_df['Year'] == 2019]
grouped_deaths_df = deaths_year_df.groupby('Country')['Chronic Respiratory Diseases'].mean().astype(int).reset_index()
countries_deaths_df = grouped_deaths_df[grouped_deaths_df['Country'].isin(grouped_poll_df['Country'])]
print(countries_deaths_df.sort_values(by='Chronic Respiratory Diseases', ascending=False).head())
print()

population_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
population_year_df = population_df[['Country', '2020 Population']]
countries_pop_df = population_year_df[population_year_df['Country'].isin(grouped_poll_df['Country'])]
print(countries_pop_df.sort_values(by='2020 Population', ascending=False).head())


combined_df = grouped_deaths_df.merge(countries_pop_df, on='Country')
combined_df['Deaths per 100k'] = (combined_df['Chronic Respiratory Diseases'] / combined_df['2020 Population']) * 100000
combined_df = combined_df[['Country', 'Deaths per 100k']]
print(combined_df.sort_values(by='Deaths per 100k', ascending=False).head())

data_df = combined_df.merge(grouped_poll_df, on='Country')
print(data_df.head())

plt.figure(figsize=(10, 6))
sns.regplot(data=data_df, x='AQI Value', y='Deaths per 100k', line_kws={'color': 'red'})
plt.title('Scatter Plot: AQI vs Chronic Respiratory Disease Deaths per 100k People', fontsize=16)
plt.xlabel('AQI Value', fontsize=12)
plt.ylabel('Deaths per 100k People', fontsize=12)
plt.tight_layout()
plt.show()


# numeric_data = data_df.select_dtypes(include=['float64', 'int64'])
# correlation_matrix = numeric_data.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, cbar=True)
# plt.title('Correlation Matrix', fontsize=16)
# plt.tight_layout()
# plt.show()
