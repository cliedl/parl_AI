from openai import OpenAI


class Evaluator:
    def __init__(self):
        self.client = OpenAI()

    def context_relevancy(self, question, context_docs):
        instruction = """
        Du hilfst mir bei der Evaluation eines RAG systems. 
        Bewerte, ob die folgenden Dokumente relevant sind für die Frage. 
        Antworte mit einer List, in der für jedes Dokument entweder 0 (nicht relevant) oder 1 (relevant) ausgegeben wird.
        Beispiel: 0, 1, 1, 1, 0
        """

        context = ""
        for i, doc in enumerate(context_docs):
            context += f"Dokument {i+1}: {doc.page_content}\n\n"

        prompt = f"""
        {instruction}
        
        Hier sind die Dokumente:
        {context}
        
        Hier ist die Frage:
        {question}"""

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        # Parse output into list
        try:
            response = completion.choices[0].message.content
            result = [int(x.strip()) for x in response.split(",")]

            # Check if all values are 0 or 1
            if False in [r in [0, 1] for r in result]:
                raise AssertionError
        except:
            return response

        context_relevancy = sum(result) / len(result)

        return context_relevancy
