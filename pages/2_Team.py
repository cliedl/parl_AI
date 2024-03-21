import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Team", page_icon="🌍")

st.markdown("# Team europarl.ai")
st.sidebar.header("Wer macht europarl.ai?")

st.header('Chris Liedl')
st.write(
    """

Physiker und löst gern Känguru-Probleme

    """)

st.header('Anna Neifer')
st.write(
    """
Journalistin und Data Scientist

  """)

st.header('Joshua Nowak')

st.write(
    """
UX Researcher und baut gern Dinge mit langchain

  """)