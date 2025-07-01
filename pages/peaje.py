import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(page_title="Precio Promedio", layout="wide")
st.title("Visualización de Peaje del Sistema")

# Cargar datos
file_path = "data/peaje.csv"
df_1 = pd.read_csv(file_path)

# Filtrar las columnas necesarias
df_1 = df_1[['CENTRAL'] + [col for col in df_1.columns if 'Peaje filiales' in col]]
df_long_1 = df_1.melt(id_vars=['CENTRAL'], var_name='Fecha', value_name='Peaje')

# Extraer mes y año de la columna de fecha
df_long_1['Fecha'] = df_long_1['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long_1['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long_1['Fecha'] = pd.to_datetime(df_long_1['Fecha'], format='%m-%y')

# Eliminar valores nulos
df_long_1 = df_long_1.dropna()

# Agrupar datos
df_total = df_long_1.groupby('Fecha')['Peaje'].median().reset_index()

# Convertir 'Fecha' a datetime para usar en el slider
df_total['Fecha'] = pd.to_datetime(df_total['Fecha'])
min_date = df_total['Fecha'].min().date()
max_date = df_total['Fecha'].max().date()

# Agregar slider en la barra lateral
st.sidebar.title("Filtros")
date_range = st.sidebar.slider("Selecciona el rango de fechas", min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Convertir rango de fechas a datetime para filtrar
date_range = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
df_filtered = df_total[(df_total['Fecha'] >= date_range[0]) & (df_total['Fecha'] <= date_range[1])]

# Crear gráfico con marcadores de puntos y color naranja
fig3 = px.line(df_filtered, x='Fecha', y='Peaje', markers=True, color_discrete_sequence=['#ff7f0e'])

# Agregar líneas de referencia
fig3.add_hline(y=df_filtered['Peaje'].mean(), line_dash="dot", line_color="gray")
fig3.add_vline(x=df_filtered['Fecha'].max(), line_dash="dot", line_color="gray")
promedio_proyecto = df_filtered['Peaje'].mean()

# Mostrar gráfico
st.plotly_chart(fig3, use_container_width=True)
st.markdown(f"**Promedio: {promedio_proyecto:,.2f}**")




