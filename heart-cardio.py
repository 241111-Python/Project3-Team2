# jesper's analysis program 
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns

PATH1 = r'maybeData/heart.csv'
PATH2 = r'maybeData/cardio_train.csv'

cardio_data = pd.read_csv(PATH2, sep=';')
heart_data = pd.read_csv(PATH1)

cardio_data['gender'] = cardio_data['gender'].replace({2:1, 1:0})
cardio_data['age'] = cardio_data['age'] / 365
cardio_data.rename(columns={'gender':'sex'}, inplace=True)
# cardio_data.rename(columns={'Age':'age'}, inplace=True)

print(cardio_data)
print(heart_data)

merged_data = pd.merge(cardio_data, heart_data, on='age', how='inner')
print(merged_data) 

plt.figure(figsize=(10, 8))
sns.heatmap(merged_data.corr(), annot=True, fmt='.2f')
plt.title('Correlation Heatmap')
plt.show()