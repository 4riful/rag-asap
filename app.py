#!/usr/bin/env python3
"""
rag-asap: tiny local RAG quickstart

Usage:
  # minimal (no extra deps)
  python app.py "your question"

  # better (optional) install sentence-transformers:
  # pip install -r requirements.txt
  python app.py --model sentence-transformers/all-MiniLM-L6-v2 "your question"
"""
import sys
import argparse
from pathlib import Path

# optional imports
try:
    from sentence_transformers import SentenceTransformer, util
    HAS_S2 = True
except Exception:
    HAS_S2 = False

EXAMPLE_DOC = Path("examples/README_DOC.txt")


def build_chunks(text, chunk_size=400):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size
    return chunks


def overlap_score(query, text):
    q = set(query.lower().split())
    t = set(text.lower().split())
    return len(q & t)


def query_by_overlap(query, chunks, top=1):
    scored = [(overlap_score(query, c), c) for c in chunks]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:top] if s > 0] or [chunks[0]]


def query_by_sbert(model_name, query, chunks, top=1):
    if not HAS_S2:
        raise RuntimeError("sentence-transformers not installed")
    model = SentenceTransformer(model_name)
    corpus_embeddings = model.encode(chunks, convert_to_tensor=True)
    q_emb = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(q_emb, corpus_embeddings, top_k=top)[0]
    # hits is list of dicts with 'corpus_id' and 'score'
    return [chunks[h['corpus_id']] for h in hits]


def load_chunks(path=EXAMPLE_DOC):
    if not path.exists():
        print(f"Error: example document not found at {path}", file=sys.stderr)
        sys.exit(2)
    text = path.read_text(encoding="utf-8")
    return build_chunks(text)


def main():
    ap = argparse.ArgumentParser(prog="rag-asap", description="Tiny local RAG demo")
    ap.add_argument("query", nargs="+", help="Question to ask")
    ap.add_argument("--model", default="overlap", help="Use 'overlap' (default) or a sentence-transformers model name")
    ap.add_argument("--top", type=int, default=1, help="Number of top chunks to return")
    args = ap.parse_args()
    q = " ".join(args.query)
    chunks = load_chunks()
    if args.model != "overlap" and HAS_S2:
        try:
            results = query_by_sbert(args.model, q, chunks, top=args.top)
        except Exception as e:
            print("SBERT query failed:", e, "- falling back to overlap", file=sys.stderr)
            results = query_by_overlap(q, chunks, top=args.top)
    else:
        results = query_by_overlap(q, chunks, top=args.top)

    print("\n=== QUERY ===")
    print(q)
    print("\n=== TOP RESULT(S) ===")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}]\n{r}\n")


if __name__ == "__main__":
    main()
