import streamlit as st

st.set_page_config(page_title="Electify - Datenschutzerklärung", page_icon="🇪🇺")


st.header("Datenschutzerklärung", divider="blue")

### WARNING: Careful, height of html box has to be large enough to fit text!!!!
st.write(
    """
    Verantwortlicher im Sinne der Datenschutzgesetze, insbesondere der EU-Datenschutzgrundverordnung (DSGVO), ist:  
    Electify GbR, siehe [Impressum](../Impressum)
    """
)

st.subheader("Ihre Betroffenenrechte")
st.write(
    """
    Unter den angegebenen [Kontaktdaten](../Impressum) unseres Datenschutzbeauftragten können Sie jederzeit folgende Rechte ausüben:
    
    * Auskunft über Ihre bei uns gespeicherten Daten und deren Verarbeitung (Art. 15 DSGVO),
    * Berichtigung unrichtiger personenbezogener Daten (Art. 16 DSGVO),
    * Löschung Ihrer bei uns gespeicherten Daten (Art. 17 DSGVO),
    * Einschränkung der Datenverarbeitung, sofern wir Ihre Daten aufgrund gesetzlicher Pflichten noch nicht löschen dürfen (Art. 18 DSGVO),
    * Widerspruch gegen die Verarbeitung Ihrer Daten bei uns (Art. 21 DSGVO) und
    * Datenübertragbarkeit, sofern Sie in die Datenverarbeitung eingewilligt haben oder einen Vertrag mit uns abgeschlossen haben (Art. 20 DSGVO).
    """
)
st.write(
    """
    Sofern Sie uns eine Einwilligung erteilt haben, können Sie diese jederzeit mit Wirkung für die Zukunft widerrufen.
    Sie können sich jederzeit mit einer Beschwerde an eine Aufsichtsbehörde wenden, z. B. an die zuständige Aufsichtsbehörde des Bundeslands Ihres Wohnsitzes oder an die für uns als verantwortliche Stelle zuständige Behörde.
    Hier finden sie eine [Liste der Aufsichtsbehörden](https://www.bfdi.bund.de/DE/Service/Anschriften/Laender/Laender-node.html) (für den nichtöffentlichen Bereich) mit Anschrift.
    """
)
st.subheader("Erfassung allgemeiner Informationen beim Besuch unserer Website")
st.write(
    """     
    ##### Art und Zweck der Verarbeitung:

    Wenn Sie auf unsere Website zugreifen, d.h., wenn Sie sich nicht registrieren oder anderweitig Informationen übermitteln, werden automatisch Informationen allgemeiner Natur erfasst. Diese Informationen (Server-Logfiles) beinhalten etwa die Art des Webbrowsers, das verwendete Betriebssystem, den Domainnamen Ihres Internet-Service-Providers, Ihre IP-Adresse und ähnliches.
    Sie werden insbesondere zu folgenden Zwecken verarbeitet:
    
    * Sicherstellung eines problemlosen Verbindungsaufbaus der Website,
    * Sicherstellung einer reibungslosen Nutzung unserer Website,
    * Auswertung der Systemsicherheit und -stabilität sowie
    * zur Optimierung unserer Website.

    Wir verwenden Ihre Daten nicht, um Rückschlüsse auf Ihre Person zu ziehen. Informationen dieser Art werden von uns ggfs. anonymisiert statistisch ausgewertet, um unseren Internetauftritt und die dahinterstehende Technik zu optimieren.
    """
)
st.write(
    """
    ##### Rechtsgrundlage und berechtigtes Interesse:

    Die Verarbeitung erfolgt gemäß Art. 6 Abs. 1 lit. f DSGVO auf Basis unseres berechtigten Interesses an der Verbesserung der Stabilität und Funktionalität unserer Website. 
    """
)

