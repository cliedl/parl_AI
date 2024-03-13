from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

import sys
sys.path.append("./parl_AI/RAG_clean")

from models.embedding import ManifestoBertaEmbeddings
from database.vector_database import VectorDatabaseCreator as BaseVectorDatabaseCreator
import os


class EnhancedVectorDatabaseCreator(BaseVectorDatabaseCreator):
    def __init__(self, embedding_model, data_directory=".", db_directory="./DB/chroma_speeches", chunk_size=1000, chunk_overlap=100):
        super().__init__(embedding_model, data_directory, db_directory, chunk_size, chunk_overlap)

        """
        Initializes the VectorDatabaseCreator.

        Parameters:
        - embedding_model: The model used to generate embeddings for the documents.
        - data_directory (str): The directory where the source documents are located. Defaults to the current directory.
        - db_directory (str): The directory to store the Chroma database. Defaults to './chroma_speeches'.
        - chunk_size (int): The size of text chunks to split the documents into. Defaults to 1000.
        - chunk_overlap (int): The number of characters to overlap between adjacent chunks. Defaults to 100.
        """

    def ensure_directory_exists(self, directory):
        """Ensures the specified directory exists, creating it if necessary."""
        os.makedirs(directory, exist_ok=True)

    def create_or_load_database(self):
        self.ensure_directory_exists(self.db_directory)  # Make sure the directory exists
        if os.path.exists(self.db_directory) and os.listdir(self.db_directory):  # Checks if the directory is not empty
            return self.load_database()
        else:
            # Assuming default loader as CSVLoader, update or overload this method as necessary for different loader types
            loader = CSVLoader(os.path.join(self.data_directory, "europarl_speeches.csv"))  # Update path as needed
            return self.build_database(loader)

    def load_database(self):
        self.db = Chroma(persist_directory=self.db_directory, embedding_function=self.embedding_model)
        return self.db

    def build_database(self, loader):

        # Load documents
        docs = loader.load()
        
        # Define text_splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        
        # Create splits
        splits = text_splitter.split_documents(docs)
        
        # Create database
        self.db = Chroma.from_documents(splits, self.embedding_model, persist_directory=self.db_directory)
        return self.db