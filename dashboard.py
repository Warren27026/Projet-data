# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 08:56:39 2025

@author: Warren
"""

import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import requests

# Exemple : Données des cryptomonnaies
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
response = requests.get(url, params=params)
data = pd.DataFrame(response.json())

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard des Cryptomonnaies"),
    dcc.Graph(id="crypto-graph", figure=px.bar(data, x="name", y="current_price",
                                               title="Prix des Cryptomonnaies")),
])

if __name__ == '__main__':
    app.run_server(debug=True)
"""
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Titre de l'application
st.title("Dashboard des Cryptomonnaies")

# Récupération des données depuis l'API CoinGecko
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}
response = requests.get(url, params=params)
data = pd.DataFrame(response.json())

# Affichage des données sous forme de tableau
st.subheader("Données des Cryptomonnaies")
st.dataframe(data[["name", "symbol", "current_price", "market_cap", "total_volume"]])

# Graphique interactif avec Plotly
st.subheader("Prix des Cryptomonnaies")
fig = px.bar(
    data,
    x="name",
    y="current_price",
    title="Prix des Cryptomonnaies",
    labels={"name": "Nom", "current_price": "Prix actuel (USD)"}
)
st.plotly_chart(fig)

# Ajout d'une option de tri
st.sidebar.subheader("Options")
sort_by = st.sidebar.selectbox("Trier les données par :", ["Prix actuel", "Capitalisation boursière"])
if sort_by == "Prix actuel":
    sorted_data = data.sort_values(by="current_price", ascending=False)
else:
    sorted_data = data.sort_values(by="market_cap", ascending=False)

st.subheader(f"Classement trié par {sort_by}")
st.dataframe(sorted_data[["name", "symbol", "current_price", "market_cap"]])"""
