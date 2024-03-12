import streamlit as st
import os
import sys
import time

# Directory of RAG modules
sys.path.append(os.path.abspath('../RAG_clean'))
sys.path.append(os.path.abspath('RAG_clean'))

# Import custom RAG modules
from models.generation import generate_chain
from models.retrieval import retriever
from database.vector_database import VectorDatabaseCreator
from models.embedding import ManifestoBertaEmbeddings

DATABASE_DIR = "../data/manifestos/chroma"
DELAY = 0.05  # pause between words in text stream (in seconds)

################ Create langchain ########################
# get embedding module
embedding_model = ManifestoBertaEmbeddings()

# get database_creator
database_creator = VectorDatabaseCreator(
    embedding_model=embedding_model,
    db_directory=DATABASE_DIR)

# load database
database = database_creator.load_database()

# get retriever
retriever = retriever(db=database,
                            search_type="similarity",
                            k=10)

# generate langchain
chain = generate_chain(retriever=retriever)

# This creates in iterable that yields each word of a text after a delay (in seconds)
def streaming(text, delay=0.05):
    # Chose random response from a list
    for word in text.split():
        yield word + " "
        time.sleep(delay)

# The rest is basically copied from
# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
# 2024-03-05

st.title(f"Europa Parlament - WTF?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Was willst du wissen?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = chain.invoke(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write_stream(streaming(response, delay=0.05))
    # Add assistant response to chat history
