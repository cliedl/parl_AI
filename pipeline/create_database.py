import json
import logging
import os
import shutil
import sys

import dotenv
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from RAG.database.vector_database import VectorDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

from langchain_openai import OpenAIEmbeddings

logging.info("Starting script...")

# Define emebdding model and name
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
embedding_name = "openai"
logging.info(f"Embedding model and name defined: {embedding_model} and {embedding_name}")

PATH_PARTY_DICT = "streamlit_app/party_dict.json"
PATH_MANIFESTOS_PDF = "data/manifestos/01_pdf_originals"
DATABASE_DIR = f"data/manifestos/chroma/{embedding_name}/"

with open(PATH_PARTY_DICT) as f:
    party_dict = json.load(f)


def clean_up_old_database():
    """Deletes old database directory if it exists"""
    if os.path.exists(DATABASE_DIR):
        logger.info(f"Removing old database in {DATABASE_DIR}")
        shutil.rmtree(DATABASE_DIR)


def download_manifestos():
    """Downloads manifesto PDFs from manifesto links in the party_dict.json file. 
        Saves them to the data/manifestos/01_pdf_originals directory.
    """
    # Download manifesto PDFs
    logger.info("Downloading manifesto PDFs...")
    for party in party_dict:
        logger.info(f"Downloading manifesto for {party}")
        file_name_pdf = f"{party}_wahlprogramm_btw_2025.pdf"
        data_path = os.path.join(PATH_MANIFESTOS_PDF, file_name_pdf)

        logger.info(f"Downloading manifesto for {party} from {party_dict[party]['manifesto_link']}")
        response = requests.get(party_dict.get(party).get("manifesto_link"))
        response.raise_for_status()
        with open(data_path, "wb") as f:
            f.write(response.content)

def build_database():
    """Builds a vector database from the manifesto PDFs.
        Saves the database to the data/manifestos/chroma/{embedding_name}/ directory.
    """
    # instantiate database
    logger.info("Initializing vector database...")
    database_manifestos = VectorDatabase(
        embedding_model=embedding_model,
        source_type="manifestos",
        database_directory=DATABASE_DIR,
        data_path=PATH_MANIFESTOS_PDF,
        loader="pdf",
        reload=False,
    )

    # Build or load database
    logger.info("Building/loading database...")
    logger.info(f"Database will be saved in {DATABASE_DIR}")
    database_manifestos.build_database()
    logger.info("Database successfully built/loaded")
    assert str(type(database_manifestos.database)) == "<class 'langchain_community.vectorstores.chroma.Chroma'>"


if __name__ == "__main__":
    download_manifestos()
    clean_up_old_database()
    build_database()
