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

    t0 = time.time()
    query = "Wie stehen die Parteien zum Krieg in der Ukraine?"

    if USE_LANGCHAIN:
        response = chain.invoke(query)
    else:
        parties = ["afd", "cdu", "fdp", "spd", "gruene", "linke"]
        context = {}
        response = {}
        prompts = {}
        for party in parties:
            # context = build_context_for_party(db_manifestos, query=query, party=party, k=5)
            docs = db_manifestos.database.max_marginal_relevance_search(
                query, k=5, fetch_k=20, filter={"party": party}
            )
            context[party] = build_context_for_party(
                db_manifestos,
                party=party,
                query=query,
                k=3,
            )
            language = "Deutsch"

            prompts[
                party
            ] = f"""
            Beantworte die unten folgende FRAGE DES NUTZERS, indem du die politischen Positionen der Partei im unten angegebenen KONTEXT zusammenfasst.
            Der KONTEXT umfasst Ausschnitte aus Redebeiträgen im EU-Parlament und aus dem EU-Wahlprogramm für 2024 für die Partei.
            Deine Antwort soll ausschließlich die Informationen aus dem genannten KONTEXT beinhalten.
            Verwende in deiner Antwort NICHT den Namen der Partei, sondern beziehe dich auf die Partei ausschließlich mit "die Partei".
            Sollte der KONTEXT keine Antwort auf die FRAGE DES NUTZERS zulassen, gib anstelle der Zusammenfassung NUR die folgende Rückmeldung:
            "Es wurde keine passende Antwort in den Quellen gefunden."
            Gib die Antwort auf {language}.

            KONTEXT:
            {context[party]}

            FRAGE DES NUTZERS:
            {query}
            """

        import asyncio

        response = asyncio.run(LARGE_LANGUAGE_MODEL.abatch(list(prompts.values())))

    t1 = time.time()
    print(f"Memory usage {process.memory_info().rss/(1024**2)} MB")

    return response, t1 - t0


for i in range(10):
    response, execution_time = run()
    print(f"this took {execution_time} s")
    time.sleep(1)
