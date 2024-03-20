import streamlit as st
import random
from trubrics.integrations.streamlit import FeedbackCollector
import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from RAG_clean.models.generation import generate_chain_with_balanced_retrieval
from RAG_clean.database.vector_database import VectorDatabase
from app_utils.translate import translate



# from RAG_clean.models.embedding import ManifestoBertaEmbeddings

DATABASE_DIR_MANIFESTOS = "./data/manifestos/chroma/openai"
DATABASE_DIR_DEBATES = "./data/debates/chroma/openai"
DELAY = 0.05  # pause between words in text stream (in seconds)
TEMPERATURE = 0.0
LARGE_LANGUAGE_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo", max_tokens=2000, temperature=TEMPERATURE
)


### LANGCHAIN SETUP ###
@st.cache_resource
def load_embedding_model():
    return OpenAIEmbeddings(model="text-embedding-3-large")


embedding_model = load_embedding_model()


@st.cache_resource
def load_db_manifestos():
    return VectorDatabase(
        embedding_model=embedding_model,
        source_type="manifestos",
        database_directory=DATABASE_DIR_MANIFESTOS,
    )


db_manifestos = load_db_manifestos()

chain = generate_chain_with_balanced_retrieval(
    [db_manifestos],
    llm=LARGE_LANGUAGE_MODEL,
    return_context=True,
)


### TRUBRICS SETUP ###
collector = FeedbackCollector(
    project="default",
    # for local testing, use environment variables:
    email=os.environ.get("TRUBRICS_EMAIL"),
    password=os.environ.get("TRUBRICS_PASSWORD"),
    # for deployment, use streamlit secrets:
    # email=st.secrets.TRUBRICS_EMAIL,
    # password=st.secrets.TRUBRICS_PASSWORD,
)


### INITIALIZATION ###
party_dict = {
    "cdu": {
        "name": "CDU/CSU",
        "image": "streamlit/assets/cdu_logo.png",
        "manifesto_link": "https://assets.ctfassets.net/nwwnl7ifahow/476rnHcYPkmyuONPvSTKO2/972e88ceb862ac4d4905d98441555e0c/europawahlprogramm-cdu-csu-2024_0.pdf",
    },
    "spd": {
        "name": "SPD",
        "image": "streamlit/assets/spd_logo.png",
        "manifesto_link": "https://www.spd.de/fileadmin/Dokumente/EuroDel/20240128_Europaprogramm.pdf",
    },
    "gruene": {
        "name": "Bündnis 90/Die Grünen",
        "image": "streamlit/assets/gruene_logo.png",
        "manifesto_link": "https://cms.gruene.de/uploads/assets/Europawahlprogramm-2024-Bu%CC%88ndnis90Die-Gru%CC%88nen_Wohlstand_Gerechtigkeit_Frieden_Freiheit.pdf",
    },
    "fdp": {
        "name": "FDP",
        "image": "streamlit/assets/fdp_logo.png",
        "manifesto_link": "https://www.fdp.de/sites/default/files/2024-01/fdp_europawahlprogramm-2024_vorabversion.pdf",
    },
    "afd": {
        "name": "AfD",
        "image": "streamlit/assets/afd_logo.png",
        "manifesto_link": "https://www.afd.de/wp-content/uploads/2023/11/2023-11-16-_-AfD-Europawahlprogramm-2024-_-web.pdf",
    },
    "linke": {
        "name": "Die Linke",
        "image": "streamlit/assets/linke_logo.png",
        "manifesto_link": "https://www.die-linke.de/fileadmin/user_upload/Europawahlprogramm_2023_neu2.pdf",
    },
}


if "response" not in st.session_state:
    st.session_state.response = None
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "query" not in st.session_state:
    st.session_state.query = ""
if "logged_prompt" not in st.session_state:
    st.session_state.logged_prompt = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0
if "language" not in st.session_state:
    st.session_state.language = "Deutsch"
if "show_parties" not in st.session_state:
    st.session_state.show_parties = True
if "parties" not in st.session_state:
    st.session_state.parties = list(party_dict.keys())


# def streaming(text, delay=DELAY):
#     # Chose random response from a list
#     for word in text.split():
#         yield word + " "
#         time.sleep(delay)


def submit_query():
    st.session_state.logged_prompt = None
    st.session_state.response = None
    st.session_state.feedback = None
    st.session_state.stage = 1
    st.session_state.feedback_key += 1
    random.shuffle(st.session_state.parties)


def generate_response():
    st.session_state.response = chain.invoke(query)


### INTERFACE ###
  

st.title("🇪🇺 europarl.ai 2024")

selected_language = st.radio(
    label="Language",
    options=["🇩🇪 Deutsch", "🇬🇧 English"],
    horizontal=True,
)
languages = {"🇩🇪 Deutsch": "Deutsch", "🇬🇧 English": "English"}
st.session_state.language = languages[selected_language]

