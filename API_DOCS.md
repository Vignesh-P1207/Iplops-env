# IPLOps-Env API Documentation

Complete API reference for the Indian Premier League Operations Environment.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for local development.

## Endpoints

### GET /

Get environment information and available tasks.

**Response:**
```json
{
  "name": "IPLOps-Env",
  "version": "1.0.0",
  "description": "Indian Premier League Operations Environment",
  "tasks": [
    {"id": 1, "name": "Staff Allocation", "difficulty": "easy"},
    {"id": 2, "name": "Playing XI Selection", "difficulty": "medium"},
    {"id": 3, "name": "Crisis Management", "difficulty": "hard"}
  ],
  "endpoints": {
    "reset": "POST /reset",
    "step": "POST /step",
    "observation": "GET /observation",
    "health": "GET /health"
  }
}
```

---

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "iplops-env",
  "version": "1.0.0"
}
```

---

### POST /reset

Initialize a new task episode.

**Request Body:**
```json
{
  "task_id": 1
}
```

**Parameters:**
- `task_id` (integer, required): Task ID (1, 2, or 3)

**Response:**
```json
{
  "observation": {
    "task_id": 1,
    "task_type": "staff_allocation",
    "data": {
      "stadium": {
        "name": "Wankhede Stadium",
        "capacity": 33000,
        "expected_crowd_percentage": 0.87,
        "match_type": "playoff",
        "gates_count": 8,
        "medical_stations": 4
      },
      "instructions": "Allocate staff for this IPL match..."
    },
    "timestamp": "2026-04-06T10:30:00.123456"
  },
  "info": {
    "message": "Task 1 initialized successfully",
    "task_type": "staff_allocation"
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "Invalid task_id: 5. Must be 1, 2, or 3"
}
```

---

### POST /step

Submit an action and receive reward.

**Request Body:**

The action format depends on the current task:

#### Task 1: Staff Allocation
```json
{
  "action": {
    "security_per_gate": 5,
    "total_security": 80,
    "medical_personnel": 35,
    "ticketing_staff": 20,
    "reasoning": "Optional explanation"
  }
}
```

#### Task 2: Playing XI Selection
```json
{
  "action": {
    "playing_xi": [
      "Rohit Sharma",
      "Ishan Kishan",
      "Suryakumar Yadav",
      "Tilak Varma",
      "Hardik Pandya",
      "Tim David",
      "Jasprit Bumrah",
      "Piyush Chawla",
      "Kumar Kartikeya",
      "Jason Behrendorff",
      "Arjun Tendulkar"
    ],
    "batting_order": [
      "Rohit Sharma",
      "Ishan Kishan",
      ...
    ],
    "bowling_combination": {
      "pacers": ["Jasprit Bumrah", "Jason Behrendorff"],
      "spinners": ["Piyush Chawla"],
      "death_overs_specialist": "Jasprit Bumrah"
    },
    "reasoning": {
      "pitch_strategy": "Selected for spin-friendly pitch",
      "opponent_matchup": "Exploiting weakness against spin",
      "balance_justification": "1 WK, 4 batsmen, 3 all-rounders, 3 bowlers"
    }
  }
}
```

#### Task 3: Crisis Management
```json
{
  "action": {
    "priority_order": [
      {"rank": 1, "crisis": "crowd_safety", "reason": "Life-threatening"},
      {"rank": 2, "crisis": "injury", "reason": "Player health"},
      {"rank": 3, "crisis": "weather", "reason": "Match continuation"},
      {"rank": 4, "crisis": "regulatory", "reason": "Compliance"},
      {"rank": 5, "crisis": "tech_failure", "reason": "Lowest priority"}
    ],
    "decisions": {
      "crowd_safety": {
        "action": "deploy_riot_squad",
        "details": {
          "security_reallocation": {"from": "VIP", "to": "Stand_C", "count": 50},
          "police_coordination": true
        },
        "timeline_minutes": 2.0
      },
      "injury": {
        "action": "impact_sub",
        "details": {"replacement_player": "Substitute"},
        "timeline_minutes": 3.0
      },
      "weather": {
        "action": "wait",
        "details": {"dls_target": 165},
        "timeline_minutes": 5.0
      },
      "regulatory": {
        "action": "request_extension",
        "details": {"justification": "Multiple crises"},
        "timeline_minutes": 1.5
      },
      "tech_failure": {
        "action": "manual_fix",
        "details": {},
        "timeline_minutes": 10.0
      }
    },
    "timeline": {
      "0-2_mins": ["Action 1", "Action 2"],
      "2-5_mins": ["Action 3"],
      "5-10_mins": ["Action 4", "Action 5"]
    },
    "risk_assessment": {
      "if_wrong_priority": "Consequences",
      "cascading_failures": "Interdependencies"
    }
  }
}
```

**Response:**
```json
{
  "observation": {
    "task_id": 1,
    "task_type": "staff_allocation",
    "data": {"message": "Task completed"},
    "timestamp": "2026-04-06T10:31:00.123456"
  },
  "reward": 0.875,
  "done": true,
  "info": {
    "grading_details": {
      "score": 0.875,
      "breakdown": {
        "security_score": 0.95,
        "medical_score": 0.88,
        "ticketing_score": 0.82,
        "overstaffing_score": 1.0,
        "understaffing_score": 1.0,
        "total_staffing_ratio": 1.05
      },
      "optimal_values": {
        "total_security": 78,
        "medical_personnel": 34,
        "ticketing_staff": 19,
        "expected_crowd": 28710
      },
      "agent_values": {
        "total_security": 80,
        "medical_personnel": 35,
        "ticketing_staff": 20
      }
    },
    "message": "Task completed successfully"
  }
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "Environment not initialized. Call reset() first"
}
```

400 Bad Request:
```json
{
  "detail": "Missing required field: security_per_gate"
}
```

---

### GET /observation

Get current observation without taking action.

**Response:**
```json
{
  "task_id": 1,
  "task_type": "staff_allocation",
  "data": {
    "stadium": {...},
    "instructions": "..."
  },
  "timestamp": "2026-04-06T10:30:00.123456"
}
```

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "No observation available. Call reset() first"
}
```

---

## Data Models

### Observation

```typescript
{
  task_id: number,           // 1, 2, or 3
  task_type: string,         // "staff_allocation" | "playing_xi" | "crisis_management"
  data: object,              // Task-specific data
  timestamp: string          // ISO 8601 format
}
```

### Task 1 Data

```typescript
{
  stadium: {
    name: string,
    capacity: number,
    expected_crowd_percentage: number,  // 0.0 to 1.0
    match_type: "league" | "playoff" | "final",
    gates_count: number,
    medical_stations: number
  },
  instructions: string
}
```

### Task 2 Data

```typescript
{
  team_name: string,
  squad: Array<{
    name: string,
    role: "batsman" | "bowler" | "all_rounder" | "wicket_keeper",
    batting_avg: number,
    strike_rate: number,
    balls_faced: number,
    runs_scored: number,
    bowling_economy: number | null,
    wickets: number | null,
    overs_bowled: number | null,
    bowling_avg: number | null,
    fielding_catches: number,
    recent_form: number  // 0-100
  }>,
  pitch_report: {
    surface_type: "spin_friendly" | "pace_friendly" | "balanced",
    bounce: "low" | "medium" | "high",
    match_time: "day" | "day_night" | "night",
    expected_score_range: [number, number]
  },
  opponent: {
    team_name: string,
    weakness_against: "spin" | "pace" | "swing",
    top_batsmen: Array<{name: string, avg_strike_rate: number}>,
    death_bowling_strength: number  // 0-100
  },
  instructions: string
}
```

### Task 3 Data

```typescript
{
  match_context: {
    current_score: string,
    target: number,
    crowd_size: number,
    crowd_capacity_percent: number,
    match_time: string,
    match_type: string
  },
  crises: Array<{
    crisis_type: "weather" | "injury" | "crowd_safety" | "tech_failure" | "regulatory",
    severity: number,  // 0-100
    description: string,
    time_sensitive: boolean,
    deadline_seconds: number | null
  }>,
  instructions: string
}
```

---

## Scoring Details

### Task 1: Staff Allocation

**Components:**
- Security accuracy: 35% (±15% tolerance)
- Medical accuracy: 25% (±20% tolerance)
- Ticketing accuracy: 20% (±25% tolerance)
- No overstaffing: 10% (penalty if >1.3x optimal)
- No understaffing: 10% (penalty if <0.8x optimal)

**Formula:**
```
score = (security_score * 0.35) + 
        (medical_score * 0.25) + 
        (ticketing_score * 0.20) + 
        (overstaffing_score * 0.10) + 
        (understaffing_score * 0.10)
```

### Task 2: Playing XI Selection

**Components:**
- Team balance: 30%
  - Must have 1 wicket-keeper
  - 5-6 specialist batsmen
  - 4-5 bowlers (at least 2 pacers, 1 spinner)
  - At least 2 all-rounders
- Pitch condition fit: 40%
  - Bowling attack matches pitch type
  - Batsmen strike rates appropriate
- Opponent matchup: 30%
  - Exploits opponent weaknesses
  - Counters their strengths

**Formula:**
```
score = (balance_score * 0.30) + 
        (pitch_fit_score * 0.40) + 
        (opponent_score * 0.30)
```

### Task 3: Crisis Management

**Components:**
- Priority ordering: 35%
  - CRITICAL: Crowd safety must be #1 (auto-fail if not)
  - Correct order: Crowd → Injury → Weather → Regulatory → Tech
- Decision quality: 40%
  - Valid actions for each crisis
  - Proper resource allocation
  - Stakeholder communication
- Operational feasibility: 25%
  - Realistic timeline
  - No resource conflicts
  - Contingency planning

**Formula:**
```
score = (priority_score * 0.35) + 
        (decision_score * 0.40) + 
        (feasibility_score * 0.25)
```

---

## Example Workflows

### Python with requests

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

print(f"Score: {result['reward']}")
print(f"Breakdown: {result['info']['grading_details']['breakdown']}")
```

### cURL

```bash
# Reset
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": 1}'

# Step
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "security_per_gate": 5,
      "total_security": 80,
      "medical_personnel": 35,
      "ticketing_staff": 20
    }
  }'
```

### JavaScript/TypeScript

```typescript
const BASE_URL = "http://localhost:8000";

// Reset
const resetResponse = await fetch(`${BASE_URL}/reset`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({task_id: 1})
});
const {observation} = await resetResponse.json();

// Step
const stepResponse = await fetch(`${BASE_URL}/step`, {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    action: {
      security_per_gate: 5,
      total_security: 80,
      medical_personnel: 35,
      ticketing_staff: 20
    }
  })
});
const result = await stepResponse.json();

console.log(`Score: ${result.reward}`);
```

---

## Rate Limits

No rate limits for local development.

## CORS

CORS is enabled for all origins in development mode.

## Error Codes

- `400 Bad Request`: Invalid input or environment state
- `500 Internal Server Error`: Server-side error

## Support

For API issues:
1. Check this documentation
2. Verify request format matches examples
3. Check server logs for detailed errors
4. Review grading breakdown in response
