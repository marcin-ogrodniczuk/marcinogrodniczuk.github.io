---
layout: page
title: Biomedical Literature RAG Pipeline
description: Retrieval-augmented generation workflow for querying PubMed-style biomedical literature.
img:
importance: 2
category: portfolio
---

Built a RAG pipeline that ingests over 100 PubMed abstracts and answers natural-language questions with inline citations, running locally via
Ollama. (GitHub: https://github.com/marcin-ogrodniczuk/p53-rag-pipeline)

Engineered the full retrieval stack: NCBI Entrez ingestion, semantic chunking (154 indexed chunks), nomic-embed
text embeddings, ChromaDB cosine vector search, feeding grounded context to a local llama3.1 LLM via Ollama.
