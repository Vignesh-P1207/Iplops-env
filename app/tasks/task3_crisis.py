"""
Task 3: Live Crisis Management
Difficulty: Hard
"""
import random
from typing import Dict, Any, List
from app.models import CrisisEvent, CrisisType


class CrisisManagementTask:
    """Generate multi-crisis scenarios during live IPL matches"""
    
    CRISIS_TEMPLATES = {
        CrisisType.WEATHER: [
            {
                "description": "Rain detected, covers coming on. Match interrupted at {overs} overs. DLS par score needs recalculation. Broadcast partner demanding clarity in 3 minutes.",
                "severity": 75,
                "time_sensitive": True,
                "deadline_seconds": 180
            },
            {
                "description": "Heavy dew affecting ball grip. Bowlers complaining, umpires considering ball change. Decision needed immediately.",
                "severity": 55,
                "time_sensitive": True,
                "deadline_seconds": 120
            }
        ],
        CrisisType.INJURY: [
            {
                "description": "Star batsman (captain) injured while running. Physio assessment: possible hamstring tear. Needs immediate substitution decision. Impact Sub available but affects team balance. Opponent team questioning substitution legality.",
                "severity": 85,
                "time_sensitive": True,
                "deadline_seconds": 240
            },
            {
                "description": "Bowler hit on head by return catch. Concussion protocol activated. Mandatory substitution required within 10 minutes per ICC rules.",
                "severity": 95,
                "time_sensitive": True,
                "deadline_seconds": 600
            }
        ],
        CrisisType.CROWD_SAFETY: [
            {
                "description": "Fight broke out in Stand C (North). 200+ people involved, escalating. Security spread thin due to VIP movement. Risk of stampede if not contained in 5 minutes. Police asking if match should be stopped.",
                "severity": 95,
                "time_sensitive": True,
                "deadline_seconds": 300
            },
            {
                "description": "Overcrowding detected at Gate 7. Fire safety capacity exceeded by 15%. Local authorities threatening to halt match if not resolved.",
                "severity": 80,
                "time_sensitive": True,
                "deadline_seconds": 420
            }
        ],
        CrisisType.TECH_FAILURE: [
            {
                "description": "LED screen showing wrong score. Causing confusion + crowd anger. Sponsor logos not displaying (contract breach risk). Tech team needs 10 mins to reboot vs. quick manual fix.",
                "severity": 45,
                "time_sensitive": False,
                "deadline_seconds": None
            },
            {
                "description": "Floodlight failure in one tower. 30% reduction in visibility. Match can continue but player safety concerns raised. Backup generator available but takes 8 minutes to activate.",
                "severity": 70,
                "time_sensitive": True,
                "deadline_seconds": 480
            }
        ],
        CrisisType.REGULATORY: [
            {
                "description": "BCCI official flagging over-rate penalty incoming. Team will lose points if next over not bowled in 90 seconds. But injured player situation is delaying play. Captain asking for time extension.",
                "severity": 65,
                "time_sensitive": True,
                "deadline_seconds": 90
            },
            {
                "description": "Third umpire system malfunction during crucial DRS review. Decision must be made manually. Both teams demanding fair process. ICC match referee involved.",
                "severity": 75,
                "time_sensitive": True,
                "deadline_seconds": 180
            }
        ]
    }
    
    def __init__(self):
        self.current_scenario = None
    
    def generate_scenario(self) -> Dict[str, Any]:
        """Generate a multi-crisis scenario"""
        # Select 5 random crises (one from each type)
        crises = []
        for crisis_type in CrisisType:
            template = random.choice(self.CRISIS_TEMPLATES[crisis_type])
            
            # Customize description with match context
            description = template["description"]
            if "{overs}" in description:
                overs = round(random.uniform(15.0, 18.5), 1)
                description = description.format(overs=overs)
            
            crises.append({
                "crisis_type": crisis_type.value,
                "severity": template["severity"] + random.randint(-5, 5),
                "description": description,
                "time_sensitive": template["time_sensitive"],
                "deadline_seconds": template["deadline_seconds"]
            })
        
        # Match context
        match_context = {
            "current_score": f"Team A {random.randint(140, 160)}/{random.randint(3, 6)} in {round(random.uniform(16.0, 18.5), 1)} overs",
            "target": random.randint(175, 190),
            "crowd_size": random.randint(25000, 32000),
            "crowd_capacity_percent": random.randint(80, 95),
            "match_time": f"{random.randint(9, 10)}:{random.randint(10, 59)} PM",
            "match_type": random.choice(["Playoff", "Final", "Eliminator"])
        }
        
        self.current_scenario = {
            "match_context": match_context,
            "crises": crises,
            "instructions": (
                "You are the Match Operations Director. Multiple crises are happening SIMULTANEOUSLY.\n\n"
                "You must:\n"
                "1. Prioritize all 5 crises by rank (1 = most urgent)\n"
                "2. Provide specific decisions for each crisis\n"
                "3. Create a timeline showing when each action will be taken\n"
                "4. Assess risks of wrong prioritization\n\n"
                "Consider:\n"
                "- Life safety always comes first\n"
                "- Time-sensitive crises have deadlines\n"
                "- Decisions are interdependent (one affects others)\n"
                "- Stakeholder conflicts (BCCI vs. broadcast vs. safety)\n"
                "- Resource constraints (can't do everything at once)"
            )
        }
        
        return {
            "match_context": match_context,
            "crises": crises,
            "instructions": self.current_scenario["instructions"]
        }
    
    def get_scenario_context(self) -> Dict[str, Any]:
        """Return current scenario for grading"""
        return self.current_scenario
    
    def get_correct_priority_order(self) -> List[CrisisType]:
        """Return the correct priority order for grading"""
        # Priority logic:
        # 1. Crowd Safety (life-threatening)
        # 2. Player Injury (health + match impact)
        # 3. Weather (match continuation)
        # 4. Regulatory (points/penalties)
        # 5. Tech Failure (lowest priority)
        
        return [
            CrisisType.CROWD_SAFETY,
            CrisisType.INJURY,
            CrisisType.WEATHER,
            CrisisType.REGULATORY,
            CrisisType.TECH_FAILURE
        ]
