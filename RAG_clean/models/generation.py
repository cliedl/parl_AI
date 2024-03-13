from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Output format
class PartySummaries(BaseModel):
    cdu_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei CDU/CSU"
    )
    spd_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei SPD"
    )
    gruene_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei Bündnis 90/Die Grünen"
    )
    linke_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei Die Linke"
    )
    fdp_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei FDP"
    )
    afd_summary: str = Field(
        description="Zusammenfassung der Positionen der Partei AfD"
    )

def generate_chain(retriever=None, 
                   llm=None, 
                   output_parser="json", 
                   verbose=False, 
                   temperature=0.0):
    """
    Generates a langchain: Change this code to change the chain!

    arguments:
    - retriever (langchain_core.vectorstores.VectorStoreRetriever): retriever object
    - question_prompt (langchain_core.prompts.chat.ChatPromptTemplate): Template for prompt
    - llm

    returns:
    - chain (langchain_core.runnables.base.RunnableSequence)

    Example usage:
    chain = generate_chain(retriever)
    chain.invoke("Was ist die Position der SPD zur Solarenergie?")
    """

    prompt_template = """
    Du hilfst dabei, die politischen Positionen der Parteien CDU/CSU, SPD, Bündnis 90/Die Grünen, Die Linke, FDP und AfD zur Europawahl 2024 zusammenzufassen.
    Beantworte die folgende Frage nur auf dem zur Verfügung gestellten Kontext.
    Falls sich die Frage auf Basis des Kontexts nicht beantworten lässt, gib eine kurze Begründung an.
    Beantworte die Frage auf Deutsch.

    FRAGE: {question}

    KONTEXT:
    {context}
    """

    # If None, use default llm (gpt-3.5-turbo)
    if llm == None:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=1000, temperature=temperature)

    # If output parser is None, use JSON parser
    if output_parser == "json":
        output_parser = JsonOutputParser(pydantic_object=PartySummaries)

        prompt_template += "\n\n{format_instructions}\n"

        question_prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["question", "context"],
            partial_variables={
                "format_instructions": output_parser.get_format_instructions()
            },
        )

    elif output_parser == "str":

        output_parser = StrOutputParser()

        question_prompt = PromptTemplate.from_template(prompt_template)

    else:
        raise ValueError("output_parser must be 'json' or 'str'")


    # Create chain that returns context
    rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: x["context"]))
    | question_prompt
    | llm
    | StrOutputParser()
    )

    chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    # Create chain without context return
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | question_prompt
        | llm
        | output_parser
    )

    if verbose:
        return chain_with_source
    else:
        return chain
