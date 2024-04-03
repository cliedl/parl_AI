import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Electify - Über uns", page_icon="🇪🇺")


st.header("Über uns", divider="blue")

st.write(
    """
    Wir sind ein unabhängiges Team von Data Scientists, die sich für die Demokratie und den Zugang zu Informationen einsetzen.
    Wir arbeiten als Team zusammen in einer gemeinsamen [Github-Organisation](https://github.com/europarl-ai/).
    """
)


st.subheader("Christian Liedl")
st.write(
    """
    Christian hat einige Jahre als Physiker geforscht und sich seit 2024 auf Data Science und Künstliche Intelligenz spezialisiert.
    """
)

col1, col2 = st.columns([0.15, 0.85])
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

col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.link_button("Webseite", "https://aneifer.de")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/anna-neifer/")

st.subheader("Joshua Nowak")

st.write(
    """
Joshua hat als User Researcher und Psychologe verschiedene digitale Produkte mitgestaltet. Seit einigen Jahren programmiert er in Python und R und hat sich auf Data Science spezialisiert.
  """
)

col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.link_button("Github", "https://github.com/josh-nowak")

with col2:
    st.link_button("Linkedin", "https://www.linkedin.com/in/nowakjoshua/")