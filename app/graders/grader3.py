"""
Grader for Task 3: Crisis Management
"""
from typing import Dict, Any, List
from app.models import CrisisType


class CrisisManagementGrader:
    """Grade crisis management decisions"""
    
    WEIGHTS = {
        "priority_ordering": 0.35,
        "decision_quality": 0.40,
        "operational_feasibility": 0.25
    }
    
    # Correct priority order (universal for all scenarios)
    CORRECT_PRIORITY = [
        CrisisType.CROWD_SAFETY,
        CrisisType.INJURY,
        CrisisType.WEATHER,
        CrisisType.REGULATORY,
        CrisisType.TECH_FAILURE
    ]
    
    def validate_structure(self, action: Dict[str, Any]) -> tuple[bool, str]:
        """Validate the action structure"""
        required_fields = ["priority_order", "decisions", "timeline", "risk_assessment"]
        for field in required_fields:
            if field not in action:
                return False, f"Missing required field: {field}"
        
        # Check priority_order structure
        if not isinstance(action["priority_order"], list):
            return False, "priority_order must be a list"
        
        if len(action["priority_order"]) != 5:
            return False, "priority_order must contain exactly 5 crises"
        
        # Check each priority has required fields
        for priority in action["priority_order"]:
            if not isinstance(priority, dict):
                return False, "Each priority must be a dict"
            if "rank" not in priority or "crisis" not in priority or "reason" not in priority:
                return False, "Each priority must have rank, crisis, and reason"
        
        # Check decisions structure
        if not isinstance(action["decisions"], dict):
            return False, "decisions must be a dict"
        
        # Check timeline structure
        if not isinstance(action["timeline"], dict):
            return False, "timeline must be a dict"
        
        return True, ""
    
    def score_priority_ordering(self, priority_order: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score the priority ordering (0.0 to 1.0)"""
        # Extract crisis types from agent's priority order
        agent_order = []
        for item in priority_order:
            crisis_str = item["crisis"]
            # Handle both string and enum formats
            if isinstance(crisis_str, str):
                # Try to match to CrisisType
                for ct in CrisisType:
                    if ct.value == crisis_str or ct.name.lower() == crisis_str.lower():
                        agent_order.append(ct)
                        break
            else:
                agent_order.append(crisis_str)
        
        if len(agent_order) != 5:
            return {
                "score": 0.0,
                "issues": ["Invalid number of crises in priority order"]
            }
        
        # Critical check: Crowd safety MUST be #1
        if agent_order[0] != CrisisType.CROWD_SAFETY:
            return {
                "score": 0.0,
                "issues": ["CRITICAL: Crowd safety must be highest priority (life-threatening)"],
                "agent_order": [c.value for c in agent_order],
                "correct_order": [c.value for c in self.CORRECT_PRIORITY]
            }
        
        # Calculate position-based score
        score = 0.0
        issues = []
        
        for i, correct_crisis in enumerate(self.CORRECT_PRIORITY):
            try:
                agent_position = agent_order.index(correct_crisis)
                position_diff = abs(i - agent_position)
                
                if position_diff == 0:
                    score += 0.2  # Perfect position
                elif position_diff == 1:
                    score += 0.15  # Off by one
                elif position_diff == 2:
                    score += 0.05  # Off by two
                else:
                    issues.append(f"{correct_crisis.value} severely misplaced")
            except ValueError:
                issues.append(f"{correct_crisis.value} missing from priority order")
        
        return {
            "score": min(1.0, score),
            "agent_order": [c.value for c in agent_order],
            "correct_order": [c.value for c in self.CORRECT_PRIORITY],
            "issues": issues
        }
    
    def score_decision_quality(self, decisions: Dict[str, Any], crises: List[Dict]) -> Dict[str, Any]:
        """Score the quality of decisions for each crisis"""
        score = 0.0
        max_score = 0.0
        feedback = {}
        
        # Build crisis lookup
        crisis_lookup = {c["crisis_type"]: c for c in crises}
        
        # Score weather decision
        if "weather" in decisions:
            max_score += 0.2
            weather_decision = decisions["weather"]
            if "action" in weather_decision and "communication" in weather_decision:
                score += 0.15
                if weather_decision["action"] in ["wait", "reduce_overs", "dls_recalculation"]:
                    score += 0.05
                    feedback["weather"] = "Valid weather management approach"
                else:
                    feedback["weather"] = "Questionable weather action"
            else:
                feedback["weather"] = "Incomplete weather decision"
        
        # Score injury decision
        if "injury" in decisions:
            max_score += 0.25
            injury_decision = decisions["injury"]
            if "action" in injury_decision:
                if injury_decision["action"] in ["impact_sub", "concussion_sub", "continue_with_10"]:
                    score += 0.2
                    if "replacement_player" in injury_decision or injury_decision["action"] == "continue_with_10":
                        score += 0.05
                        feedback["injury"] = "Proper injury protocol followed"
                    else:
                        feedback["injury"] = "Missing replacement player details"
                else:
                    feedback["injury"] = "Invalid injury action"
            else:
                feedback["injury"] = "Incomplete injury decision"
        
        # Score crowd safety decision (CRITICAL)
        if "crowd_safety" in decisions:
            max_score += 0.3
            crowd_decision = decisions["crowd_safety"]
            if "action" in crowd_decision:
                if crowd_decision["action"] in ["deploy_riot_squad", "evacuate_stand", "stop_match"]:
                    score += 0.25
                    if "security_reallocation" in crowd_decision:
                        score += 0.05
                        feedback["crowd_safety"] = "Effective crowd safety response"
                    else:
                        feedback["crowd_safety"] = "Missing security reallocation details"
                else:
                    score += 0.1
                    feedback["crowd_safety"] = "Weak crowd safety action"
            else:
                feedback["crowd_safety"] = "CRITICAL: No crowd safety action specified"
        else:
            feedback["crowd_safety"] = "CRITICAL: Crowd safety decision missing"
        
        # Score tech failure decision
        if "tech_failure" in decisions:
            max_score += 0.1
            tech_decision = decisions["tech_failure"]
            if "action" in tech_decision:
                score += 0.08
                if tech_decision["action"] in ["manual_fix", "full_reboot", "ignore"]:
                    score += 0.02
                    feedback["tech_failure"] = "Reasonable tech approach"
        
        # Score regulatory decision
        if "regulatory" in decisions:
            max_score += 0.15
            reg_decision = decisions["regulatory"]
            if "action" in reg_decision and "justification" in reg_decision:
                score += 0.12
                if reg_decision["action"] in ["request_extension", "rush_play", "accept_penalty"]:
                    score += 0.03
                    feedback["regulatory"] = "Proper regulatory handling"
        
        final_score = score / max_score if max_score > 0 else 0.0
        
        return {
            "score": final_score,
            "feedback": feedback
        }
    
    def score_operational_feasibility(self, timeline: Dict[str, List[str]], decisions: Dict[str, Any]) -> Dict[str, Any]:
        """Score operational feasibility of the plan"""
        score = 1.0
        issues = []
        
        # Check timeline exists and has reasonable structure
        if not timeline:
            return {
                "score": 0.0,
                "issues": ["No timeline provided"]
            }
        
        # Count total actions across timeline
        total_actions = sum(len(actions) for actions in timeline.values())
        
        if total_actions == 0:
            score = 0.0
            issues.append("No actions in timeline")
        elif total_actions > 15:
            score -= 0.3
            issues.append("Too many simultaneous actions (unrealistic)")
        
        # Check for immediate actions (0-2 mins should have crowd safety)
        immediate_keys = [k for k in timeline.keys() if "0" in k or "1" in k or "2" in k]
        if immediate_keys:
            immediate_actions = []
            for key in immediate_keys:
                immediate_actions.extend(timeline[key])
            
            # Check if crowd safety is addressed immediately
            crowd_mentioned = any("crowd" in str(action).lower() or "safety" in str(action).lower() 
                                for action in immediate_actions)
            if not crowd_mentioned:
                score -= 0.4
                issues.append("Crowd safety not addressed in first 2 minutes")
        else:
            score -= 0.2
            issues.append("No immediate action timeline specified")
        
        # Check risk assessment exists
        if not decisions:
            score -= 0.2
            issues.append("No decisions provided")
        
        return {
            "score": max(0.0, score),
            "total_actions": total_actions,
            "issues": issues
        }
    
    def grade(self, action: Dict[str, Any], scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Grade the crisis management action
        
        Args:
            action: Agent's crisis management decisions
            scenario: Current scenario context
            
        Returns:
            Dict with score and detailed breakdown
        """
        # Validate structure
        valid, error = self.validate_structure(action)
        if not valid:
            return {
                "score": 0.0,
                "error": error,
                "breakdown": {}
            }
        
        # Score each component
        priority_result = self.score_priority_ordering(action["priority_order"])
        decision_result = self.score_decision_quality(action["decisions"], scenario["crises"])
        feasibility_result = self.score_operational_feasibility(action["timeline"], action["decisions"])
        
        # Calculate weighted final score
        final_score = (
            priority_result["score"] * self.WEIGHTS["priority_ordering"] +
            decision_result["score"] * self.WEIGHTS["decision_quality"] +
            feasibility_result["score"] * self.WEIGHTS["operational_feasibility"]
        )
        
        return {
            "score": round(final_score, 3),
            "breakdown": {
                "priority_ordering": {
                    "score": round(priority_result["score"], 3),
                    "weight": self.WEIGHTS["priority_ordering"],
                    "agent_order": priority_result.get("agent_order", []),
                    "correct_order": priority_result.get("correct_order", []),
                    "issues": priority_result.get("issues", [])
                },
                "decision_quality": {
                    "score": round(decision_result["score"], 3),
                    "weight": self.WEIGHTS["decision_quality"],
                    "feedback": decision_result["feedback"]
                },
                "operational_feasibility": {
                    "score": round(feasibility_result["score"], 3),
                    "weight": self.WEIGHTS["operational_feasibility"],
                    "issues": feasibility_result.get("issues", [])
                }
            }
        }
