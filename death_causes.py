import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

deaths_df = pd.read_csv("maybeData/cause_of_deaths.csv")
population_df = pd.read_csv("maybeData/world_population.csv")

deaths_df.columns = deaths_df.columns.str.strip()
deaths_df.columns = deaths_df.columns.str.replace(' ', '_')
deaths_df.columns = deaths_df.columns.str.replace('/', '_')
deaths_df.columns = deaths_df.columns.str.replace("'", "")

df = deaths_df.drop(columns=['Code'])
df.rename(columns={'Country_Territory': 'Country'}, inplace=True)
grouped_deaths_df = df.groupby('Country').mean().reset_index()

population_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
pop_df = population_df[['Country','2020 Population', '2010 Population', '2000 Population', '1990 Population']]
pop_df['Avg_Population'] = pop_df[['2020 Population', '2010 Population', '2000 Population', '1990 Population']].mean(axis=1)

merged_df = pd.merge(grouped_deaths_df, pop_df[['Country', 'Avg_Population']], on='Country', how='left')

death_causes_df = merged_df.drop(columns=['Country', 'Year'])

for column in death_causes_df.columns:
    death_causes_df[column] = (death_causes_df[column] / merged_df['Avg_Population']) * 100000

death_causes_df = death_causes_df.drop(columns=['Avg_Population'])

correlation_matrix = death_causes_df.corr()
plt.figure(figsize=(18, 16))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, cbar_kws={"shrink": 0.75})
plt.xticks(rotation=90, ha='right')
plt.yticks(rotation=0, va='center')
plt.tight_layout()
plt.savefig("Death_correlation.png")