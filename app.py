import pandas as pd
import glob as gl
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import numpy as np
import streamlit as st
import seaborn as sns
import altair as alt
from plotly import express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go 

#Na etapa inicial de leitura dos dados do CSV, 
#utilizei o método com pandas ensinado pelo professor Fernando
data = pd.concat([pd.read_csv(f, sep=';') for f in gl.glob('data/*.csv')], ignore_index=True)

#CRIANDO AS SEGMENTAÇÕES DOS DATAFRAMES QUE SERÃO UTILIZADOS

#Definindo dados do país
brasil = data[data.estado.isna()]
brasil.set_index('data', inplace=True)

#Dados das regioes Norte, Nordeste e Sudeste
regioes = data[data.regiao.isin(['Norte','Nordeste','Sudeste'])]
regioes.set_index('data', inplace=True)

#Dados da região sudeste
regiao_sudeste = data[data.regiao=='Sudeste']
regiao_sudeste.set_index('data',inplace=True)

#Definindo dados do estado do Rio Grande do Sul
rs = data[(data.estado == 'RS') & data.municipio.isna()]
rs['data'] = pd.to_datetime(rs['data'])
rs.set_index('data', inplace=True)
rs.sort_index(inplace=True)

#definindo os dados de todos os estados
estados = data[data.estado.notna()]
estados = estados[estados.municipio.isna()]
estados.set_index('data', inplace=True)

#3 Estados - Exercicio 4
uf_3 = data[(data.estado.isin(['SP','RS','MG'])) & data.municipio.isna()]
uf_3['data'] = pd.to_datetime(uf_3['data'])
uf_3.set_index('data', inplace=True)
uf_3.sort_index(inplace=True)

#Função para pegar as coordenadas dos 3 estados
coodernadas_estados = {
    'RS': {'latitude': -30.0346, 'longitude': -51.2177},
    'SP': {'latitude': -23.5505, 'longitude': -46.6333},
    'MG': {'latitude': -19.9167, 'longitude': -43.9345}
}

def obter_coordenadas(estado):
    return coodernadas_estados.get(estado, {'latitude': None, 'longitude': None})

uf_3['latitude'] = uf_3['estado'].apply(lambda x: obter_coordenadas(x)['latitude'])
uf_3['longitude'] = uf_3['estado'].apply(lambda x: obter_coordenadas(x)['longitude'])

#Criando medida para dividir os casos por 100 e melhorar a visualização
uf_3['casosAcumulado_cem'] = uf_3['casosAcumulado']/100

#Definindo dados do município de Caxias do Sul
caxias_do_sul = data[(data.municipio == 'Caxias do Sul')]
caxias_do_sul['data'] = pd.to_datetime(caxias_do_sul['data'])
caxias_do_sul.set_index('data', inplace=True)
caxias_do_sul.sort_index(inplace=True)

#Criando as funções dos gráficos

def bar_plot_streamlit(data:pd.DataFrame, x:str, y:str) -> None:
    """
    Criar um gráfico de barras

    Args:
    data = dataframe com os dados
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    """
    st.bar_chart(data,x=x,y=y)

def line_plot_streamlit(data:pd.DataFrame, x:str, y:str) -> None:
    """
    Criar um gráfico de linhas

    Args:
    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    """
    st.line_chart(data, x=x, y=y)

def area_plot_streamlit(data:pd.DataFrame, x:str, y:str, color:str) -> None:
    """
    Criar um gráfico de áreas
    
    Args:
    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    color = categorias que serão inclusas no gráfico
    """

    st.area_chart(data = data, x = x, y = y, color = color)

def map_plot_streamlit(data:pd.DataFrame, lat, long, size) -> None:
    """
    Criar um mapa com o streamlit

    Args:
    data = Dataframe que será utilizado
    lat = latitude da capital do estado
    long = longitude da capital do estado
    size = tamanho de acordo com os valores dos dados
    """

    st.map(data = data, latitude=lat, longitude=long, size=size)

