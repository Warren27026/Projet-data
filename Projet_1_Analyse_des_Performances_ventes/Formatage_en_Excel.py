# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:19:50 2025

@author: Warren
"""

import pandas as pd

input_file = "Sample - Superstore.csv"
output_file = "Sample - Superstore.xlsx"


# Lire le fichier CSV
data = pd.read_csv(input_file, sep=',', encoding='ISO-8859-1')


# Vérification des premières lignes pour validation
print("Aperçu des données :")
print(data.head())

# Enregistrer les données dans un fichier Excel
data.to_excel(output_file, index=False, engine='openpyxl')

print(f"Données enregistrées dans {output_file}")
