import streamlit as st
import random
from trubrics.integrations.streamlit import FeedbackCollector
import os
import re
import csv
import random
from datetime import datetime


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from RAG.models.generation import generate_chain
from RAG.models.RAG import RAG
from RAG.database.vector_database import VectorDatabase
from streamlit_app.utils.translate import translate

# The following is necessary to make the code work in the deployed version.
# (We need a newer version of sqlite3 than the one provided by Streamlit.)
# The environment variable IS_DEPLOYED is created only in the Streamlit Secrets and set to the string "TRUE".
if os.getenv("IS_DEPLOYED", default="FALSE") == "TRUE":
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules["pysqlite3"]

# from RAG.models.embedding import ManifestoBertaEmbeddings

DATABASE_DIR_MANIFESTOS = "./data/manifestos/chroma/openai"
DATABASE_DIR_DEBATES = "./data/debates/chroma/openai"
DELAY = 0.05  # pause between words in text stream (in seconds)
TEMPERATURE = 0.0
LARGE_LANGUAGE_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo", max_tokens=400, temperature=TEMPERATURE
)


# Streamlit page conifg
st.set_page_config(page_title="europarl.ai", page_icon="🇪🇺", layout="centered")


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


@st.cache_resource
def load_db_debates():
    return VectorDatabase(
        embedding_model=embedding_model,
        source_type="debates",
        database_directory=DATABASE_DIR_DEBATES,
    )


