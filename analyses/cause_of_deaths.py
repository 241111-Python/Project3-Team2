import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

deaths_df = pd.read_csv("maybeData/cause_of_deaths.csv")
population_df = pd.read_csv("maybeData/world_population.csv")

deaths_df.columns = deaths_df.columns.str.strip()
deaths_df.columns = deaths_df.columns.str.replace(' ', '_')
deaths_df.columns = deaths_df.columns.str.replace('/', '_')

df = deaths_df.drop(columns=['Code'])
df.rename(columns={'Country_Territory': 'Country'}, inplace=True)
grouped_deaths_df = df.groupby('Country').mean().reset_index()

population_df.rename(columns={'Country/Territory': 'Country'}, inplace=True)
pop_df = population_df[['Country','2020 Population', '2010 Population', '2000 Population', '1990 Population']]
pop_df = pop_df.copy()
pop_df['Avg_Population'] = pop_df[['2020 Population', '2010 Population', '2000 Population', '1990 Population']].mean(axis=1)

merged_df = pd.merge(grouped_deaths_df, pop_df[['Country', 'Avg_Population']], on='Country', how='left')

death_causes_df = merged_df.drop(columns=['Country', 'Year'])

for column in death_causes_df.columns:
    death_causes_df[column] = (death_causes_df[column] / merged_df['Avg_Population']) * 100000

death_causes_df = death_causes_df.drop(columns=['Avg_Population'])

death_causes_df.rename(columns={
    'Meningitis': 'Meningitis',
    "Alzheimer's_Disease_and_Other_Dementias": "Alzheimer's",
    'Parkinson_s_Disease': "Parkinson's",
    'Nutritional_Deficiencies': 'Nutrition Def.',
    'Malaria': 'Malaria',
    'Drowning': 'Drowning',
    'Interpersonal_Violence': 'Violence',
    'Maternal_Disorders': 'Maternal',
    'HIV_AIDS': 'HIV/AIDS',
    'Drug_Use_Disorders': 'Drug Use',
    'Tuberculosis': 'TB',
    'Cardiovascular_Diseases': 'Cardio Diseases',
    'Lower_Respiratory_Infections': 'LRI',
    'Neonatal_Disorders': 'Neonatal',
    'Alcohol_Use_Disorders': 'Alcohol Use',
    'Self-harm': 'Self-harm',
    'Exposure_to_Forces_of_Nature': 'Forces of Nature',
    'Diarrheal_Diseases': 'Diarrhea',
    'Environmental_Heat_and_Cold_Exposure': 'Heat/Cold Exposure',
    'Neoplasms': 'Neoplasms',
    'Conflict_and_Terrorism': 'Conflict/Terrorism',
    'Diabetes_Mellitus': 'Diabetes',
    'Chronic_Kidney_Disease': 'CKD',
    'Poisonings': 'Poisoning',
    'Protein-Energy_Malnutrition': 'PEM',
    'Road_Injuries': 'Road Injuries',
    'Chronic_Respiratory_Diseases': 'Chronic Resp.',
    'Cirrhosis_and_Other_Chronic_Liver_Diseases': 'Cirrhosis',
    'Digestive_Diseases': 'Digestive Dis.',
    'Fire,_Heat,_and_Hot_Substances': 'Fire/Heat',
    'Acute_Hepatitis': 'Acute Hep.'
}, inplace=True)

death_causes_df = death_causes_df.drop(columns=['Diabetes', 'CKD', 'Cirrhosis', 'Digestive Dis.', 'PEM', 'Conflict/Terrorism', 'Forces of Nature', 'Drowning', 'Heat/Cold Exposure'])

correlation_matrix = death_causes_df.corr()
plt.figure(figsize=(18, 16))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5, cbar_kws={"shrink": 0.75})
plt.xticks(rotation=90, ha='right')
plt.yticks(rotation=0, va='center')
plt.tight_layout()
plt.savefig("./graphs/death_causes_heatmap.png")