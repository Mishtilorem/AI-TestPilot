# 🚀 AI TestPilot

**An AI-powered test automation platform.** Describe a feature in plain English — AI TestPilot generates the test cases, writes the Selenium automation, runs it in a real browser, and explains failures with AI root-cause analysis.

🔗 **Live:** [ai-testpilot.vercel.app](https://ai-testpilot.vercel.app) · 🎥 **Demo video:** [watch here](https://drive.google.com/file/d/1gADIRv-8cJAuG-1sPC_0_bqwqTzMSreQ/view?usp=sharing) · 📦 **Source:** [github.com/anmol-284/ai-testpilot](https://github.com/anmol-284/ai-testpilot)

---

## ✨ What it does

1. **Describe a requirement** in plain English.
2. **AI generates test cases** — positive, negative, boundary, validation, security.
3. **AI writes Selenium scripts** (Page Object Model, explicit waits).
4. **Executes in headless Chrome** — captures status, duration, logs, failure screenshots.
5. **AI explains failures** — root cause, suggested fixes, confidence score.
6. **Dashboard** tracks projects, runs, and pass rates.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS, shadcn/Radix, TanStack Query |
| **Backend** | Python, FastAPI, SQLAlchemy 2.0, Alembic, JWT auth |
| **Database** | PostgreSQL (Neon) / SQLite (local) |
| **AI** | Ollama + Llama 3 (local) · Groq (production) |
| **Automation** | Selenium (headless Chrome), Page Object Model |
| **Deployment** | Vercel · Render · Neon |

**Design highlights:** pluggable AI provider (swap Ollama ↔ Groq via one env var), layered backend (endpoint → service → repository), and DB-agnostic config (SQLite locally, Postgres in prod).

---

## ⚙️ Local Setup

**Prerequisites:** Python 3.12+, Node.js 20+, Chrome, and [Ollama](https://ollama.com) (`ollama pull llama3.1`).

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # defaults to SQLite + Ollama, no accounts needed
alembic upgrade head
uvicorn app.main:app --reload  # http://localhost:8000/docs

# Frontend
cd frontend
npm install
cp .env.example .env.local
npm run dev                    # http://localhost:3000
```

---

## 🚢 Deployment

Free-tier stack (Vercel + Render + Neon + Groq) — see [`DEPLOYMENT.md`](./DEPLOYMENT.md).

> Selenium **execution** runs locally (it needs a Chrome binary). The deployed app runs everything else — AI test/script generation, failure analysis, and reporting.

---

## 📂 Structure

```
backend/app/   api · services · repositories · models · schemas · ai · selenium · core
frontend/src/  app · components · hooks
```
