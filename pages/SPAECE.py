import streamlit as st
import pandas as pd
import plotly.express as px

# Set page layout to "wide"
st.set_page_config(layout='wide')

# Load data, specifying ',' as decimal separator
df = pd.read_excel('SPAECE_dados/seduc2anoLP.xlsx', sheet_name='MUNICÍPIO - ALFA', skiprows=3, decimal=',')

# Convert 'Edição' column to string
df['Edição'] = df['Edição'].astype(str)

# Remove rows containing "2022 - DIAGNÓSTICO" in the 'Edição' column
df = df[~df['Edição'].str.contains('2022 - DIAGNÓSTICO')]

# Clean 'CREDE' column values
df['CREDE'] = df['CREDE'].str.replace('CREDE ', '')

# Filter data for 'MARACANAU' region
df_maracanau = df[df['CREDE'] == 'MARACANAU']

# Group data by 'Município', 'Edição', and calculate mean performance metrics
df_mun_performance = df_maracanau.groupby(['Município', 'Edição'])['Proficiência Média', 'Não Alfabetizado', 'Alfabetização Incompleta', 'Intermediário', 'Suficiente', 'Desejável'].mean().reset_index()

# Page title
st.title("Resultados SPAECE")

# Municipality filter
municipio_options = ['CREDE 1'] + list(df_mun_performance['Município'].unique())
selected_municipio = st.sidebar.multiselect("Filtrar por Município", municipio_options, default=['CREDE 1'])

# Filter DataFrame based on selections
if 'CREDE 1' in selected_municipio:
    filtered_df = df_mun_performance.groupby('Edição')['Proficiência Média', 'Não Alfabetizado', 'Alfabetização Incompleta', 'Intermediário', 'Suficiente', 'Desejável'].mean().reset_index()
else:
    filtered_df = df_mun_performance[df_mun_performance['Município'].isin(selected_municipio)]

# Display filtered DataFrame within an expander
with st.expander('Ver tabela'):
    st.write(filtered_df)

# Create two columns for layout
col1, col2 = st.columns(2)

# Cria o gráfico de barras com a escala de cores personalizada
with col1:
    fig = px.bar(filtered_df, x='Edição', y='Proficiência Média', title='Proficiência Média por Edição', 
                 color='Proficiência Média', color_continuous_scale='RdYlGn')
    fig.update_xaxes(title_text='Edição')
    fig.update_yaxes(title_text='Desempenho Médio')
    st.plotly_chart(fig)
        
# Define um dicionário de mapeamento de cores para os padrões de desempenho
color_map = {
    'Não Alfabetizado': '#ed1c24',
    'Alfabetização Incompleta': '#ffc30e',
    'Intermediário': '#fff200',
    'Suficiente': '#c1e2cb',
    'Desejável': '#20ac52'
}

# Cria o gráfico de barras empilhadas com cores personalizadas
with col2:
    fig2 = px.bar(filtered_df, x='Edição', y=['Não Alfabetizado', 'Alfabetização Incompleta', 'Intermediário', 'Suficiente', 'Desejável'], 
                  title='Desempenho por Métrica', barmode='relative', color_discrete_map=color_map)
    fig2.update_xaxes(title_text='Edição')
    fig2.update_yaxes(title_text='Padrão de Desempenho')
    st.plotly_chart(fig2)
