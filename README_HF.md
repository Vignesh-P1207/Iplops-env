---
title: IPLOps-Env
emoji: 🏏
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
  - reinforcement-learning
  - cricket
  - ipl
  - operations
  - real-world
---

# IPLOps-Env - Indian Premier League Operations Environment

A production-grade OpenEnv environment simulating real-world IPL match operations for AI agent evaluation.

## 🎯 Environment Overview

IPLOps-Env models authentic operational challenges faced by IPL franchises, BCCI officials, and stadium operators. Agents must handle:

1. **Staff Allocation** (Easy) - Allocate security, medical, and ticketing staff
2. **Playing XI Selection** (Medium) - Select optimal team from 20-player squad  
3. **Crisis Management** (Hard) - Handle 5 simultaneous match-day crises

## 📊 Action & Observation Spaces

### Task 1: Staff Allocation
**Observation:**
```json
{
  "stadium": {
    "name": "Wankhede Stadium",
    "capacity": 33000,
    "expected_crowd_percentage": 0.87,
    "match_type": "playoff",
    "gates_count": 8,
    "medical_stations": 4
  }
}
```

**Action:**
```json
{
  "security_per_gate": 12,
  "total_security": 100,
  "medical_personnel": 43,
  "ticketing_staff": 23
}
```

### Task 2: Playing XI Selection
**Observation:** Squad of 20 players with stats, pitch report, opponent analysis

**Action:** 11 players, batting order, bowling combination

### Task 3: Crisis Management
**Observation:** 5 simultaneous crises (weather, injury, crowd, tech, regulatory)

**Action:** Priority order, decisions, timeline, risk assessment

## 🚀 Quick Start

### Using the API

```python
import requests

# Reset environment
response = requests.post("http://localhost:8000/reset", json={"task_id": 1})
observation = response.json()["observation"]

# Submit action
action = {
    "security_per_gate": 5,
    "total_security": 80,
    "medical_personnel": 35,
    "ticketing_staff": 20
}
response = requests.post("http://localhost:8000/step", json={"action": action})
score = response.json()["reward"]
```

### Running Inference

```bash
python inference.py 1  # Task 1
python inference.py 2  # Task 2
python inference.py 3  # Task 3
```

## 📈 Baseline Scores

| Task | Difficulty | Baseline Score | Success Threshold |
|------|-----------|----------------|-------------------|
| Task 1: Staff Allocation | Easy | 0.95 | 0.85 |
| Task 2: Playing XI | Medium | 0.85 | 0.75 |
| Task 3: Crisis Management | Hard | 0.75 | 0.70 |

## 🏗️ Setup Instructions

### Docker (Recommended)
```bash
docker build -t iplops-env .
docker run -p 8000:8000 iplops-env
```

### Local Development
```bash
pip install -r requirements.txt
python app/main.py
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **Complete Guide**: See [USAGE.md](USAGE.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)

## 🎓 Real-World Utility

This environment models genuine operational challenges:
- **Staff Allocation**: Used by stadium operators for 60+ IPL matches annually
- **Team Selection**: Mirrors actual franchise decision-making process
- **Crisis Management**: Based on real match-day incident protocols

## 🏆 OpenEnv Compliance

✅ Full OpenEnv spec implementation  
✅ Typed Pydantic models  
✅ step() / reset() / state() API  
✅ 3 tasks with programmatic graders  
✅ Meaningful reward function with partial credit  
✅ Baseline inference script  
✅ Docker deployment  
✅ Comprehensive documentation

## 📊 Scoring System

### Task 1: Staff Allocation
- Security accuracy: 35%
- Medical accuracy: 25%
- Ticketing accuracy: 20%
- No overstaffing: 10%
- No understaffing: 10%

### Task 2: Playing XI Selection
- Team balance: 30%
- Pitch condition fit: 40%
- Opponent matchup: 30%

### Task 3: Crisis Management
- Priority ordering: 35% (crowd safety must be #1)
- Decision quality: 40%
- Operational feasibility: 25%

## 🔧 Environment Variables

```bash
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4
OPENAI_API_KEY=your_key_here
ENV_BASE_URL=http://localhost:8000
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is an OpenEnv hackathon submission. For extending the environment, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md).

---

**Built for OpenEnv Hackathon** | **Real-world IPL Operations** | **Production-Ready**
