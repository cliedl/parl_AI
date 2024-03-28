from langchain_openai import ChatOpenAI
import asyncio


class RAG:
    def __init__(self, databases, llm=None, k=3, language="Deutsch"):
        self.databases = databases
        self.llm = llm
        self.k = k
        self.language = language
        self.parties = ["gruene", "spd", "cdu", "afd", "fdp", "linke"]

        if self.llm == None:
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo", max_tokens=2000, temperature=0
            )

    def get_documents_for_party(self, questions, party):
        docs = {}
        for db in self.databases:
            docs[db.source_type] = db.database.max_marginal_relevance_search(
                questions, k=self.k, fetch_k=5, filter={"party": party}
            )
        return docs

    def build_context_from_docs(self, docs):

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
        return {"question": question, "prompt": prompt, "docs": docs}

    def generate_prompts(self, question):
        prompts = {
            party: self.generate_prompt_for_party(question, party)
            for party in self.parties
        }
        return prompts

    def query(self, question):
        response = self.generate_prompts(question)

        response_ = asyncio.run(
            self.llm.abatch([response[party]["prompt"] for party in response.keys()])
        )

        # Attach response content to party dictionary
        for i, party in enumerate(response):
            response[party]["answer"] = response_[i].content

        response = self.format_response(response)

        return response

    def format_response(self, response):
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
