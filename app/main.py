"""
FastAPI Server for IPLOps-Env
OpenEnv spec compliant: /reset, /step, /observation, /state, /health
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.env import IPLOpsEnvironment
from app.models import ResetRequest, StepRequest, StepResponse, ResetResponse
import uvicorn
from typing import Optional

app = FastAPI(
    title="IPLOps-Env",
    description="Indian Premier League Operations Environment - AI Agent Evaluation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Global environment instance
env = IPLOpsEnvironment()


@app.get("/")
async def root():
    """Root endpoint — returns 200 with env info (required by HF Space ping)"""
    return {
        "name": "IPLOps-Env",
        "version": "1.0.0",
        "status": "ok",
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
            "state": "GET /state",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "iplops-env",
        "version": "1.0.0",
        "tasks": ["staff_allocation", "playing_xi_selection", "crisis_management"]
    }


@app.post("/reset", response_model=ResetResponse)
async def reset(request: Optional[ResetRequest] = None):
    """Reset environment and initialize a new task"""
    try:
        task_id = request.task_id if request else 1
        result = env.reset(task_id)
        return ResetResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/step", response_model=StepResponse)
async def step(request: StepRequest):
    """Execute agent action and get reward"""
    try:
        result = env.step(request.action)
        return StepResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/observation")
async def get_observation():
    """Get current observation without taking action"""
    try:
        return env.get_observation()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/state")
async def get_state():
    """
    OpenEnv spec: state() endpoint — returns full environment state.
    Required for spec compliance and HF Space validation.
    """
    try:
        obs = env.get_observation()
        return {
            "task_id": env.current_task_id,
            "task_type": env.current_task_type.value if env.current_task_type else None,
            "done": env.done,
            "observation": obs,
            "status": "active" if env.current_task_id and not env.done else "idle"
        }
    except Exception:
        return {
            "task_id": None,
            "task_type": None,
            "done": False,
            "observation": None,
            "status": "idle"
        }


@app.get("/task2")
async def task2_ui():
    """Serve Task 2 UI"""
    static_file = Path(__file__).parent.parent / "static" / "task2.html"
    if static_file.exists():
        return FileResponse(static_file)
    raise HTTPException(status_code=404, detail="Task 2 UI not found")


@app.get("/api/ipl/teams")
async def get_ipl_teams():
    from app.api_clients import IPLDataAggregator
    aggregator = IPLDataAggregator()
    teams = aggregator.espn_client.get_ipl_teams()
    return {"teams": teams}


@app.get("/api/ipl/stadiums")
async def get_ipl_stadiums():
    from app.api_clients import IPLDataAggregator
    aggregator = IPLDataAggregator()
    stadiums = aggregator.get_all_stadiums()
    return {"stadiums": stadiums}


@app.get("/api/ipl/squad/{team_name}")
async def get_team_squad(team_name: str):
    from app.api_clients import IPLDataAggregator
    aggregator = IPLDataAggregator()
    squad = aggregator.get_enriched_squad(team_name)
    return {"team": team_name, "squad": squad}


@app.get("/api/ipl/pitch/{venue}")
async def get_pitch_report(venue: str):
    from app.api_clients import IPLDataAggregator
    aggregator = IPLDataAggregator()
    pitch = aggregator.get_pitch_report(venue)
    return {"venue": venue, "pitch_report": pitch}


@app.post("/api/ipl/select-team")
async def ai_select_team(request: dict):
    from app.team_selector import team_selector
    from app.api_clients import IPLDataAggregator

    team_name = request.get("team_name")
    venue = request.get("venue")
    opponent_name = request.get("opponent_name", "Chennai Super Kings")

    aggregator = IPLDataAggregator()
    squad = aggregator.get_enriched_squad(team_name)
    pitch_report = aggregator.get_pitch_report(venue)

    opponent_profile = {
        "team_name": opponent_name,
        "weakness_against": request.get("opponent_weakness", "spin"),
        "death_bowling_strength": request.get("opponent_death_strength", 75)
    }

    selection = team_selector.select_playing_xi(squad, pitch_report, opponent_profile)
    return selection


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏏 IPLOps-Env Server Starting...")
    print("="*60)
    print("📍 Server: http://0.0.0.0:8000")
    print("📍 Health: http://localhost:8000/health")
    print("📍 Docs:   http://localhost:8000/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
