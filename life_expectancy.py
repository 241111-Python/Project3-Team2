import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

print(f"Running {__file__}")
print(f"Pandas version: {pd.__version__}")

df = pd.read_csv("maybeData/Life-Expectancy-Data-Averaged.csv")
df.sort_values('GDP_per_capita', inplace=True)
print(df.columns)




# Alcohol consumption vs Schooling
# Best fit curves
log_gdp = np.log(df['GDP_per_capita'])

coeffs_alcohol = np.polyfit(log_gdp, df['Alcohol_consumption'], 2)
coeffs_schooling = np.polyfit(log_gdp, df['Schooling'], 2)

best_fit_alcohol = np.polyval(coeffs_alcohol, log_gdp)
best_fit_schooling = np.polyval(coeffs_schooling, log_gdp)


# Alcohol consumption vs schooling
plt.scatter(df['GDP_per_capita'], df['Alcohol_consumption'], color='blue', label="Alcohol Comsumption", alpha=0.5)
plt.scatter(df['GDP_per_capita'], df['Schooling'], color='orange', label="Schooling", alpha=0.5)
plt.plot(df['GDP_per_capita'], best_fit_alcohol, color='blue', linestyle='dashed', label='Best Fit (Alcohol)')
plt.plot(df['GDP_per_capita'], best_fit_schooling, color='orange', linestyle='dashed', label='Best Fit (Schooling)')

plt.xscale('log')
plt.xlabel('GDP per capita')

plt.title('Schooling vs Alcohol Consumption over GDP per Capita')

plt.legend()
plt.savefig('alcohol-schooling-vs-gdp.png', bbox_inches='tight')

plt.clf()

plt.scatter(df['Alcohol_consumption'], df['Schooling'])
plt.title('Alcohol consumption vs Schooling')
plt.xlabel('')
plt.savefig('alcohol-schooling.png', bbox_inches='tight')
