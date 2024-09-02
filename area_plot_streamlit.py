import streamlit as st
import pandas as pd

def area_plot(data: pd.DataFrame, x:str, y:str, color:str) -> None:
    """
    Criar um gráfico de áreas
    
    Args:
    data = dataframe que será utilizado no gráfico
    x = nome da coluna que irá no eixo X
    y = nome da coluna que irá no eixo Y
    color = categorias que serão inclusas no gráfico
    """
    st.area_chart(data = data, x = x, y = y, color = color)