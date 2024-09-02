import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd

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