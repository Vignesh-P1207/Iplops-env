# IPLOps-Env Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        IPLOps-Env                           │
│         Indian Premier League Operations Environment        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         FastAPI REST API Server         │
        │         (app/main.py)                   │
        │                                         │
        │  Endpoints:                             │
        │  • GET  /                               │
        │  • GET  /health                         │
        │  • POST /reset                          │
        │  • POST /step                           │
        │  • GET  /observation                    │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Environment Core (app/env.py)      │
        │                                         │
        │  • IPLOpsEnvironment class              │
        │  • Task orchestration                   │
        │  • State management                     │
        │  • Reward calculation                   │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌───────────┐  ┌───────────┐  ┌───────────┐
        │  Task 1   │  │  Task 2   │  │  Task 3   │
        │  Staffing │  │ Playing XI│  │  Crisis   │
        └───────────┘  └───────────┘  └───────────┘
                │             │             │
                ▼             ▼             ▼
        ┌───────────┐  ┌───────────┐  ┌───────────┐
        │ Grader 1  │  │ Grader 2  │  │ Grader 3  │
        └───────────┘  └───────────┘  └───────────┘
```

## Data Flow

```
Agent Request
     │
     ▼
┌─────────────────┐
│  POST /reset    │  ← Initialize task
│  {task_id: 1}   │
└─────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Task Generator                 │
│  • Generate scenario            │
│  • Create observation           │
│  • Return to agent              │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Observation                    │
│  {                              │
│    task_id: 1,                  │
│    task_type: "staff_allocation"│
│    data: {...}                  │
│  }                              │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Agent Processing               │
│  • Analyze observation          │
│  • Make decision                │
│  • Prepare action               │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────┐
│  POST /step     │  ← Submit action
│  {action: {...}}│
└─────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Grader                         │
│  • Validate action              │
│  • Calculate score              │
│  • Generate breakdown           │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Response                       │
│  {                              │
│    reward: 0.875,               │
│    done: true,                  │
│    info: {grading_details}      │
│  }                              │
└─────────────────────────────────┘
```

## Component Architecture

### Task Generators

```
┌──────────────────────────────────────────────────────┐
│                  Task Generators                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Task 1: StaffAllocationTask                        │
│  ├─ STADIUMS: 8 real IPL stadiums                   │
│  ├─ SECURITY_RATIO: Match type based                │
│  ├─ generate_scenario()                             │
│  └─ get_optimal_allocation()                        │
│                                                      │
│  Task 2: PlayingXITask                              │
│  ├─ IPL_SQUADS: 2 teams, 20 players each           │
│  ├─ PITCH_CONDITIONS: 6 variations                  │
│  ├─ generate_scenario()                             │
│  └─ get_scenario_context()                          │
│                                                      │
│  Task 3: CrisisManagementTask                       │
│  ├─ CRISIS_TEMPLATES: 5 types                       │
│  ├─ generate_scenario()                             │
│  ├─ get_scenario_context()                          │
│  └─ get_correct_priority_order()                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Graders