def bar_plot_pyplot(x:str, y:float, x_label:str, y_label:str, title:str) -> None:
    """
    Criar um gráfico de barras com matplotlib

    Args:
    x = categoria que irá no eixo horizontal (eixo x)
    y = valor que irá no eixo vertical (eixo y)
    x_label = nome da categoria do argumento x
    y_label = nome da categoria do argumento y
    title = titulo do gráfico
    """
    fig, ax = plt.subplots()
    ax.bar(x,y)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

def boxplot_seaborn(data:pd.DataFrame, x:str, y:str, hue:str, title:str) -> None:
    """
    Cria um gráfico de boxplot com seaborn

    Args:
    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y  
    hue = legenda que será utilizado para definir as cores de cada categoria
    title = titulo do gráfico
    """
    fig,ax = plt.subplots()
    sns.boxplot(data = data, x=x, y=y, hue=hue)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc = 'best')
    st.pyplot(fig)

def area_chart_altair(data:pd.DataFrame, x:str, y:str) -> None:
    """
    Cria um gráfico de área no altair

    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    """
    area_chart = alt.Chart(data).mark_area().encode(
        x = x,
        y = y
    )

    st.altair_chart(area_chart, use_container_width=True)

def pie_chart_plotly(data:pd.DataFrame, values:str, names:str) -> None:
    """
    Cria um gráfico de pizza

    Args:
    data = dataframe com os dados necessarios
    values = nome da coluna que contém os valores
    names = nome da coluna que contém as categorias
    """
    fig = px.pie(data_frame = data, values = values, names = names)

    st.plotly_chart(fig)

def sub_plots(data:pd.DataFrame, x_1:str, y_1:str, y_2:str, title:str) -> None:
    """
    Cria subplots para gráficos de barra

    Args:
    data = Dataframe com os dados utilizados
    x_1 = nome da coluna do eixo X
    y_1 = nome da coluna com os valores do eixo Y
    y_2 = nome da outra coluna com os valores de um novo eixo Y
    """
    categoria_1 = y_1
    categoria_2 = y_2

    fig = make_subplots(rows=1,cols=2)
    fig.add_trace(go.Bar(x = data[x_1], y = data[y_1],name=categoria_1), row = 1, col = 1)
    fig.update_layout(title = title)
    fig.add_trace(go.Bar(x = data[x_1], y = data[y_2],name=categoria_2), row = 1, col = 2)
    fig.update_layout(title = title)

    st.plotly_chart(fig)


