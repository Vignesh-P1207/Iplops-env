"""
OpenEnv-compliant inference script for IPLOps-Env
Uses LLM proxy via API_BASE_URL and API_KEY env vars (injected by OpenEnv validator).
"""
import os
import sys
import json
import asyncio
from typing import List, Any, Optional
import requests
from openai import OpenAI

# Read env vars — client is created lazily inside llm_call to avoid crash at import time
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")
BENCHMARK = "iplops-env"
SUCCESS_SCORE_THRESHOLD = 0.7


def get_llm_client() -> OpenAI:
    """Create the OpenAI client using injected proxy credentials."""
    api_base = os.environ["API_BASE_URL"]
    api_key = os.environ["API_KEY"]
    return OpenAI(base_url=api_base, api_key=api_key)


def llm_call(system: str, user: str) -> str:
    """Make a call through the OpenEnv LLM proxy and return the text response."""
    client = get_llm_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


def parse_json_response(text: str) -> dict:
    """Extract JSON from LLM response, stripping markdown fences if present."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: Any, reward: float, done: bool, error: Optional[str] = None) -> None:
    line = f"[STEP] step={step} reward={reward} done={done}"
    if error:
        line += f" error={error}"
    print(line, flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    print(f"[END] score={score} steps={steps} success={success}", flush=True)


class IPLOpsAgent:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def solve_task1(self, observation: dict) -> dict:
        """Task 1: Staff Allocation — decided by LLM."""
        system = (
            "You are an IPL stadium operations expert. "
            "Given stadium data, return a JSON object with keys: "
            "security_per_gate (int), total_security (int), "
            "medical_personnel (int), ticketing_staff (int), reasoning (str). "
            "Return only valid JSON, no extra text."
        )
        user = f"Stadium data:\n{json.dumps(observation['data'], indent=2)}"
        # LLM call is NOT wrapped — must reach the proxy
        raw = llm_call(system, user)
        # Only JSON parsing is wrapped
        try:
            return parse_json_response(raw)
        except Exception:
            stadium = observation["data"]["stadium"]
            crowd = int(stadium["capacity"] * stadium["expected_crowd_percentage"])
            ratio = {"league": 2.5, "playoff": 3.5, "final": 5.0}.get(stadium["match_type"], 3.0)
            total_sec = int((crowd / 1000) * ratio)
            return {
                "security_per_gate": max(2, total_sec // stadium["gates_count"]),
                "total_security": total_sec,
                "medical_personnel": int((crowd / 1000) * 1.5),
                "ticketing_staff": int((crowd / 1000) * 0.8),
                "reasoning": f"Heuristic fallback for {crowd} crowd",
            }

    def solve_task2(self, observation: dict) -> dict:
        """Task 2: Playing XI Selection — decided by LLM."""
        system = (
            "You are an IPL team selection expert. "
            "Given squad, pitch report, and opponent data, select the best Playing XI. "
            "Return a JSON object with keys: "
            "playing_xi (list of 11 player name strings), "
            "batting_order (list of 11 names), "
            "bowling_combination (object with pacers and spinners lists), "
            "reasoning (string). "
            "Return only valid JSON, no extra text."
        )
        user = f"Selection data:\n{json.dumps(observation['data'], indent=2)}"
        raw = llm_call(system, user)
        try:
            return parse_json_response(raw)
        except Exception:
            squad = observation["data"]["squad"]
            squad_sorted = sorted(squad, key=lambda p: p.get("recent_form", 0), reverse=True)
            xi = [p["name"] for p in squad_sorted[:11]]
            return {
                "playing_xi": xi,
                "batting_order": xi,
                "bowling_combination": {"pacers": [], "spinners": []},
                "reasoning": "Fallback: top 11 by recent form",
            }

    def solve_task3(self, observation: dict) -> dict:
        """Task 3: Crisis Management — decided by LLM."""
        system = (
            "You are an IPL crisis management expert. "
            "Given active crises during a match, return a JSON object with keys: "
            "priority_order (list of objects with rank, crisis, reason), "
            "decisions (object keyed by crisis name, each with action, details, timeline_minutes), "
            "timeline (object with time windows as keys), "
            "risk_assessment (object). "
            "Return only valid JSON, no extra text."
        )
        user = f"Crisis data:\n{json.dumps(observation['data'], indent=2)}"
        raw = llm_call(system, user)
        try:
            return parse_json_response(raw)
        except Exception:
            return {
                "priority_order": [
                    {"rank": 1, "crisis": "crowd_safety", "reason": "Life-threatening"},
                    {"rank": 2, "crisis": "injury", "reason": "Player health"},
                    {"rank": 3, "crisis": "weather", "reason": "Match continuation"},
                    {"rank": 4, "crisis": "regulatory", "reason": "Compliance"},
                    {"rank": 5, "crisis": "tech_failure", "reason": "Minimal impact"},
                ],
                "decisions": {},
                "timeline": {},
                "risk_assessment": {},
            }

    def run(self, task_id: int) -> float:
        task_names = {1: "staff_allocation", 2: "playing_xi_selection", 3: "crisis_management"}
        task_name = task_names.get(task_id, f"task_{task_id}")

        rewards: List[float] = []
        steps_taken = 0
        score = 0.0
        success = False

        log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

        try:
            response = requests.post(f"{self.base_url}/reset", json={"task_id": task_id})
            observation = response.json()["observation"]

            if task_id == 1:
                action = self.solve_task1(observation)
            elif task_id == 2:
                action = self.solve_task2(observation)
            else:
                action = self.solve_task3(observation)

            steps_taken = 1

            response = requests.post(f"{self.base_url}/step", json={"action": action})
            result = response.json()

            reward = result["reward"]
            done = result["done"]
            rewards.append(reward)

            log_step(step=1, action=action, reward=reward, done=done)

            score = reward
            success = score >= SUCCESS_SCORE_THRESHOLD

        except Exception as e:
            log_step(step=steps_taken, action={}, reward=0.0, done=True, error=str(e))

        finally:
            log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

        return score


async def main() -> None:
    agent = IPLOpsAgent(base_url=ENV_BASE_URL)

    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        if arg not in ["1", "2", "3"]:
            print(f"Error: Invalid task_id {arg}. Must be 1, 2, or 3", file=sys.stderr)
            sys.exit(1)
        task_ids = [int(arg)]
    else:
        task_ids = [1, 2, 3]

    all_scores = {}
    try:
        for task_id in task_ids:
            score = agent.run(task_id)
            all_scores[f"task_{task_id}"] = round(score, 3)
            print(f"[RESULT] Task {task_id} Score: {score:.3f}", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to environment. Is the server running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if len(all_scores) > 1:
        avg = sum(all_scores.values()) / len(all_scores)
        print(f"[SUMMARY] {all_scores} | Average: {avg:.3f}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
