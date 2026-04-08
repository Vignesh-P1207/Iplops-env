from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Any
from enum import Enum


class TaskType(str, Enum):
    STAFF_ALLOCATION = "staff_allocation"
    PLAYING_XI = "playing_xi"
    CRISIS_MANAGEMENT = "crisis_management"


class MatchType(str, Enum):
    LEAGUE = "league"
    PLAYOFF = "playoff"
    FINAL = "final"


class SurfaceType(str, Enum):
    SPIN_FRIENDLY = "spin_friendly"
    PACE_FRIENDLY = "pace_friendly"
    BALANCED = "balanced"


class PlayerRole(str, Enum):
    BATSMAN = "batsman"
    BOWLER = "bowler"
    ALL_ROUNDER = "all_rounder"
    WICKET_KEEPER = "wicket_keeper"


# Task 1 Models
class StadiumInfo(BaseModel):
    name: str
    capacity: int
    expected_crowd_percentage: float
    match_type: MatchType
    gates_count: int
    medical_stations: int


class StaffAllocationAction(BaseModel):
    security_per_gate: int
    total_security: int
    medical_personnel: int
    ticketing_staff: int
    reasoning: Optional[str] = None


# Task 2 Models
class PlayerStats(BaseModel):
    name: str
    role: PlayerRole
    batting_avg: float
    strike_rate: float
    balls_faced: int
    runs_scored: int
    bowling_economy: Optional[float] = None
    wickets: Optional[int] = None
    overs_bowled: Optional[float] = None
    bowling_avg: Optional[float] = None
    fielding_catches: int
    recent_form: float  # 0-100 score


class PitchReport(BaseModel):
    surface_type: SurfaceType
    bounce: Literal["low", "medium", "high"]
    match_time: Literal["day", "day_night", "night"]
    expected_score_range: tuple[int, int]


class OpponentProfile(BaseModel):
    team_name: str
    weakness_against: Literal["spin", "pace", "swing"]
    top_batsmen: List[Dict[str, Any]]
    death_bowling_strength: float  # 0-100


class PlayingXIAction(BaseModel):
    playing_xi: List[str]
    batting_order: List[str]
    bowling_combination: Dict[str, Any]
    reasoning: Dict[str, str]


# Task 3 Models
class CrisisType(str, Enum):
    WEATHER = "weather"
    INJURY = "injury"
    CROWD_SAFETY = "crowd_safety"
    TECH_FAILURE = "tech_failure"
    REGULATORY = "regulatory"


class CrisisEvent(BaseModel):
    crisis_type: CrisisType
    severity: float  # 0-100
    description: str
    time_sensitive: bool
    deadline_seconds: Optional[int] = None


class CrisisPriority(BaseModel):
    rank: int
    crisis: CrisisType
    reason: str


class CrisisDecision(BaseModel):
    action: str
    details: Dict[str, Any]
    timeline_minutes: float


class CrisisManagementAction(BaseModel):
    priority_order: List[CrisisPriority]
    decisions: Dict[str, CrisisDecision]
    timeline: Dict[str, List[str]]
    risk_assessment: Dict[str, str]


# Environment Models
class Observation(BaseModel):
    task_id: int
    task_type: TaskType
    data: Dict[str, Any]
    timestamp: str


class ResetRequest(BaseModel):
    task_id: int = Field(default=1, ge=1, le=3)


class StepRequest(BaseModel):
    action: Dict[str, Any]


class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]


class ResetResponse(BaseModel):
    observation: Observation
    info: Dict[str, str]
