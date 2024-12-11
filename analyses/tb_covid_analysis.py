import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

PATH1 = r'maybeData/WHO-COVID-19-global-table-data.csv'
PATH2 = r'maybeData/TB_Burden_Country.csv'

covid_data = pd.read_csv(PATH1)
tb_data = pd.read_csv(PATH2)

merged_data = pd.merge(covid_data, tb_data, 
                       left_on='Name', 
                       right_on='Country or territory name')

merged_data = merged_data[[
    'Cases - cumulative total per 100000 population', 
    'Estimated incidence (all forms) per 100 000 population'
]]
merged_data.columns = ['COVID-19 Incidence per 100k', 'TB Incidence per 100k']
merged_data = merged_data.replace([np.inf, -np.inf], np.nan).dropna()

correlation = merged_data.corr()

print("Correlation Coefficient:")
print(correlation)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title("Correlation Heatmap: COVID-19 vs TB Incidence")
plt.show()

plt.figure(figsize=(8, 6))
x = merged_data['COVID-19 Incidence per 100k']
y = merged_data['TB Incidence per 100k']
plt.scatter(x, y, alpha=0.7, label='Data Points')
try:
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='red', label='Regression Line')
except np.linalg.LinAlgError:
    print("Error: Linear regression could not be computed.")

plt.title("Scatterplot: COVID-19 vs TB Incidence with Regression Line")
plt.xlabel("COVID-19 Incidence per 100k")
plt.ylabel("TB Incidence per 100k")
plt.legend()
plt.grid(True)
plt.show()
