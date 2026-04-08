---
title: IPLOps Env
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

<div align="center">

<img src="https://img.shields.io/badge/🏏_IPLOps--Env-v1.0.0-1a1a2e?style=for-the-badge&labelColor=ff6b35" alt="IPLOps-Env" />

<br/><br/>

<img src="https://img.shields.io/badge/OpenEnv-Compliant-00c896?style=flat-square&logo=checkmarx&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />

<br/><br/>

**An AI agent evaluation environment built around the operational reality of running an IPL match.**

*Not a toy. Not a benchmark dressed up in cricket clothes.*

<br/>

<img src="https://img.shields.io/badge/Task%201-Staff%20Allocation-4CAF50?style=for-the-badge" />
<img src="https://img.shields.io/badge/Task%202-Playing%20XI-FF9800?style=for-the-badge" />
<img src="https://img.shields.io/badge/Task%203-Crisis%20Management-F44336?style=for-the-badge" />

</div>

---

## Why This Exists

Most agent benchmarks test things that don't matter outside the benchmark. IPLOps-Env is different. The Indian Premier League runs 74 matches a season across 10 cities. Each match involves 50,000+ fans, 22 players, dozens of officials, and an operations team making hundreds of calls in real time. Get the team selection wrong and you lose a match. Get the crowd management wrong and people get hurt.

This environment puts an AI agent in that seat and asks: *can it make the right call?*

---

## The Three Tasks

### 🟢 Task 1 — Match Day Staff Allocation `Easy`

A stadium with 60,000 seats, 12 entry gates, and a match starting in 3 hours. Allocate security, medical, and ticketing staff correctly. The scoring penalises both overstaffing (budget waste) and understaffing (safety failure). There's an optimal band — find it.

```
Scored on: security accuracy (35%) · medical ratio (25%) · ticketing coverage (20%) · efficiency (20%)
```

### 🟡 Task 2 — Playing XI Selection `Medium`

Pick 11 players from a 20-man squad. The pitch is spin-friendly. The opponent's top order collapses against pace. You have three all-rounders and only one genuine wicket-keeper. Who plays?

The grader doesn't reward guesses. It rewards coherent decisions — team balance, pitch adaptation, and opponent exploitation all measured independently, then weighted.

```
Scored on: team balance (30%) · pitch fit (40%) · opponent matchup (30%)
```

> **What makes this hard:** The grader enforces a minimum of 5 bowling options, requires exactly 1 wicket-keeper, and detects spinner/pacer type using a `bowling_type` field with economy-rate fallback. An agent that ignores pitch conditions scores ~0.5. An agent that reads the scenario and adapts scores 0.85+.

### 🔴 Task 3 — Live Crisis Management `Hard`

It's the 14th over. Five things go wrong at once: a crowd incident in Stand C, a player injury on the field, rain clouds building, a DRS tech failure, and a regulatory compliance deadline expiring. Rank the crises. Make the calls. The grader auto-fails any response that doesn't put life safety first.

```
Scored on: priority ordering (35%) · decision quality (40%) · operational feasibility (25%)
```

---

## Scoring

All tasks return a continuous score in `[0.0, 1.0]`. Partial credit throughout — designed to give agents useful gradient signal, not just pass/fail.

| Task | Random Agent | Rule-Based | Optimised |
|------|:-----------:|:----------:|:---------:|
| Staff Allocation | 0.35 | 0.75 | **0.95+** |
| Playing XI Selection | 0.25 | 0.65 | **0.85+** |
| Crisis Management | 0.15 | 0.55 | **0.80+** |

---

## Quickstart

<img src="https://img.shields.io/badge/Docker-Recommended-2496ED?style=flat-square&logo=docker&logoColor=white" />

```bash
docker build -t iplops-env .
docker run -p 8000:8000 \
  -e API_BASE_URL="https://api.openai.com/v1" \
  -e MODEL_NAME="gpt-4o-mini" \
  -e HF_TOKEN="your_token" \
  iplops-env
```

<img src="https://img.shields.io/badge/Local-Python%203.11-3776AB?style=flat-square&logo=python&logoColor=white" />

```bash
pip install -r requirements.txt
python app/main.py
```

Server starts at `http://localhost:8000` — interactive docs at `/docs`.

---

## Running the Baseline Agent

```bash
# All three tasks — used for hackathon baseline evaluation
python inference.py

# Single task
python inference.py 2
```

Output follows the OpenEnv structured log format:

```json
{"type": "START", "task": "playing_xi_selection", "env": "iplops-env", "model": "gpt-4o-mini"}
{"type": "STEP",  "step": 1, "action": {...}, "reward": 0.847, "done": true,  "error": null}
{"type": "END",   "success": true, "steps": 1, "score": 0.847, "total_reward": 0.847}
```

---

## API Reference