def dashboard() -> None:
    st.title('Análise da Pandemia de Covid-19')
    '''
    st.header('Atividade 1: Importância da Visualização de Dados')
    st.write("""
                 Explique a importância da visualização de dados no contexto de uma pandemia como a COVID-19. 
                 Como essas visualizações podem ajudar gestores de saúde pública e a população em geral a tomar decisões informadas?
                 """)
    st.write("""
            Os dados já são naturalmente importantes pra decisões básicas que tomamos no dia-a-dia. 
            No cenário de pandemia, não seria diferente.
            Os dados durante a pandemia, poderia demostrar aonde instituições governamentais deveriam focar na distribuição de vacinas contra covid-19.
            Por exemplo, os dados nos mostram que São Paulo é a maior cidade do Brasil, e foi um dos principais focos de covid. A partir dessa análise, já é possível direcionar da melhor maneira a distribuição das vacinas.
            Além disso, identificar regiões onde a covid está diminuindo, pode ajudar na hora de criar correlações com características da região e a evolução dos casos de covid.
            Porém, pela imensa quantidade de dados, é necessário que gráficos/visuais sejam utilizados para facilitar o acesso nessa informação.
            """)

    st.header('Atividade 2:')
    st.write("""
                 Usando os dados de casos novos de COVID-19 por semana epidemiológica de notificação, 
                 crie um gráfico de barras em Streamlit que mostre a evolução semanal dos casos em um determinado estado. 
                 Indique o estado escolhido e explique sua escolha.
                 """)
    bar_plot_streamlit(data = rs, x='semanaEpi', y='casosNovos')
    st.write('Defini em escolher o Rio Grande do Sul pois é o estado em que resido.')

    st.header('Atividade 3:')
    st.write("""
                 Crie um gráfico de linha utilizando Streamlit para representar o número de 
                 óbitos acumulados por COVID-19 ao longo das semanas epidemiológicas de 
                 notificação para todo o Brasil. 
                 Explique como a curva de óbitos acumulados pode ser interpretada.
                 """)
    line_plot_streamlit(data = brasil, x= 'semanaEpi', y= 'obitosAcumulado')
    st.write('A curva acentuada acima, pode ser interpretada que fora gerada no primeiro ano de pandemia ainda, e tendo crescimento próximo ao final do ano, que naturalmente são datas festivas.')

    st.header('Atividade 4:')
    st.write("""
                 Utilizando os dados de casos acumulados por COVID-19, 
                 crie um gráfico de área em Streamlit para comparar a evolução 
                 dos casos em três estados diferentes. 
                 Explique as diferenças observadas entre os estados escolhidos.
                 """)
    area_plot_streamlit(data = uf_3, y = 'casosNovos', x = 'semanaEpi', color = 'estado')
    st.write('No geral, São Paulo sempre esteve com mais casos novos, tendo a cor vermelha predominante no gráfico. Minas Gerais por sua vez, teve uma semana que teve casos negativos, provavelmente para "ajustar" alguma informação.')

    st.header('Atividade 5:')
    st.write("""
            Crie um mapa interativo utilizando a função st.map do Streamlit que mostre a distribuição dos casos acumulados de COVID-19 por município em um estado específico. Explique como esse tipo de visualização pode ajudar na análise geográfica da pandemia. 
            """)
    map_plot_streamlit(data = uf_3, 
                       lat='latitude', long = 'longitude', 
                       size = 'casosAcumulado_cem')
    st.write('Esse tipo de visualização, pode ajudar na hora de identificar os principais focos da doença. Como citado anteriormente, São Paulo, por sua densidade populacional, é o estado no qual mais teve casos de Covid, por isso o tamanho da bolha fica maior em comparação às duas demais.')

    st.header('Atividade 6:')
    st.write('Utilize a biblioteca Matplotlib para criar um gráfico de barras que mostre a comparação entre os casos novos e os óbitos novos de COVID-19 por estado na semana epidemiológica mais recente disponível. Explique o que os dados sugerem sobre a relação entre casos e óbitos.')
    df_estados_filtered = estados[estados['semanaEpi'] == 53]
    #Plotando gráfico de casos novos
    bar_plot_pyplot(x = df_estados_filtered['estado'],
                    y=df_estados_filtered['casosNovos'], 
                    x_label= 'Estados',
                    y_label = 'Casos Novos',
                    title = 'Casos Novos na Semana Epidemiológica 53')
    #Plotando gráfico de obitos novos
    bar_plot_pyplot(x = df_estados_filtered['estado'],
                    y=df_estados_filtered['obitosNovos'], 
                    x_label= 'Estados',
                    y_label = 'Obitos Novos',
                    title = 'Obitos Novos na Semana Epidemiológica 53')
    st.write('É notável que os estados que mais têm casos novos de COVID-19, também são os que mais registram novos óbitos.')
    
    st.header('Atividade 7:')
    st.write('Usando a biblioteca Seaborn, crie um boxplot que compare a distribuição dos casos novos de COVID-19 por semana epidemiológica entre três regiões do Brasil (Norte, Nordeste, Sudeste). Explique as principais diferenças observadas.')
    boxplot_seaborn(data = regioes, 
                    x = 'semanaEpi', 
                    y = 'casosNovos', 
                    hue = 'regiao', 
                    title = 'Comparação de Casos Novos por Semana Epidemiológica')
    st.write('Aparentemente, a presença de outliers está prejudicando a visualização do gráfico. Por conta disso, não consigo extrair uma análise das diferenças')

    st.header('Atividade 8:')
    st.write('Crie um gráfico de área em Altair para mostrar a evolução dos casos novos de COVID-19 por semana epidemiológica de notificação em uma determinada região do Brasil. Explique a escolha da região e as tendências observadas nos dados.')
    
    #Filtrei a partir da dsemana 40 pois os dados completos ficaram muito pesados para carregar
    df_regiao_sudeste_filtered = regiao_sudeste[regiao_sudeste['semanaEpi'] >= 40]
    area_chart_altair(data = df_regiao_sudeste_filtered, x='semanaEpi', y='casosNovos')
    st.write('Com a análise a partir da semana 40, é possível identificar que as últimas semenas têm mais casos novos que as anteriores, isso deve acontecer por conta das festas de final de ano. Porém, na última semana os casos caem bastante. Provavelmente isso se dá por conta que ao final do ano, os testes são realizados com uma frequência bem menor.')
    st.write('Escolhi a região Sudeste pois é uma das mais habitadas do pais, por conta disso, imagino que tenha dados mais robustos para análise')

    st.header('Atividade 9:')
    st.write('Desenvolva um heatmap em Altair que mostre a correlação entre casos novos, óbitos novos e leitos hospitalares ocupados (caso os dados estejam disponíveis) em um determinado estado. Explique as possíveis correlações observadas.')

    df_rs_filtered = rs[['casosNovos','obitosNovos']]
    df_rs_filtered = df_rs_filtered.reset_index()
    df_rs_filtered = df_rs_filtered.rename(columns={'index': 'casosNovos'})
    df_rs_filtered = df_rs_filtered.set_index('casosNovos', drop=False).drop(columns=['data'])
    heatmap_chart = alt.Chart(df_rs_filtered.melt('casosNovos')).mark_rect().encode(
        x = 'casosNovos:O',
        y = 'variable:O',
        color = 'value:Q'
    )
    st.altair_chart(heatmap_chart, use_container_width=True)

    st.header('Atividade 10:')
    st.write('Usando Plotly, crie um gráfico de pizza (pie chart) que mostre a distribuição percentual dos casos acumulados de COVID-19 entre as cinco regiões do Brasil. Explique o que os dados revelam sobre a distribuição geográfica dos casos.')
    pie_chart_plotly(data = estados, values = 'casosAcumulado', names = 'regiao')
    st.write('O gráfico demonstra que a região mais populosa do Brasil, tem a maior incidência dos casos acumulados de COVID-19.')
    '''
    st.header('Atividade 11:')
    st.write('Crie subplots em Plotly que mostrem, lado a lado, gráficos de barras comparando os casos novos e os óbitos novos de COVID-19 por semana epidemiológica em duas diferentes regiões do Brasil. Explique as diferenças observadas entre as regiões.')
    sub_plots(data = estados[estados['regiao'] == 'Sul'],
              x_1 = 'semanaEpi', 
              y_1 = 'casosNovos', y_2 = 'obitosNovos', 
              title = 'Sul')
    sub_plots(data = estados[estados['regiao'] == 'Sudeste'],
              x_1 = 'semanaEpi', 
              y_1 = 'casosNovos', y_2 = 'obitosNovos', 
              title = 'Sudeste')
    st.write('As principais diferenças entre os casos novos do Sul e do Sudeste, é o volume, visto que o comportamento durante as semanas foram semelhantes.')
    st.write('Já quando falamos dos obitos novos, as regiões foram inversamente proporcionais, com o Sul tendo muito obitos nas semanas 10 até 15, enquanto o Sudeste teve a concentração de obitos numa escalar maior, indo da semana 15 até 35.')

if __name__ == '__main__':
    dashboard()