import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Precio Promedio", layout="wide")

st.title("Visualización de Precio Promedio por Proyecto y Tecnología")

# Sidebar para filtros
st.sidebar.title("Filtros")

# Cargar datos
file_path = "data/precio.csv"
df = pd.read_csv(file_path)

file_path_1 = "data/precios_promedio.csv"
df_1 = pd.read_csv(file_path_1)

# Filtrar columnas necesarias
df = df[['CENTRAL', 'Tecnología'] + [col for col in df.columns if 'PROMEDIO' in col]]
df_long = df.melt(id_vars=['CENTRAL', 'Tecnología'], var_name='Fecha', value_name='Precio')

# Extraer mes y año
df_long['Fecha'] = df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long['Fecha'] = pd.to_datetime(df_long['Fecha'], format='%m-%y')

# Eliminar valores nulos
df_long.dropna(inplace=True)

# Sidebar selectors
tecnologias = df_long['Tecnología'].unique()
tecnologia_seleccionada = st.sidebar.selectbox("Selecciona una tecnología", tecnologias)

df_filtrado = df_long[df_long['Tecnología'] == tecnologia_seleccionada]
proyectos = df_filtrado['CENTRAL'].unique()
proyecto_seleccionado = st.sidebar.selectbox("Selecciona un proyecto", proyectos)

df_final = df_filtrado[df_filtrado['CENTRAL'] == proyecto_seleccionado]

# Definir rango de fechas para filtros
df_long['Fecha'] = pd.to_datetime(df_long['Fecha'])
min_date = df_long['Fecha'].min().date()
max_date = df_long['Fecha'].max().date()

# Slider para el rango de fechas
date_range = st.sidebar.slider("Selecciona el rango de fechas", min_value=min_date, max_value=max_date, value=(min_date, max_date), key="slider_1")

date_range = (pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))
df_final = df_final[(df_final['Fecha'] >= date_range[0]) & (df_final['Fecha'] <= date_range[1])]

# Diseño de columnas
col1, col2 = st.columns(2)

# Gráfico de precio por proyecto
with col1:
    st.subheader(f"Precio Promedio de {proyecto_seleccionado} ({tecnologia_seleccionada})")
    fig1 = px.bar(df_final, x='Fecha', y='Precio', color_discrete_sequence=['#1f77b4'])
    fig1.add_hline(y=df_final['Precio'].mean(), line_dash="dot", line_color="gray")
    promedio_proyecto = df_final['Precio'].mean()
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(f"**Promedio por planta: {promedio_proyecto:,.2f}**")

# Gráfico de precio promedio por tecnología
df_tecnologia = df_long.groupby(['Fecha', 'Tecnología'])['Precio'].mean().reset_index()
df_tecnologia_filtrado = df_tecnologia[df_tecnologia['Tecnología'] == tecnologia_seleccionada]
df_tecnologia_filtrado = df_tecnologia_filtrado[(df_tecnologia_filtrado['Fecha'] >= date_range[0]) & (df_tecnologia_filtrado['Fecha'] <= date_range[1])]

with col2:
    st.subheader(f"Precio Promedio de Tecnología: {tecnologia_seleccionada}")
    fig2 = px.area(df_tecnologia_filtrado, x='Fecha', y='Precio', color_discrete_sequence=['#d62728'])
    fig2.add_hline(y=df_tecnologia_filtrado['Precio'].mean(), line_dash="dot", line_color="gray")
    promedio_proyecto = df_tecnologia_filtrado['Precio'].mean()
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(f"**Promedio de tecnologia: {promedio_proyecto:,.2f}**")

# Línea divisoria
st.markdown("---")

# Precio Promedio de Generación Total
st.subheader("Precio Promedio de Generación Total")

df_1 = df_1[['CENTRAL'] + [col for col in df_1.columns if 'PROMEDIO' in col]]
df_long_1 = df_1.melt(id_vars=['CENTRAL'], var_name='Fecha', value_name='Precio')

df_long_1['Fecha'] = df_long_1['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long_1['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long_1['Fecha'] = pd.to_datetime(df_long_1['Fecha'], format='%m-%y')
df_long_1.dropna(inplace=True)

df_total = df_long_1.groupby('Fecha')['Precio'].mean().reset_index()
df_filtered = df_total[(df_total['Fecha'] >= date_range[0]) & (df_total['Fecha'] <= date_range[1])]

fig3 = px.line(df_filtered, x='Fecha', y='Precio', color_discrete_sequence=['#ff7f0e'])
fig3.add_hline(y=df_filtered['Precio'].mean(), line_dash="dot", line_color="gray")
promedio_proyecto = df_filtered['Precio'].mean()
st.plotly_chart(fig3, use_container_width=True)
st.markdown(f"**Promedio el sistema: {promedio_proyecto:,.2f}**")

