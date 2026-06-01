"""sentence-transformers 기반 임베딩 생성기."""
from __future__ import annotations

from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
