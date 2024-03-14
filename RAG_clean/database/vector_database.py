from langchain_community.document_loaders import PyPDFDirectoryLoader, PDFMinerLoader
from langchain_community.document_loaders.pdf import UnstructuredPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import glob
import os


class VectorDatabaseCreator:
    def __init__(
        self,
        embedding_model,
        source_type,  # "manifestos" or "debates"
        data_path=".",
        db_directory="./chroma",
        chunk_size=1000,
        chunk_overlap=200,
        loader="pdf",
        concatenate_pages=True,
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
        self.source_type = source_type
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
            # loader = PyPDFDirectoryLoader(self.data_path)
            # get file_paths of all pdfs in data_folder
            pdf_paths = glob.glob(os.path.join(self.data_path, "*.pdf"))

            docs = []
            for pdf_path in pdf_paths:
                file_name = os.path.basename(pdf_path)
                party = file_name.split("_")[0]
                # Create doc loader
                loader = PDFMinerLoader(pdf_path, concatenate_pages=True)
                # load document
                doc = loader.load()
                # Add party to metadata
                for i in range(len(doc)):
                    doc[i].metadata.update({"party": party})
                # append  to list
                docs.extend(doc)

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

    def get_retriever(self, search_type="similarity", k=10):
        retriever = self.db.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": k,
                # "where": {  # https://docs.trychroma.com/usage-guide#using-where-filters
                #     "source": "something" #
                # },
            },
        )
        return retriever

    def build_context(self, query, k=5):

        # TODO: Update this list later according to metadata
        # sources = [
        #     "SPD",
        #     "CDU/CSU",
        #     "Bündnis 90/Die Grünen",
        #     "Die Linke",
        #     "FDP",
        #     "AfD",
        # ]

        # Sample sources for testing and debugging with manifestos
        sources = [
            "../data/manifestos/01_pdf_originals/gruene_manifesto.pdf",
            "../data/manifestos/01_pdf_originals/spd_manifesto.pdf",
            "../data/manifestos/01_pdf_originals/fdp_manifesto.pdf",
        ]

        docs = []

        for source in sources:
            docs.extend(
                self.db.similarity_search(
                    query, k=k, filter={"source": source}
                )  # TODO: use correct metadata field
            )

        context = ""

        if self.source_type == "manifestos":
            context += "Ausschnitte aus den Wahlprogrammen zur Europawahl 2024:\n"
            source_desc = "dem Wahlprogramm zur Europawahl 2024"
        elif self.source_type == "debates":
            context += "Ausschnitte aus vergangenen Reden im Europaparlament im Zeitraum 2019-2024:\n"
            source_desc = "vergangenen Reden im Europaparlament"

        for doc in docs:
            context += f"Ausschnitt aus {source_desc} "
            context += f"von der Partei {doc.metadata['source']}:\n"
            context += f"{doc.page_content}\n\n"

        return context
