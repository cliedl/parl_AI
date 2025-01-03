from langchain_openai import ChatOpenAI
import asyncio


class RAG:
    """
    RAG model for generating answers to questions about political parties in the context of their manifestos and debates.

    Args:
    databases: list of VectorDatabase objects
    llm: ChatOpenAI object, default is ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=2000, temperature=0)
    k: int, number of documents to fetch from each database, default is 3
    language: str, language of the generated answer, default is "Deutsch"
    """

    def __init__(self, databases, parties=None, llm=None, k=3, language="Deutsch"):
        self.databases = databases
        self.llm = llm
        self.k = k
        self.language = language
        if parties == None:
            self.parties = ["gruene", "spd", "cdu", "afd", "fdp", "linke"]
        else:
            self.parties = parties
        if self.llm == None:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo", max_tokens=2000, temperature=0
            )

    def get_documents_for_party(self, question, party):
        """
        Fetches documents from each database for a given party and a list of questions.

        Args:
        question: str, question
        party: str, party name (one of "gruene", "spd", "cdu", "afd", "fdp", "linke")

        Returns:
        docs: dict, dictionary of documents for each source type ("manifestos" and "debates")
        """
        docs = {}
        for db in self.databases:
            docs[db.source_type] = db.database.max_marginal_relevance_search(
                question, k=self.k, fetch_k=5, filter={"party": party}
            )
        return docs

    def build_context_from_docs(self, docs):
        """
        Builds context string from documents for use in prompting.

        Args:
        docs: dict, dictionary of documents for each source type ("manifestos" and "debates")

        Returns:
        context: str, context string (formatted and human-readable excerpts from documents)
        """

        context = ""
        for source_type in docs:
            if source_type == "manifestos":
                context_header = (
                    "Ausschnitte aus den Wahlprogrammen zur Europawahl 2024:\n"
                )
            elif source_type == "debates":
                context_header = "Ausschnitte aus vergangenen Reden im Europaparlament im Zeitraum 2019-2024:\n\n"

            context_source = (
                context_header
                + "\n\n".join([doc.page_content for doc in docs[source_type]])
                + "\n\n"
            )

            context += context_source

        return context

    def generate_prompt_for_party(self, question, party):
        """
        Generates a prompt for a given party and question.

        Args:
        question: str, question
        party: str, party name (one of "gruene", "spd", "cdu", "afd", "fdp", "linke")

        Returns:
        prompt_dict: dict, dictionary containing the question, prompt, and documents for the party
        """
        docs = self.get_documents_for_party(question, party)
        context = self.build_context_from_docs(docs)
        prompt = f"""   
            Beantworte die unten folgende FRAGE DES NUTZERS, indem du die politischen Positionen der Partei im unten angegebenen KONTEXT zusammenfasst.
            Der KONTEXT umfasst Ausschnitte aus Redebeiträgen im EU-Parlament und aus dem EU-Wahlprogramm für 2024 für die Partei. 
            Deine Antwort soll ausschließlich die Informationen aus dem genannten KONTEXT beinhalten.
            Verwende in deiner Antwort NICHT den Namen der Partei, sondern beziehe dich auf die Partei ausschließlich mit "die Partei".
            Sollte der KONTEXT keine Antwort auf die FRAGE DES NUTZERS zulassen, gib anstelle der Zusammenfassung NUR die folgende Rückmeldung: 
            "Es wurde keine passende Antwort in den Quellen gefunden."
            Gib die Antwort auf {self.language}.

            KONTEXT:
            {context}

            FRAGE DES NUTZERS: 
            {question}
            """
        prompt_dict = {"question": question, "prompt": prompt, "docs": docs}
        return prompt_dict

    def generate_prompts(self, question):
        """
        Generates prompts for each party given a question.

        Args:
        question: str, question

        Returns:
        prompts_dict: dict, dictionary containing the question, prompt, and documents for each party
        """
        prompts_dict = {
            party: self.generate_prompt_for_party(question, party)
            for party in self.parties
        }
        return prompts_dict

    def query(self, question):
        """
        Generates answers for each party given a question.

        Args:
        question: str, question

        Returns:
        response_dict: dict, dictionary containing the question, prompt, documents, and answer for each party
        """
        response_dict = self.generate_prompts(question)

        # Run LLM on all prompts in parallel
        response_ = asyncio.run(
            self.llm.abatch(
                [response_dict[party]["prompt"] for party in response_dict.keys()]
            )
        )

        # Attach response content to party dictionary
        for i, party in enumerate(response_dict):
            response_dict[party]["answer"] = response_[i].content

        response_dict = self.format_response(response_dict)

        return response_dict

    def format_response(self, response):
        """
        Formats the response dictionary for simpler use in the app.

        Args:
        response: dict, dictionary containing the question, prompt, documents, and answer for each party

        Returns:
        response: dict, formatted dictionary containing the question, prompt, documents, and answer for each party
        """
        q = response[list(response.keys())[0]]["question"]
        p = {party: response[party]["prompt"] for party in response.keys()}
        d = {
            source: {
                party: response[party]["docs"][source] for party in response.keys()
            }
            for source in response[list(response.keys())[0]]["docs"].keys()
        }
        a = {party: response[party]["answer"] for party in response.keys()}
        response = {"question": q, "prompt": p, "docs": d, "answer": a}
        return response
