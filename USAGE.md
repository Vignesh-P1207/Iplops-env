# IPLOps-Env Usage Guide

Complete guide for using the Indian Premier League Operations Environment.

## Installation

### Option 1: Docker (Recommended)

```bash
# Build the image
docker build -t iplops-env .

# Run the container
docker run -p 8000:8000 iplops-env
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app/main.py
```

The server will start on `http://localhost:8000`

## Quick Start

### 1. Test the Server

```bash
# Health check
curl http://localhost:8000/health

# Get environment info
curl http://localhost:8000/
```

### 2. Run Example Agent

```bash
# Test all tasks
python test_agent.py

# Run inference on specific task
python inference.py 1  # Task 1
python inference.py 2  # Task 2
python inference.py 3  # Task 3
```

## API Reference

### POST /reset

Initialize a new task episode.

**Request:**
```json
{
  "task_id": 1
}
```

**Response:**
```json
{
  "observation": {
    "task_id": 1,
    "task_type": "staff_allocation",
    "data": { ... },
    "timestamp": "2026-04-06T10:30:00"
  },
  "info": {
    "message": "Task 1 initialized successfully",
    "task_type": "staff_allocation"
  }
}
```

### POST /step

Submit an action and receive reward.

**Request:**
```json
{
  "action": {
    "security_per_gate": 5,
    "total_security": 80,
    "medical_personnel": 35,
    "ticketing_staff": 20
  }
}
```

**Response:**
```json
{
  "observation": { ... },
  "reward": 0.875,
  "done": true,
  "info": {
    "grading_details": { ... },
    "message": "Task completed successfully"
  }
}
```

### GET /observation

Get current observation without taking action.

**Response:**
```json
{
  "task_id": 1,
  "task_type": "staff_allocation",
  "data": { ... },
  "timestamp": "2026-04-06T10:30:00"
}
```

## Task Details

### Task 1: Staff Allocation (Easy)

**Objective:** Allocate security, medical, and ticketing staff for an IPL match.

**Input:**
- Stadium information (capacity, gates, medical stations)
- Expected crowd percentage
- Match type (league/playoff/final)

**Output:**
```json
{
  "security_per_gate": 5,
  "total_security": 80,
  "medical_personnel": 35,
  "ticketing_staff": 20,
  "reasoning": "Explanation of allocation"
}
```

**Scoring:**
- Security accuracy: 35%
- Medical accuracy: 25%
- Ticketing accuracy: 20%
- No overstaffing: 10%
- No understaffing: 10%

**Tips:**
- League matches: 2.5 security per 1000 people
- Playoff matches: 3.5 security per 1000 people
- Final matches: 5.0 security per 1000 people
- Medical: 1.5 per 1000 people
- Ticketing: 0.8 per 1000 people

---

### Task 2: Playing XI Selection (Medium)

**Objective:** Select best 11 players from 20-player squad.

**Input:**
- Squad of 20 players with detailed stats
- Pitch report (surface type, bounce, match time)
- Opponent profile (weaknesses, top batsmen)

**Output:**
```json
{
  "playing_xi": ["Player 1", "Player 2", ...],
  "batting_order": ["Player 1", "Player 2", ...],
  "bowling_combination": {
    "pacers": ["Player A", "Player B"],
    "spinners": ["Player C"],
    "death_overs_specialist": "Player A"
  },
  "reasoning": {
    "pitch_strategy": "Why this XI suits the pitch",
    "opponent_matchup": "How to exploit opponent weakness",
    "balance_justification": "Team balance explanation"
  }
}
```

**Scoring:**
- Team balance: 30%
  - Must have 1 wicket-keeper
  - 5-6 specialist batsmen
  - 4-5 bowlers (at least 2 pacers, 1 spinner)
  - At least 2 all-rounders
- Pitch condition fit: 40%
  - Spin-friendly → more spinners
  - Pace-friendly → more pacers
  - Balanced → mixed attack
