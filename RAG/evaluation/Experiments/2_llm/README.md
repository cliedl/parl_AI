22.03.2024, experiment performed with commit a0bd6c5

# Experiment 2_llm:
This experiment tests how the lllm influences faithfulness and answer_relevancy

# Settings: 
* Embeddings: OpenAI (text-embedding-3-large)
* Retrieval: 3 manifestos and 3 debates per party, maximal_marginal_relevance_retrieval with 20 docs
* Evaluator LLM: OpenAI gpt3.5-turbo

# Experimental runs: 
* 2a: 
    LARGE_LANGUAGE_MODEL = ChatOpenAI(
    model_name="gpt-3.5-turbo", max_tokens=300, temperature=0)

* 2b: LARGE_LANGUAGE_MODEL = ChatMistralAI(
    name="open-mixtral-8x7b", max_tokens=300, temperature=0)

* 3b: LARGE_LANGUAGE_MODEL = ChatAnthropic(
    model_name="claude-3-haiku-20240307", max_tokens=300, temperature=0)
