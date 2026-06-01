# 🧠 Local RAG Assistant

로컬에서 완전히 동작하는 **개인 지식 비서**입니다. 내 문서(PDF, 텍스트, 마크다운)를
불러와 임베딩한 뒤, [Ollama](https://ollama.com)로 구동되는 로컬 LLM에게
"내 문서 기반으로" 질문할 수 있습니다. 외부 API 없이 프라이버시를 지키며 동작합니다.

## ✨ 특징

- 🔒 **완전 로컬 동작** — 데이터가 외부로 나가지 않음
- 📚 **다양한 문서 지원** — PDF, TXT, Markdown
- 🔍 **RAG (검색 증강 생성)** — 내 문서를 근거로 답변
- 🧩 **모듈식 구조** — 로더 / 청커 / 임베더 / 벡터스토어 분리

## 🛠 사전 준비

1. [Ollama 설치](https://ollama.com/download)
2. 모델 다운로드:
   ```bash
   ollama pull llama3.2
