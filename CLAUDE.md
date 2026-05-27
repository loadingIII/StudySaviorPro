# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

StudySaviorPro is an AI-powered study assistant with a FastAPI backend and Vue 3 frontend. The backend uses a multi-agent architecture (Agent-as-Tool pattern) where a Supervisor Agent routes user queries to specialized sub-agents (RAG, WebSearch, Question generation).

## Common Commands

### Backend
```bash
# Run the FastAPI server (with uvicorn)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Install Python dependencies
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production (vue-tsc + vite build)
npm run preview  # Preview production build
```

## Architecture

### Backend Structure
- **`main.py`** — FastAPI app entry point, registers routers and JWT middleware
- **`router/`** — API route handlers (agent, user, vector_store)
- **`agent/`** — Multi-agent system core
  - `agent.py` — Entry point exposing `agent_invoke` and `agent_stream`
  - `sub_agents/supervisor.py` — Supervisor Agent that routes to sub-agents via `create_agent`
  - `sub_agents/base_agent.py` — `BaseSubAgent` ABC with `as_tool()` pattern
  - `sub_agents/` — Individual agents: `rag_agent`, `web_search_agent`, `question_agent`
  - `llms/` — LLM instances (ChatOpenAI wrappers, configured via env)
  - `rag/` — RAG pipeline (ChromaDB vector store, retrieval, query generation)
  - `memory/` — PostgreSQL-based conversation memory (checkpointer/store)
  - `tool/` — Base tool utilities
- **`model/`** — SQLAlchemy ORM models (Base in `model/base.py`)
- **`crud/`** — Database service layer
- **`schemas/`** — Pydantic request/response schemas
- **`utils/`** — Shared utilities (config, DB, JWT, logging, file handling)
- **`middleware/jwtMiddleware.py`** — JWT auth middleware (excludes `/user/login`, `/docs`)

### Frontend Structure
Vue 3 + TypeScript + Vite app in `frontend/` with vue-router.

### Key Configuration
- **`.env`** — Environment variables (see `.env.example`): model API keys, JWT secret, model endpoints
- **`properties/database.yml`** — PostgreSQL connection config
- **`properties/chroma.yml`** — ChromaDB config

## Multi-Agent Pattern

The Supervisor Agent uses `langchain.agents.create_agent` and routes to sub-agents exposed as `StructuredTool` via `as_tool()`. To add a new sub-agent:
1. Create `agent/sub_agents/xxx_agent.py`, inherit `BaseSubAgent`, implement `_run()`
2. Instantiate at module level and export
3. Register in `supervisor.py` by adding to `get_sub_agent_tools()` list
4. Update the Supervisor's `SYSTEM_PROMPT`

## Database

Async PostgreSQL via SQLAlchemy (`asyncpg`). Session management in `utils/dbUtils.py` with `get_db()` dependency. Uses `DeclarativeBase` from `model/base.py`.

## Environment Setup

Copy `.env.example` to `.env` and fill in: `MODEL_API`, `MODEL_URL`, `MODEL_NAME`, `ZHI_PU_API_KEY`, `JWT_SECRET_KEY`, `ALGORITHM`. PostgreSQL config goes in `properties/database.yml`.
