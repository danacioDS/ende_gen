import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Precio", layout="wide")

st.title("Visualización de Precio Promedio por Proyecto y Tecnología")

# Cargar los datos
file_path = "precio.csv"
df = pd.read_csv(file_path)

# Filtrar las columnas necesarias
df = df[['CENTRAL', 'Tecnología'] + [col for col in df.columns if 'PROMEDIO' in col]]

# Convertir el DataFrame a formato largo para Plotly
df_long = df.melt(id_vars=['CENTRAL', 'Tecnología'], var_name='Fecha', value_name='Precio')

# Extraer mes y año de la columna de fecha
df_long['Fecha'] = df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[0] + '-' + df_long['Fecha'].str.extract(r'(\d{2})(\d{2})')[1]
df_long['Fecha'] = pd.to_datetime(df_long['Fecha'], format='%m-%y')

# Eliminar valores nulos
df_long = df_long.dropna()

# Filtros de selección
tecnologias = df_long['Tecnología'].unique()
tecnologia_seleccionada = st.selectbox("Selecciona una tecnología", tecnologias)
df_filtrado = df_long[df_long['Tecnología'] == tecnologia_seleccionada]

proyectos = df_filtrado['CENTRAL'].unique()
proyecto_seleccionado = st.selectbox("Selecciona un proyecto", proyectos)
df_final = df_filtrado[df_filtrado['CENTRAL'] == proyecto_seleccionado]

# Cálculo del precio promedio por tecnología y total
df_tecnologia = df_long.groupby(['Fecha', 'Tecnología'])['Precio'].mean().reset_index()
df_tecnologia_filtrado = df_tecnologia[df_tecnologia['Tecnología'] == tecnologia_seleccionada]
df_total = df_long.groupby('Fecha')['Precio'].mean().reset_index()

# Gráficos
fig1 = px.bar(df_final, x='Fecha', y='Precio', title=f'Precio de {proyecto_seleccionado} ({tecnologia_seleccionada})', color_discrete_sequence=['blue'])
fig1.update_layout(
    title='Evolución de la Precio por Proyecto',
    xaxis_title='Fecha',
    yaxis_title='Energía (MWh)',
    font=dict(family='Arial', size=14, color='black'),
    xaxis=dict(showgrid=False, gridwidth=0.5, gridcolor='gray'),
    yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='gray')
)

fig2 = px.area(df_tecnologia_filtrado, x='Fecha', y='Precio', title=f'Precio por Tecnología: {tecnologia_seleccionada}', color_discrete_sequence=['red'])
fig2.update_layout(
    title='Evolución de la Precio Promedio por Tecnologia',
    xaxis_title='Fecha',
    yaxis_title='Energía (MWh)',
    font=dict(family='Arial', size=14, color='black'),
    xaxis=dict(showgrid=False, gridwidth=0.5, gridcolor='gray'),
    yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='gray')
)


# Edicion figura 3
fig3 = px.line(df_total, x='Fecha', y='Precio', title='Precio Promedio de Generación Total', color_discrete_sequence=['green'])
fig3.update_layout(
    title='Evolución de la Precio Promedio del Sistema',
    xaxis_title='Fecha',
    yaxis_title='Energía (MWh)',
    font=dict(family='Arial', size=14, color='black'),
    xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='gray'),
    yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='gray')
)

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
