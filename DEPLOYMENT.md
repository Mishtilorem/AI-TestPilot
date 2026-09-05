# Deploying AI TestPilot (free tier)

Architecture in production:

- **Frontend** → Vercel (Next.js)
- **Backend** → Render (FastAPI, native Python runtime — no Docker)
- **Database** → Neon (Postgres)
- **AI** → Groq API (fast hosted Llama 3)
- **Screenshots** → Cloudinary

> **One limitation:** the Render free Python runtime has no Chrome browser, so
> **live Selenium test execution is a local-only feature**. Everything else —
> auth, projects, AI test-case generation, AI script generation, AI failure
> analysis, and reporting — runs fully in the cloud. Demo test *execution*
> locally (where Chrome is installed) and the rest on the deployed site.

---

## Step 0 — Push the code to GitHub

```bash
cd ~/ai-testpilot
git add -A && git commit -m "chore: deployment config"
# create an empty repo on github.com first, then:
git remote add origin https://github.com/<you>/ai-testpilot.git
git branch -M main
git push -u origin main
```

## Step 1 — Database (Neon)

1. Sign up at https://neon.tech → create a project.
2. Copy the **connection string** (looks like `postgresql://user:pass@ep-xxx.aws.neon.tech/dbname?sslmode=require`).
3. Keep it — it becomes `DATABASE_URL` on Render.

## Step 2 — AI (Groq)

1. Sign up at https://console.groq.com → **API Keys** → create one.
2. Keep it — it becomes `GROQ_API_KEY`. Model is `llama-3.1-8b-instant`.

## Step 3 — Screenshots (Cloudinary)

1. Sign up at https://cloudinary.com → dashboard shows **Cloud name**, **API Key**, **API Secret**.
2. Keep all three.

## Step 4 — Backend (Render)

1. Sign up at https://render.com → **New + → Blueprint** → connect your GitHub repo.
   Render reads `render.yaml` automatically.
2. When prompted, fill the secret env vars:
   - `DATABASE_URL` = your Neon string
   - `GROQ_API_KEY` = your Groq key
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
   - `CORS_ORIGINS` = (set after Step 5; your Vercel URL)
3. Deploy. Render installs the Python deps and starts the app.
4. Verify: open `https://<your-service>.onrender.com/health` → `{"status":"ok"}`.
   The start command runs `alembic upgrade head` on boot, so tables are created automatically.

## Step 5 — Frontend (Vercel)

1. Sign up at https://vercel.com → **Add New → Project** → import the repo.
2. Set **Root Directory** to `frontend`.
3. Add env var: `NEXT_PUBLIC_API_URL = https://<your-service>.onrender.com/api/v1`
4. Deploy → you get `https://<project>.vercel.app`.

## Step 6 — Connect them (CORS)

1. Back in Render, set `CORS_ORIGINS = https://<project>.vercel.app` (your real Vercel URL).
2. Save → Render redeploys.
3. Open the Vercel URL, register, and run the full flow.

---

## Notes & limitations (good to know)

- **Render free tier sleeps** after 15 min idle → first request after that takes ~30s to wake. Normal for free hosting.
- **Selenium execution is local-only on free hosting.** The native Python runtime has no Chrome, so clicking "Run Tests" on the deployed site marks tests as failed with a clear message. Run executions locally for the demo. To run them in the cloud, deploy the backend with a Chrome-equipped Docker image (or a paid runner) instead.
- **Groq is much faster than local Ollama** — test generation that took ~60s locally is near-instant in production.
- Secrets are never committed — they live only in the Render/Vercel dashboards.
