import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


# Configura o layout da página para ser "wide" (modo amplo)
st.set_page_config(layout='wide')

 # Título da página Início
st.title("Pagina Inicial")
# Texto descritivo do dashboard
dashboard_description = """
## Painel de Resultados das Avaliações SPAECE e AvalieCE
### Orgaização: CECOM 1 - Crede Maracanaú

Bem-vindo ao Dashboard de Resultados das Avaliações no Estado do Ceará. Este painel interativo foi desenvolvido para oferecer uma visão abrangente e detalhada dos resultados das avaliações **SPAECE** (Sistema Permanente de Avaliação da Educação Básica do Ceará) e **AvalieCE** (Avaliação Formativa do Ensino Fundamental
do Programa PAIC Integral), permitindo aos usuários explorar e analisar os dados de maneira intuitiva e visualmente atraente.

### Funcionalidades Principais

1. **Visão Geral:**
- Na página inicial, você encontrará uma visão geral dos principais indicadores e métricas das avaliações, proporcionando uma compreensão rápida e eficiente dos resultados globais.

2. **Resultados SPAECE:**
- A seção SPAECE é dedicada aos resultados detalhados do Sistema Permanente de Avaliação da Educação Básica do Ceará.
- Aqui, você pode visualizar gráficos interativos e tabelas que destacam o desempenho dos estudantes em diferentes áreas e etapas da educação básica.
- Explore os dados filtrando por município, escola, ano e outros parâmetros relevantes para obter insights específicos.

3. **Resultados AvalieCE:**
- A seção AvalieCE permite uma análise detalhada dos resultados desta avaliação específica.
- Utilize os filtros disponíveis na barra lateral para selecionar o município, etapa de ensino e componente curricular de interesse.
- Visualize gráficos de barras interativos que mostram o percentual de habilidades por município, facilitando a comparação e identificação de áreas de melhoria.

### Características do Dashboard

- **Interatividade:**
    - O dashboard é altamente interativo, permitindo que os usuários ajustem os filtros e vejam os resultados em tempo real.
    - Os gráficos e tabelas se atualizam automaticamente com base nas seleções feitas, proporcionando uma experiência de usuário dinâmica e responsiva.

- **Visualização de Dados:**
    - Gráficos de barras, tabelas e outras visualizações são utilizados para apresentar os dados de maneira clara e compreensível.
    - As visualizações são personalizadas com cores e estilos que destacam as informações mais importantes.

- **Acessibilidade:**
    - O layout "wide" (modo amplo) garante que o conteúdo seja exibido de forma otimizada, independentemente do dispositivo utilizado para acessar o dashboard.
    - Imagens e gráficos são centralizados e dispostos de maneira organizada para facilitar a navegação e análise dos dados.

### Navegação Fácil

- **Barra Lateral:**
    - A barra lateral oferece acesso rápido às diferentes seções do dashboard.
    - Imagens institucionais e o título da barra lateral estão centralizados para uma melhor apresentação visual.
    - Filtros intuitivos permitem a personalização da visualização dos dados de acordo com as necessidades específicas do usuário.

### Conclusão

Este dashboard é uma ferramenta poderosa para educadores, gestores e demais interessados em monitorar e melhorar o desempenho educacional no Estado do Ceará. Ao fornecer uma visão detalhada e interativa dos resultados das avaliações SPAECE e AvalieCE, esperamos contribuir para o avanço da educação básica e para a implementação de estratégias mais eficazes de ensino e aprendizagem.
"""
st.markdown(dashboard_description)