st.write(
    """
    ##### Drittanbieter:

    * Wir nutzen den Webhoster Google Cloud der Google Ireland Ltd. (Irland, EU), die gemäß Artikel 28 DSGVO beauftragt wurde.
    Näheres zur Art und Weise der Verarbeitung bei diesem Drittanbieter ist [hier](https://cloud.google.com/run?hl=de) beschrieben. 
    Der Serverstandort befindet sich dabei in Belgien, EU.
    Es ist nicht auszuschließen, dass eine Datenübermittlung an die Muttergesellschaft Google LLC (USA) z.B. zu Wartungszwecken erfolgt.
    Dies steht der Beauftragung nicht entgegen, da sich die Google LLC (USA) gemäß den EU-Standardvertragsklauseln verpflichtet hat.

    * Wir nutzen im Zusammenhang mit dem Einsatz künstlicher Intelligenz (KI) das API-Tool
    der OpenAI, LLC (USA), die gemäß Artikel 28 DSGVO beauftragt wurde. 
    Dabei werden Eingabedaten über ein Eingabefeld erhoben und an die externe Anwendung der OpenAI LLC übermittelt, die mit Hilfe künstlicher Intelligenz eine Antwort generiert.
    Aus dieser Interaktion werden Erkenntnisse gewonnen, die einerseits das KI-System trainieren und andererseits sowohl den
    Verantwortlichen als auch OpenAI LLC zur Verfügung stehen. Zweck ist die zielgerichtete
    und stets verfügbare Kommunikation mit den Betroffenen. Darin liegt auch das berechtigte Interesse.
    Hierbei werden folgende Daten verarbeitet: Eingabedaten, Erkenntnisse aus den Eingaben.
    Näheres zur Art und Weise der Verarbeitung bei diesem Drittanbieter ist [hier](https://openai.com/policies/privacy-policy) beschrieben. 
    Dem Einsatz dieses Drittanbieters steht nicht entgegen, dass dieser seinen Sitz außerhalb der EU
    hat, da der Anbieter hat sich gemäß den EU-Standardvertragsklauseln verpflichtet.

    * Der Nutzer hat die Möglichkeit, seine Wertschätzung für die zur Verfügung gestellten Informationen durch eine Spende auszudrücken. 
    Dies geschieht über einen externen Link zum Dienst „Buy me a Coffee“ der Publisherr Inc. (USA). Dabei werden Daten von „Buy me a Coffee“ verarbeitet und auf Systemen von Publisherr Inc. gespeichert. 
    Wir weisen darauf hin, dass wir keine Kenntnis vom Inhalt der übermittelten Daten sowie deren Nutzung durch „Buy me a Coffee“ erhalten. 
    Weitere Informationen hierzu finden Sie [hier](https://www.buymeacoffee.com/privacy-policy).
    """
)

st.write(
    """
    ##### Speicherdauer: 

    Die Daten werden gelöscht, sobald diese für den Zweck der Erhebung nicht mehr erforderlich sind. Dies ist für die Daten, die der Bereitstellung der Website dienen, grundsätzlich der Fall, wenn die jeweilige Sitzung beendet ist.

    ##### Bereitstellung vorgeschrieben oder erforderlich:

    Die Bereitstellung der vorgenannten personenbezogenen Daten ist weder gesetzlich noch vertraglich vorgeschrieben. Ohne die IP-Adresse ist jedoch der Dienst und die Funktionsfähigkeit unserer Website nicht gewährleistet. Zudem können einzelne Dienste und Services nicht verfügbar oder eingeschränkt sein. Aus diesem Grund ist ein Widerspruch ausgeschlossen.
    """
)

st.subheader("Cookies")
st.write(
    """
    Wie viele andere Webseiten verwenden wir auch so genannte „Cookies“. Bei Cookies handelt es sich um kleine Textdateien, die auf Ihrem Endgerät (Laptop, Tablet, Smartphone o.ä.) gespeichert werden, wenn Sie unsere Webseite besuchen.
    Sie können einzelne Cookies oder den gesamten Cookie-Bestand löschen. Darüber hinaus erhalten Sie Informationen und Anleitungen, wie diese Cookies gelöscht oder deren Speicherung vorab blockiert werden können. Je nach Anbieter Ihres Browsers finden Sie die notwendigen Informationen unter den nachfolgenden Links:

    * [Mozilla Firefox](https://support.mozilla.org/de/kb/cookies-loeschen-daten-von-websites-entfernen)
    * [Internet Explorer](https://support.microsoft.com/de-de/help/17442/windows-internet-explorer-delete-manage-cookies)
    * [Google Chrome](https://support.google.com/accounts/answer/61416?hl=de)
    * [Opera](http://www.opera.com/de/help)
    * [Safari](https://support.apple.com/de-de/105082)
    """
)

