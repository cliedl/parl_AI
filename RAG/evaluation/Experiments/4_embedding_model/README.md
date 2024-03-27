22.03.2024, experiment performed with commit 335c64b

# Experiment 4_embedding model:
This experiments checks how the embedding model influences context relevancy

# Settings: 
* Embeddings: variable
* Retrieval: 3 manifestos and 3 debates per party, maximal_marginal_relevance_retrieval fetch_k=5
* LARGE_LANGUAGE_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo", max_tokens=300, temperature=0)
* Evaluator LLM: OpenAI gpt3.5-turbo

# Experimental runs: 
* 4a: embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
* 4b: embedding_model = ManifestoBertaEmbeddings() (manifesto-project/manifestoberta-xlm-roberta-56policy-topics-sentence-2023-1-1)
* 4c: embedding_model = SentenceTransformerEmbedding("multi-qa-mpnet-base-dot-v1")
* 4d: embedding_model = JinaAIEmbedding() (jinaai/jina-embeddings-v2-base-de)
* 4e: embedding_model = MistralAIEmbeddings(model="mistral-embed")
* 4f: embedding_model = E5BaseEmbedding() (danielheinz/e5-base-sts-en-de)