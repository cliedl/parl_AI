import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Team", page_icon=":point_right:")

st.header("Wir haben europarl.ai erstellt", divider='blue')
st.sidebar.header("Das sind wir")

st.header('Chris Liedl')
st.write(
    """

Physiker und löst gern Känguru-Probleme

    """)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Github", "https://github.com/cliedl")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/christian-liedl-2aaa03133/")


st.header('Anna Neifer')
st.write(
    """
Anna hat als Journalistin für die ARD, ZDF, funk und die Kooperarive Berlin gearbeitet. Seit 2023 lernt sie coden und ist jetzt als Data Scientist tätig.

  """)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Webseite", "https://aneifer.de")

with col2:
    st.link_button("Linkedin", "Linkedin.com/in/anna-neifer/")

st.header('Joshua Nowak')

st.write(
    """
UX Researcher und baut gern Dinge mit langchain

  """)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Github", "https://github.com/josh-nowak")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/nowakjoshua/")

