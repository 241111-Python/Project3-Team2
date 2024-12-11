import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

# Paths to the datasets
COVID_DATA_PATH = r'maybeData/WHO-COVID-19-global-table-data.csv'
AIR_QUALITY_DATA_PATH = r'maybeData/airquality.csv'

# Load the datasets
covid_data = pd.read_csv(COVID_DATA_PATH)
air_quality_data = pd.read_csv(AIR_QUALITY_DATA_PATH)

# Inspect the column names to confirm structure
print("COVID-19 Data Columns:", covid_data.columns)
print("Air Quality Data Columns:", air_quality_data.columns)

# Select relevant columns from air quality data
air_quality_data = air_quality_data[['WHO Country Name', 'PM2.5', 'PM10']]
# Rename columns for consistency
air_quality_data.columns = ['Country Name', 'PM2.5', 'PM10']

# Merge datasets on the country name
merged_data = pd.merge(
    covid_data, 
    air_quality_data, 
    left_on='Name', 
    right_on='Country Name', 
    how='inner'
)

# Select relevant columns for analysis
merged_data = merged_data[['Cases - cumulative total per 100000 population', 'PM2.5', 'PM10']]
merged_data.columns = ['COVID-19 Incidence per 100k', 'PM2.5 (μg/m3)', 'PM10 (μg/m3)']

# Handle missing or infinite values
merged_data = merged_data.replace([np.inf, -np.inf], np.nan).dropna()

# Calculate the correlation
correlation = merged_data.corr()
print("Correlation Coefficient:")
print(correlation)

# Plot the correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
plt.title("Correlation Heatmap: COVID-19 Incidence vs Air Quality Metrics")
plt.show()

# Scatter plot: COVID-19 Incidence vs PM2.5
plt.figure(figsize=(8, 6))
x = merged_data['COVID-19 Incidence per 100k']
y = merged_data['PM2.5 (μg/m3)']
plt.scatter(x, y, alpha=0.7, label='Data Points')
try:
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='red', label='Regression Line')
except np.linalg.LinAlgError:
    print("Error: Linear regression could not be computed.")

plt.title("Scatterplot: COVID-19 Incidence vs PM2.5 Levels with Regression Line")
plt.xlabel("COVID-19 Incidence per 100k")
plt.ylabel("PM2.5 (μg/m3)")
plt.legend()
plt.grid(True)
plt.show()

# Scatter plot: COVID-19 Incidence vs PM10
plt.figure(figsize=(8, 6))
x = merged_data['COVID-19 Incidence per 100k']
y = merged_data['PM10 (μg/m3)']
plt.scatter(x, y, alpha=0.7, label='Data Points')
try:
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, color='red', label='Regression Line')
except np.linalg.LinAlgError:
    print("Error: Linear regression could not be computed.")

plt.title("Scatterplot: COVID-19 Incidence vs PM10 Levels with Regression Line")
plt.xlabel("COVID-19 Incidence per 100k")
plt.ylabel("PM10 (μg/m3)")
plt.legend()
plt.grid(True)
plt.show()
