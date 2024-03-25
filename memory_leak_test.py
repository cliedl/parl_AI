import streamlit as st
import random
from trubrics.integrations.streamlit import FeedbackCollector
import os
import re
import csv
import random
from datetime import datetime
import time
import psutil


process = psutil.Process()


from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from RAG.models.generation import generate_chain
from RAG.models.RAG import RAG
from RAG.database.vector_database import VectorDatabase
from streamlit_app.utils.translate import translate
from RAG.models.generation import build_context_for_party

print(f"Memory usage {process.memory_info().rss/(1024**2)} MB")


def run():
    DATABASE_DIR_MANIFESTOS = "./data/manifestos/chroma/openai"
    DATABASE_DIR_DEBATES = "./data/debates/chroma/openai"
    DELAY = 0.05  # pause between words in text stream (in seconds)
    TEMPERATURE = 0.0
    LARGE_LANGUAGE_MODEL = ChatOpenAI(
        model_name="gpt-3.5-turbo", max_tokens=400, temperature=TEMPERATURE
    )
    USE_LANGCHAIN = False

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

    @st.cache_resource
    def load_db_debates():
        return VectorDatabase(
            embedding_model=embedding_model,
            source_type="debates",
            database_directory=DATABASE_DIR_DEBATES,
        )

    db_debates = load_db_debates()

    chain = generate_chain(
        [db_manifestos, db_debates],
        llm=LARGE_LANGUAGE_MODEL,
        language="Deutsch",
        k=3,
    )

    rag = RAG(
        databases=[db_manifestos, db_debates],
        llm=LARGE_LANGUAGE_MODEL,
        k=3,
        language="Deutsch",
    )

    t0 = time.time()
    query = "Wie stehen die Parteien zum Krieg in der Ukraine?"

    if USE_LANGCHAIN:
        response = chain.invoke(query)

    else:
        response = rag.query(query)

    t1 = time.time()
    print(f"Memory usage {process.memory_info().rss/(1024**2)} MB")

    return response, t1 - t0


for i in range(10):
    response, execution_time = run()

    print(f"this took {execution_time} s")
    time.sleep(1)
