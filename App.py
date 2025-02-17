import base64
import csv
import json
import os
import random
from datetime import datetime
from pathlib import Path

import dotenv
import streamlit as st
from langchain_openai import AzureChatOpenAI, ChatOpenAI, OpenAIEmbeddings  # noqa: F401

from RAG.database.vector_database import VectorDatabase
from RAG.models.RAG import RAG
from streamlit_app.utils.log import add_log_dict, update_log_dict
from streamlit_app.utils.support_widgets import support_button
from streamlit_app.utils.translate import translate

dotenv.load_dotenv()

# Load dictionary with party names, image file paths, and links to manifestos
with open("streamlit_app/party_dict.json") as file:
    party_dict = json.load(file)

# The following is necessary to make the code work for deploying on Streamlit Cloud.
# (We need a newer version of sqlite3 than the one provided by Streamlit.)
# The environment variable IS_DEPLOYED is created only in the Streamlit Secrets and set to the string "TRUE".
# if os.getenv("IS_DEPLOYED", default="FALSE") == "TRUE":
#     __import__("pysqlite3")
#     import sys

#     sys.modules["sqlite3"] = sys.modules["pysqlite3"]

# Streamlit page conifg
st.set_page_config(page_title="Electify", page_icon="🗳️", layout="centered")

##################################
### RAG SETUP ####################
##################################

DATABASE_DIR_MANIFESTOS = "./data/manifestos/chroma/openai"
# DATABASE_DIR_DEBATES = "./data/debates/chroma/openai"
TEMPERATURE = 0.0
MAX_TOKENS = 400

# LARGE_LANGUAGE_MODEL = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=MAX_TOKENS, temperature=TEMPERATURE)
LARGE_LANGUAGE_MODEL = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_SWEDEN"],
    api_key=os.environ["AZURE_OPENAI_API_KEY_SWEDEN"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION_SWEDEN"],
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE,
)


# Load the OpenAI embeddings model
@st.cache_resource
def load_embedding_model():
    return OpenAIEmbeddings(model="text-embedding-3-large")


embedding_model = load_embedding_model()


# Load the databases
@st.cache_resource
def load_db_manifestos():
    return VectorDatabase(
        embedding_model=embedding_model, source_type="manifestos", database_directory=DATABASE_DIR_MANIFESTOS
    )


# TODO: Commented out since we do not use debate data yet
# @st.cache_resource
# def load_db_debates():
#     return VectorDatabase(
#         embedding_model=embedding_model,
#         source_type="debates",
#         database_directory=DATABASE_DIR_DEBATES,
#     )


# Initialize RAG module with default parties
rag = RAG(
    databases=[load_db_manifestos()],
    parties=["cdu", "spd", "gruene", "fdp", "linke", "afd"],
    llm=LARGE_LANGUAGE_MODEL,
    k=5,
)


##################################
### SESSION STATES ###############
##################################

# The "query" string will contain the user input (i.e., the question or keyword):
if "query" not in st.session_state:
    st.session_state.query = ""

# The "response" dictionary will contain the generated answer from the RAG system:
if "response" not in st.session_state:
    st.session_state.response = None

# The "stage" integer value will determine which part of the app is currently displayed:
if "stage" not in st.session_state:
    st.session_state.stage = 0

# The "language" string will determine the language of the interface and response:
if "language" not in st.session_state:
    st.session_state.language = "de"
else:
    rag.language = st.session_state.language

# The "parties" list determines which parties will be used for the RAG query:
if "parties" not in st.session_state:
    st.session_state.parties = rag.parties

# The "show_all_parties" boolean determines whether all party names are revealed or not:
if "show_all_parties" not in st.session_state:
    st.session_state.show_all_parties = True
    # Note that this will be overridden by the "show_individual_parties" dictionary below if the user reveals individual parties.

# The "show_individual_parties" dictionary will determine which party names are revealed in the app:
if "show_individual_parties" not in st.session_state:
    # The values in this dict will only be set true if a party name is explicitly "revealed" by the user.
    # The keys represent the (random) order of appearance of the parties in the app
    # and not fixed parties as opposed to the above party_dict.

    st.session_state.show_individual_parties = {f"party_{i + 1}": False for i in range(len(st.session_state.parties))}

# The "example_prompts" dictionary will contain randomly selected example prompts for the user to choose from:
if "example_prompts" not in st.session_state:
    all_example_prompts = {}
    with open("streamlit_app/example_prompts.csv") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            for key, value in row.items():
                if key not in all_example_prompts:
                    all_example_prompts[key] = []
                all_example_prompts[key].append(value)

    st.session_state.example_prompts = {key: random.sample(value, 3) for key, value in all_example_prompts.items()}

if "number_of_requests" not in st.session_state:
    st.session_state.number_of_requests = 0

# The "log_id" string identifies query's log in the database:
if "log_id" not in st.session_state:
    st.session_state.log_id = None

# The "feedback_rating" integer will contain the user's rating of the response:
if "feedback_rating" not in st.session_state:
    st.session_state.feedback_rating = None

