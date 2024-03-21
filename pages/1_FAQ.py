import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Projekt europarl.ai", page_icon=":iphone:")

st.sidebar.header("Mehr zu europarl.ai")

st.header('Am 9. Juni ist Europawahl. ✖️ :Informier Informier dich mit europarl.ai!', divider='blue')

st.subheader('Was ist europarl.ai?')

st.write(
    """
europarl.ai ist eine App, mit der du die Positionen der verschiedener Parteien komprimiert und übersichtlich zusammengefasst bekommst. 
Im Hintergrund nutzen wir eine Retrieval Augmented Generation (RAG) Engine, das tausende von politischen Dokumenten durchsucht. 
Die Stellen in den Dokumenten, die am ähnlichsten zu den keywords in deiner Frage sind, werden rausgepickt und mithilfe eines Large Language Models präzise zusammengefasst.
So erhältst du in der europarl.ai - App eine übersichtliche Zusammenfassung.

    """
)


st.subheader('Wie stellt ihr sicher, dass das LLM nicht halluziniert?')

st.write(
    """
Wir nutzen sehr präzise Prompts und konservative Einstellungen für das LLMs. Wenn deine Frage anhand der politischen Dokumente nicht beantworten kann, antwortet es, dass es keine Informationen dazu gefunden hat.
Außerdem legen wir die Quellen offen, auf denen die Antworten in der App basieren. So kannst du selbst überprüfen, wie deine Antwort zustande gekommen ist.
Dennoch lassen sich Bugs zu 100 Prozent kaum ausschließen. Über einen Feedbackbutton in der App kannst du uns auf Fehler oder Ungereimtheiten in der Antwort aufmerksam machen.


    """
)


st.subheader('Welche Daten verwendet ihr für die App?')

st.write(
    """
Wir nutzen die öffentlichen Wahlprogramme der deutschen Parteien zur Europawahl. Außerdem laden wir die öffentlichen Reden von deutschen Politiker_innen im Europarlament aus der Legislaturperiode 2019 - 2024 über eine API.


    """
)


st.subheader('Bekomme ich Informationen zu jeder Partei?')

st.write(
    """
Nein, europarl.ai liefert dir eine Zusammenfassung der Positionen der größten Parteien in Deutschland. Es treten jedoch noch sehr viel mehr Kleinstparteien bei der Europawahl an, da es im Gegensatz zur Bundeswahl keine pozentuale Sperrklausel gibt für den Einzug ins Parlament.
Einen Überblick über alle weiteren Parteien findest du hier.


    """
)

st.subheader('Ist europarl.ai neutral und unparteiisch?')

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Quellen der Parteien schöpft, ohne die persönlichen Meinungen oder Interpretationen der Macher hinzuzufügen.
Hinter dem Projekt stehen keine Parteien oder Unternehmen.

    """
)
st.subheader('Wie aktuell ist europarl.ai?')

st.write(
    """
Die App ist Anfang April 2024 fertiggestellt worden und wird Anfang Juni 2024 vor der Europawahl aktualisiert werden. 

    """
)

st.subheader('Warum wurde europarl.ai entwickelt?')

st.write(
    """
europarl.ai ist unser Abschluss-Projekt für das "Data Science Retreat", ein Bootcamp in Berlin bei dem wir Techniken rund um Data Scince, Maschinelles Lernen und Künstliche Intelligenz erlernt haben.
Mit europarl.ai wollen wir es Wähler_innen erleichtern, sich vor der Europawahl 2024 zu informieren.

    """
)
