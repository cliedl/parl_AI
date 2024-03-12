from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os

# Build vector storage if not yet existing
if not os.path.exists("./db_speeches"):  # Updated vector database name

    # Loader for europarl_speeches.csv
    speeches_loader = CSVLoader(
        "../parl_ai/data/debates/europarl_speeches.csv"
    )  

    # Loader for europarl_members.csv -     
    members_loader = CSVLoader(
        "../parl_ai/data/debates/europarl_members.csv"
    )  

    # Loading documents from CSV files
    speeches_docs = speeches_loader.load()
    members_docs = members_loader.load()  
    
    # Merging documents, if necessary
    # Here, assuming that both sets of documents need to be combined in some form
    combined_docs = speeches_docs + members_docs
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(combined_docs)

    db_speeches = Chroma.from_documents(splits, embeddings, persist_directory="./db_speeches")

# Load the vector storage if it already exists
else:
    db_speeches = Chroma(persist_directory="./db_speeches", embedding_function=embeddings)
