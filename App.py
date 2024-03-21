import streamlit as st
import random
from trubrics.integrations.streamlit import FeedbackCollector
import os
import re
import csv
import random
from datetime import datetime


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from RAG.models.generation import generate_chain_with_balanced_retrieval
from RAG.database.vector_database import VectorDatabase, rename_party
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


@st.cache_resource
def load_db_debates():
    return VectorDatabase(
        embedding_model=embedding_model,
        source_type="debates",
        database_directory=DATABASE_DIR_DEBATES,
    )


db_manifestos = load_db_manifestos()
db_debates = load_db_debates()


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
    "partei_a": {
        "name": "CDU/CSU",
        "image": "streamlit_app/assets/cdu_logo.png",
        "manifesto_link": "https://assets.ctfassets.net/nwwnl7ifahow/476rnHcYPkmyuONPvSTKO2/972e88ceb862ac4d4905d98441555e0c/europawahlprogramm-cdu-csu-2024_0.pdf",
    },
    "partei_b": {
        "name": "SPD",
        "image": "streamlit_app/assets/spd_logo.png",
        "manifesto_link": "https://www.spd.de/fileadmin/Dokumente/EuroDel/20240128_Europaprogramm.pdf",
    },
    "partei_c": {
        "name": "Bündnis 90/Die Grünen",
        "image": "streamlit_app/assets/gruene_logo.png",
        "manifesto_link": "https://cms.gruene.de/uploads/assets/Europawahlprogramm-2024-Bu%CC%88ndnis90Die-Gru%CC%88nen_Wohlstand_Gerechtigkeit_Frieden_Freiheit.pdf",
    },
    "partei_d": {
        "name": "Die Linke",
        "image": "streamlit_app/assets/linke_logo.png",
        "manifesto_link": "https://www.die-linke.de/fileadmin/user_upload/Europawahlprogramm_2023_neu2.pdf",
    },
    "partei_e": {
        "name": "FDP",
        "image": "streamlit_app/assets/fdp_logo.png",
        "manifesto_link": "https://www.fdp.de/sites/default/files/2024-01/fdp_europawahlprogramm-2024_vorabversion.pdf",
    },
    "partei_f": {
        "name": "AfD",
        "image": "streamlit_app/assets/afd_logo.png",
        "manifesto_link": "https://www.afd.de/wp-content/uploads/2023/11/2023-11-16-_-AfD-Europawahlprogramm-2024-_-web.pdf",
    },
}


# The following function replaces mentions of "Partei A/B/C/..." with "Partei"
def clean_party_names_in_response(text):
    text = re.sub(r"Partei [A-F]", "Partei", text)
    text = re.sub(r"PARTEI [A-F]", "Partei", text)
    text = re.sub(r"Partei_[A-F]", "Partei", text)
    text = re.sub(r"PARTEI_[A-F]", "Partei", text)
    return text


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
if "parties" not in st.session_state:
    st.session_state.parties = list(party_dict.keys())
if "show_individual_parties" not in st.session_state:
    # The values in this dict will only be set true if a party name is explicitly "revealed" by the user.
    # The keys represent the (random) order of appearance of the parties in the app
    # and not fixed parties as opposed to the above party_dict.
    st.session_state.show_individual_parties = {
        "party_1": False,
        "party_2": False,
        "party_3": False,
        "party_4": False,
        "party_5": False,
        "party_6": False,
    }
if "show_all_parties" not in st.session_state:
    st.session_state.show_all_parties = True
if "example_prompts" not in st.session_state:
    all_example_prompts = {}
    with open("data/questions/complex_questions_with_translations.csv", "r") as file:
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
        "party_1": False,
        "party_2": False,
        "party_3": False,
        "party_4": False,
        "party_5": False,
        "party_6": False,
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
            st.session_state.response = chain.invoke(query)

            print(set(st.session_state.response["answer"].keys()))
            print(set(party_dict.keys()))

            # Assert that the response contains all parties
            assert set(st.session_state.response["answer"].keys()) == set(
                party_dict.keys()
            ), "LLM response does not contain all parties"

            # Assert that the response contains non-empty strings
            assert all(
                isinstance(party_answer, str) and party_answer
                for party_answer in st.session_state.response["answer"].values()
            ), "Some entries in the LLM response are empty strings"

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
                        "Das Sprachmodell hat eine inkompatible Antwort generiert. Das kann zufällig passieren. **Bitte versuche es erneut.**",
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

chain = generate_chain_with_balanced_retrieval(
    [db_manifestos, db_debates],
    llm=LARGE_LANGUAGE_MODEL,
    return_context=True,
    language=st.session_state.language,
    k=3,
)

st.title("🇪🇺 europarl.ai")
st.write(
    translate(
        "Erfahre die Positionen der Parteien zur Europawahl 2024.",
        st.session_state.language,
    )
)

query = st.text_input(
    label=translate(
        "Stelle eine Frage oder gib ein Stichwort ein:",
        st.session_state.language,
    ),
    placeholder=translate(
        "Wie stehen die Parteien zum Emmissionshandel?",
        language=st.session_state.language,
    ),
    value=st.session_state.query,
)

st.write(translate("Oder wähle aus den Beispielen:", st.session_state.language))

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
            "Suche nach Antworten in Wahlprogrammen und Parlamentsdebatten...",
            st.session_state.language,
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
        ][rename_party(party, "deanonymize")][0].metadata["page"]

        with col_list[i]:
            st.write("")
            st.write("")
            if (
                st.session_state.show_all_parties
                or st.session_state.show_individual_parties[f"party_{p}"]
            ):
                st.image(party_dict[party]["image"])
            else:
                st.image("streamlit_app/assets/placeholder_logo.png")
            if not (
                st.session_state.show_all_parties
                or st.session_state.show_individual_parties[f"party_{p}"]
            ):
                st.button(
                    translate("Partei aufdecken", st.session_state.language),
                    on_click=reveal_party,
                    args=(p,),
                    key=p,
                )

        with col_list[i + 1]:
            if (
                st.session_state.show_all_parties
                or st.session_state.show_individual_parties[f"party_{p}"]
            ):
                st.header(party_dict[party]["name"])
            else:
                st.header(f"Partei {p}")
            answer = clean_party_names_in_response(
                st.session_state.response["answer"][party]
            )
            st.write(answer)
            if (
                st.session_state.show_all_parties
                or st.session_state.show_individual_parties[f"party_{p}"]
            ):
                st.write(
                    f"""{translate('Mehr dazu im', st.session_state.language)}
                        [{translate('Europawahlprogramm der Partei', st.session_state.language)} 
                        **{party_dict[party]['name']}** 
                        ({translate('z.B. Seite', st.session_state.language)} {most_relevant_manifesto_page_number+1})]({party_dict[party]['manifesto_link']}#page={most_relevant_manifesto_page_number+1})"""
                )
        i += 2
        p += 1

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
            true_party = rename_party(party, "deanonymize")
            for doc in st.session_state.response["docs"]["manifestos"][true_party]:
                manifesto_excerpt = doc.page_content.replace("\n", " ")
                page_number_of_excerpt = doc.metadata["page"] + 1
                link_to_manifesto_page = f"{party_dict[party]['manifesto_link']}#page={page_number_of_excerpt}"
                st.markdown(
                    f'[**Seite {page_number_of_excerpt} im Wahlprogramm**]({link_to_manifesto_page}): \n "{manifesto_excerpt}"\n\n'
                )
            for doc in st.session_state.response["docs"]["debates"][true_party]:
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
