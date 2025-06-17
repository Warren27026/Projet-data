# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 19:54:23 2025

@author: Warren
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Charger les données
df = pd.read_csv('Sample - Superstore.csv',encoding='ISO-8859-1')

# Nettoyage des données (exemple)
df.dropna(subset=['Sales', 'Profit'], inplace=True)

# Visualisation - Scatter plot entre Ventes et Marges
sns.scatterplot(x='Sales', y='Profit', data=df)
plt.title('Relation entre les Ventes et les Marges')
plt.show()

# Heatmap de corrélation
corr_matrix = df[['Sales', 'Quantity', 'Profit', 'Discount']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Heatmap de Corrélation')
plt.show()

# Calcul de la corrélation entre les ventes et les marges
corr, _ = pearsonr(df['Sales'], df['Profit'])
print(f"Corrélation entre les ventes et les marges : {corr}")
