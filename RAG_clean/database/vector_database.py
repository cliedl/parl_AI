from langchain_community.document_loaders import PyPDFDirectoryLoader, PDFMinerLoader
from langchain_community.document_loaders.pdf import UnstructuredPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import glob
import os
import random
import shutil
import time


class VectorDatabase:
    def __init__(
        self,
        embedding_model,
        source_type,  # "manifestos" or "debates"
        data_path=".",
        database_directory="./chroma",
        chunk_size=1000,
        chunk_overlap=200,
        loader="pdf",
        reload=True,
    ):
        """
        Initializes the VectorDatabase.

        Parameters:
        - embedding_model: The model used to generate embeddings for the documents.
        - data_directory (str): The directory where the source documents are located. Defaults to the current directory.
        - database_directory (str): The directory to store the Chroma database. Defaults to './chroma'.
        - chunk_size (int): The size of text chunks to split the documents into. Defaults to 1000.
        - chunk_overlap (int): The number of characters to overlap between adjacent chunks. Defaults to 100.
        - loader(str): "pdf" or "csv", depending on data format
        """

        self.embedding_model = embedding_model
        self.source_type = source_type
        self.data_path = data_path
        self.database_directory = database_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.loader = loader

        if reload:
            self.database = self.load_database()

    def load_database(self):
        """
        Loads an existing Chroma database.

        Returns:
        - The loaded Chroma database.
        """
        if os.path.exists(self.database_directory):
            self.database = Chroma(
                persist_directory=self.database_directory,
                embedding_function=self.embedding_model,
            )
            print("reloaded database")
        else:
            raise AssertionError(
                f"{self.database_directory} does not include database."
            )

        return self.database

    def build_database(self, overwrite=True):
        """
        Builds a new Chroma database from the documents in the data directory.

        Parameters:
        - loader: Optional, a document loader instance. If None, PyPDFDirectoryLoader will be used with the data_directory.

        Returns:
        - The newly built Chroma database.
        """
        # # If overwrite flag is true, remove old databases from directory if they exist
        # if overwrite:
        #     if os.path.exists(self.database_directory):
        #         shutil.rmtree(self.database_directory)
        #         time.sleep(1)

        # PDF is the default loader defined above

        if os.path.exists(self.database_directory):
            raise AssertionError("Delete old database first and restart session!")

        # Define text_splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        if self.loader == "pdf":
            # loader = PyPDFDirectoryLoader(self.data_path)
            # get file_paths of all pdfs in data_folder
            pdf_paths = glob.glob(os.path.join(self.data_path, "*.pdf"))

            splits = []
            for pdf_path in pdf_paths:
                file_name = os.path.basename(pdf_path)
                party = file_name.split("_")[0]

                # Load pdf as single doc
                loader = PDFMinerLoader(pdf_path, concatenate_pages=True)
                doc = loader.load()

                # Also load pdf as individual pages, this is important to extract the page number later
                loader = PDFMinerLoader(pdf_path, concatenate_pages=False)
                doc_pages = loader.load()

                # Add party to metadata
                for i in range(len(doc)):
                    doc[i].metadata.update({"party": party})

                # Create splits
                splits_temp = text_splitter.split_documents(doc)

                # For each split, we search for the page on which it has occurred
                for split in splits_temp:
                    for i, doc_page in enumerate(doc_pages):
                        # Create first and second half of split
                        split_1 = split.page_content[
                            : int(0.5 * len(split.page_content))
                        ]
                        split_2 = split.page_content[
                            int(0.5 * len(split.page_content)) :
                        ]
                        # If the first half is on page i, set page=i
                        if split_1 in doc_page.page_content:
                            split.metadata.update({"page": i})
                        # If the second half is on page i, set page=i
                        elif split_2 in doc_page.page_content:
                            split.metadata.update({"page": i})

                splits.extend(splits_temp)

        elif self.loader == "csv":
            loader = CSVLoader(
                self.data_path,
                metadata_columns=["date", "fullName", "politicalGroup", "party"],
            )
            # Load documents
            docs = loader.load()

            # Create splits
            splits = text_splitter.split_documents(docs)

        # Create database
        self.database = Chroma.from_documents(
            splits,
            self.embedding_model,
            persist_directory=self.database_directory,
            collection_metadata={"hnsw:space": "cosine"},
        )

        return self.database

    def get_retriever(self, search_type="similarity", k=10):
        retriever = self.database.as_retriever(
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

        sources = ["gruene", "spd", "cdu", "afd", "fdp", "linke"]

        random.shuffle(sources)

        docs = []

        for source in sources:
            docs.extend(
                self.database.similarity_search(query, k=k, filter={"party": source})
            )

        context = ""

        if self.source_type == "manifestos":
            context += "Ausschnitte aus den Wahlprogrammen zur Europawahl 2024:\n"
            source_description = "dem Wahlprogramm zur Europawahl 2024"
        elif self.source_type == "debates":
            context += "Ausschnitte aus vergangenen Reden im Europaparlament im Zeitraum 2019-2024:\n"
            source_description = "vergangenen Reden im Europaparlament"

        for doc in docs:
            context += f"Ausschnitt aus {source_description} "
            context += f"von der Partei {doc.metadata['party']}:\n"
            context += f"{doc.page_content}\n\n"

        return context


if __name__ == "__main__":
    from langchain_openai import OpenAIEmbeddings

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    embedding_name = "openai"

    DATABASE_DIR = f"data/manifestos/chroma/{embedding_name}/"
    DATA_PATH = "data/manifestos/01_pdf_originals"

    database_manifestos = VectorDatabase(
        embedding_model=embedding_model,
        source_type="manifestos",
        database_directory=DATABASE_DIR,
        data_path=DATA_PATH,
        loader="pdf",
        reload=False,
    )

    database_manifestos.build_database()