```
┌──────────────────────────────────────────────────────┐
│                     Graders                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Grader 1: StaffAllocationGrader                    │
│  ├─ Weights: security(35%), medical(25%),           │
│  │           ticketing(20%), over/under(10% each)   │
│  ├─ calculate_deviation()                           │
│  ├─ score_category()                                │
│  └─ grade() → {score, breakdown}                    │
│                                                      │
│  Grader 2: PlayingXIGrader                          │
│  ├─ Weights: balance(30%), pitch(40%),              │
│  │           opponent(30%)                          │
│  ├─ validate_structure()                            │
│  ├─ score_team_balance()                            │
│  ├─ score_pitch_fit()                               │
│  ├─ score_opponent_matchup()                        │
│  └─ grade() → {score, breakdown}                    │
│                                                      │
│  Grader 3: CrisisManagementGrader                   │
│  ├─ Weights: priority(35%), decisions(40%),         │
│  │           feasibility(25%)                       │
│  ├─ CORRECT_PRIORITY: [crowd, injury, weather,      │
│  │                      regulatory, tech]           │
│  ├─ validate_structure()                            │
│  ├─ score_priority_ordering()                       │
│  ├─ score_decision_quality()                        │
│  ├─ score_operational_feasibility()                 │
│  └─ grade() → {score, breakdown}                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Data Models

```
┌──────────────────────────────────────────────────────┐
│              Pydantic Data Models                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Enums:                                             │
│  ├─ TaskType                                        │
│  ├─ MatchType                                       │
│  ├─ SurfaceType                                     │
│  ├─ PlayerRole                                      │
│  └─ CrisisType                                      │
│                                                      │
│  Task 1 Models:                                     │
│  ├─ StadiumInfo                                     │
│  └─ StaffAllocationAction                           │
│                                                      │
│  Task 2 Models:                                     │
│  ├─ PlayerStats                                     │
│  ├─ PitchReport                                     │
│  ├─ OpponentProfile                                 │
│  └─ PlayingXIAction                                 │
│                                                      │
│  Task 3 Models:                                     │
│  ├─ CrisisEvent                                     │
│  ├─ CrisisPriority                                  │
│  ├─ CrisisDecision                                  │
│  └─ CrisisManagementAction                          │
│                                                      │
│  Environment Models:                                │
│  ├─ Observation                                     │
│  ├─ ResetRequest/Response                           │
│  └─ StepRequest/Response                            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Docker Container                  │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │         Python 3.11 Runtime                   │ │
│  │                                               │ │
│  │  ┌─────────────────────────────────────────┐ │ │
│  │  │      FastAPI Application                │ │ │
│  │  │                                         │ │ │
│  │  │  • Uvicorn ASGI Server                  │ │ │
│  │  │  • Port 8000                            │ │ │
│  │  │  • CORS enabled                         │ │ │
│  │  │  • Health checks                        │ │ │
│  │  └─────────────────────────────────────────┘ │ │
│  │                                               │ │
│  │  ┌─────────────────────────────────────────┐ │ │
│  │  │      Application Code                   │ │ │
│  │  │                                         │ │ │
│  │  │  • app/main.py                          │ │ │
│  │  │  • app/env.py                           │ │ │
│  │  │  • app/models.py                        │ │ │
│  │  │  • app/tasks/                           │ │ │
│  │  │  • app/graders/                         │ │ │
│  │  └─────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  Exposed: Port 8000                                 │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │   HTTP Clients   │
            │                  │
            │  • Python        │
            │  • cURL          │
            │  • JavaScript    │
            │  • Any HTTP      │
            └──────────────────┘
```

## Scoring Pipeline

```
Action Submitted
     │
     ▼
┌─────────────────────────────────┐
│  Validation                     │
│  • Check required fields        │
│  • Validate data types          │
│  • Check constraints            │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Component Scoring              │
│                                 │
│  Task 1:                        │
│  ├─ Security score              │
│  ├─ Medical score               │
│  ├─ Ticketing score             │
│  ├─ Overstaffing check          │
│  └─ Understaffing check         │
│                                 │
│  Task 2:                        │
│  ├─ Team balance score          │
│  ├─ Pitch fit score             │
│  └─ Opponent matchup score      │
│                                 │
│  Task 3:                        │
│  ├─ Priority ordering score     │
│  ├─ Decision quality score      │
│  └─ Feasibility score           │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Weighted Aggregation           │
│                                 │
│  final_score = Σ(component_i    │
│                  × weight_i)    │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Response Generation            │
│                                 │
│  {                              │
│    reward: 0.875,               │
│    breakdown: {...},            │
│    optimal_values: {...},       │
│    agent_values: {...}          │
│  }                              │
└─────────────────────────────────┘
```

## State Management

```
┌─────────────────────────────────────────────────────┐
│            IPLOpsEnvironment State                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  current_task_id: int | None                        │
│  current_task_type: TaskType | None                 │
│  current_observation: Dict | None                   │
│  done: bool                                         │
│                                                     │
│  Task Instances:                                    │
│  ├─ task1: StaffAllocationTask                      │
│  ├─ task2: PlayingXITask                            │
│  └─ task3: CrisisManagementTask                     │
│                                                     │
│  Grader Instances:                                  │
│  ├─ grader1: StaffAllocationGrader                  │
│  ├─ grader2: PlayingXIGrader                        │
│  └─ grader3: CrisisManagementGrader                 │
│                                                     │
└─────────────────────────────────────────────────────┘

