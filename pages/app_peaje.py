import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Peaje", layout="wide")
st.title("Análisis de Peaje")

# Cargar datos
file_path = "peaje.csv"
df = pd.read_csv(file_path)

# Filtrar y procesar datos
df_long = df.melt(id_vars=['CENTRAL'], var_name='Fecha', value_name='Peaje filiales ENDE')
df_long['Fecha'] = df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long['Fecha'] = pd.to_datetime(df_long['Fecha'], format='%m-%y')

df_long = df_long.dropna()

# Promedio por Tecnología para Pejase
df_tecnologia = df_long.groupby(['Fecha'])['Peaje filiales ENDE'].median().reset_index()

# Gráfico
fig = px.line(df_tecnologia, x='Fecha', y='Peaje filiales ENDE'
'',  title="Evolución de Pejase por Tecnología")

fig = px.line(df_tecnologia, x='Fecha', y='Peaje filiales ENDE', title="Evolución de Peaje por Tecnología", color_discrete_sequence=['green'])
fig.update_traces(mode='lines+markers', marker=dict(size=8, symbol='circle', color="blue"))

st.plotly_chart(fig)