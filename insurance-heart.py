# jesper's analysis program 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns

PATH1 = r'maybeData/heart.csv'
PATH2 = r'maybeData/insurance_data.csv'

insurance_data = pd.read_csv(PATH2, usecols=['Year', 
                                             'Month', 
                                             'Age', 
                                             'Gender', 
                                             'BMI', 
                                             'Annual Visits', 
                                             'Insurance Cost'])
heart_data = pd.read_csv(PATH1)

insurance_data['Gender'] = insurance_data['Gender'].replace({'Male':1, 'Female':0})
insurance_data.rename(columns={'Age':'age'}, inplace=True)

print(insurance_data)
print(heart_data)

merged_data = pd.merge(insurance_data, heart_data, 
                       right_on=['age', 'sex'], 
                       left_on=['age', 'Gender'], 
                       how='inner')
print(merged_data.corr()) 

plt.figure(figsize=(10, 8))
sns.heatmap(merged_data.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()