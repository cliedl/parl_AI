import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Project europarl.ai", page_icon="")

st.sidebar.header("Was ist europarl.ai?")

st.header('Projekt europarl.ai', divider='rainbow')
st.write(
    """Europa ist cool, aber auch mega kompliziert. Und am 9.6.2024 ist schon die Europawahl. Welcher Partei also die Stimme geben?
    Mit europarl.ai kannst du dir die Positionen der Parteien zu einem bestimmten Thema anzeigen lassen.
    Was planen die Parteien auf europäischer Ebene im Bereich Energie, Renten, Migration?
    Mit europarl.ai durchsuchen wir im Hintergrund die Wahlprogramme der deutschen Parteien zur Europawahl und die Reden der Parteien im EU-Parlament.
    Du bekommst dann in der App pro Partei eine Position der Parteien zusammengefasst. 
    

    """
)



# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