# The "feedback_text" string will contain the user's feedback text:
if "feedback_text" not in st.session_state:
    st.session_state.feedback_text = ""

if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False


##################################
### HELPER FUNCTIONS #############
##################################
def reveal_party(p):
    st.session_state.show_individual_parties[f"party_{p}"] = True


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid' style='width:100%'>"
    return img_html


def set_query(query):
    st.session_state.query = query


def submit_query():
    set_query(query)
    st.session_state.response = None
    st.session_state.log_id = None
    st.session_state.feedback_rating = None
    st.session_state.feedback_text = ""
    st.session_state.feedback_submitted = False
    st.session_state.stage = 1
    st.session_state.show_individual_parties = {f"party_{i + 1}": False for i in range(len(st.session_state.parties))}
    random.shuffle(st.session_state.parties)


def submit_example(query):
    set_query(query)
    submit_query()


def generate_response():
    max_retries = 2
    retry_count = 0
    while retry_count <= max_retries:
        try:
            print("Getting response")
            st.session_state.response = rag.query(query)

            # Assert that the response contains all parties
            assert set(st.session_state.response["answer"].keys()) == set(st.session_state.parties), (
                "LLM response does not contain all parties"
            )
            break

        except Exception as e:
            print(f"An error occurred: {e}")
            # Error occured, increment retry counter
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max number of tries ({max_retries}) reached, aborting")
                st.session_state.response = None
                st.error(translate("error-api-unavailable", st.session_state.language))
                # Display error message in app:
                raise e
            else:
                print(f"Retrying, retry number {retry_count}")
                pass
    st.session_state.log_id = add_log_dict({"query": query, "answer": st.session_state.response["answer"]})


def submit_feedback(feedback_rating, feedback_text):
    update_log_dict(st.session_state.log_id, {"feedback-rating": feedback_rating, "feedback-text": feedback_text})
    st.rerun()


# The following function converts a date string from the format "YYYY-MM-DD" to "DD.MM.YYYY"
# (for display in the sources)
def convert_date_format(date_string):
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")

    # Format the datetime object into the new string format
    new_date_string = date_obj.strftime("%d.%m.%Y")

    return new_date_string


##################################
### USER INTERFACE ###############
##################################

with st.sidebar:
    selected_language = st.radio(label="Language", options=["🇩🇪 Deutsch", "🇬🇧 English"], horizontal=True)
    languages = {"🇩🇪 Deutsch": "de", "🇬🇧 English": "en"}
    st.session_state.language = languages[selected_language]
    rag.language = st.session_state.language

st.header("🗳️ electify.eu", divider="blue")
st.write("##### :grey[" + translate("subheadline", st.session_state.language) + "]")

support_button(
    text=f"💙  {translate('support-button', st.session_state.language)}",
    link="https://www.buymeacoffee.com/electify.eu",
)

if st.session_state.number_of_requests >= 3:
    # Show support banner after 3 requests in a single session.
    st.info(
        f"{translate('support-banner', st.session_state.language)}(https://buymeacoffee.com/electify.eu)", icon="💙"
    )

query = st.text_input(
    label=translate("query-instruction", st.session_state.language), placeholder="", value=st.session_state.query
)

col_submit, col_checkbox = st.columns([1, 3])

# Submit button
with col_submit:
    st.button(translate("submit-query", st.session_state.language), on_click=submit_query, type="primary")

# Checkbox to show/hide party names globally
with col_checkbox:
    st.session_state.show_all_parties = st.checkbox(
        label=translate("show-party-names", st.session_state.language),
        value=True,
        help=translate("show-party-names-help", st.session_state.language),
    )

# Allow the user to select up to 6 parties
with st.expander(translate("select-parties-heading", st.session_state.language)):
    available_parties = list(party_dict.keys())

    party_selection = {party: False for party in available_parties}
    for party in st.session_state.parties:
        party_selection[party] = True

    def update_party_selection(party):
        party_selection[party] = not party_selection[party]
        st.session_state.parties = [k for k, v in party_selection.items() if v]

    st.write(translate("select-parties-instruction", st.session_state.language))
    for party in available_parties:
        st.checkbox(
            label=party_dict[party]["name"],
            value=party_selection[party],
            on_change=update_party_selection,
            kwargs={"party": party},
        )

    if len(st.session_state.parties) == 0:
        st.markdown(f"⚠️ **:red[{translate('error-min-1-party', st.session_state.language)}]**")
        # Reset to default parties
        st.session_state.parties = rag.parties
    elif len(st.session_state.parties) > 6:
        st.markdown(f"⚠️ **:red[{translate('error-max-6-parties', st.session_state.language)}]**")
        # Limit to the six first selected parties
        st.session_state.parties = st.session_state.parties[:6]

    # Update the RAG module with the selected parties
    rag.parties = st.session_state.parties

# STAGE 0: User has not yet submitted a query
if st.session_state.stage == 0:
    st.write(translate("examples-heading", st.session_state.language))

    for i in range(3):
        st.button(
            st.session_state.example_prompts[st.session_state.language][i],
            on_click=submit_example,
            args=(st.session_state.example_prompts[st.session_state.language][i],),
            key=f"example_prompt_{i}",
        )

