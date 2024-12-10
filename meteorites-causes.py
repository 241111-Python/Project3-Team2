import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


meteors = pd.read_csv(r"maybeData\Meteorite_Countries.csv", usecols=['year', 'GeoLocation'])
causes = pd.read_csv(r"maybeData\cause_of_deaths.csv")
pop = pd.read_csv(r"maybeData\world_population.csv")


pop.rename(columns={'Country/Territory': 'GeoLocation'}, inplace=True)
causes.drop(columns='Code', inplace=True)
causes.rename(columns={'Country/Territory': "GeoLocation", 'Year':'year'}, inplace=True)

#Thank you Romeo for the code below
group = causes.drop(columns='year').groupby('GeoLocation').mean().reset_index()

pop_df = pop[['GeoLocation','2020 Population', '2010 Population', '2000 Population', '1990 Population']]
pop_df['Avg_Population'] = pop_df[['2020 Population', '2010 Population', '2000 Population', '1990 Population']].mean(axis=1)
merged_df = pd.merge(group, pop_df[['GeoLocation', 'Avg_Population']], on='GeoLocation', how='left')

death_causes_df = merged_df.drop(columns='GeoLocation')

for column in death_causes_df.columns:
    death_causes_df[column] = (death_causes_df[column] / merged_df['Avg_Population']) * 100000

death_causes_df = death_causes_df.drop(columns=['Avg_Population'])
#Thank you Romeo for the code above

death_causes_df['GeoLocation'] = merged_df['GeoLocation']
group = meteors.groupby('GeoLocation').count().rename(columns={'year': 'Meteors'})
causes_meteors = pd.merge(group, death_causes_df, 'inner', 'GeoLocation')



sb.heatmap(causes_meteors.corr(numeric_only=True))
print(causes_meteors.corr(numeric_only=True))
plt.savefig('meteor-cause-corr.png')