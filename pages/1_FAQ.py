import streamlit as st

st.set_page_config(page_title="Electify - FAQ", page_icon="🇪🇺")

st.header("Am 23. Februar 2025 ist Bundestagswahl in Deutschland. 🗳️ Informiere dich mit Electify!", divider="blue")

st.subheader("Was ist Electify?")

st.write(
    """
Electify ist eine App, mit der du dich zur Bundestagswahl 2025 in Deutschland informieren kannst. 
Stelle deine Frage und unser Modell fasst die Positionen der Parteien zusammen.

Im Hintergrund nutzen wir eine Retrieval-Augmented Generation (RAG) Engine, die Zugriff auf die Wahlprogramme der Parteien hat. 
Unser Algorithmus sucht nach den Textpassagen, die am relevantesten für deine Frage sind. 
Mit Hilfe dieser Information generiert ein KI-Sprachmodell dann übersichtliche Zusammenfassungen für die verschiedenen Parteien.
"""
)

st.subheader("Ist Electify neutral und unparteiisch?")

st.write(
    """
Die App zielt darauf ab, objektive Informationen zu liefern, indem sie direkt aus den Aussagen der Parteien und Politiker_innen schöpft. Dabei werden weder unsere persönlichen Meinungen noch Interpretationen hinzugefügt.
Hinter dem Projekt stehen keine Parteien oder Unternehmen. Wir sind ein unabhängiges Team von Data Scientists, die sich für die Demokratie und den Zugang zu Informationen einsetzen. Mehr zu uns erfährst du [unter Team](https://electify.eu/Team).
    """
)

st.subheader("Wie stellt ihr sicher, dass das KI-Sprachmodell keine Fehler macht?")

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
Wir nutzen die öffentlichen Wahlprogramme der deutschen Parteien zur Bundestagswahl 2025. 
    """
)

st.subheader("Wo finde ich den Code von Electify?")

st.write(
    """
Das Open-Source-Projekt Electify findest du auf [GitHub](https://github.com/electify-eu/electify-app).
    """
)

st.subheader("Bekomme ich Informationen zu jeder Partei?")

st.write(
    """
Über das Menü "Parteien auswählen" können fast alle deutschen Parteien (maximal sechs gleichzeitig) ausgewählt werden, die zurzeit im Bundestag vertreten sind. 
Wir haben "Die Partei" nicht in Electify integriert, da KI-Sprachmodelle Satire und Ironie nur schwer erkennen können.
Standardmäßig sind die sechs größten Parteien ausgewählt.
Electify liefert dir dann eine Zusammenfassung der Positionen dieser Parteien zu deiner Frage. 
Es treten jedoch noch sehr viel mehr Kleinparteien bei der Bundestagswahl an, die bis jetzt nicht im Bundestag vertreten sind. 
Hier findest du einen [Überblick über alle Parteien, die zur Bundestagswahl antreten](https://www.bundeswahlleiterin.de/info/presse/mitteilungen/bundestagswahl-2025/10_25_parteien-wahlteilnahme.html).
    """
)

st.subheader("Wie aktuell ist Electify?")

st.write(
    """
Die Wahlprogramme der Parteien sind teilweise noch nicht beschlossen, sondern stellen nur Entwürfe dar. Wir aktualisieren Electify laufend, sobald neue Informationen verfügbar sind.
    """
)

st.subheader("Warum wurde Electify entwickelt?")

st.write(
    """
Electify wurde zunächst für die Europawahl 2024 entwickelt und hat über 6000 Nutzern bei der Wahlentscheidung unterstützt. Für die Bundestagswahl 2025 wird Electify weiter verbessert und aktualisiert.
Mit Electify wollen wir es Wähler_innen erleichtern, sich vor Wahlen besser über die Standpunkte der verschiedenen Parteien zu informieren.
    """
)
