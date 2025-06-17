# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 17:47:48 2025

@author: Warren
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Afficher les décimales avec au plus 2 décimales
pd.options.display.float_format = '{:.2f}'.format

# Charger le dataset
donnees = pd.read_csv('HRDataset_v14.xls',sep=',')

# Afficher les premières lignes
donnees.head()

# Vérification des types de données et les valeurs manquantes
donnees.info()

# Suppression des lignes avec des valeurs manquantes
donnees = donnees.dropna()


# Afficher les catégories uniques dans la colonne PerformanceScore
donnees['PerformanceScore'].value_counts()

# Conversion en catégorie ordonnée
categories = ['PIP', 'Needs Improvement', 'Fully Meets', 'Exceeds']
donnees['PerformanceScore'] = pd.Categorical(donnees['PerformanceScore'], categories=categories, ordered=True)

# Fréquence des catégories
frequence_performance = donnees['PerformanceScore'].value_counts()
print(frequence_performance)

# Diagramme en barres
frequence_performance.plot(kind='bar', color='skyblue')
plt.title('Répartition des scores de performance')
plt.xlabel('Score de performance')
plt.ylabel('Nombre d\'employés')
plt.show()

# Identifier les catégories rares
seuil = 0.05  # Exemple : moins de 5 % des employés
rare_categories = frequence_performance[frequence_performance / len(donnees) < seuil]
print(rare_categories)

# Tableau croisé (nombre d'employés par score de performance et département)
tableau_croise = pd.crosstab(donnees['Department'], donnees['PerformanceScore'])
print(tableau_croise)

# Diagramme en barres empilées
tableau_croise.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Répartition des scores de performance par département')
plt.xlabel('Département')
plt.ylabel('Nombre d\'employés')
plt.show()

# Calcul des moyennes d'abscences par département
moyennes_departements = donnees.groupby('Department')[['Absences', 'SpecialProjectsCount', 'EngagementSurvey']].mean()
print(moyennes_departements)
# Ajouter PerformanceScore comme catégorie
categories_performance = ['PIP', 'Needs Improvement', 'Fully Meets', 'Exceeds']
donnees['PerformanceScore'] = pd.Categorical(donnees['PerformanceScore'], categories=categories_performance, ordered=True)

# Croisement des absences avec les scores de performance
croisement = donnees.groupby(['Department', 'PerformanceScore'], observed=True)['Absences'].mean().unstack()
croisement = croisement.fillna(0)#éliminer les NaN qui apparaissent dans le tableau et remplacer par 0
print( "\n Croisement des départements avec  les scores de performance")
print(croisement)

# Diagramme en barres
sns.barplot(x='Department', y='Absences', data=donnees, errorbar=None)
plt.xticks(rotation=45)
plt.title('Absences moyennes par département')
plt.show()

# Boxplot des absences par score de performance
sns.boxplot(x='PerformanceScore', y='Absences', data=donnees)
plt.title('Absences par score de performance')
plt.show()


# Histogramme des scores d'engagement
plt.figure(figsize=(8, 6))
sns.histplot(donnees['EngagementSurvey'], kde=True, bins=10, color='blue')
plt.title("Répartition des scores d'engagement")
plt.xlabel("Score d'engagement")
plt.ylabel("Fréquence")
plt.show()

# Moyenne des scores d'engagement par département
engagement_par_dept = donnees.groupby('Department')['EngagementSurvey'].mean().sort_values()

# Visualisation
plt.figure(figsize=(10, 6))
sns.barplot(x=engagement_par_dept.index, y=engagement_par_dept.values, palette='viridis')
plt.title("Score moyen d'engagement par département")
plt.xlabel("Département")
plt.ylabel("Score moyen d'engagement")
plt.xticks(rotation=45)
plt.show()

# Croiser engagement et absences
plt.figure(figsize=(8, 6))
sns.scatterplot(x='EngagementSurvey', y='Absences', data=donnees, hue='Department')
plt.title("Relation entre engagement et absences")
plt.xlabel("Score d'engagement")
plt.ylabel("Nombre d'absences")
plt.legend(bbox_to_anchor=(1, 1))
plt.show()

donnees['NiveauEngagement'] = pd.cut(donnees['EngagementSurvey'], bins=[0, 3, 7, 10], labels=['Faible', 'Moyen', 'Élevé'])
print(donnees.groupby('NiveauEngagement', observed=True)['Absences'].mean())

##Vérification de la présences ou non de outliers
# Calculer les quartiles et l'IQR
Q1 = donnees['Absences'].quantile(0.25)
Q3 = donnees['Absences'].quantile(0.75)
IQR = Q3 - Q1

# Définir les bornes inférieure et supérieure pour les outliers
borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR

# Identifier les outliers
outliers = donnees[(donnees['Absences'] < borne_inf) | (donnees['Absences'] > borne_sup)]

print(f"Nombre d'outliers détectés : {outliers.shape[0]}")
# Histogramme des absences
plt.figure(figsize=(8, 6))
sns.histplot(donnees['Absences'], bins=20, kde=True)
plt.title("Distribution des absences")
plt.xlabel("Nombre d'absences")
plt.ylabel("Fréquence")
plt.show()

# Boxplot des scores de performance
plt.figure(figsize=(8, 6))
sns.boxplot(x='PerformanceScore', data=donnees)
plt.title("Boxplot des scores de performance")
plt.show()
# Histogramme des scores de performance
plt.figure(figsize=(8, 6))
sns.histplot(donnees['PerformanceScore'], bins=10, kde=True)
plt.title("Distribution des scores de performance")
plt.xlabel("Score de performance")
plt.ylabel("Fréquence")
plt.show()

# Croisement des outliers avec le salaire
outliers_salaire = donnees[(donnees['Absences'] < borne_inf) | (donnees['Absences'] > borne_sup)]

plt.figure(figsize=(8, 6))

sns.scatterplot(x='Salary', y='Absences', data=donnees)

plt.title("Relation entre Salaire et Absences pour les Outliers")
plt.xlabel("Salaire")
plt.ylabel("Absences")
plt.show()

# Scatter plot entre les absences et les scores de performance
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Absences', y='PerformanceScore', data=donnees)
plt.title("Relation entre Absences et Score de Performance")
plt.xlabel("Absences")
plt.ylabel("Score de performance")
plt.show()

# Visualisation de l'engagement des employés (par exemple avec la variable 'EmpSatisfaction')
plt.figure(figsize=(8, 6))
sns.barplot(x='EmpSatisfaction', y='Absences', data=donnees)
plt.title("Engagement des employés et Absences")
plt.xlabel("Satisfaction des employés")
plt.ylabel("Absences")
plt.show()

# Barplot pour comparer les absences par département
plt.figure(figsize=(10, 6))
sns.barplot(x='Department', y='Absences', data=donnees)
plt.title("Absences par Département")
plt.xlabel("Département")
plt.ylabel("Absences")
plt.xticks(rotation=45)
plt.show()