# STAGE > 0: Show disclaimer once the user has submitted a query (and keep showing it)
if st.session_state.stage > 0:
    if len(st.session_state.parties) == 0:
        st.error(translate("error-min-1-party", st.session_state.language))
        st.session_state.stage = 0

    else:
        st.info(
            "☝️ "
            + translate("disclaimer-llm", st.session_state.language)
            + "  \n"
            + translate("disclaimer-research", st.session_state.language)
            + "  \n"
            + translate("disclaimer-random-order", st.session_state.language)
        )

# STAGE 1: User submitted a query and we are waiting for the response
if st.session_state.stage == 1:
    st.session_state.number_of_requests += 1
    with st.spinner(translate("loading-response", st.session_state.language) + "🕵️"):
        generate_response()

    st.session_state.stage = 2


# STAGE > 1: The response has been generated and is displayed
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

        most_relevant_manifesto_page_number = st.session_state.response["docs"]["manifestos"][party][0].metadata[
            "page"
        ]

        show_party = st.session_state.show_all_parties or st.session_state.show_individual_parties[f"party_{p}"]

        # In this column, we show the party image
        with col1:
            st.write("\n" * 2)
            if show_party:
                file_loc = party_dict[party]["image"]
                st.markdown(img_to_html(file_loc), unsafe_allow_html=True)

            else:
                file_loc = "streamlit_app/assets/placeholder_logo.png"
                st.markdown(img_to_html(file_loc), unsafe_allow_html=True)
                st.button(translate("show-party", st.session_state.language), on_click=reveal_party, args=(p,), key=p)
        # In this column, we show the RAG response
        with col2:
            if show_party:
                st.header(party_dict[party]["name"])
            else:
                st.header(f"{translate('party', st.session_state.language)} {p}")

            if party == "afd" and show_party:
                st.caption(f"⚠️ **{translate('warning-afd', st.session_state.language)}**")

            st.write(st.session_state.response["answer"][party])
            if show_party:
                is_answer_empty = "keine passende antwort" in st.session_state.response["answer"][party].lower()

                page_reference_string = (
                    ""
                    if is_answer_empty
                    else f" ({translate('page-reference', st.session_state.language)} {most_relevant_manifesto_page_number + 1})"
                )

                st.write(
                    f"""{translate("learn-more-in", st.session_state.language)} [{translate("party-manifesto", st.session_state.language)} **{party_dict[party]["name"]}**{page_reference_string}]({party_dict[party]["manifesto_link"]}#page={most_relevant_manifesto_page_number + 1})."""
                )

    st.markdown("---")

    # Display a section with all retrieved excerpts from the sources
    st.subheader(translate("sources-subheading", st.session_state.language))
    st.write(translate("sources-intro", st.session_state.language))
    st.write(translate("sources-excerpts-intro", st.session_state.language))
    for party in st.session_state.parties:
        with st.expander(translate("sources", st.session_state.language) + f": {party_dict[party]['name']}"):
            for doc in st.session_state.response["docs"]["manifestos"][party]:
                manifesto_excerpt = doc.page_content.replace("\n", " ")
                page_number_of_excerpt = doc.metadata["page"] + 1
                link_to_manifesto_page = f"{party_dict[party]['manifesto_link']}#page={page_number_of_excerpt}"
                st.markdown(
                    f'[**Seite {page_number_of_excerpt} im Wahlprogramm**]({link_to_manifesto_page}): \n "{manifesto_excerpt}"\n\n'
                )

            # TODO: Commented out since we do not use debate data yet
            # for doc in st.session_state.response["docs"]["debates"][party]:
            #     debate_excerpt = doc.page_content.replace("\n", " ")
            #     date_of_excerpt = convert_date_format(doc.metadata["date"])
            #     speaker_of_excerpt = doc.metadata["fullName"]

            #     st.write(
            #         f'**Ausschnitt aus einer Rede im EU-Parlament von {speaker_of_excerpt} am {date_of_excerpt}**: "{debate_excerpt}"\n\n'
            #     )

    st.write("---")

    st.subheader(translate("feedback-heading", st.session_state.language))

    if not st.session_state.feedback_submitted:
        st.write(translate("feedback-intro", st.session_state.language))

        with st.form(key="feedback-form"):
            feedback_options = {"negative": "☹️", "neutral": "😐", "positive": "😊"}

            feedback_rating = st.segmented_control(
                label=translate("feedback-question-rating", st.session_state.language),
                options=feedback_options.keys(),
                format_func=lambda option: feedback_options[option],
            )
            feedback_text = st.text_area(label=translate("feedback-question-text", st.session_state.language))
            submitted = st.form_submit_button(
                label=translate("feedback-submit", st.session_state.language), type="primary"
            )
            if submitted:
                st.session_state.feedback_submitted = True
                submit_feedback(feedback_rating, feedback_text)

    else:
        st.success(translate("feedback-thanks", st.session_state.language))
