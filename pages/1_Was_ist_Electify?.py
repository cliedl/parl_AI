import streamlit as st

st.set_page_config(page_title="Electify - Was ist Electify?", page_icon="🇪🇺")

st.header(
    "Am 9. Juni 2024 ist Europawahl. 🗳️ :placeholder Informiere dich mit Electify!",
    divider="blue",
)

st.subheader("Was ist Electify?")

st.write(
    """
Electify ist eine App, mit der du dich zur Europawahl 2024 in Deutschland informieren kannst. 
Stelle deine Frage und unser Modell fasst die Positionen der Parteien zusammen.

Im Hintergrund nutzen wir eine Retrieval-Augmented Generation (RAG) Engine, die Zugriff auf tausende politische Dokumente hat (Wahlprogramme und Parlamentsdebatten). 
Unser Algorithmus sucht nach den Dokumenten, die am relevantesten für deine Frage sind. 
Mit Hilfe dieser Information generiert ein KI-Sprachmodell dann übersichtliche Zusammenfassungen für die verschiedenen Parteien.
"""
)


st.subheader("Wie stellt ihr sicher, dass das KI-Sprachmodell nicht halluziniert?")

st.write(
    """
Wir nutzen sehr präzise Prompts und robuste Einstellungen für das KI-Sprachmodell. Wenn deine Frage anhand der politischen Dokumente nicht beantwortet werden kann, sollte der Algorithmus auch genau das antworten.
Außerdem legen wir die Quellen offen, auf denen die Antworten basieren. So kannst du selbst überprüfen, wie deine Antwort zustande gekommen ist.
Dennoch lassen sich Fehler nicht zu 100 Prozent ausschließen. Wenn dir Fehler oder Ungereimtheiten auffallen, [melde dich gerne bei uns](mailto:electify.eu@gmail.com). Dadurch kannst du uns helfen, Electify zu verbessern.
    """
)


st.subheader("Welche Daten verwendet ihr für die App?")

st.write(
    """
Wir nutzen die öffentlichen Wahlprogramme der deutschen Parteien zur Europawahl. Außerdem nutzen wir die [öffentlichen Reden](https://data.europarl.europa.eu/de/home) von deutschen Politiker_innen im EU-Parlament aus der Legislaturperiode 2019 - 2024. 
    """
)

st.subheader("Wo finde ich den Code von Electify?")

st.write(
    """
Das Open-Source-Projekt Electify findest du auf [GitHub](https://github.com/europarl-ai/europarl-ai) (MIT-Lizenz).
    """
)

st.subheader("Bekomme ich Informationen zu jeder Partei?")

st.write(
    """
Über das Menü "Parteien auswählen" können alle deutschen Parteien (maximal sechs gleichzeitig) ausgewählt werden, die zurzeit im Europaparlament vertreten sind. 
Standardmäßig sind die sechs größten Parteien ausgewählt.
Electify liefert dir dann eine Zusammenfassung der Positionen dieser Parteien zu deiner Frage. 
Es treten jedoch noch sehr viel mehr Kleinparteien bei der Europawahl an, die bis jetzt nicht im Europaparlament vertreten sind. 
Da unser Modell auch auf den Reden der deutschen Politiker_innen im EU-Parlament basiert, können wir keine Informationen zu diesen Parteien liefern.
Hier findest du einen [Überblick über alle Parteien, die zur Europawahl antreten](https://www.europawahl-bw.de/deutsche-parteien).
    """
)

st.subheader("Ist Electify neutral und unparteiisch?")

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Aussagen der Parteien und Politiker_innen schöpft. Dabei werden weder unsere persönlichen Meinungen noch Interpretationen hinzugefügt.
Hinter dem Projekt stehen keine Parteien oder Unternehmen. Wir sind ein unabhängiges Team von Data Scientists, die sich für die Demokratie und den Zugang zu Informationen einsetzen.
    """
)
st.subheader("Wie aktuell ist Electify?")

st.write(
    """
Die App ist Anfang April 2024 fertiggestellt worden und wird kurz vor der Europawahl aktualisiert werden.
    """
)

st.subheader("Warum wurde Electify entwickelt?")

st.write(
    """
Electify ist unser Abschluss-Projekt für das ["Data Science Retreat"](https://datascienceretreat.com/), ein Weiterbildungsprogramm für Data Science, Maschinelles Lernen und Künstliche Intelligenz.
Mit Electify wollen wir es Wähler_innen erleichtern, sich vor der Europawahl 2024 besser über die Standpunkte der verschiedenen Parteien zu informieren.
    """
)