State Transitions:

  [Uninitialized]
       │
       │ reset(task_id)
       ▼
  [Task Active]
       │
       │ step(action)
       ▼
  [Episode Done]
       │
       │ reset(task_id)
       ▼
  [Task Active]
```

## Error Handling

```
┌─────────────────────────────────────────────────────┐
│                 Error Flow                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Request                                            │
│     │                                               │
│     ▼                                               │
│  ┌──────────────────┐                               │
│  │  Validation      │                               │
│  └──────────────────┘                               │
│     │         │                                     │
│     │         └─────► ValueError                    │
│     │                    │                          │
│     │                    ▼                          │
│     │              HTTP 400 Bad Request             │
│     │              {detail: "error message"}        │
│     │                                               │
│     ▼                                               │
│  ┌──────────────────┐                               │
│  │  Processing      │                               │
│  └──────────────────┘                               │
│     │         │                                     │
│     │         └─────► Exception                     │
│     │                    │                          │
│     │                    ▼                          │
│     │              HTTP 500 Internal Error          │
│     │              {detail: "error message"}        │
│     │                                               │
│     ▼                                               │
│  Success Response                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Extensibility Points

```
┌─────────────────────────────────────────────────────┐
│            How to Extend IPLOps-Env                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Add New Stadium (Task 1)                        │
│     └─ Edit: app/tasks/task1_staffing.py           │
│        └─ STADIUMS list                             │
│                                                     │
│  2. Add New IPL Team (Task 2)                       │
│     └─ Edit: app/tasks/task2_selection.py          │
│        └─ IPL_SQUADS dict                           │
│                                                     │
│  3. Add New Crisis Type (Task 3)                    │
│     └─ Edit: app/tasks/task3_crisis.py             │
│        ├─ CrisisType enum (models.py)               │
│        └─ CRISIS_TEMPLATES dict                     │
│                                                     │
│  4. Adjust Scoring Weights                          │
│     └─ Edit: app/graders/grader*.py                │
│        └─ WEIGHTS dict                              │
│                                                     │
│  5. Add New Task (Task 4)                           │
│     ├─ Create: app/tasks/task4_*.py                │
│     ├─ Create: app/graders/grader4.py              │
│     ├─ Update: app/env.py                           │
│     └─ Update: app/models.py                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Performance Characteristics

```
┌─────────────────────────────────────────────────────┐
│              Performance Metrics                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Response Times (typical):                          │
│  ├─ GET /health:        < 5ms                       │
│  ├─ POST /reset:        < 50ms                      │
│  ├─ POST /step:         < 100ms                     │
│  └─ GET /observation:   < 10ms                      │
│                                                     │
│  Memory Usage:                                      │
│  ├─ Base application:   ~50MB                       │
│  ├─ Per episode:        ~1MB                        │
│  └─ Docker container:   ~200MB                      │
│                                                     │
│  Scalability:                                       │
│  ├─ Stateless design (except current episode)       │
│  ├─ No database required                            │
│  ├─ Horizontal scaling ready                        │
│  └─ Can handle 100+ concurrent agents               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

This architecture is designed for:
- **Simplicity**: Easy to understand and modify
- **Extensibility**: Add new tasks/scenarios easily
- **Performance**: Fast response times
- **Reliability**: Comprehensive error handling
- **Scalability**: Stateless design for horizontal scaling