rag = RAG(
    databases=[load_db_manifestos(), load_db_debates()],
    llm=LARGE_LANGUAGE_MODEL,
    k=3,
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
        "image": "streamlit_app/assets/cdu_logo.png",
        "manifesto_link": "https://assets.ctfassets.net/nwwnl7ifahow/476rnHcYPkmyuONPvSTKO2/972e88ceb862ac4d4905d98441555e0c/europawahlprogramm-cdu-csu-2024_0.pdf",
    },
    "spd": {
        "name": "SPD",
        "image": "streamlit_app/assets/spd_logo.png",
        "manifesto_link": "https://www.spd.de/fileadmin/Dokumente/EuroDel/20240128_Europaprogramm.pdf",
    },
    "gruene": {
        "name": "Bündnis 90/Die Grünen",
        "image": "streamlit_app/assets/gruene_logo.png",
        "manifesto_link": "https://cms.gruene.de/uploads/assets/Europawahlprogramm-2024-Bu%CC%88ndnis90Die-Gru%CC%88nen_Wohlstand_Gerechtigkeit_Frieden_Freiheit.pdf",
    },
    "linke": {
        "name": "Die Linke",
        "image": "streamlit_app/assets/linke_logo.png",
        "manifesto_link": "https://www.die-linke.de/fileadmin/user_upload/Europawahlprogramm_2023_neu2.pdf",
    },
    "fdp": {
        "name": "FDP",
        "image": "streamlit_app/assets/fdp_logo.png",
        "manifesto_link": "https://www.fdp.de/sites/default/files/2024-01/fdp_europawahlprogramm-2024_vorabversion.pdf",
    },
    "afd": {
        "name": "AfD",
        "image": "streamlit_app/assets/afd_logo.png",
        "manifesto_link": "https://www.afd.de/wp-content/uploads/2023/11/2023-11-16-_-AfD-Europawahlprogramm-2024-_-web.pdf",
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
else:
    rag.language = st.session_state.language
if "parties" not in st.session_state:
    st.session_state.parties = list(party_dict.keys())
if "show_individual_parties" not in st.session_state:
    # The values in this dict will only be set true if a party name is explicitly "revealed" by the user.
    # The keys represent the (random) order of appearance of the parties in the app
    # and not fixed parties as opposed to the above party_dict.

    st.session_state.show_individual_parties = {
        f"party_{i+1}": False for i in range(len(st.session_state.parties))
    }


if "show_all_parties" not in st.session_state:
    st.session_state.show_all_parties = True
if "example_prompts" not in st.session_state:
    all_example_prompts = {}
    with open("streamlit_app/example_prompts.csv", "r") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            for key, value in row.items():
                if key not in all_example_prompts:
                    all_example_prompts[key] = []
                all_example_prompts[key].append(value)

    st.session_state.example_prompts = {
        key: random.sample(value, 3) for key, value in all_example_prompts.items()
    }


def reveal_party(p):
    st.session_state.show_individual_parties[f"party_{p}"] = True


def submit_query():
    st.session_state.logged_prompt = None
    st.session_state.response = None
    st.session_state.feedback = None
    st.session_state.stage = 1
    st.session_state.feedback_key += 1
    st.session_state.show_individual_parties = {
        f"party_{i+1}": False for i in range(len(st.session_state.parties))
    }
    random.shuffle(st.session_state.parties)


def set_query(query):
    st.session_state.query = query


def generate_response():
    max_retries = 2
    retry_count = 0
    while retry_count <= max_retries:
        try:
            print("Getting response")
            st.session_state.response = rag.query(query)

            # Assert that the response contains all parties
            assert set(st.session_state.response["answer"].keys()) == set(
                party_dict.keys()
            ), "LLM response does not contain all parties"
            break

        except Exception as e:
            print(f"An error occurred: {e}")
            # Error occured, increment retry counter
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max number of tries ({max_retries}) reached, aborting")
                st.session_state.response = None
                st.error(
                    translate(
                        "Das Sprachmodell ist gerade nicht verfügbar. **Bitte versuche es gleich nochmal.**",
                        st.session_state.language,
                    )
                )
                # Display error message in app:
                raise e
            else:
                print(f"Retrying, retry number {retry_count}")
                pass


# The following function converts a date string from the format "YYYY-MM-DD" to "DD.MM.YYYY"
# (for display in the sources)
def convert_date_format(date_string):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")

    # Format the datetime object into the new string format
    new_date_string = date_obj.strftime("%d.%m.%Y")

    return new_date_string


### INTERFACE ###
sidebar = st.sidebar.title("")


with sidebar:
    selected_language = st.radio(
        label="Language",
        options=["🇩🇪 Deutsch", "🇬🇧 English"],
        horizontal=True,
    )
    languages = {"🇩🇪 Deutsch": "Deutsch", "🇬🇧 English": "English"}
    st.session_state.language = languages[selected_language]
    rag.language = st.session_state.language


st.header("🇪🇺 europarl.ai", divider="blue")
st.write(
    translate(
        "Informiere dich über die Positionen der Parteien zur Europawahl 2024.",
        st.session_state.language,
    )
)

query = st.text_input(
    label=translate(
        "Stelle eine Frage oder gib ein Stichwort ein:",
        st.session_state.language,
    ),
    placeholder=translate(
        "Tippe hier deine Frage ein oder wähle unten eine aus!",
        language=st.session_state.language,
    ),
    value=st.session_state.query,
)

st.write(translate("Hier sind Beispielfragen:", st.session_state.language))
st.button(
    st.session_state.example_prompts[st.session_state.language][0],
    on_click=set_query,
    args=(st.session_state.example_prompts[st.session_state.language][0],),
)
st.button(
    st.session_state.example_prompts[st.session_state.language][1],
    on_click=set_query,
    args=(st.session_state.example_prompts[st.session_state.language][1],),
)
st.button(
    st.session_state.example_prompts[st.session_state.language][2],
    on_click=set_query,
    args=(st.session_state.example_prompts[st.session_state.language][2],),
)


st.session_state.show_all_parties = st.checkbox(
    label=translate("Parteinamen anzeigen", st.session_state.language),
    value=True,
    help=translate(
        "Blende die Parteinamen aus, um Antworten unvoreingenommen lesen zu können.",
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
            "Suche nach Antworten in Wahlprogrammen und Parlamentsdebatten...",
            st.session_state.language,
        )
        + "🕵️"
    ):

        with st.info(
            "☝️ "
            + translate(
                "**Die Antworten wurden von einem Sprachmodell generiert und können fehlerhaft sein.**",
                st.session_state.language,
            )
            + "  \n"
            + translate(
                "Bitte informiere dich zusätzlich in den verlinkten Wahlprogrammen.",
                st.session_state.language,
            )
            + "  \n"
            + translate(
                "Die Reihenfolge der angezeigten Parteien ist zufällig.",
                st.session_state.language,
            )
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

    # Initialize an empty list to hold all columns
    col_list = []
    # Create a pair of columns for each party
    num_parties = len(st.session_state.parties)
    col_list = [st.columns([0.3, 0.7]) for _ in range(num_parties)]

    # Show image and RAG response for each party
    for i, party in enumerate(st.session_state.parties):
        p = i + 1
        col1, col2 = col_list[i]

        most_relevant_manifesto_page_number = st.session_state.response["docs"][
            "manifestos"
        ][party][0].metadata["page"]

        show_party = (
            st.session_state.show_all_parties
            or st.session_state.show_individual_parties[f"party_{p}"]
        )

        # In this column, we show the party image
        with col1:
            st.write("\n" * 2)
            if show_party:
                st.image(party_dict[party]["image"])
            else:
                st.image("streamlit_app/assets/placeholder_logo.png")
                st.button(
                    translate("Partei aufdecken", st.session_state.language),
                    on_click=reveal_party,
                    args=(p,),
                    key=p,
                )
        # In this column, we show the RAG response
        with col2:
            if show_party:
                st.header(party_dict[party]["name"])
            else:
                st.header(f"{translate('Partei', st.session_state.language)} {p}")

            st.write(st.session_state.response["answer"][party])
            if show_party:
                st.write(
                    f"""{translate('Mehr dazu im', st.session_state.language)} [{translate('Europawahlprogramm der Partei', st.session_state.language)} **{party_dict[party]['name']}** ({translate('z.B. Seite', st.session_state.language)} {most_relevant_manifesto_page_number + 1})]({party_dict[party]['manifesto_link']}#page={most_relevant_manifesto_page_number + 1})"""
                )

    st.markdown("---")
    st.subheader(
        translate(
            "Quellen: Worauf basieren diese Antworten?", st.session_state.language
        )
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
    for party in st.session_state.parties:
        with st.expander(
            translate(
                f"{translate('Quellen', st.session_state.language)}: {party_dict[party]['name']}",
                st.session_state.language,
            )
        ):
            for doc in st.session_state.response["docs"]["manifestos"][party]:
                manifesto_excerpt = doc.page_content.replace("\n", " ")
                page_number_of_excerpt = doc.metadata["page"] + 1
                link_to_manifesto_page = f"{party_dict[party]['manifesto_link']}#page={page_number_of_excerpt}"
                st.markdown(
                    f'[**Seite {page_number_of_excerpt} im Wahlprogramm**]({link_to_manifesto_page}): \n "{manifesto_excerpt}"\n\n'
                )
            for doc in st.session_state.response["docs"]["debates"][party]:
                debate_excerpt = doc.page_content.replace("\n", " ")
                date_of_excerpt = convert_date_format(doc.metadata["date"])
                speaker_of_excerpt = doc.metadata["fullName"]

                st.write(
                    f'**Ausschnitt aus einer Rede im EU-Parlament von {speaker_of_excerpt} am {date_of_excerpt}**: "{debate_excerpt}"\n\n'
                )

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