- Opponent matchup: 30%
  - Exploit opponent weaknesses
  - Counter their strengths

**Tips:**
- Check `recent_form` scores (0-100)
- Match bowling attack to pitch type
- Consider opponent's `weakness_against` field
- Balance batting depth with bowling variety

---

### Task 3: Crisis Management (Hard)

**Objective:** Handle 5 simultaneous crises during a live match.

**Input:**
- Match context (score, crowd, time, match type)
- 5 crisis events:
  1. Weather (rain/dew)
  2. Player injury
  3. Crowd safety incident
  4. Tech failure
  5. Regulatory issue

**Output:**
```json
{
  "priority_order": [
    {"rank": 1, "crisis": "crowd_safety", "reason": "Life-threatening"},
    {"rank": 2, "crisis": "injury", "reason": "Player health"},
    ...
  ],
  "decisions": {
    "crowd_safety": {
      "action": "deploy_riot_squad",
      "details": { ... },
      "timeline_minutes": 2.0
    },
    ...
  },
  "timeline": {
    "0-2_mins": ["Action 1", "Action 2"],
    "2-5_mins": ["Action 3"],
    ...
  },
  "risk_assessment": {
    "if_wrong_priority": "Consequences of wrong prioritization",
    "cascading_failures": "How crises affect each other"
  }
}
```

**Scoring:**
- Priority ordering: 35%
  - **CRITICAL:** Crowd safety MUST be #1 (auto-fail if not)
  - Correct order: Crowd → Injury → Weather → Regulatory → Tech
- Decision quality: 40%
  - Valid actions for each crisis
  - Proper resource allocation
  - Stakeholder communication
- Operational feasibility: 25%
  - Realistic timeline
  - No resource conflicts
  - Contingency planning

**Tips:**
- Life safety always comes first
- Time-sensitive crises have deadlines
- Decisions are interdependent
- Consider stakeholder conflicts (BCCI vs. broadcast vs. safety)

## Example Agent Implementation

```python
import requests

class MyAgent:
    def __init__(self):
        self.base_url = "http://localhost:8000"
    
    def run_task(self, task_id):
        # Reset
        response = requests.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id}
        )
        observation = response.json()["observation"]
        
        # Your logic here
        action = self.solve(observation)
        
        # Submit
        response = requests.post(
            f"{self.base_url}/step",
            json={"action": action}
        )
        return response.json()["reward"]
```

## Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify Python version (3.11+)
- Install all dependencies: `pip install -r requirements.txt`

### Connection refused
- Make sure server is running: `python app/main.py`
- Check firewall settings
- Verify URL: `http://localhost:8000`

### Low scores
- Read task-specific tips above
- Check grading breakdown in response
- Review example agent in `test_agent.py`

## Advanced Usage

### Custom Scenarios

Modify task generators in `app/tasks/` to create custom scenarios:
- `task1_staffing.py` - Add new stadiums or safety ratios
- `task2_selection.py` - Add real IPL 2026 squads when available
- `task3_crisis.py` - Create new crisis templates

### Custom Grading

Modify graders in `app/graders/` to adjust scoring:
- `grader1.py` - Change tolerance thresholds
- `grader2.py` - Adjust component weights
- `grader3.py` - Add new decision quality checks

## Performance Benchmarks

| Task | Random Agent | Rule-Based | Good Agent | Expert Agent |
|------|-------------|------------|------------|--------------|
| Task 1 | 0.3-0.5 | 0.7-0.8 | 0.85-0.95 | 0.95+ |
| Task 2 | 0.2-0.4 | 0.6-0.7 | 0.75-0.85 | 0.90+ |
| Task 3 | 0.1-0.3 | 0.5-0.6 | 0.70-0.80 | 0.85+ |

## Support

For issues or questions:
1. Check this guide
2. Review example code in `test_agent.py`
3. Check API responses for error messages
4. Review grading breakdown for improvement areas
