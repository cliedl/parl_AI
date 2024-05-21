import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Electify - Team", page_icon="🇪🇺")


st.header("Über uns", divider="blue")

st.write(
    """
    Wir sind ein unabhängiges Team von Data Scientists, die sich für die Demokratie und den Zugang zu Informationen einsetzen.
    Wir arbeiten als Team zusammen in einer gemeinsamen [Github-Organisation](https://github.com/electify-eu).
    """
)


st.subheader("Christian Liedl")
st.write(
    """
    Christian hat einige Jahre als Physiker geforscht und sich seit 2024 auf Data Science und Künstliche Intelligenz spezialisiert.  
    [Github](https://github.com/cliedl) | [LinkedIn](https://www.linkedin.com/in/christian-liedl-2aaa03133/)
    """
)


st.subheader("Anna Neifer")
st.write(
    """
Anna hat als Journalistin für die ARD, ZDF, funk und andere Medien gearbeitet. Seit 2023 lernt sie mit Python zu coden und interessiert sich für Projekte an der Schnittstelle von Künstlicher Intelligenz und Journalismus. 
[Webseite](https://aneifer.de) | [LinkedIn](https://www.linkedin.com/in/anna-neifer/)

  """
)

st.subheader("Joshua Nowak")

st.write(
    """
Joshua hat als User Researcher und Psychologe verschiedene digitale Produkte mitgestaltet. Seit einigen Jahren programmiert er in Python und R und hat sich auf Data Science spezialisiert.  
[Github](https://github.com/josh-nowak) | [LinkedIn](https://www.linkedin.com/in/nowakjoshua/)
  """
)
