import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Projekt europarl.ai", page_icon=":iphone:")

st.sidebar.header("Was ist europarl.ai?")

st.header('FAQ - europarl.ai', divider='blue')

st.subheader('Was ist europarl.ai?')

st.write(
    """
europarl.ai ist eine App, mit der du die Positionen der verschiedener Parteien komprimiert und übersichtlich zusammengefasst bekommst. 




    """
)

st.subheader('Woher kommen die Informationen in der App?')

st.write(
    """
Aus den Wahlprogrammen der deutschen Parteien zur Europawahl und den Reden von deutschen Politiker:innen im Europarlament 


    """
)

st.subheader('Warum wurde europarl.ai entwickelt?')

st.write(
    """
europarl.ai ist unser Abschluss-Projekt für das "Data Science Retreat", ein Bootcamp in Berlin bei dem wir Techniken rund um Data Scince, Maschinelles Lernen und Künstliche Intelligenz erlernt haben.
Mit europarl.ai wollen wir es Wähler:innen erleichtern 

    """
)

st.subheader('Bekomme ich Informationen zu jeder Partei?')

st.write(
    """
Nein, europarl.ai liefert dir eine Zusammenfassung der Positionen der größten Parteien in Deutschland, da es bei der Europawahl allerdings keine Sperrklausel gibt, können sehr viel mehr Kleinstaprteien in das EU-Parlament gewählt werden und treten daher auch bei der Wahl an.


    """
)

st.subheader('Ist europarl.ai neutral und unparteiisch?')

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Quellen der Parteien schöpft, ohne eigene Meinungen oder Interpretationen hinzuzufügen.

    """
)

st.subheader('Wie kann europarl.ai mir bei der Wahl helfen?')
st.write(
    """
Indem du einfach ein Thema auswählst oder eine Frage stellst, durchsucht europarl.ai die Wahlprogramme und Parlamentsreden, um dir eine klare Zusammenfassung der Parteipositionen zu geben.

    """
)


st.subheader('Wie aktuell ist europarl.ai?')

st.write(
    """
Die App ist Anfang April 2024 fertiggestellt worden und wird EAnfang Juni vor der Europawahl aktualisiert werden. 

    """
)