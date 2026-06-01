"""data/ 디렉터리에서 문서를 읽어 텍스트로 변환."""
from __future__ import annotations

import os
from dataclasses import dataclass

from pypdf import PdfReader


@dataclass
class Document:
    source: str
    text: str


def _load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_documents(data_dir: str) -> list[Document]:
    """디렉터리 내 .pdf / .txt / .md 파일을 모두 로드."""
    docs: list[Document] = []
    for name in sorted(os.listdir(data_dir)):
        path = os.path.join(data_dir, name)
        if not os.path.isfile(path):
            continue
        ext = name.lower().rsplit(".", 1)[-1]
        if ext == "pdf":
            text = _load_pdf(path)
        elif ext in {"txt", "md"}:
            text = _load_text(path)
        else:
            continue
        if text.strip():
            docs.append(Document(source=name, text=text))
    return docs
