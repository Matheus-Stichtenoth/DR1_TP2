import pandas as pd
import streamlit as st
import altair as alt

def area_chart_altair (data:pd.DataFrame, x:str, y:str) -> None:
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