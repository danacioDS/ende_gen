import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Precio Promedio", layout="wide")

st.title("Energía entregada por tipo de tecnología")

# Sidebar para filtros
st.sidebar.title("Filtros")

# Cargar datos
file_path = "data/energia.csv"
df = pd.read_csv(file_path)

file_path_1 = "data/energias_totales.csv"
df_1 = pd.read_csv(file_path_1)


# Filtrar columnas necesarias
df = df[['CENTRAL', 'Tecnología'] + [col for col in df.columns if 'Energía' in col]]
df_long = df.melt(id_vars=['CENTRAL', 'Tecnología'], var_name='Fecha', value_name='Energía')

# Extraer mes y año
df_long['Fecha'] = df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long['Fecha'] = pd.to_datetime(df_long['Fecha'], format='%m-%y')

# Eliminar valores nulos
df_long.dropna(inplace=True)

# Cargar datos
df_long['Año'] = df_long['Fecha'].dt.year  # Extraer el año

df_energia_anual = df_long.groupby(['Año', 'Tecnología'])['Energía'].sum().reset_index()

# Gráfico de energía agregada por año y tecnología
fig4 = px.bar(df_energia_anual, x='Año', y='Energía', color='Tecnología', 
              title='Energía Agregada por Año y Tecnología', 
              labels={'Energía': 'Energía Total (MWh)', 'Año': 'Año'},
              barmode='group', color_discrete_sequence=px.colors.qualitative.Set1)

# Mostrar gráfico
st.plotly_chart(fig4, use_container_width=True)

# Calcular la energía total por tecnología y año
df_anual = df_long.groupby(['Año', 'Tecnología'])['Energía'].sum().reset_index()

df_total_anual = df_anual.groupby('Año')['Energía'].sum().reset_index()
df_anual = df_anual.merge(df_total_anual, on='Año', suffixes=('', '_Total'))
df_anual['Porcentaje'] = (df_anual['Energía'] / df_anual['Energía_Total']) * 100


# Crear gráficos de torta por año
st.subheader("Distribución de Energía por Tecnología en Cada Año")

for year in sorted(df_anual['Año'].unique()):
    df_year = df_anual[df_anual['Año'] == year]
    fig = px.pie(df_year, values='Energía', names='Tecnología', title=f"Año {year}", 
                 hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)