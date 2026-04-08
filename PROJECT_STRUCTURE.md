# IPLOps-Env Project Structure

```
iplops-env/
│
├── README.md                    # Project overview and quick start
├── USAGE.md                     # Comprehensive usage guide
├── PROJECT_STRUCTURE.md         # This file
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container configuration
├── openenv.yaml                 # OpenEnv specification
├── .gitignore                   # Git ignore rules
│
├── inference.py                 # Example inference script for hackathon
├── test_agent.py               # Comprehensive test suite
│
└── app/                        # Main application package
    ├── main.py                 # FastAPI server (entry point)
    ├── env.py                  # Core environment logic
    ├── models.py               # Pydantic data models
    │
    ├── tasks/                  # Task generators
    │   ├── task1_staffing.py   # Staff allocation scenarios
    │   ├── task2_selection.py  # Playing XI selection scenarios
    │   └── task3_crisis.py     # Crisis management scenarios
    │
    └── graders/                # Scoring systems
        ├── grader1.py          # Staff allocation grader
        ├── grader2.py          # Playing XI grader
        └── grader3.py          # Crisis management grader
```

## File Descriptions

### Root Level

**README.md**
- Project overview
- Quick start guide
- Task descriptions
- Tech stack
- Basic usage

**USAGE.md**
- Detailed API reference
- Task-specific guides
- Example implementations
- Troubleshooting
- Performance benchmarks

**requirements.txt**
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pydantic 2.5.3
- Requests 2.31.0
- Python-dotenv 1.0.0
- NumPy 1.26.3

**Dockerfile**
- Python 3.11-slim base
- Port 8000 exposed
- Uvicorn server

**openenv.yaml**
- Environment metadata
- Task definitions
- API endpoints
- Scoring configuration

**inference.py**
- Example agent implementation
- CLI interface for testing
- Demonstrates all 3 tasks
- Ready for hackathon submission

**test_agent.py**
- Comprehensive test suite
- Tests all 3 tasks
- Displays detailed results
- Validates environment

### app/ Package

**main.py** (FastAPI Server)
- REST API endpoints
- CORS middleware
- Error handling
- Health checks

Endpoints:
- `GET /` - Environment info
- `GET /health` - Health check
- `POST /reset` - Initialize task
- `POST /step` - Submit action
- `GET /observation` - Get current state

**env.py** (Environment Core)
- `IPLOpsEnvironment` class
- Task orchestration
- Observation management
- Reward calculation

Key methods:
- `reset(task_id)` - Initialize new episode
- `step(action)` - Execute action, return reward
- `get_observation()` - Get current state

**models.py** (Data Models)
All Pydantic models for type safety:

Task 1:
- `StadiumInfo`
- `StaffAllocationAction`

Task 2:
- `PlayerStats`
- `PitchReport`
- `OpponentProfile`
- `PlayingXIAction`

Task 3:
- `CrisisEvent`
- `CrisisPriority`
- `CrisisDecision`
- `CrisisManagementAction`

Environment:
- `Observation`
- `ResetRequest/Response`
- `StepRequest/Response`

### app/tasks/ Package

**task1_staffing.py**
- `StaffAllocationTask` class
- 8 real IPL stadiums
- Safety ratio calculations
- Scenario generation

Features:
- Random stadium selection
- Match type variation
- Crowd percentage simulation
- Optimal allocation calculation

**task2_selection.py**
- `PlayingXITask` class
- 2 IPL squads (Mumbai Indians, Chennai Super Kings)
- 20 players per squad with realistic stats
- Pitch condition variations
- Opponent profile generation

Features:
- Real player stats (batting avg, strike rate, economy, etc.)
- 6 pitch condition types
- Opponent weakness simulation
- Recent form tracking

**task3_crisis.py**
- `CrisisManagementTask` class
- 5 crisis types with multiple templates
- Match context generation
- Time-sensitive scenarios

Crisis Types:
1. Weather (rain, dew)
2. Injury (player health)
3. Crowd Safety (fights, overcrowding)
4. Tech Failure (LED, floodlights)
5. Regulatory (over-rate, DRS)

### app/graders/ Package

**grader1.py**
- `StaffAllocationGrader` class
- Tolerance-based scoring
- Deviation calculation
- Overstaffing/understaffing penalties

Weights:
- Security accuracy: 35%
- Medical accuracy: 25%
- Ticketing accuracy: 20%
- No overstaffing: 10%
- No understaffing: 10%

**grader2.py**
- `PlayingXIGrader` class
- Multi-component scoring
- Team balance validation
- Pitch fit analysis
- Opponent matchup evaluation

Weights:
- Team balance: 30%
- Pitch condition fit: 40%
- Opponent matchup: 30%

**grader3.py**
- `CrisisManagementGrader` class
- Priority order validation
- Decision quality assessment
- Operational feasibility check
- Critical failure detection

Weights:
- Priority ordering: 35%
- Decision quality: 40%
- Operational feasibility: 25%

## Data Flow

```
1. Agent calls POST /reset
   ↓
2. Environment generates scenario (task generator)
   ↓
3. Returns observation to agent
   ↓
4. Agent processes observation
   ↓
5. Agent calls POST /step with action
   ↓
6. Environment validates action
   ↓
7. Grader scores action
   ↓
8. Returns reward + breakdown to agent
```

## Key Design Decisions

### 1. Real IPL Context
- Actual stadium names and capacities
- Realistic player stats
- Authentic operational challenges
- India-focused scenarios

### 2. Progressive Difficulty
- Task 1: Deterministic calculations
- Task 2: Multi-factor optimization
- Task 3: Complex prioritization + interdependencies

### 3. Comprehensive Grading
- Weighted scoring
- Detailed breakdowns
- Actionable feedback
- Critical failure detection

### 4. Type Safety
- Pydantic models throughout
- Request/response validation
- Clear error messages
- IDE autocomplete support

### 5. Extensibility
- Modular task generators
- Pluggable graders
- Easy to add new scenarios
- Configurable weights

## Adding New Content

### New Stadium (Task 1)
Edit `app/tasks/task1_staffing.py`:
```python
STADIUMS = [
    {"name": "New Stadium", "capacity": 45000, "gates": 10, "medical_stations": 5},
    ...
]
```

### New IPL Squad (Task 2)
Edit `app/tasks/task2_selection.py`:
```python
IPL_SQUADS = {
    "New Team": [
        {"name": "Player", "role": "batsman", ...},
        ...
    ]
}
```

### New Crisis Type (Task 3)
Edit `app/tasks/task3_crisis.py`:
```python
CRISIS_TEMPLATES = {
    CrisisType.NEW_CRISIS: [
        {"description": "...", "severity": 80, ...}
    ]
}
```

## Performance Considerations

- Lightweight FastAPI server
- No database required
- Stateless design (except current episode)
- Fast response times (<100ms)
- Docker-ready for deployment

## Testing Strategy

1. Unit tests: Individual graders
2. Integration tests: Full task flow
3. End-to-end: `test_agent.py`
4. Inference: `inference.py`

## Future Enhancements

- [ ] Real-time API integration (ESPN/Crickbuzz)
- [ ] Historical match data
- [ ] Multi-episode learning support
- [ ] Leaderboard system
- [ ] Web UI for visualization
- [ ] More IPL teams (all 10)
- [ ] Player injury history
- [ ] Weather API integration
- [ ] Live match simulation
