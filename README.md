# rag-asap — Local RAG Quickstart

Tiny, practical example demonstrating Retrieval-Augmented Generation locally.

## Why this exists
- Show minimal end-to-end RAG: index text → retrieve relevant chunk → return answer.
- Low friction: works without cloud keys. Optional improved accuracy with `sentence-transformers`.

## Quickstart (no deps)
```bash
python3 app.py "what is rag"
```

## Quickstart (better)

```bash
python3 -m pip install -r requirements.txt
python3 app.py --model sentence-transformers/all-MiniLM-L6-v2 "what is rag"
```

## Files

* `app.py` — demo CLI (overlap fallback + optional SBERT)
* `examples/README_DOC.txt` — sample doc
* `.github/` — CI and templates

## Contributing

* Add small backends (FAISS, simple disk index)
* Improve README, add more examples, add tests
* See `.github/CONTRIBUTING.md` for contribution steps

## Run tests (CI)

* We run static checks (flake8) and basic Python lint in CI.

## License

* MIT
