"""chunker 모듈 단위 테스트."""
import pytest

from src.chunker import chunk_text


def test_empty_text_returns_empty_list():
    assert chunk_text("", chunk_size=100, overlap=10) == []


def test_short_text_single_chunk():
    chunks = chunk_text("hello world", chunk_size=100, overlap=10)
    assert chunks == ["hello world"]


def test_long_text_is_split():
    text = "a" * 250
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=10, overlap=10)
