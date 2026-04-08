# IPLOps-Env - Indian Premier League Operations Environment

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade AI agent evaluation environment for IPL match operations, built for the OpenEnv Hackathon.

## 🏏 What is IPLOps-Env?

IPLOps-Env simulates **real-world operational challenges** faced by IPL franchises, BCCI officials, and stadium operators. Agents are evaluated on three progressively complex tasks using authentic IPL context.

### Why IPL Operations?

- **Cultural Relevance**: IPL is India's biggest sporting event
- **Real Problems**: Actual challenges faced by operations teams
- **Judge Appeal**: Indian engineers deeply understand the context
- **Complexity Range**: From simple staffing to complex crisis management

## 🎯 The Three Tasks

### Task 1: Match Day Staff Allocation (Easy)
Allocate security, medical, and ticketing staff for IPL matches.

**Input**: Stadium capacity, crowd %, match type  
**Output**: Staff allocation numbers  
**Score**: 0.0 - 1.0 based on safety ratios and resource optimization

### Task 2: Playing XI Selection (Medium)
Select the best 11 players from a 20-player squad based on pitch conditions and opponent analysis.

**Input**: Squad stats, pitch report, opponent analysis  
**Output**: Playing XI, batting order, bowling combination  
**Score**: 0.0 - 1.0 based on team balance, pitch fit, opponent matchup  
**UI**: http://localhost:8000/task2  
**Features**: Real IPL data integration with ESPN Cricinfo and Crickbuzz APIs

### Task 3: Live Crisis Management (Hard)
Handle 5 simultaneous crises during a live match.

**Input**: Weather, injury, crowd, tech, regulatory crises  
**Output**: Priority order, decisions, timeline, risk assessment  
**Score**: 0.0 - 1.0 based on priority, decisions, feasibility

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
docker build -t iplops-env .
docker run -p 8000:8000 iplops-env
```

### Option 2: Local Python
```bash
pip install -r requirements.txt
python app/main.py
```

### Test the Environment
```bash
# Run comprehensive test suite
python test_agent.py

# Run inference on specific task
python inference.py 1  # Task 1
python inference.py 2  # Task 2
python inference.py 3  # Task 3
```

## 📚 Documentation

**Start Here:**
- **[INDEX.md](INDEX.md)** - Complete documentation index
- **[SUMMARY.md](SUMMARY.md)** - Project summary

**For Users:**
- **[USAGE.md](USAGE.md)** - Comprehensive usage guide
- **[API_DOCS.md](API_DOCS.md)** - Complete API reference

**For Developers:**
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization

**For Deployment:**
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Production deployment

**For Judges:**
- **[HACKATHON_SUBMISSION.md](HACKATHON_SUBMISSION.md)** - Submission overview

## 💻 Example Usage

```python
import requests

BASE_URL = "http://localhost:8000"

# Reset environment
response = requests.post(f"{BASE_URL}/reset", json={"task_id": 1})
observation = response.json()["observation"]

# Prepare action
action = {
    "security_per_gate": 5,
    "total_security": 80,
    "medical_personnel": 35,
    "ticketing_staff": 20
}

# Submit action
response = requests.post(f"{BASE_URL}/step", json={"action": action})
result = response.json()

print(f"Score: {result['reward']:.3f}")
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI REST API Server         │
│         (app/main.py)                   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Environment Core (app/env.py)      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │ Task 1 │  │ Task 2 │  │ Task 3 │
   └────────┘  └────────┘  └────────┘
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Grader 1│  │Grader 2│  │Grader 3│
   └────────┘  └────────┘  └────────┘
```

## 📊 Project Stats

- **Total Files**: 30
- **Lines of Code**: ~2,400 (Python)
- **Lines of Docs**: ~2,500 (Markdown)
- **IPL Stadiums**: 8 real stadiums
- **IPL Players**: 40 players (2 teams)
- **Crisis Types**: 5 types
- **API Endpoints**: 5 endpoints

## ✨ Key Features

✅ **Real IPL Context**
- 8 actual stadiums (Wankhede, Eden Gardens, etc.)
- 2 IPL squads with realistic player stats
- Authentic crisis scenarios

✅ **Progressive Difficulty**
- Easy: Deterministic calculations
- Medium: Multi-factor optimization
- Hard: Complex prioritization

✅ **Comprehensive Grading**
- Weighted scoring
- Detailed breakdowns
- Critical failure detection

✅ **Production Ready**
- Type-safe with Pydantic
- Docker containerized
- REST API with FastAPI
- Comprehensive error handling

✅ **Well Documented**
- 11 documentation files
- API reference
- Usage examples
- Architecture guide

## 🎮 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Environment info |
| `/health` | GET | Health check |
| `/reset` | POST | Initialize task |
| `/step` | POST | Submit action |
| `/observation` | GET | Get current state |

## 🧪 Testing

```bash
# Run all tests
python test_agent.py

# Run basic agent
python inference.py 1

# Run advanced agent
python example_custom_agent.py
```

## 📦 Tech Stack

- **Python 3.11**: Modern Python features
- **FastAPI**: High-performance REST API
- **Pydantic**: Type-safe data models
- **Uvicorn**: ASGI server
- **Docker**: Containerization
- **NumPy**: Numerical operations

## 🎯 Performance Targets

| Task | Good Score | Expert Score |
|------|-----------|--------------|
| Task 1 | 0.85+ | 0.95+ |
| Task 2 | 0.75+ | 0.90+ |
| Task 3 | 0.70+ | 0.85+ |

## 🚢 Deployment

See **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** for complete deployment guide.

```bash
# Build Docker image
docker build -t iplops-env .

# Run container
docker run -d -p 8000:8000 --name iplops iplops-env

# Check health
curl http://localhost:8000/health
```

## 🤝 Contributing

This is a hackathon submission. For extending the environment:

1. Read **[ARCHITECTURE.md](ARCHITECTURE.md)** (Extensibility Points)
2. Modify files in `app/tasks/` or `app/graders/`
3. Update documentation
4. Test thoroughly

## 📄 License

MIT License - see LICENSE file for details

## 🏆 Hackathon Submission

This project is submitted for the OpenEnv Hackathon.

**Key Highlights:**
- ✅ Complete implementation of 3 tasks
- ✅ Production-grade code quality
- ✅ Comprehensive documentation (2,500+ lines)
- ✅ Docker containerization
- ✅ Real IPL context and data
- ✅ Cultural relevance for Indian judges
- ✅ Extensible architecture

## 📞 Support

- **Documentation**: See [INDEX.md](INDEX.md) for complete documentation index
- **Examples**: Check `inference.py` and `example_custom_agent.py`
- **API Reference**: See [API_DOCS.md](API_DOCS.md)
- **Issues**: Review error messages and logs

## 🌟 What Makes This Special

1. **Real IPL Context**: Authentic stadiums, players, and scenarios
2. **Progressive Difficulty**: Easy → Medium → Hard
3. **Comprehensive Grading**: Multi-factor weighted scoring
4. **Production Quality**: Type-safe, documented, tested
5. **Cultural Relevance**: India-focused, judge-friendly
6. **Extensibility**: Easy to add more content
7. **Documentation**: 2,500+ lines of comprehensive docs
8. **Real-World Impact**: Actual operational problems

---

**Ready to deploy. Ready to test. Ready to win.** 🏆

For complete documentation, start with **[INDEX.md](INDEX.md)**
