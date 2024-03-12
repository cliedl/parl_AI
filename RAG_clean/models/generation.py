from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def generate_chain(retriever=None,
                   question_prompt=None,
                   llm=None):
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

    # If None, use default question prompt
    if question_prompt == None:
        question_prompt = ChatPromptTemplate.from_template("""
            Du hilfst dabei, die politischen Positionen verschiedener Parteien zur Europawahl 2024 zusammenzufassen und zu vergleichen.
            Beantworte die folgende Frage nur auf dem zur Verfügung gestellten Kontext.
            Falls sich die Frage auf Basis des Kontexts nicht beantworten lässt, gib eine kurze Begründung an.
                                                    
            KONTEXT:
            {context}

            FRAGE: {question}

            """)
    # If None, use default llm (gpt-3.5-turbo)
    if llm == None:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                         max_tokens=1000,
                         temperature=0.7)

    # Create chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | question_prompt
        | llm
        | StrOutputParser()
    )

    return chain
