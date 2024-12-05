import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

deaths_df = pd.read_csv("maybeData/cause_of_deaths.csv")
deaths_df.columns = deaths_df.columns.str.strip()
deaths_df.columns = deaths_df.columns.str.replace(' ', '_')
deaths_df.columns = deaths_df.columns.str.replace('/', '_')
deaths_df.columns = deaths_df.columns.str.replace("'", "")

df = deaths_df.drop(columns=['Code'])
df.rename(columns={'Country_Territory': 'Country'}, inplace=True)
grouped_deaths_df = df.groupby('Country').mean().reset_index()

death_causes_df = grouped_deaths_df.drop(columns=['Country', 'Year', 'Conflict_and_Terrorism', 'Malaria', 'HIV_AIDS', 'Exposure_to_Forces_of_Nature'])

print(death_causes_df)

correlation_matrix = death_causes_df.corr()
plt.figure(figsize=(18, 16))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, cbar_kws={"shrink": 0.75})
plt.xticks(rotation=90, ha='right')
plt.yticks(rotation=0, va='center')
plt.tight_layout()
plt.show()