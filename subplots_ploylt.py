from plotly.subplots import make_subplots
from plotly import graph_objects as go 
import pandas as pd
import streamlit as st

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
    fig.add_trace(go.Bar(x = data[x_1], y = data[y_1],name=categoria_1), 
                  row = 1, col = 1)
    fig.update_layout(title = title)
    fig.add_trace(go.Bar(x = data[x_1], y = data[y_2],name=categoria_2), 
                  row = 1, col = 2)
    fig.update_layout(title = title)

    st.plotly_chart(fig)