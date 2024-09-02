import streamlit as st
import pandas as pd

def bar_plot_streamlit(data, x:str, y:str) -> None:
    """
    Criar um gráfico de barras

    Args:
    data = dataframe com os dados
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    """
    st.bar_chart(data,x=x,y=y)

