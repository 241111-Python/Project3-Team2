import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
print(f"Running {__file__} with pandas {pd.__version__}")
print(f"Current time: {datetime.now()}\n")

stroke_df = pd.read_csv("maybeData/healthcare-dataset-stroke-data.csv")
diabetes_df = pd.read_csv("maybeData/diabetes_dataset.csv")

print(f"{stroke_df.shape=}")
print(f"{diabetes_df.shape=}")

stroke_df.rename(columns={"age": "Age"}, inplace=True)
stroke_df['Age'] = stroke_df['Age'].astype(int)

diabetes_df.rename(columns={'Outcome': 'hasDiabetes'}, inplace=True)

print("diabetes data:", "\n", diabetes_df.head())
print("stroke data:", "\n", stroke_df.head())

# Dropping non numerical coluumns
stroke_df = stroke_df.drop(['Residence_type', 'smoking_status', 'gender'], axis=1)

# Average the values in each column after grouping by age. 
diabetes_groupby_age_mean = diabetes_df.groupby('Age')[['Glucose', 'BloodPressure', 'BMI', 'DiabetesPedigreeFunction', 'hasDiabetes']].mean()
stroke_groupby_age_mean = stroke_df.groupby('Age')[['hypertension', 'heart_disease', 'stroke']].mean()

print(stroke_groupby_age_mean.head())
print(diabetes_groupby_age_mean.head())

merged_df = pd.merge(diabetes_groupby_age_mean, stroke_groupby_age_mean, on='Age', how='inner')

print(merged_df.shape)

# Plot correlations
correlation_matrix = merged_df.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.savefig('graphs/diabetes_stroke.png', bbox_inches='tight')
plt.close()




