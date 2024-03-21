21.03.2024, experiment performed with commit 53b617c

# Experiment 1:
This experiment tests how faithfulness and answer_relevancy change when the context is anonymized, i.e., the llm does not know which context belongs to which party: 

# Settings: 
* LLM: OpenAI (gpt-3.5-turbo)
* Embeddings: OpenAI (text-embedding-3-large)
* Retrieval: 5 manifestos per party

# Experimental runs: 
* 1a: context is anonymzed when passed to LLM (LLM does not know which party the context comes from)
* 1b: context is not anonymzed (LLM knows which party the context comes from)


