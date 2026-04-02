# AI DevOps Agent

A production-ready DevOps showcase project demonstrating AI integration with modern CI/CD pipelines. Built with Rust, Docker, GitHub Actions, and Groq AI.

[![CI](https://github.com/soumeet96/ai-devops-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/soumeet96/ai-devops-agent/actions/workflows/ci.yml)
[![Deploy](https://github.com/soumeet96/ai-devops-agent/actions/workflows/deploy.yml/badge.svg)](https://github.com/soumeet96/ai-devops-agent/actions/workflows/deploy.yml)

---

## What This Project Demonstrates

| Skill | Implementation |
|---|---|
| **Containerization** | Multi-stage Dockerfile — Rust builder → minimal Debian runtime |
| **CI/CD Pipeline** | GitHub Actions: build → test → push Docker image to GHCR |
| **Cloud Deployment** | Auto-deploy to Render.com on every push to main |
| **AI Integration** | PR review bot using Groq (Llama 3.3 70B) — posts AI review as PR comment |
| **Infrastructure as Code** | `render.yaml` for declarative deployment config |
| **API Design** | REST + SSE server in Rust (Axum) with session management |

---

## Architecture

```
GitHub Push / PR
      │
      ▼
┌─────────────────────────────────────────────┐
│           GitHub Actions                     │
│                                              │
│  ci.yml ──────────────────────────────────► │
│   ├─ cargo check + cargo test               │
│   ├─ docker build                           │
│   └─ push → ghcr.io/soumeet96/ai-devops-agent│
│                                              │
│  deploy.yml (on CI success)                 │
│   └─ curl RENDER_DEPLOY_HOOK_URL ──────────►│
│                                              │
│  pr-ai-review.yml (on PR open/update)       │
│   ├─ git diff → /tmp/pr_diff.txt           │
│   ├─ python3 scripts/ai_review.py           │
│   │    └─ Groq API (Llama 3.3 70B)         │
│   └─ post review comment on PR             │
└─────────────────────────────────────────────┘
      │                         │
      ▼                         ▼
 Render.com               PR Comment
 (Live REST API)          (AI Review)
```

---

## Live Service

The `claw-server` is a Rust/Axum REST API with Server-Sent Events for real-time session streaming.

**Endpoints:**

| Method | Path | Description |
|---|---|---|
| `POST` | `/sessions` | Create a new session |
| `GET` | `/sessions` | List all sessions |
| `GET` | `/sessions/{id}` | Get session details |
| `POST` | `/sessions/{id}/message` | Send a message to a session |
| `GET` | `/sessions/{id}/events` | Stream session events (SSE) |

---

## Running Locally

**Prerequisites:** Docker, or Rust 1.87+

### With Docker
```bash
docker compose up --build
# Server available at http://localhost:3000
curl http://localhost:3000/sessions
```

### With Cargo
```bash
cd rust
cargo build --release -p claw-server-bin
../target/release/claw-server
```

---

## AI PR Review Bot

Every pull request automatically gets an AI-powered code review posted as a comment.

The bot:
1. Gets the full PR diff
2. Sends it to **Llama 3.3 70B** via Groq API
3. Returns a structured review covering security, DevOps concerns, and code quality
4. Posts the review as a PR comment

**Required GitHub Secrets:**
- `GROQ_API_KEY` — free from [console.groq.com](https://console.groq.com)
- `RENDER_DEPLOY_HOOK_URL` — from Render dashboard → your service → Settings → Deploy Hook
- `RENDER_SERVICE_URL` — your Render app URL (e.g. `https://ai-devops-agent.onrender.com`)

---

## Tech Stack

- **Language:** Rust (edition 2021, safe-only — `unsafe_code = "forbid"`)
- **Web Framework:** Axum 0.8 with async/await (Tokio)
- **Containerization:** Docker (multi-stage build)
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry (GHCR)
- **Deployment:** Render.com (free tier)
- **AI Model:** Llama 3.3 70B via Groq API (free tier)

---

## Project Structure

```
ai-devops-agent/
├── rust/
│   └── crates/
│       ├── server/          # REST + SSE API library (Axum)
│       ├── claw-server-bin/ # Binary wrapper — runs the server
│       ├── runtime/         # Session state & conversation management
│       └── ...              # api, tools, commands, plugins, lsp
├── .github/workflows/
│   ├── ci.yml               # Build, test, push to GHCR
│   ├── deploy.yml           # Deploy to Render on main push
│   └── pr-ai-review.yml     # AI PR review bot
├── scripts/
│   └── ai_review.py         # Groq API integration (pure Python, no deps)
├── Dockerfile               # Multi-stage Rust build
├── docker-compose.yml       # Local development
└── render.yaml              # Render.com IaC config
```

---

## Author

**Soumeet Acharya** — [github.com/soumeet96](https://github.com/soumeet96)

Built as a DevOps + AI integration showcase. The Rust server core is based on the MIT-licensed [claw-code](https://github.com/instructkr/claw-code) project.
