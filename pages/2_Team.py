import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="europarl.ai - Team", page_icon="🇪🇺")


st.header("Das europarl.ai Team:", divider="blue")
# st.sidebar.header("Das sind wir")

st.subheader("GitHub - Account")
st.write(
    """
    Wir arbeiten als Team zusammen und haben auf GitHub einen gemeinsamen Account erstellt.
    Hier findest du ("europarl.ai auf GitHub", "https://github.com/europarl-ai/").
    """
)


st.subheader("Christian Liedl")
st.write(
    """
    Christian hat einige Jahre als Physiker geforscht und sich seit 2024 auf Data Science und Künstliche Intelligenz spezialisiert.
    """
)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Github", "https://github.com/cliedl")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/christian-liedl-2aaa03133/")


st.subheader("Anna Neifer")
st.write(
    """
Anna hat als Journalistin für die ARD, ZDF, funk und die Kooperarive Berlin gearbeitet. Seit 2023 lernt sie coden und ist jetzt als Data Scientist tätig.

  """
)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Webseite", "https://aneifer.de")

with col2:
    st.link_button("Linkedin", "Linkedin.com/in/anna-neifer/")

st.subheader("Joshua Nowak")

st.write(
    """
Joshua hat als User Researcher und Psychologe verschiedene digitale Produkte mitgestaltet.
  """
)

col1, col2 = st.columns(2)
with col1:
    st.link_button("Github", "https://github.com/josh-nowak")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/nowakjoshua/")
