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
grouped_deaths_df = deaths_df.groupby('Country')['Chronic Respiratory Diseases'].mean().astype(int).reset_index()
countries_deaths_df = grouped_deaths_df[grouped_deaths_df['Country'].isin(grouped_poll_df['Country'])]
#print(countries_deaths_df.sort_values(by='Chronic Respiratory Diseases', ascending=False).head())
#print()

population_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
pop_df = population_df[['Country', '2020 Population', '2010 Population', '2000 Population', '1990 Population']]
pop_df = pop_df.copy()
pop_df['Avg_Population'] = pop_df[['2020 Population', '2010 Population', '2000 Population', '1990 Population']].mean(axis=1)
countries_pop_df = pop_df[pop_df['Country'].isin(grouped_poll_df['Country'])]

# health_df.rename(columns={'HExp_Pctage_Y' : 'Health_Expenditure_Perc_GDP'})
# grouped_health_df = health_df.groupby('Country_Name')['Health_Expenditure_Perc_GDP'].mean().reset_index()
# print(grouped_health_df)

combined_df = grouped_deaths_df.merge(countries_pop_df, on='Country')
combined_df['Deaths per 100k'] = (combined_df['Chronic Respiratory Diseases'] / combined_df['Avg_Population']) * 100000
combined_df = combined_df[['Country', 'Deaths per 100k']]
#print(combined_df.sort_values(by='Deaths per 100k', ascending=False).head())

data_df = combined_df.merge(grouped_poll_df, on='Country')
#print(data_df.head())

plt.figure(figsize=(10, 6))
sns.regplot(data=data_df, x='AQI Value', y='Deaths per 100k', line_kws={'color': 'red'})
plt.title('Chronic Respiratory Disease Deaths per 100k People vs AQI Value', fontsize=16)
plt.xlabel('AQI Value', fontsize=12)
plt.ylabel('Deaths per 100k People', fontsize=12)
plt.tight_layout()
plt.savefig("./graphs/airquality_respdeaths_scatter.png")