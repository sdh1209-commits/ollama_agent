"""CLI 진입점: index / ask / chat 명령 처리."""
import argparse
import sys

from src.rag import RAGAssistant


def cmd_index(_args: argparse.Namespace) -> None:
    assistant = RAGAssistant()
    count = assistant.index_documents()
    print(f"✅ 색인 완료: {count}개 청크가 저장되었습니다.")


def cmd_ask(args: argparse.Namespace) -> None:
    assistant = RAGAssistant()
    answer = assistant.ask(args.question)
    print(f"\n🤖 {answer}\n")


def cmd_chat(_args: argparse.Namespace) -> None:
    assistant = RAGAssistant()
    print("💬 대화형 모드입니다. 종료하려면 'exit' 입력.\n")
    while True:
        try:
            question = input("나> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break
        if question.lower() in {"exit", "quit", "q"}:
            break
        if not question:
            continue
        print(f"🤖> {assistant.ask(question)}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local RAG Assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("index", help="data/ 폴더의 문서를 색인합니다")

    ask = sub.add_parser("ask", help="한 번 질문하고 답변을 받습니다")
    ask.add_argument("question", help="질문 내용")

    sub.add_parser("chat", help="대화형 모드를 실행합니다")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    dispatch = {"index": cmd_index, "ask": cmd_ask, "chat": cmd_chat}
    dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
