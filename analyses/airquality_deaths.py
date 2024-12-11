import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pollution_df = pd.read_csv("maybeData/global-air-pollution-dataset.csv")
deaths_df = pd.read_csv("maybeData/cause_of_deaths.csv")
population_df = pd.read_csv("maybeData/world_population.csv")

grouped_poll_df = pollution_df.groupby('Country')['AQI Value'].mean().astype(int).reset_index()
#print(grouped_poll_df.sort_values(by='AQI Value', ascending=False).head())
#print()

deaths_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
numeric_columns = deaths_df.select_dtypes(include=['number']).columns
grouped_deaths_df = deaths_df.groupby('Country')[numeric_columns].mean().astype(int).reset_index()
countries_deaths_df = grouped_deaths_df[grouped_deaths_df['Country'].isin(grouped_poll_df['Country'])]
#print(countries_deaths_df.sort_values(by='Chronic Respiratory Diseases', ascending=False).head())
#print()

population_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
pop_df = population_df[['Country', '2020 Population', '2010 Population', '2000 Population', '1990 Population']]
pop_df = pop_df.copy()
pop_df['Avg_Population'] = pop_df[['2020 Population', '2010 Population', '2000 Population', '1990 Population']].mean(axis=1)
countries_pop_df = pop_df[pop_df['Country'].isin(grouped_poll_df['Country'])]


combined_df = grouped_deaths_df.merge(countries_pop_df, on='Country')
combined_df.drop(columns=['Year', '2020 Population', '2010 Population', '2000 Population', '1990 Population'], inplace=True)

normalized_df = combined_df.copy()
numerical_cols = combined_df.select_dtypes(include=['number']).columns.difference(['Avg_Population'])
normalized_df[numerical_cols] = (combined_df[numerical_cols].div(combined_df['Avg_Population'], axis=0)) * 100000
#print(normalized_df.head())

data_df = normalized_df.merge(grouped_poll_df, on='Country')
#print(data_df.head())

numeric_data = data_df.select_dtypes(include=['float64', 'int64'])
correlations = numeric_data.corrwith(data_df['AQI Value'])
colors = ['blue' if corr < 0 else 'red' for corr in correlations]

plt.figure(figsize=(12, 6))
sns.barplot(x=correlations.index, y=correlations.values, palette=colors)
plt.xticks(rotation=45, ha="right")
plt.title("Causes of Death Correlated with the AQI Value")
plt.xlabel("")
plt.ylabel("Correlation Coefficient")
plt.tight_layout()
plt.savefig("./graphs/airquality_deaths_barplot.png")