import streamlit as st
from plotly import express as px
import pandas as pd

def pie_chart_plotly(data:pd.DataFrame, values:str, names:str) -> None:
    fig = px.pie(data_frame = data, values = values, names = names)

    st.plotly_chart(fig)