st.write(
    """
    ##### Speicherdauer und eingesetzte Cookies:

    Soweit Sie uns durch Ihre Browsereinstellungen oder Zustimmung die Verwendung von Cookies erlauben, können folgende Cookies auf unseren Webseiten zum Einsatz kommen:
    Wir setzen Cookies ein, um unsere Website nutzerfreundlicher zu gestalten. Einige Elemente unserer Internetseite erfordern es, dass der aufrufende Browser auch nach einem Seitenwechsel identifiziert werden kann.
    Der Zweck der Verwendung technisch notwendiger Cookies ist, die Nutzung von Websites für die Nutzer zu vereinfachen. Einige Funktionen unserer Internetseite können ohne den Einsatz von Cookies nicht angeboten werden. Für diese ist es erforderlich, dass der Browser auch nach einem Seitenwechsel wiedererkannt wird.

    ##### Rechtsgrundlage und berechtigtes Interesse: 

    Die Verarbeitung erfolgt gemäß Art. 6 Abs. 1 lit. f DSGVO auf Basis unseres berechtigten Interesses an einer nutzerfreundlichen Gestaltung unserer Website.

    ##### Bereitstellung vorgeschrieben oder erforderlich:

    Die Bereitstellung der vorgenannten personenbezogenen Daten ist weder gesetzlich noch vertraglich vorgeschrieben. Ohne diese Daten ist jedoch der Dienst und die Funktionsfähigkeit unserer Website nicht gewährleistet. Zudem können einzelne Dienste und Services nicht verfügbar oder eingeschränkt sein.

    ##### Widerspruch:

    Lesen Sie dazu die Informationen über Ihr Widerspruchsrecht nach Art. 21 DSGVO weiter unten.

    """
)

st.subheader("SSL-Verschlüsselung")
st.write(
    "Um die Sicherheit Ihrer Daten bei der Übertragung zu schützen, verwenden wir dem aktuellen Stand der Technik entsprechende Verschlüsselungsverfahren (z. B. SSL) über HTTPS."
)

st.subheader("Information über Ihr Widerspruchsrecht nach Art. 21 DSGVO")
st.write(
    """
    ##### Einzelfallbezogenes Widerspruchsrecht:

    Sie haben das Recht, aus Gründen, die sich aus Ihrer besonderen Situation ergeben, jederzeit gegen die Verarbeitung Sie betreffender personenbezogener Daten, die aufgrund Art. 6 Abs. 1 lit. f DSGVO (Datenverarbeitung auf der Grundlage einer Interessenabwägung) erfolgt, Widerspruch einzulegen; dies gilt auch für ein auf diese Bestimmung gestütztes Profiling im Sinne von Art. 4 Nr. 4 DSGVO.
    Legen Sie Widerspruch ein, werden wir Ihre personenbezogenen Daten nicht mehr verarbeiten, es sei denn, wir können zwingende schutzwürdige Gründe für die Verarbeitung nachweisen, die Ihre Interessen, Rechte und Freiheiten überwiegen, oder die Verarbeitung dient der Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen.

    ##### Empfänger eines Widerspruchs:

    Electify GbR, siehe [Impressum](../Impressum).
    """
)

st.subheader("Änderung unserer Datenschutzbestimmungen")

st.write(
    "Wir behalten uns vor, diese Datenschutzerklärung anzupassen, damit sie stets den aktuellen rechtlichen Anforderungen entspricht oder um Änderungen unserer Leistungen in der Datenschutzerklärung umzusetzen, z.B. bei der Einführung neuer Services. Für Ihren erneuten Besuch gilt dann die neue Datenschutzerklärung."
)

st.write(
    """
    ##### Fragen an den Datenschutzbeauftragten:

    Wenn Sie Fragen zum Datenschutz haben, schreiben Sie uns bitte eine [E-Mail](mailto:electify.eu@gmail.com) oder kontaktieren Sie uns [postalisch](../Impressum).
    """
)

st.write(
    "Die Datenschutzerklärung wurde mithilfe der activeMind AG erstellt, den Experten für [externe Datenschutzbeauftragte](https://www.activemind.de/datenschutz/datenschutzbeauftragter/) (Version #2020-09-30)."
)
