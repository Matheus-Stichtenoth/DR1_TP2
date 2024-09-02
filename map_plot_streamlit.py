import streamlit as st
import pandas as pd

def map_plot_streamlit(data: pd.DataFrame, lat, long, size) -> None:
    """
    Criar um mapa com o streamlit

    Args:
    data = Dataframe que será utilizado
    lat = latitude da capital do estado
    long = longitude da capital do estado
    size = tamanho de acordo com os valores dos dados
    """

    st.map(data = data, latitude=lat, longitude=long, size=size)