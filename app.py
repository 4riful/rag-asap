# app.py - RAG-ASAP tiny demo
import sys
from pathlib import Path

def build_index(doc_path="examples/README_DOC.txt"):
    text = Path(doc_path).read_text(encoding="utf-8")
    # super-simple "index": split into paragraphs
    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    return chunks

def query_index(q, chunks):
    # naive: return chunk with max overlap words
    qwords = set(q.lower().split())
    best = max(chunks, key=lambda c: len(qwords & set(c.lower().split())))
    return best

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py \"your question\"")
        return
    q = sys.argv[1]
    chunks = build_index()
    answer = query_index(q, chunks)
    print("=== Best chunk ===\n", answer)

if __name__ == "__main__":
    main()
