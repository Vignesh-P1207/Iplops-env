"""
System and user prompts for Task 3: Crisis Management
These prompts guide AI agents in handling multiple simultaneous crises during live IPL matches
"""

TASK3_SYSTEM_PROMPT = """You are the IPL Match Operations AI — the real-time crisis command center for live IPL matches.

You operate under extreme time pressure. Multiple crises can fire simultaneously mid-match.

## YOUR RESPONSIBILITIES

You must:
1. Triage all active crises by PRIORITY (life safety > match integrity > operations)
2. Make correct, justified operational decisions for EACH crisis independently
3. Coordinate between departments: Medical, Security, BCCI Match Referee, DLS Calculator, Team Management
4. Output structured decisions in a format that field teams can act on immediately

## PRIORITY FRAMEWORK (use this ordering strictly):

P0 — Life & Safety (crowd injury, player collapse, medical emergency)
P1 — Match Integrity (DLS, ball change, pitch breach, umpire incident)  
P2 — Operational (player injury reshuffle, strategic timeout, equipment failure)
P3 — Communication (media, social, sponsor updates)

## DECISION QUALITY RUBRIC

Each decision is graded on:
- Speed: Is the response actionable in <2 minutes of real time?
- Accuracy: Is the cricket/operational rule applied correctly?
- Completeness: Are all downstream effects addressed?
- Communication: Is it clearly formatted for field teams?

## RESPONSE FORMAT (strict JSON only)

{
  "match_state_snapshot": {
    "over": "<current over e.g. 14.3>",
    "batting_team": "<team name>",
    "bowling_team": "<team name>",
    "score": "<runs/wickets e.g. 112/3>",
    "target": <integer or null if first innings>
  },
  "crisis_triage": [
    {
      "crisis_id": "<string e.g. CRISIS_A>",
      "priority": "P0|P1|P2|P3",
      "crisis_type": "<type>",
      "handle_order": <1-N>,
      "time_to_resolve_minutes": <integer>
    }
  ],
  "decisions": [
    {
      "crisis_id": "<string>",
      "decision_title": "<short title>",
      "immediate_actions": ["<action 1>", "<action 2>", ...],
      "department_instructions": {
        "security": "<instruction or null>",
        "medical": "<instruction or null>",
        "match_referee": "<instruction or null>",
        "team_management_batting": "<instruction or null>",
        "team_management_bowling": "<instruction or null>",
        "dls_calculator": "<instruction or null>",
        "stadium_ops": "<instruction or null>"
      },
      "rule_applied": "<specific ICC/IPL rule cited e.g. ICC DLS Method clause 8.3>",
      "decision_rationale": "<2-3 sentences>",
      "downstream_effects": ["<effect 1>", "<effect 2>"],
      "decision_quality_score": <0.0-1.0>
    }
  ],
  "overall_priority_order_correct": true|false,
  "total_crises_handled": <integer>,
  "overall_response_score": <0.0-1.0>,
  "command_broadcast": "<one unified broadcast message to all departments, max 3 sentences>"
}
"""

TASK3_USER_PROMPT_TEMPLATE = """## LIVE CRISIS EVENT — MATCH OPS AI ACTIVATED

### MATCH CONTEXT:
- Match: {team_a} vs {team_b}
- Venue: {venue}
- Over: {current_over} | Innings: {innings}
- Score: {score} | Target: {target}
- Weather: {weather_status}
- Crowd: {crowd_count} / {stadium_capacity} capacity
- DLS Par Score at this over: {dls_par}

### SIMULTANEOUS CRISIS EVENTS FIRED:

#### CRISIS A — {crisis_a_title}
{crisis_a_description}
Affected Zone: {crisis_a_zone}
Reported By: {crisis_a_reporter}
Time Reported: {crisis_a_time}

#### CRISIS B — {crisis_b_title}
{crisis_b_description}
Affected Zone: {crisis_b_zone}
Reported By: {crisis_b_reporter}
Time Reported: {crisis_b_time}

#### CRISIS C — {crisis_c_title}
{crisis_c_description}
Affected Zone: {crisis_c_zone}
Reported By: {crisis_c_reporter}
Time Reported: {crisis_c_time}

### AVAILABLE RESOURCES:
- Medical Teams On-Site: {medical_teams}
- Security Personnel Available: {security_count}
- Reserve/Substitute Players: {substitute_players}
- DLS System: {dls_status}  # "online" or "offline"
- Backup Referee: {backup_referee}

### CONSTRAINTS:
- {special_constraints}

You are the command AI. Triage all crises, prioritize correctly, and issue decisions for each.
Return strict JSON only. Field teams are waiting.
"""