query = st.text_input(
    label=translate(
        "Gib ein Stichwort ein oder stelle eine Frage an die Parteien zur Europawahl:",
        st.session_state.language,
    ),
    placeholder=translate(
        "Wie stehen die Parteien zum Emmissionshandel?",
        language=st.session_state.language,
    ),
    value="",
)

st.session_state.show_parties = st.checkbox(
    label=translate("Parteinamen anzeigen", st.session_state.language),
    value=True,
    help=translate(
        "Du kannst die Namen der Parteien ausblenden, wenn du die Antworten zunächst unvoreingenommen lesen möchtest.",
        st.session_state.language,
    ),
)

st.button(
    translate("Frage stellen", st.session_state.language),
    on_click=submit_query,
    type="primary",
)

# STAGE 1: GENERATE RESPONSE
if st.session_state.stage == 1:
    with st.spinner(
        translate(
            "Suche nach Antworten in Wahlprogrammen...", st.session_state.language
        )
        + "🕵️"
    ):
        generate_response()

    st.session_state.logged_prompt = collector.log_prompt(
        config_model={"model": LARGE_LANGUAGE_MODEL.model_name},
        prompt=query,
        generation=str(st.session_state.response),
    )

    st.session_state.stage = 2

# STAGE >= 1: DISPLAY RESPONSE
if st.session_state.stage > 1:
    st.markdown(
        f":grey[{translate('Die Reihenfolge der Parteien ist zufällig.', st.session_state.language,)}]",
    )

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
    p = 1
    for party in st.session_state.parties:

        most_relevant_manifesto_page_number = st.session_state.response["docs"][
            "manifestos"
        ][party][0].metadata["page"]

        with col_list[i]:
            st.write("")
            st.write("")
            if st.session_state.show_parties:
                st.image(party_dict[party]["image"])
            else:
                st.image("streamlit/assets/placeholder_logo.png")

        with col_list[i + 1]:
            if st.session_state.show_parties:
                st.header(party_dict[party]["name"])
            else:
                st.header(f"Partei {p}")
            st.write(st.session_state.response["answer"][party])
            if st.session_state.show_parties:
                st.write(
                    f"""{translate('Mehr dazu im', st.session_state.language)}
                        [{translate('Europawahlprogramm der Partei', st.session_state.language)} 
                        **{party_dict[party]['name']}** 
                        ({translate('z.B. Seite', st.session_state.language)} {most_relevant_manifesto_page_number+1})]({party_dict[party]['manifesto_link']}#page={most_relevant_manifesto_page_number+1})"""
                )
        i += 2
        p += 1

    st.subheader(
        translate("Worauf basieren diese Antworten?", st.session_state.language)
    )
    st.write(
        translate(
            "Die Antworten wurden von dem KI-Sprachmodell GPT 3.5 generiert – unter Berücksichtigung der Wahlprogramme zur Europawahl 2024 und vergangenen Reden im Europaparlament im Zeitraum 2019-2024.",
            st.session_state.language,
        )
    )
    st.write(
        translate(
            "Hier kannst du die genutzten Ausschnitte aus den Quellen einsehen:",
            st.session_state.language,
        )
    )
    with st.expander(translate("Quellen anzeigen", st.session_state.language)):
        for party in st.session_state.parties:
            st.subheader(party_dict[party]["name"])
            for doc in st.session_state.response["docs"]["manifestos"][party]:
                manifesto_excerpt = doc.page_content.replace("\n", " ")
                st.markdown(
                    f"**Seite {doc.metadata['page']+1} im Wahlprogramm**: \n {manifesto_excerpt}\n\n"
                )
            # TODO: Add debates once we load them as well
            # for doc in st.session_state.response["docs"]["debates"][party]:
            #     st.write(f"Rede: {doc.page_content}")

    st.markdown("---")
    st.write(
        f"### {translate('Waren diese Antworten hilfreich für dich?', st.session_state.language)}"
    )
    st.write(
        translate(
            "Mit deinem Feedback hilfst du uns, die Qualität der Antworten zu verbessern.",
            st.session_state.language,
        )
    )

    st.session_state.stage = 3


# TRUBRICS FEEDBACK
if st.session_state.stage == 3:

    st.session_state.feedback = collector.st_feedback(
        component="default",
        feedback_type="thumbs",
        model=LARGE_LANGUAGE_MODEL.model_name,
        prompt_id=st.session_state.logged_prompt.id,
        open_feedback_label="Weiteres Feedback (optional)",
        align="flex-start",
        key=f"feedback_{st.session_state.feedback_key}",
    )

    if st.session_state.feedback is not None:
        st.write(
            translate("Vielen Dank für dein Feedback!", st.session_state.language)
            + " 🙏"
        )
