import torch
import torch.nn.functional as F
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


class ManifestoBertaEmbeddings(Embeddings):
	"""Embeddings using ManifestoBerta for use with LangChain."""

	def __init__(self):
		# Load the tokenizer and model
		self.tokenizer = AutoTokenizer.from_pretrained(
			"manifesto-project/manifestoberta-xlm-roberta-56policy-topics-sentence-2023-1-1"
		)
		self.model = AutoModel.from_pretrained(
			"manifesto-project/manifestoberta-xlm-roberta-56policy-topics-sentence-2023-1-1"
		)

	def _embed(self, text: str, mean_over_tokens=True) -> list[float]:
		"""Embed a text using ManifestoBerta.

		Args:
		    text: The text to embed.

		Returns:
		    Embeddings for the text.
		"""

		# Encode the text
		inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

		# Get model output (make sure to set output_hidden_states to True)
		with torch.no_grad():
			outputs = self.model(**inputs, output_hidden_states=True)

		# Extract the last hidden states
		last_hidden_states = outputs.hidden_states[-1]

		# Average the token embeddings for a representation of the whole text
		if mean_over_tokens:
			embedding = torch.mean(last_hidden_states, dim=1)
		else:
			embedding = last_hidden_states

		# Convert to list
		embedding_list = embedding.cpu().tolist()

		return embedding_list[0]

	def embed_documents(self, texts: list[str]) -> list[list[float]]:
		return [self._embed(text) for text in texts]

	def embed_query(self, text: str) -> list[float]:
		# return self.embed_documents([text])[0] # previous version
		return self._embed(text)


class E5BaseEmbedding(Embeddings):
	"""Embeddings using ManifestoBerta for use with LangChain."""

	def __init__(self):
		# Load the tokenizer and model
		self.tokenizer = AutoTokenizer.from_pretrained("danielheinz/e5-base-sts-en-de")

		self.model = AutoModel.from_pretrained("danielheinz/e5-base-sts-en-de")

	def _embed(self, text: str, mean_over_tokens=True) -> list[float]:
		"""Embed a text using ManifestoBerta.

		Args:
		    text: The text to embed.

		Returns:
		    Embeddings for the text.
		"""

		# Encode the text
		inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

		# Get model output (make sure to set output_hidden_states to True)
		with torch.no_grad():
			outputs = self.model(**inputs, output_hidden_states=True)

		# Extract the last hidden states
		last_hidden_states = outputs.hidden_states[-1]

		# Average the token embeddings for a representation of the whole text
		if mean_over_tokens:
			embedding = torch.mean(last_hidden_states, dim=1)
		else:
			embedding = last_hidden_states

		# Convert to list
		embedding_list = embedding.cpu().tolist()

		return embedding_list[0]

	def embed_documents(self, texts: list[str]) -> list[list[float]]:
		return [self._embed(text) for text in texts]

	def embed_query(self, text: str) -> list[float]:
		# return self.embed_documents([text])[0] # previous version
		return self._embed(text)


class JinaAIEmbedding(Embeddings):
	"""Embeddings using ManifestoBerta for use with LangChain."""

	def __init__(self):
		# Load the tokenizer and model
		self.tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v2-base-de")
		self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-base-de", trust_remote_code=True)

	def _embed(self, text: str, mean_over_tokens=True) -> list[float]:
		"""Embed a text using ManifestoBerta.

		Args:
		    text: The text to embed.

		Returns:
		    Embeddings for the text.
		"""

		# Encode the text
		inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")

		# Get model output (make sure to set output_hidden_states to True)
		with torch.no_grad():
			model_output = self.model(**inputs)

		embedding = mean_pooling(model_output, inputs["attention_mask"])
		embedding = F.normalize(embedding, p=2, dim=1)

		# Convert to list
		embedding_list = embedding.cpu().tolist()

		return embedding_list[0]

	def embed_documents(self, texts: list[str]) -> list[list[float]]:
		return [self._embed(text) for text in texts]

	def embed_query(self, text: str) -> list[float]:
		# return self.embed_documents([text])[0] # previous version
		return self._embed(text)


class SentenceTransformerEmbedding(Embeddings):
	"""Embeddings using ManifestoBerta for use with LangChain."""

	def __init__(self, model_name="multi-qa-mpnet-base-dot-v1"):
		# Load the tokenizer and model
		self.model = SentenceTransformer(model_name)

	def _embed(self, text: str) -> list[float]:
		"""Embed a text using ManifestoBerta.

		Args:
		    text: The text to embed.

		Returns:
		    Embeddings for the text.
		"""

		# Encode the text
		embedding = self.model.encode(text)
		embedding = [float(e) for e in embedding]
		return embedding

	def embed_documents(self, texts: list[str]) -> list[list[float]]:
		return [self._embed(text) for text in texts]

	def embed_query(self, text: str) -> list[float]:
		# return self.embed_documents([text])[0] # previous version
		return self._embed(text)