def format_task3_prompt(observation: dict) -> str:
    """
    Format the user prompt for Task 3 with actual observation data
    
    Args:
        observation: Environment observation containing crisis data
        
    Returns:
        Formatted prompt string
    """
    data = observation.get("data", {})
    crises = data.get("crises", [])
    match_state = data.get("match_state", {})
    resources = data.get("resources", {})
    
    # Extract crisis details (up to 3)
    crisis_details = {}
    for i, crisis in enumerate(crises[:3], 1):
        letter = chr(64 + i)  # A, B, C
        crisis_details[f"crisis_{letter.lower()}_title"] = crisis.get("crisis_type", "Unknown Crisis")
        crisis_details[f"crisis_{letter.lower()}_description"] = crisis.get("description", "No description")
        crisis_details[f"crisis_{letter.lower()}_zone"] = crisis.get("affected_zone", "Unknown")
        crisis_details[f"crisis_{letter.lower()}_reporter"] = crisis.get("reported_by", "Unknown")
        crisis_details[f"crisis_{letter.lower()}_time"] = crisis.get("time_reported", "Unknown")
    
    # Fill in template
    prompt_data = {
        "team_a": match_state.get("batting_team", "Team A"),
        "team_b": match_state.get("bowling_team", "Team B"),
        "venue": match_state.get("venue", "Unknown Stadium"),
        "current_over": match_state.get("current_over", "0.0"),
        "innings": match_state.get("innings", "1st"),
        "score": match_state.get("score", "0/0"),
        "target": match_state.get("target", "N/A"),
        "weather_status": match_state.get("weather", "Clear"),
        "crowd_count": match_state.get("crowd_count", 30000),
        "stadium_capacity": match_state.get("stadium_capacity", 40000),
        "dls_par": match_state.get("dls_par", "N/A"),
        "medical_teams": resources.get("medical_teams", 3),
        "security_count": resources.get("security_personnel", 150),
        "substitute_players": resources.get("substitute_players", "Available"),
        "dls_status": resources.get("dls_system", "online"),
        "backup_referee": resources.get("backup_referee", "Available"),
        "special_constraints": data.get("constraints", "No special constraints"),
        **crisis_details
    }
    
    return TASK3_USER_PROMPT_TEMPLATE.format(**prompt_data)


# Example crisis types and their priorities
CRISIS_PRIORITIES = {
    # P0 - Life & Safety
    "crowd_safety": "P0",
    "player_collapse": "P0",
    "medical_emergency": "P0",
    "fire": "P0",
    "bomb_threat": "P0",
    
    # P1 - Match Integrity
    "weather": "P1",
    "dls_calculation": "P1",
    "ball_tampering": "P1",
    "pitch_invasion": "P1",
    "umpire_injury": "P1",
    "regulatory": "P1",
    
    # P2 - Operational
    "injury": "P2",
    "equipment_failure": "P2",
    "power_outage": "P2",
    "tech_failure": "P2",
    
    # P3 - Communication
    "media_issue": "P3",
    "sponsor_complaint": "P3",
    "social_media": "P3"
}


# Correct decision actions for common crises
CORRECT_ACTIONS = {
    "crowd_safety": {
        "action": "deploy_riot_squad",
        "timeline_minutes": 2.0,
        "departments": ["security", "stadium_ops", "medical"]
    },
    "injury": {
        "action": "impact_sub",
        "timeline_minutes": 3.0,
        "departments": ["medical", "team_management_batting", "match_referee"]
    },
    "weather": {
        "action": "wait",
        "timeline_minutes": 5.0,
        "departments": ["match_referee", "dls_calculator", "stadium_ops"]
    },
    "regulatory": {
        "action": "request_extension",
        "timeline_minutes": 1.5,
        "departments": ["match_referee"]
    },
    "tech_failure": {
        "action": "manual_fix",
        "timeline_minutes": 10.0,
        "departments": ["stadium_ops"]
    }
}
