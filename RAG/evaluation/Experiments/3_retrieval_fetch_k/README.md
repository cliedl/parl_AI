22.03.2024, experiment performed with commit 15fe371

# Experiment 3_retrieval_fetch_k:
This experiments tests the fetch_k hyperparameter of max_marginal_relevance_search

# Settings: 
* Embeddings: OpenAI (text-embedding-3-large)
* Retrieval: 3 manifestos and 3 debates per party, maximal_marginal_relevance_retrieval fetch_k variable
* LARGE_LANGUAGE_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo", max_tokens=300, temperature=0)
* Evaluator LLM: OpenAI gpt3.5-turbo

# Experimental runs: 
* 3a: fetch_k = 20
* 3b: fetch_k = 15
* 3c: fetch_k = 10
* 3d: fetch_k = 5