import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns


df = pd.read_csv("./maybeData/cause_of_deaths.csv")
# print(df['Year'].value_counts())
df = df.groupby("Year", as_index=False)[['Alcohol Use Disorders', 'Cardiovascular Diseases', 'Environmental Heat and Cold Exposure', 'Conflict and Terrorism', 'Diabetes Mellitus', 'Fire, Heat, and Hot Substances', 'Maternal Disorders']].sum()

print(df.columns)
print(df.head())

years = df['Year']
alcohol = df['Alcohol Use Disorders']
cardio = df['Cardiovascular Diseases']
diabetes = df['Diabetes Mellitus']
maternal = df['Maternal Disorders']

scaler = MinMaxScaler()
alcohol_normalized = scaler.fit_transform(alcohol.values.reshape(-1, 1)).flatten()
cardio_normalized = scaler.fit_transform(cardio.values.reshape(-1, 1)).flatten()
diabetes_normalized = scaler.fit_transform(diabetes.values.reshape(-1, 1)).flatten()
maternal_normalized = scaler.fit_transform(maternal.values.reshape(-1, 1)).flatten()


plt.scatter(years, alcohol_normalized, label="alcohol related deaths")
plt.scatter(years, cardio_normalized, label="cardiovascular disease deaths")
plt.legend()

plt.savefig('graphs/alcohol_cardio_year.png')
plt.clf()

plt.scatter(years, maternal_normalized, label="maternal deaths")
plt.scatter(years, diabetes_normalized, label="diabetes deaths")
plt.legend()
plt.savefig('graphs/maternal_diabetes_year.png')
plt.clf()

plt.scatter(maternal_normalized, diabetes_normalized)
plt.savefig('graphs/maternal_diabetes.png')
plt.clf()

sns.heatmap(df.corr())
plt.title("Heatmap of Causes of Deaths Over Years", fontsize=16)
plt.savefig('graphs/cause_of_death_heatmap.png', bbox_inches='tight')
plt.clf()

