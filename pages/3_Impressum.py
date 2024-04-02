import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="europarl.ai - Impressum", page_icon="🇪🇺")


st.header("Impressum", divider="blue")
# st.sidebar.header("Daten")
st.write(
    """
    Electify GbR

    Vertretungsberechtigte Gesellschafter: Christian Liedl, Anna Neifer, Joshua Nowak

    Anschrift: .....

    Email: ....
    """
)
