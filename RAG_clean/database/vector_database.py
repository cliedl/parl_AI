from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


class VectorDatabaseCreator:
    def __init__(
        self,
        embedding_model,
        data_path=".",
        db_directory="./chroma",
        chunk_size=1000,
        chunk_overlap=200,
        loader="pdf",
    ):
        """
        Initializes the VectorDatabaseCreator.

        Parameters:
        - embedding_model: The model used to generate embeddings for the documents.
        - data_directory (str): The directory where the source documents are located. Defaults to the current directory.
        - db_directory (str): The directory to store the Chroma database. Defaults to './chroma'.
        - chunk_size (int): The size of text chunks to split the documents into. Defaults to 1000.
        - chunk_overlap (int): The number of characters to overlap between adjacent chunks. Defaults to 100.
        """

        self.embedding_model = embedding_model
        self.data_path = data_path
        self.db_directory = db_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.db = None
        self.loader = loader

    def load_database(self):
        """
        Loads an existing Chroma database.

        Returns:
        - The loaded Chroma database.
        """
        self.db = Chroma(
            persist_directory=self.db_directory, embedding_function=self.embedding_model
        )

        return self.db

    def build_database(self):
        """
        Builds a new Chroma database from the documents in the data directory.

        Parameters:
        - loader: Optional, a document loader instance. If None, PyPDFDirectoryLoader will be used with the data_directory.

        Returns:
        - The newly built Chroma database.
        """

        # PDF is the default loader defined above
        if self.loader == "pdf":
            loader = PyPDFDirectoryLoader(self.data_path)
        elif self.loader == "csv":
            loader = CSVLoader(self.data_path)

        # Load documents
        docs = loader.load()

        # Define text_splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        # Create splits
        splits = text_splitter.split_documents(docs)

        # Create database
        self.db = Chroma.from_documents(
            splits, self.embedding_model, persist_directory=self.db_directory
        )

        return self.db