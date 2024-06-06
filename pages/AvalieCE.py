import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
import base64


# Configura o layout da página para ser "wide" (modo amplo)
st.set_page_config(layout='wide')


# Define o título do aplicativo
st.title("AvalieCE")  
# Define os filtros para AvalieCE
st.sidebar.title("Filtros:")
# Carrega os dados do arquivo CSV
dados = pd.read_csv('Avaliece_dados/CompiladoAvalieCE.csv', low_memory=False)
# Define as opções para os filtros com base nas colunas do CSV
municipios_opcoes = dados['Município'].unique()
etapas_opcoes = dados['Etapa'].unique()
componentes_opcoes = dados['Componente Curricular'].unique()
# Adiciona filtros na barra lateral para selecionar município, etapa e componente curricular
municipio_selecionado = st.sidebar.selectbox('Selecione um município:', municipios_opcoes)
etapa_selecionada = st.sidebar.selectbox('Selecione uma etapa:', etapas_opcoes)
componente_selecionada = st.sidebar.selectbox('Selecione um componente:', componentes_opcoes)

# Filtra os dados com base nas seleções dos filtros
df_filtrado = dados[(dados['Município'] == municipio_selecionado) &
                    (dados['Etapa'] == etapa_selecionada) &
                    (dados['Componente Curricular'] == componente_selecionada)]

# Filtra colunas que começam com "H"
columns_h = [col for col in df_filtrado.columns if col.startswith('H')]
columns_h.insert(0, 'Município')  # Adiciona a coluna 'Município' à lista

# Seleciona apenas as colunas filtradas
df_habilidades = df_filtrado[columns_h]

# Transforma o DataFrame para o formato longo (long format)
df_long = df_habilidades.melt(id_vars='Município', 
                              var_name='Habilidade', 
                              value_name='Percentual')

# Cria o gráfico de barras
fig = px.bar(
    data_frame=df_long,
    x='Habilidade',
    y='Percentual',
    color='Percentual',
    title='Habilidades por Município',
    labels={
        'Habilidade': 'Habilidade',
        'Percentual': 'Percentual'
    },
    height=500,
    width=1000,
)

# Atualiza o layout do gráfico para usar a fonte Isidora Sans
fig.update_layout(
    font=dict(
        family="Isidora Sans, Arial, sans-serif",  # Define a fonte Isidora Sans
        size=14,
        color="#3f4d57"
    ),
    title_font=dict(
        family="Kanit, Arial, sans-serif",  # Define a fonte Kanit para o título
        size=28,
        color="#3f4d57"
    ),
    xaxis=dict(
        title=dict(
            font=dict(
                family="Isidora Sans, Arial, sans-serif",  # Define a fonte Isidora Sans para o eixo x
                size=16,
                color="#3f4d57"
            )
        ),
        tickangle=-90  # Inclina os rótulos do eixo x para melhor legibilidade
    ),
    yaxis=dict(
        title=dict(
            font=dict(
                family="Isidora Sans, Arial, sans-serif",  # Define a fonte Isidora Sans para o eixo y
                size=16,
                color="#3f4d57",
            )
        ),
        range=[0, 100]  # Define o range do eixo y de 0 a 100
    ),
    showlegend=False  # Oculta a legenda
)

# Adiciona rótulos aos valores
fig.update_traces(texttemplate='%{y:.0f}', textposition='inside')


# Mostra o gráfico na aplicação Streamlit
st.plotly_chart(fig)

