import streamlit as st
import pandas as pd

def line_plot_streamlit(data, x:str, y:str) -> None:
    """
    Criar um gráfico de linhas

    Args:
    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    """
    st.line_chart(data, x=x, y=y)