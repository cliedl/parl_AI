import json
import os
import sys

import dotenv
from langchain_openai import OpenAIEmbeddings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RAG.database.vector_database import VectorDatabase

dotenv.load_dotenv()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

DATABASE_DIR_MANIFESTOS = "data/manifestos/chroma/openai"
PATH_PARTY_DICT = "streamlit_app/party_dict.json"

with open(PATH_PARTY_DICT) as f:
    party_dict = json.load(f)

db = VectorDatabase(
    embedding_model=embedding_model, source_type="manifestos", database_directory=DATABASE_DIR_MANIFESTOS
)


def test_db_connection():
    assert db.database is not None

    results = db.database.similarity_search("Wie sieht die Steuerpolitik der Parteien aus?")
    assert len(results) > 0


def test_party_counts():
    collection = db.database._collection
    party_counts = {}
    for doc in collection.get()["metadatas"]:
        if "party" in doc:
            party = doc["party"]
            party_counts[party] = party_counts.get(party, 0) + 1
    for party in sorted(party_counts.keys()):
        print(f"{party}: {party_counts[party]}")

    assert set(party_counts.keys()) == set(party_dict.keys())


def test_has_page_metadata():
    collection = db.database._collection
    for doc in collection.get()["metadatas"]:
        assert "page" in doc
        assert doc["page"] is not None
