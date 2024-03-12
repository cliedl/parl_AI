from transformers import AutoModel, AutoTokenizer
from langchain_core.embeddings import Embeddings
import torch
from typing import List


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

    def _embed(self, text: str, sentence_level=True) -> List[float]:
        """Embed a text using ManifestoBerta.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """

        # Encode the text
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=512
        )

        # Get model output (make sure to set output_hidden_states to True)
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)

        # Extract the last hidden states
        last_hidden_states = outputs.hidden_states[-1]

        # Optionally, you can average the token embeddings for sentence-level representation
        if sentence_level:
            embedding = torch.mean(last_hidden_states, dim=1)
        else:
            embedding = last_hidden_states

        # Convert to list
        embedding_list = embedding.cpu().tolist()

        return embedding_list[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        # return self.embed_documents([text])[0] # previous version
        return self._embed(text)
