"""긴 텍스트를 겹침(overlap)을 둔 청크로 분할."""
from __future__ import annotations


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """문자 기준으로 chunk_size만큼 자르되 overlap만큼 겹치게 분할."""
    if chunk_size <= 0:
        raise ValueError("chunk_size는 0보다 커야 합니다.")
    if overlap >= chunk_size:
        raise ValueError("overlap은 chunk_size보다 작아야 합니다.")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks
