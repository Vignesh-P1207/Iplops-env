# IPLOps-Env 🏏

**OpenEnv-compliant IPL Operations Management Environment for AI Agents**

A comprehensive environment for training and evaluating AI agents on real-world IPL (Indian Premier League) cricket operations management tasks.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compliant-green)](https://github.com/openenv)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Overview

IPLOps-Env provides three challenging tasks for AI agents to solve:

1. **Task 1: Staff Allocation** (Easy) - Optimize match day staffing
2. **Task 2: Playing XI Selection** (Medium) - Select optimal cricket team with AI/GPT-4
3. **Task 3: Crisis Management** (Hard) - Handle multiple simultaneous match crises

## ✨ Features

- ✅ **OpenEnv Compliant** - Standard API for agent evaluation
- 🤖 **GPT-4 Integration** - Optional AI-powered team selection
- 📊 **Real IPL Data** - Dynamic squad generation with form variations
- 🏟️ **14 IPL Stadiums** - Detailed pitch reports and characteristics
- 🎯 **Sophisticated Grading** - Multi-criteria evaluation system
- 🐳 **Docker Support** - Easy deployment
- 📝 **Comprehensive Docs** - 15+ markdown documentation files

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/iplops-env.git
cd iplops-env

# Install dependencies
pip install -r requirements.txt

# Start server
python app/main.py
```

Server runs at `http://localhost:8000`

### Test All Tasks

```bash
# Run comprehensive test suite
python test_all_tasks_terminal.py

# Or test individual tasks
python inference.py 1  # Task 1
python inference.py 2  # Task 2
python inference.py 3  # Task 3
```

## 📋 Tasks

### Task 1: Staff Allocation

Optimize staffing for match day operations based on:
- Stadium capacity and expected crowd
- Match type (league/playoff/final)
- Security, medical, and ticketing requirements

**Score**: 1.000 (Perfect allocation possible)

```bash
python demo_task1.py
```

### Task 2: Playing XI Selection

Select optimal cricket team considering:
- Player form, stats, and fitness
- Pitch conditions (spin/pace/batting-friendly)
- Opponent weaknesses
- Minimum 5 bowling options

**Score**: 0.930 (Excellent team selection)

```bash
python run_task2_mi_vs_csk.py
```

**GPT-4 Integration** (Optional):
```bash
export OPENAI_API_KEY="sk-..."
python app/main.py
# AI will use GPT-4 for intelligent team selection
```

### Task 3: Crisis Management

Handle multiple simultaneous crises:
- Crowd safety incidents
- Player injuries
- Weather delays
- Regulatory issues
- Technical failures

**Score**: 0.720 (Good crisis management)

```bash
python run_task3_demo.py
```

## 🤖 AI Agent Integration

### Basic Agent

```python
import requests

# Reset environment
response = requests.post("http://localhost:8000/reset", json={"task_id": 2})
observation = response.json()["observation"]

# Make decision
action = {
    "playing_xi": ["Player 1", "Player 2", ...],
    "batting_order": [...],
    "bowling_combination": {...}
}

# Submit action
response = requests.post("http://localhost:8000/step", json={"action": action})
result = response.json()
score = result["reward"]
```

### GPT-4 Agent (Task 2)

```python
from app.team_selector import IntelligentTeamSelector

selector = IntelligentTeamSelector()
result = selector.select_playing_xi(squad, pitch_report, opponent_profile)

# Returns:
# - selected_players: List of 11 players
# - batting_order: Optimal batting lineup
# - bowling_plan: Bowling strategy
# - reasoning: AI explanation
# - selection_method: "GPT-4 AI" or "Algorithmic"
```

### Advanced Crisis Agent (Task 3)

```python
from app.prompts import TASK3_SYSTEM_PROMPT, format_task3_prompt

# Use structured prompts with GPT-4
user_prompt = format_task3_prompt(observation)
# Send to GPT-4 for intelligent crisis triage
```

## 📊 API Endpoints

- `POST /reset` - Reset environment with task_id
- `POST /step` - Submit action and get reward
- `GET /observation` - Get current observation
- `GET /health` - Health check
- `GET /api/ipl/teams` - List IPL teams
- `GET /api/ipl/squad/{team}` - Get team squad
- `GET /api/ipl/pitch/{venue}` - Get pitch report
- `POST /api/ipl/select-team` - AI team selection

Full API docs: `http://localhost:8000/docs`

## 🏗️ Architecture

```
iplops-env/
├── app/
│   ├── main.py              # FastAPI server
│   ├── env.py               # Environment logic
│   ├── models.py            # Pydantic models
│   ├── team_selector.py     # GPT-4 team selection
│   ├── tasks/               # Task implementations
│   ├── graders/             # Scoring systems
│   ├── prompts/             # AI prompts (Task 3)
│   └── api_clients.py       # IPL data aggregation
├── static/                  # Web UI (optional)
├── inference.py             # OpenEnv agent
├── test_all_tasks_terminal.py  # Test suite
└── requirements.txt
```

## 🧪 Testing

```bash
# All tasks
python test_all_tasks_terminal.py

# Individual demos
python demo_task1.py
python run_task2_mi_vs_csk.py
python run_task3_demo.py

# GPT-4 integration test
python test_gpt4_integration.py

# Advanced Task 3 agent
python advanced_agent_task3.py
```

## 📈 Performance

| Task | Score | Status |
|------|-------|--------|
| Task 1: Staff Allocation | 1.000 | ✅ Perfect |
| Task 2: Playing XI Selection | 0.930 | ✅ Excellent |
| Task 3: Crisis Management | 0.720 | ✅ Good |

All tasks exceed 0.7 success threshold.

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI GPT-4 (optional, for Task 2)
export OPENAI_API_KEY="sk-..."
export MODEL_NAME="gpt-4"  # default

# Hugging Face (alternative)
export HF_TOKEN="hf_..."
export API_BASE_URL="https://api-inference.huggingface.co/..."

# Server
export ENV_BASE_URL="http://localhost:8000"
```

### Docker

```bash
docker build -t iplops-env .
docker run -p 8000:8000 iplops-env
```

## 📚 Documentation

- `README.md` - Main documentation
- `API_DOCS.md` - API reference
- `TERMINAL_READY.md` - Terminal/API usage
- `GPT4_INTEGRATION.md` - GPT-4 setup guide
- `TASK2_GUIDE.md` - Task 2 detailed guide
- `ARCHITECTURE.md` - System architecture
- `DEPLOYMENT_CHECKLIST.md` - Deployment guide

## 🎓 Use Cases

- **AI Research**: Train agents on complex decision-making
- **Cricket Analytics**: Optimize team selection strategies
- **Operations Management**: Learn crisis handling
- **Education**: Teach AI planning and reasoning
- **Hackathons**: OpenEnv competition environment

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- OpenEnv framework
- IPL cricket data
- FastAPI framework
- OpenAI GPT-4

## 📞 Contact

- GitHub Issues: [Report bugs](https://github.com/YOUR_USERNAME/iplops-env/issues)
- Documentation: See `/docs` folder

## 🌟 Star History

If you find this project useful, please star it on GitHub!

---

**Built for OpenEnv Hackathon** | **Ready for Production** | **AI-Powered**
