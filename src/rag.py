"""문서 색인 + 검색 증강 답변 생성 오케스트레이션."""
from __future__ import annotations

import ollama

import config
from src.chunker import chunk_text
from src.embedder import Embedder
from src.loader import load_documents
from src.vectorstore import VectorStore

PROMPT_TEMPLATE = """당신은 사용자의 문서를 기반으로 답하는 비서입니다.
아래 '문맥'만을 근거로 한국어로 답하세요. 문맥에 답이 없으면
"제공된 문서에서 답을 찾을 수 없습니다."라고 말하세요.

[문맥]
{context}

[질문]
{question}

[답변]"""


class RAGAssistant:
    def __init__(self) -> None:
        self._embedder = Embedder(config.EMBEDDING_MODEL)
        self._store = VectorStore(config.CHROMA_PATH, config.COLLECTION_NAME)
        self._client = ollama.Client(host=config.OLLAMA_HOST)

    def index_documents(self) -> int:
        """data/ 문서를 청크화·임베딩하여 벡터 DB에 저장."""
        self._store.reset()
        documents = load_documents(config.DATA_DIR)

        ids, embeddings, texts, metas = [], [], [], []
        for doc in documents:
            chunks = chunk_text(doc.text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            for i, chunk in enumerate(chunks):
                ids.append(f"{doc.source}-{i}")
                texts.append(chunk)
                metas.append({"source": doc.source, "chunk": i})

        if not texts:
            return 0

        embeddings = self._embedder.embed(texts)
        self._store.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metas)
        return len(texts)

    def ask(self, question: str) -> str:
        """질문에 대해 관련 문서를 검색하고 LLM으로 답변 생성."""
        query_vec = self._embedder.embed_one(question)
        context_chunks = self._store.query(query_vec, config.TOP_K)
        context = "\n\n---\n\n".join(context_chunks) if context_chunks else "(관련 문서 없음)"

        prompt = PROMPT_TEMPLATE.format(context=context, question=question)
        response = self._client.generate(model=config.LLM_MODEL, prompt=prompt)
        return response["response"].strip()
