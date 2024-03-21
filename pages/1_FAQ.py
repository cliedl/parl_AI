import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Projekt europarl.ai", page_icon=":iphone:")

st.sidebar.header("Was ist europarl.ai?")

st.header('FAQ - europarl.ai', divider='blue')

st.subheader('Was ist europarl.ai?')

st.write(
    """
europarl.ai ist eine App, die dir hilft, die Positionen verschiedener Parteien zu Themen, die dir wichtig sind, herauszufinden. Perfekt für die bevorstehende Europawahl!

    """
)


st.subheader('Warum wurde europarl.ai entwickelt?')

st.write(
    """
Weil Europa spannend, aber auch ziemlich komplex ist. Wir wollen es einfacher machen, zu verstehen, wofür die verschiedenen Parteien stehen, besonders wenn es um wichtige Entscheidungen wie die Europawahl geht.

    """
)

st.subheader('Wie kann europarl.ai mir bei der Wahl helfen?')
st.write(
    """
Indem du einfach ein Thema auswählst oder eine Frage stellst, durchsucht europarl.ai die Wahlprogramme und Parlamentsreden, um dir eine klare Zusammenfassung der Parteipositionen zu geben.

    """
)

st.subheader('Welche Themen deckt europarl.ai ab?')
st.write(
    """
Alles von Energiepolitik über Renten bis hin zur Migrationspolitik – europarl.ai deckt eine breite Palette von Themen ab, die auf europäischer Ebene wichtig sind.

    """
)

st.subheader('Woher kommen die Informationen in der App?')

st.write(
    """
Die Informationen werden aus den offiziellen Wahlprogrammen der deutschen Parteien für die Europawahl und den Reden dieser Parteien im EU-Parlament bezogen.


    """
)

st.subheader('Bekomme ich Informationen zu jeder Partei?')

st.write(
    """
Nein, europarl.ai liefert dir eine Zusammenfassung der Positionen der größten Parteien in Deutschland, da es bei der Europawahl allerdings keine Sperrklausel gibt, können sehr viel mehr Kleinstaprteien in das EU-Parlament gewählt werden und treten daher auch bei der Wahl an.


    """
)

st.subheader('Kann europarl.ai mir auch helfen, wenn ich nicht viel über EU-Politik weiß?')
st.write(
    """
Genau dafür ist es da! Die App ist benutzerfreundlich und bietet dir die Informationen, die du brauchst, um eine informierte Entscheidung zu treffen, unabhängig von deinem Vorwissen.

    """
)


st.subheader('Was mache ich, wenn ich spezifische Fragen zu einem Thema habe?')

st.write(
    """
Alles von Energiepolitik über Renten bis hin zur Migrationspolitik – europarl.ai deckt eine breite Palette von Themen ab, die auf europäischer Ebene wichtig sind.Gib einfach deine Frage in die App ein, und europarl.ai wird die relevanten Daten durchsuchen, um dir eine präzise Antwort zu geben.
    """
)


st.subheader('Ist europarl.ai neutral und unparteiisch?')

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Quellen der Parteien schöpft, ohne eigene Meinungen oder Interpretationen hinzuzufügen.

    """
)


st.subheader('Wie aktuell ist europarl.ai?')

st.write(
    """
Die App ist Anfang April 2024 fertiggestellt worden und wird EAnfang Juni vor der Europawahl aktualisiert werden. 

    """
)