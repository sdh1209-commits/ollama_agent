"""ChromaDB 영속 벡터 저장소 래퍼."""
from __future__ import annotations

import chromadb


class VectorStore:
    def __init__(self, path: str, collection_name: str) -> None:
        self._client = chromadb.PersistentClient(path=path)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, embedding: list[float], top_k: int) -> list[str]:
        result = self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )
        docs = result.get("documents") or [[]]
        return docs[0]

    def reset(self) -> None:
        """컬렉션을 비웁니다 (재색인 시 사용)."""
        name = self._collection.name
        self._client.delete_collection(name)
        self._collection = self._client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )
