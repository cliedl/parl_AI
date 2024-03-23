import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="europarl.ai - FAQ", page_icon="🇪🇺")

# st.sidebar.header("Mehr zu europarl.ai")

st.header(
    "Am 9. Juni ist Europawahl. 🗳️ :Informier Informier dich mit europarl.ai!",
    divider="blue",
)

st.subheader("Was ist europarl.ai?")

st.write(
    """
europarl.ai ist eine App, mit der du dich zur Europawahl 2024 informieren kannst. 
Stelle deine Frage oder gib ein Stichwort ein und unser Modell fasst die Positionen der Parteien zu deinem Input zusammen.

Im Hintergrund nutzen wir eine Retrieval Augmented Generation (RAG) Engine, die Zugriff auf tausende politische Dokumenten hat. 
Unser Algorithmus sucht nach den Dokumente die am relevantesten für deinen Input sind. 
Mit Hilfe dieser Information generiert ein KI-Sprachmodell dann übersichtliche Zusammenfassungen für die verschiedenen Parteien.

So erhältst du in der europarl.ai - App eine übersichtliche Zusammenfassung.
    """
)


st.subheader("Wie stellt ihr sicher, dass das LLM nicht halluziniert?")

st.write(
    """
Wir nutzen sehr präzise Prompts und konservative Einstellungen für das LLM. Wenn deine Frage anhand der politischen Dokumente nicht beantwortet werden kann, sollte der Algorithmus antworten, dass es keine Informationen dazu gefunden hat.
Außerdem legen wir die Quellen offen, auf denen die Antworten in der App basieren. So kannst du selbst überprüfen, wie deine Antwort zustande gekommen ist.
Dennoch lassen sich Fehler zu 100 Prozent kaum ausschließen. Über einen Feedbackbutton in der App kannst du uns auf Fehler oder Ungereimtheiten in der Antwort aufmerksam machen. Dadurch kannst du uns helfen, europarl.ai zu verbessern.
    """
)


st.subheader("Welche Daten verwendet ihr für die App?")

st.write(
    """
Wir nutzen die öffentlichen Wahlprogramme der deutschen Parteien zur Europawahl. 
In der App findest du nur sechs größten deutschen Partein, die auch im Bundestag vertreten sind.
Außerdem nutzen wir die öffentlichen Reden von deutschen Politiker_innen im Europarlament aus der Legislaturperiode der Jahre 2019 - 2024.
    """
)

st.subheader("Wo finde ich den Code von europarl.ai?")

st.write(
    """
Das Projekt europarl.ai findest du auf [GitHub](https://github.com/europarl-ai/europarl-ai). Das Projekt ist Open-Source und mit einer MIT-Lizenz lizensiert.
    """
)

st.subheader("Bekomme ich Informationen zu jeder Partei?")

st.write(
    """
Nein, europarl.ai liefert dir eine Zusammenfassung der Positionen der größten Parteien in Deutschland. Es treten jedoch noch sehr viel mehr Kleinstparteien bei der Europawahl an, da es im Gegensatz zur Wahl des Bundestages keine pozentuale Sperrklausel gibt für den Einzug ins EU-Parlament.
Einen Überblick über alle weiteren Parteien findest du [hier](https://www.europawahl-bw.de/deutsche-parteien).


    """
)

st.subheader("Ist europarl.ai neutral und unparteiisch?")

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Quellen der Parteien und Reden der Politiker_innen schöpft. Dabei werden weder die persönlichen Meinungen noch Interpretationen der Macher_innen hinzugefügt.
Hinter dem Projekt stehen keine Parteien oder Unternehmen.

    """
)
st.subheader("Wie aktuell ist europarl.ai?")

st.write(
    """
Die App ist Anfang April 2024 fertiggestellt worden und wird Anfang Juni 2024 vor der Europawahl aktualisiert werden. 

    """
)

st.subheader("Warum wurde europarl.ai entwickelt?")

st.write(
    """
europarl.ai ist unser Abschluss-Projekt für das ["Data Science Retreat"](https://datascienceretreat.com/), ein Bootcamp in Berlin bei dem wir Techniken rund um Data Scince, Maschinelles Lernen und Künstliche Intelligenz erlernt haben.
Mit europarl.ai wollen wir es Wähler_innen erleichtern, sich vor der Europawahl 2024 besser über die Standpunkte der verschiedenen Parteien zu informieren.

    """
)
