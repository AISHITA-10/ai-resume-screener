# AI Resume Screener (RAG + LLM) — Prototype

This is a lightweight **LLM-powered resume screening assistant** with **RAG (embeddings + vector DB)**, a **chunking strategy**, **prompt guardrails**, and a **Streamlit UI**.
Check the video for functional working.
## Features
- **Ingest resumes**: PDF / DOCX / TXT
- **Chunking strategy**: section-aware + bounded chunks with overlap
- **Vector DB**: local persistent **SQLite-based vector store** (prototype-friendly)
- **Embeddings**: **local hashing embeddings** (pure Python, no external API)
- **LLM**: local **Ollama** model (e.g. `llama3.1`)
- **RAG chat**: source-grounded answers with citations over indexed resumes
- **Resume screening**: generate a structured fit assessment vs a job description
- **Guardrails**:
  - **Source-grounded answering** 
  - **Confidence gating** via retrieval score thresholds
- **Advanced capability (Task 3)**: **multi-document reasoning** (compare multiple resumes with evidence)

## Design choices & rationale
- **Local-first stack**: embeddings, vector DB, and LLM all run locally (hashing embeddings + SQLite + Ollama), which:
  - avoids external API quotas and internet dependency,
  - makes the prototype easy to run on any machine.
- **SQLite vector store**: simple, file-based storage that is:
  - easy to reason about,
  - sufficient for a small corpus of resumes,
  - closer to how a real vector DB would be used (ids, metadata, similarity search).
- **Hashing embeddings**: a lightweight alternative to large embedding models:
  - pure Python, fast enough, and robust to Python 3.13,
  - still supports cosine-style retrieval for RAG.
- **Ollama LLM**:
  - lets you use strong open models (e.g. Llama 3.1) without managing CUDA / containers directly,
  - keeps prompts and data on your machine for privacy.
- **Guardrails in the RAG layer**:
  - retrieval confidence thresholds reduce hallucinated answers,
  - prompts explicitly enforce “answer only from context” + citations,
  - resume screening is done per-document to avoid cross-candidate leakage.

## Quickstart (Windows PowerShell)

```powershell
cd "C:\Users\Admin\Documents\AI Krisent\AI Resume Screener"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
copy .env.example .env
# Optional: adjust .env to change Ollama model
streamlit run .\app\streamlit_app.py
```

### Notes
- All components are **local**: embeddings, vector store, and LLM (via Ollama).
- If Ollama is disabled (set `USE_OLLAMA=0` in `.env`), the app still runs in **no-LLM** mode and returns evidence-only summaries.
- All app data is stored locally under `.data/`.

### Libraries, APIs, and services used
- **Python libraries**:
  - `streamlit`: web UI.
  - `python-dotenv`: load `.env` configuration.
  - `pypdf`, `python-docx`: parse PDF / DOCX resumes.
  - `pydantic`: data models (`ScreeningResult`, citations, etc.).
  - `requests`: HTTP client for calling Ollama.
- **Local services**:
  - `Ollama` (e.g. `llama3.1` model) for all LLM completions.
  - Local filesystem for the SQLite vector store and uploaded resumes.

## Repository layout
- `app/streamlit_app.py`: UI
- `src/rag/`: ingestion, chunking, embeddings, retrieval, prompting
- `docs/`: writeups for Tasks 1–4

## Task mapping
- **Task 1 (LLM + RAG prototype)**: implemented via `src/rag/*` and the Streamlit UI for ingesting resumes, chunking, indexing, and querying with an LLM.
- **Task 2 (hallucination & quality control)**: guardrails in prompts and `RAGService` (confidence thresholds, source-grounded answers, scoped retrieval).
- **Task 3 (advanced capability)**: **multi-document reasoning** in the “Compare” tab, where multiple resumes are evaluated against the same JD with evidence-backed ranking.
- **Task 4 (enterprise architecture)**: high-level internal assistant architecture documented in `docs/task4_enterprise_ai_architecture.md`.