<img src="https://img.shields.io/badge/REST-API-009688?style=flat-square&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Swagger-Docs%20at%20%2Fdocs-85EA2D?style=flat-square&logo=swagger&logoColor=black" />

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `POST` | `/reset` | Initialise a task. Body: `{"task_id": 1\|2\|3}` |
| `POST` | `/step` | Submit an action. Body: `{"action": {...}}` |
| `GET` | `/observation` | Current observation (no action taken) |
| `GET` | `/state` | Full environment state |
| `GET` | `/health` | Health check — returns `{"status": "healthy"}` |
| `GET` | `/docs` | Interactive Swagger UI |

**Reset**
```bash
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": 2}'
```

**Submit action (Task 2)**
```bash
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "playing_xi": ["Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", "..."],
      "batting_order": ["Rohit Sharma", "Ishan Kishan", "..."],
      "bowling_combination": {
        "pacers": ["Jasprit Bumrah", "Jason Behrendorff"],
        "spinners": ["Piyush Chawla"],
        "death_overs_specialist": "Jasprit Bumrah"
      }
    }
  }'
```

---

## Project Structure

```
iplops-env/
│
├── app/
│   ├── main.py                  # FastAPI server — all endpoints
│   ├── env.py                   # Core environment: reset(), step(), state()
│   ├── models.py                # Pydantic request/response models
│   ├── api_clients.py           # IPL data (ESPN, Crickbuzz, static fallback)
│   ├── team_selector.py         # Algorithmic + GPT-powered XI selection
│   ├── scraper.py               # Dynamic squad data generation
│   ├── stadium_data.py          # 8 IPL venues with real capacities
│   │
│   ├── tasks/
│   │   ├── task1_staffing.py    # Scenario generator — staff allocation
│   │   ├── task2_selection.py   # Scenario generator — Playing XI
│   │   └── task3_crisis.py      # Scenario generator — live crises
│   │
│   └── graders/
│       ├── grader1.py           # Staff allocation scorer
│       ├── grader2.py           # Playing XI scorer (pitch-aware, type-safe)
│       └── grader3.py           # Crisis management scorer
│
├── static/
│   ├── index.html               # Task 1 web UI
│   └── task2.html               # Task 2 interactive player selector
│
├── inference.py                 # Baseline agent — all 3 tasks
├── openenv.yaml                 # OpenEnv specification
├── Dockerfile                   # Container — binds 0.0.0.0:8000
└── requirements.txt
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | LLM API endpoint | `https://api.openai.com/v1` |
| `MODEL_NAME` | Model identifier | `gpt-4o-mini` |
| `HF_TOKEN` | Hugging Face / API key | — |
| `ENV_BASE_URL` | Where inference hits the env | `http://localhost:8000` |

The server runs without any of these set. They're only consumed by `inference.py` when making LLM calls.

---

## Data & Squad Coverage

<img src="https://img.shields.io/badge/Teams-10%20IPL%20Franchises-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Players-20%20per%20squad-orange?style=flat-square" />
<img src="https://img.shields.io/badge/Venues-8%20IPL%20Stadiums-purple?style=flat-square" />
<img src="https://img.shields.io/badge/Data-Offline%20Fallback-green?style=flat-square" />

Squad data for all 10 IPL teams is bundled with realistic 2026 stats — batting average, strike rate, bowling economy, recent form, and a `bowling_type` field (`"pace"` or `"spin"`) for accurate grader classification. When ESPN Cricinfo or Crickbuzz API keys are provided, the environment upgrades to live data automatically. The fallback is seamless — no functionality is lost offline.

---

## OpenEnv Compliance

<img src="https://img.shields.io/badge/openenv%20validate-passing-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/graders-deterministic%20%26%20reproducible-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/score%20range-0.0%20%E2%86%92%201.0-brightgreen?style=flat-square" />

- `openenv.yaml` specifies tasks, scoring weights, action/observation spaces, and deployment config
- All graders return `float` in `[0.0, 1.0]` — deterministic and reproducible
- `reset()` produces clean state with zero bleed between episodes
- `step()` is single-action per episode, matching the real-world decision structure
- Docker image exposes and binds to port `8000` on `0.0.0.0`

---

## Tech Stack

<div align="center">

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" />
<img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />

</div>

---

## Deploy to Hugging Face Spaces

<img src="https://img.shields.io/badge/Deploy-Hugging%20Face%20Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black" />

1. Create a new Space with **Docker** SDK at `huggingface.co/new-space`
2. Push this repository or upload files via the Files tab
3. Add `HF_TOKEN`, `MODEL_NAME`, `API_BASE_URL` as Space secrets
4. Wait for build (~2 min) — your env will be live at `https://YOUR_USERNAME-iplops-env.hf.space`

```bash
# Verify it's running
curl https://YOUR_USERNAME-iplops-env.hf.space/health
```

---

<div align="center">

<img src="https://img.shields.io/badge/Built%20for-Meta%20OpenEnv%20Hackathon%202026-1877F2?style=flat-square&logo=meta&logoColor=white" />
<img src="https://img.shields.io/badge/Domain-Sports%20Operations%20%2F%20Cricket-ff6b35?style=flat-square" />
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />

*IPLOps-Env — where AI meets match day.*

</div>