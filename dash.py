import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Definir o layout wide da página
st.set_page_config(layout="wide")

# Carregar os dados principais
file_path = 'CompiladoGeral - Compilado_2023.csv'
data = pd.read_csv(file_path)

# Carregar o arquivo de habilidades
habilidades_file_path = 'habilidades.csv'  # Caminho relativo
habilidades_data = pd.read_csv(habilidades_file_path)

# Carregar o arquivo de Série Histórica
serie_file_path = 'serie_hist_compilada.csv'  # Caminho relativo
serie_data = pd.read_csv(serie_file_path)

# Layout do dashboard
st.title('SPAECE 2023')

# Filtros
municipios = data['Município'].dropna().unique()
etapas = data['Etapa'].dropna().unique()
componentes = data['Componente Curricular'].dropna().unique()

selected_municipio = st.sidebar.selectbox('Selecione o Município', municipios)
selected_etapa = st.sidebar.selectbox('Selecione a Etapa', etapas)
selected_componente = st.sidebar.selectbox('Selecione o Componente Curricular', componentes)

# Verificar a combinação inválida
if selected_etapa == '2° Ano' and selected_componente == 'Matemática':
    st.error("Não existe avaliação de matemática para 2º ano.")
else:

    # Filtrar os dados com base nas seleções
    filtered_data = data[(data['Município'] == selected_municipio) & 
                        (data['Etapa'] == selected_etapa) & 
                        (data['Componente Curricular'] == selected_componente)]

    filtered_serie_data = serie_data[(serie_data['Município'] == selected_municipio) & 
                        (serie_data['Etapa'] == selected_etapa) & 
                        (serie_data['Componente Curricular'] == selected_componente)]


    # Calcular a média das habilidades para o filtro aplicado
    habilidades_cols = [col for col in data.columns if col.startswith('H')]
    habilidades_data_main = data[habilidades_cols]
    habilidades_data_main = habilidades_data_main.loc[filtered_data.index].dropna(axis=1, how='all').apply(pd.to_numeric, errors='coerce')
    habilidades_mean_filtered = habilidades_data_main.mean().reset_index()
    habilidades_mean_filtered.columns = ['Habilidade', 'Média']
    habilidades_mean_filtered = habilidades_mean_filtered[habilidades_mean_filtered['Média'].notna() & (habilidades_mean_filtered['Média'] != 0)]

    # Ajustar a coluna Habilidade para garantir compatibilidade para o merge
    habilidades_mean_filtered['Habilidade'] = habilidades_mean_filtered['Habilidade'].str.strip()

    # Filtrar e adicionar as descrições das habilidades
    habilidades_descricao = habilidades_data[(habilidades_data['Etapa'] == selected_etapa) & 
                                            (habilidades_data['Componente Curricular'] == selected_componente)]
    habilidades_descricao['Habilidade'] = habilidades_descricao['Habilidade'].str.strip()

    # Verifique se as colunas existem
    if 'Descrição' in habilidades_descricao.columns:
        habilidades_mean_filtered = habilidades_mean_filtered.merge(habilidades_descricao[['Habilidade', 'Descrição']], on='Habilidade', how='left')
    else:
        habilidades_mean_filtered['Descrição'] = "Descrição não disponível"

    # Calcular a proficiência média para o filtro aplicado
    proficiencia_media_filtered = filtered_data.groupby('Município')['Proficiência média 2023'].mean().reset_index()
    
     # Definir cores para cada categoria
    color_discrete_map = {
        'Não alfabetizado': '#ed1c24',
        'Alfabetização incompleta': '#ffc30e',
        'Muito crítico': '#ed1c24',
        'Crítico': '#ffc30e',
        'Intermediário': '#fff200',
        'Adequado': '#20ac52',
        'Suficiente': '#c1e2cb',
        'Desejável': '#20ac52'
    }

    # Função para definir a cor com base na média e na etapa/componente
    def get_color_for_value(value, etapa, componente):
        if componente == 'Língua Portuguesa':
            if etapa == '2° Ano':
                if value < 75:
                    return '#ed1c24'  # Não Alfabetizado
                elif 75 <= value < 100:
                    return '#ffc30e'  # Alfabetização Incompleta
                elif 100 <= value < 125:
                    return '#fff200'  # Intermediário
                elif 125 <= value < 150:
                    return '#c1e2cb'  # Suficiente
                else:
                    return '#20ac52'  # Desejável
            elif etapa == '5° Ano':
                if value < 125:
                    return '#ed1c24'  # Muito Crítico
                elif 125 <= value < 175:
                    return '#ffc30e'  # Crítico
                elif 175 <= value < 225:
                    return '#fff200'  # Intermediário
                else:
                    return '#20ac52'  # Adequado
            elif etapa == '9° Ano':
                if value < 200:
                    return '#ed1c24'  # Muito Crítico
                elif 200 <= value < 250:
                    return '#ffc30e'  # Crítico
                elif 250 <= value < 300:
                    return '#fff200'  # Intermediário
                else:
                    return '#20ac52'  # Adequado
        elif componente == 'Matemática':
            if etapa == '5° Ano':
                if value < 150:
                    return '#ed1c24'  # Muito Crítico
                elif 150 <= value < 200:
                    return '#ffc30e'  # Crítico
                elif 200 <= value < 250:
                    return '#fff200'  # Intermediário
                else:
                    return '#20ac52'  # Adequado
            elif etapa == '9° Ano':
                if value < 225:
                    return '#ed1c24'  # Muito Crítico
                elif 225 <= value < 275:
                    return '#ffc30e'  # Crítico
                elif 275 <= value < 325:
                    return '#fff200'  # Intermediário
                else:
                    return '#20ac52'  # Adequado

    # Definir as cores para cada município com base na média de proficiência
    proficiencia_media_filtered['Cor'] = proficiencia_media_filtered['Proficiência média 2023'].apply(lambda x: get_color_for_value(x, selected_etapa, selected_componente))

    # Criar o gráfico de barras das habilidades com cores definidas e informações adicionais no hover
    fig_habilidades = px.bar(
        habilidades_mean_filtered, 
        x='Habilidade', 
        y='Média',
        title=f'Média percentual de acertos por habilidade',
        color='Média',
        text='Média',
        color_continuous_scale='Portland_r',
        hover_data={'Descrição': True}  # Adiciona a descrição ao hover
    )
    fig_habilidades.update_yaxes(range=[0, 110])

    # Aumentar as fontes
    fig_habilidades.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title='Média de acertos (%)',
        yaxis_title_font_size=16,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        hoverlabel_font_size=20,
        coloraxis_colorbar=dict(title="Média")
    )
    # Adicionando o texto nas barras
    fig_habilidades.update_traces(texttemplate='%{text:.2f}', 
                                textposition='outside',
                                textfont=dict(size=20) )

    # Removendo a legenda
    fig_habilidades.update_layout(showlegend=False)

    # Criar o gráfico de barras da proficiência média com cores definidas
    fig_proficiencia = px.bar(proficiencia_media_filtered, x='Município', y='Proficiência média 2023',
                            title=f'Proficiência Média',
                            color='Cor',
                            text='Proficiência média 2023',
                            color_discrete_map='identity')
    fig_proficiencia.update_yaxes(range=[0, 350])

    # Aumentar as fontes
    fig_proficiencia.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        hoverlabel_font_size=20
    )
    # Adicionando o texto nas barras
    fig_proficiencia.update_traces(texttemplate='%{text:.2f}', 
                                textposition='outside',
                                textfont=dict(size=20) )

    # Carregar dados de avaliados e previstos
    avaliados_previstos = data[['Município', 'Etapa', 'Componente Curricular', 'Avaliados', 'Previstos']].dropna()

    # Filtrar os dados com base nas seleções de município, etapa e componente curricular
    avaliados_previstos_filtered = avaliados_previstos[(avaliados_previstos['Município'] == selected_municipio) & 
                                                    (avaliados_previstos['Etapa'] == selected_etapa) & 
                                                    (avaliados_previstos['Componente Curricular'] == selected_componente)]

    if not avaliados_previstos_filtered.empty:
        avaliados = avaliados_previstos_filtered['Avaliados'].values[0]
        previstos = avaliados_previstos_filtered['Previstos'].values[0]
    else:
        avaliados = 0
        previstos = 1  # Para evitar divisão por zero

    percentual_avaliados = (avaliados / previstos) * 100

    # Adicionando Gauge
    fig_gauge = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=percentual_avaliados,
        mode="gauge+number",
        delta={'reference': 100},
        gauge={'axis': {'range': [None, 100]},
            'bar': {'color': 'gray'},  # Mudar a cor da linha central para cinza
            'steps': [
                    {'range': [0, 25], 'color': "#ed1c24"},
                    {'range': [25, 50], 'color': "#ffc30e"},
                    {'range': [50, 75], 'color': "#fff200"},
                    {'range': [75, 100], 'color': "#20ac52"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75}}))
    # Adicionando título à figura
    fig_gauge.update_layout(
    title_text="Percentual de Avaliados",
    #title_x=0.5,  # Centraliza o título
    title_font=dict(size=20)  # Tamanho da fonte do título
    )


    # Criar o gráfico de linha com Plotly Express

    fig_serie = px.line(filtered_serie_data, x='Ano', y='Proficiência Média', 
                        title='Série Temporal de Proficiência Média', 
                        markers=True, text='Proficiência Média')  # Tamanho dos marcadores
    fig_serie.update_traces(textposition='top center')  # Posição do texto nos marcadores

    # Aumentar as fontes
    fig_serie.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        hoverlabel_font_size=20
    )

    # Criando um expander com o título "Dados Pessoais"
    with st.expander("Dados Filtrados"):

        # Conteúdo dentro do expander
        st.write("Proficiência por Habilidades:")
        st.dataframe(filtered_data)  # Exibindo o DataFrame dentro do expander
        st.write("Série Histórica")
        st.dataframe(filtered_serie_data)  # Exibindo o DataFrame dentro do expander

    # Layout dos gráficos
    st.write(f'## Município:  {selected_municipio}')
    st.write(f'### Etapa: {selected_etapa}')
    st.write(f'### Componente Curricular: {selected_componente}')
    st.metric(label="Proficiência média 2023", value=proficiencia_media_filtered['Proficiência média 2023'].values[0])
    
    # Grafico de barras empilhadas
    fig_bar_empilhadas = px.bar(
        filtered_data,
        title=f'Média percentual de acertos por habilidade',
        x='Município', 
        y=['Não alfabetizado','Alfabetização incompleta','Muito crítico','Crítico','Intermediário','Adequado','Suficiente','Desejável'], 
        barmode = 'stack',
        color_discrete_map=color_discrete_map
    )
    # Aumentar as fontes
    fig_bar_empilhadas.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title='Nível de proficiência (%)',
        yaxis_title_font_size=16,
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        hoverlabel_font_size=20,
        coloraxis_colorbar=dict(title="Nível de proficiência"),
        showlegend=False
    )
    
    #Primeira Linha
    col1, col2 = st.columns([6, 1])

    with col1:
        st.plotly_chart(fig_habilidades, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.plotly_chart(fig_proficiencia, use_container_width=True, config={'displayModeBar': False})
        
    # Segunda Linha   
    col1, col2 ,col3 = st.columns([1, 4, 1])

    with col1:
        st.plotly_chart(fig_gauge)

    with col2:
        # Série Temporal
        st.plotly_chart(fig_serie, use_container_width=True)
        
    with col3:
        st.plotly_chart(fig_bar_empilhadas)
