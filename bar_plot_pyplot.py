import streamlit as st
from matplotlib import pyplot as plt

def bar_plot_pyplot(x: str, y:float, x_label:str, y_label:str, title:str) -> None:
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