import streamlit as st
import sys
import time
import random

# Directory of RAG modules

from RAG_clean.models.generation import generate_chain_with_balanced_retrieval
from RAG_clean.database.vector_database import VectorDatabase
from RAG_clean.models.embedding import ManifestoBertaEmbeddings

DATABASE_DIR_MANIFESTOS = "../data/manifestos/chroma"
DATABASE_DIR_DEBATES = "../data/debates/chroma"
DELAY = 0.05  # pause between words in text stream (in seconds)


### LANGCHAIN ###
@st.cache_resource
def load_embedding_model():
    return ManifestoBertaEmbeddings()


embedding_model = ManifestoBertaEmbeddings()


@st.cache_resource
def load_db_manifestos():
    return VectorDatabase(
        embedding_model=embedding_model,
        source_type="debates",
        database_directory=DATABASE_DIR_MANIFESTOS,
    )


db_manifestos = load_db_manifestos()

chain = generate_chain_with_balanced_retrieval([db_manifestos])


### INITIALIZATION ###
if "query_submitted" not in st.session_state:
    st.session_state.query_submitted = False
if "response" not in st.session_state:
    st.session_state.response = None


def streaming(text, delay=DELAY):
    # Chose random response from a list
    for word in text.split():
        yield word + " "
        time.sleep(delay)


party_dict = {
    "cdu_summary": {
        "name": "CDU/CSU",
        "image": "streamlit/assets/cdu_logo.png",
        "manifesto_link": "https://assets.ctfassets.net/nwwnl7ifahow/476rnHcYPkmyuONPvSTKO2/972e88ceb862ac4d4905d98441555e0c/europawahlprogramm-cdu-csu-2024_0.pdf",
    },
    "spd_summary": {
        "name": "SPD",
        "image": "streamlit/assets/spd_logo.png",
        "manifesto_link": "https://www.spd.de/fileadmin/Dokumente/EuroDel/20240128_Europaprogramm.pdf",
    },
    "gruene_summary": {
        "name": "Bündnis 90 / Die Grünen",
        "image": "streamlit/assets/gruene_logo.png",
        "manifesto_link": "https://cms.gruene.de/uploads/assets/Europawahlprogramm-2024-Bu%CC%88ndnis90Die-Gru%CC%88nen_Wohlstand_Gerechtigkeit_Frieden_Freiheit.pdf",
    },
    "fdp_summary": {
        "name": "FDP",
        "image": "streamlit/assets/fdp_logo.png",
        "manifesto_link": "https://www.fdp.de/sites/default/files/2024-01/fdp_europawahlprogramm-2024_vorabversion.pdf",
    },
    "afd_summary": {
        "name": "AfD",
        "image": "streamlit/assets/afd_logo.png",
        "manifesto_link": "https://www.afd.de/wp-content/uploads/2023/11/2023-11-16-_-AfD-Europawahlprogramm-2024-_-web.pdf",
    },
    "linke_summary": {
        "name": "Die Linke",
        "image": "streamlit/assets/linke_logo.png",
        "manifesto_link": "https://www.die-linke.de/fileadmin/user_upload/Europawahlprogramm_2023_neu2.pdf",
    },
}


def submit_query():
    st.session_state.query_submitted = True


def generate_response():
    st.session_state.response = chain.invoke(query)


### INTERFACE ###
st.title("🇪🇺 Europawahl 2024: Find your match")

query = st.text_input(
    label="Stelle eine Frage an die Parteien zur Europawahl:",
    # placeholder="Wie stehen die Parteien zum Emmissionshandel?",
    value="Wie stehen die Parteien zum Emmissionshandel?",
)


st.button("Frage stellen", on_click=submit_query, type="primary")

if st.session_state.query_submitted:
    with st.spinner(
        "Suche nach Antworten in Wahlprogrammen und Parlamentsdebatten... 🕵️‍♂️"
    ):
        generate_response()

    parties = list(party_dict.keys())
    random.shuffle(parties)

    if st.session_state.response is not None:
        st.markdown(":grey[Die Reihenfolge der Parteien ist zufällig.]")

        col1, col2 = st.columns([0.3, 0.7])
        col3, col4 = st.columns([0.3, 0.7])
        col5, col6 = st.columns([0.3, 0.7])
        col7, col8 = st.columns([0.3, 0.7])
        col9, col10 = st.columns([0.3, 0.7])
        col11, col12 = st.columns([0.3, 0.7])

        col_list = [
            col1,
            col2,
            col3,
            col4,
            col5,
            col6,
            col7,
            col8,
            col9,
            col10,
            col11,
            col12,
        ]

        i = 0
        for party in parties:
            with col_list[i]:
                st.write("")
                st.write("")
                st.image(party_dict[party]["image"])
            with col_list[i + 1]:
                st.header(party_dict[party]["name"])
                st.write_stream(streaming(st.session_state.response[party]))
                st.write(
                    f'Mehr dazu im [Europawahlprogramm der Partei **{party_dict[party]["name"]}**]({party_dict[party]["manifesto_link"]})'
                )
            i += 2
