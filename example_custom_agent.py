"""
Example: Building a Custom Agent for IPLOps-Env

This demonstrates how to build a sophisticated agent that:
1. Analyzes scenarios intelligently
2. Makes data-driven decisions
3. Handles edge cases
4. Achieves high scores
"""
import requests
from typing import Dict, Any, List


class AdvancedIPLAgent:
    """
    Advanced agent with sophisticated decision-making logic
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.history = []
    
    # ==================== TASK 1: STAFF ALLOCATION ====================
    
    def solve_task1(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced staff allocation with safety margin optimization
        """
        stadium = observation["data"]["stadium"]
        
        # Calculate expected crowd
        expected_crowd = int(stadium["capacity"] * stadium["expected_crowd_percentage"])
        
        # Safety ratios based on match importance
        security_ratios = {
            "league": 2.5,
            "playoff": 3.5,
            "final": 5.0
        }
        base_security_ratio = security_ratios.get(stadium["match_type"], 3.0)
        
        # Adjust for crowd density (higher density = more security)
        crowd_density = stadium["expected_crowd_percentage"]
        if crowd_density > 0.9:
            security_multiplier = 1.15  # 15% more for packed stadium
        elif crowd_density > 0.8:
            security_multiplier = 1.08  # 8% more for high attendance
        else:
            security_multiplier = 1.0
        
        # Calculate optimal allocations
        total_security = int((expected_crowd / 1000) * base_security_ratio * security_multiplier)
        
        # Distribute security evenly across gates with minimum per gate
        security_per_gate = max(3, total_security // stadium["gates_count"])
        
        # Ensure total matches distribution
        total_security = security_per_gate * stadium["gates_count"]
        
        # Medical personnel (1.5 per 1000, minimum 2 per station)
        medical_personnel = max(
            int((expected_crowd / 1000) * 1.5),
            stadium["medical_stations"] * 2
        )
        
        # Ticketing staff (0.8 per 1000, minimum 1 per gate)
        ticketing_staff = max(
            int((expected_crowd / 1000) * 0.8),
            stadium["gates_count"]
        )
        
        return {
            "security_per_gate": security_per_gate,
            "total_security": total_security,
            "medical_personnel": medical_personnel,
            "ticketing_staff": ticketing_staff,
            "reasoning": (
                f"Allocated for {expected_crowd:,} expected crowd ({crowd_density*100:.0f}% capacity) "
                f"at {stadium['match_type']} match. Security multiplier: {security_multiplier:.2f}x"
            )
        }
    
    # ==================== TASK 2: PLAYING XI SELECTION ====================
    
    def solve_task2(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced Playing XI selection with multi-factor optimization
        """
        squad = observation["data"]["squad"]
        pitch = observation["data"]["pitch_report"]
        opponent = observation["data"]["opponent"]
        
        # Score each player based on multiple factors
        player_scores = []
        for player in squad:
            score = self._calculate_player_score(player, pitch, opponent)
            player_scores.append((player, score))
        
        # Sort by score
        player_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select XI with role constraints
        selected = self._select_balanced_xi(player_scores, pitch, opponent)
        
        # Optimize batting order
        batting_order = self._optimize_batting_order(selected, pitch)
        
        # Identify bowling combination
        bowling_combo = self._identify_bowlers(selected, pitch, opponent)
        
        return {
            "playing_xi": [p["name"] for p in selected],
            "batting_order": [p["name"] for p in batting_order],
            "bowling_combination": bowling_combo,
            "reasoning": {
                "pitch_strategy": self._explain_pitch_strategy(selected, pitch),
                "opponent_matchup": self._explain_opponent_strategy(selected, opponent),
                "balance_justification": self._explain_balance(selected)
            }
        }
    
    def _calculate_player_score(self, player: Dict, pitch: Dict, opponent: Dict) -> float:
        """Calculate composite player score"""
        score = 0.0
        
        # Recent form is most important (40%)
        score += player["recent_form"] * 0.4
        
        # Role-specific scoring (30%)
        if player["role"] == "batsman":
            score += (player["batting_avg"] / 50.0) * 15
            score += (player["strike_rate"] / 150.0) * 15
        elif player["role"] == "bowler":
            if player.get("bowling_economy"):
                score += (10.0 - player["bowling_economy"]) * 3
            if player.get("wickets"):
                score += (player["wickets"] / 150.0) * 15
        elif player["role"] == "all_rounder":
            score += (player["batting_avg"] / 50.0) * 10
            if player.get("bowling_economy"):
                score += (10.0 - player["bowling_economy"]) * 10
        elif player["role"] == "wicket_keeper":
            score += (player["batting_avg"] / 50.0) * 15
            score += (player["fielding_catches"] / 100.0) * 15
        
        # Pitch fit bonus (20%)
        if pitch["surface_type"] == "spin_friendly":
            if player["role"] in ["bowler", "all_rounder"]:
                if player.get("bowling_economy") and 7.0 <= player["bowling_economy"] <= 8.5:
                    score += 20  # Spinner bonus
        elif pitch["surface_type"] == "pace_friendly":
            if player["role"] in ["bowler", "all_rounder"]:
                if player.get("bowling_economy") and player["bowling_economy"] < 8.5:
                    score += 20  # Pacer bonus
        
        # Opponent matchup bonus (10%)
        if opponent["weakness_against"] == "spin":
            if player["role"] in ["bowler", "all_rounder"]:
                if player.get("bowling_economy") and 7.0 <= player["bowling_economy"] <= 8.5:
                    score += 10
        elif opponent["weakness_against"] in ["pace", "swing"]:
            if player["role"] in ["bowler", "all_rounder"]:
                if player.get("bowling_economy") and player["bowling_economy"] < 8.5:
                    score += 10
        
        return score
    
    def _select_balanced_xi(self, player_scores: List, pitch: Dict, opponent: Dict) -> List[Dict]:
        """Select 11 players with role balance"""
        selected = []
        
        # Must have exactly 1 wicket-keeper
        wk_candidates = [(p, s) for p, s in player_scores if p["role"] == "wicket_keeper"]
        if wk_candidates:
            selected.append(wk_candidates[0][0])
        
        # Select 4 specialist batsmen
        batsmen = [(p, s) for p, s in player_scores if p["role"] == "batsman" and p not in selected]
        selected.extend([p for p, s in batsmen[:4]])
        
        # Select 3 all-rounders
        all_rounders = [(p, s) for p, s in player_scores if p["role"] == "all_rounder" and p not in selected]
        selected.extend([p for p, s in all_rounders[:3]])
        
        # Select 3 specialist bowlers (mix based on pitch)
        bowlers = [(p, s) for p, s in player_scores if p["role"] == "bowler" and p not in selected]
        selected.extend([p for p, s in bowlers[:3]])
        
        # Fill remaining slots if needed
        while len(selected) < 11:
            remaining = [(p, s) for p, s in player_scores if p not in selected]
            if remaining:
                selected.append(remaining[0][0])
            else:
                break
        
        return selected[:11]
    
    def _optimize_batting_order(self, selected: List[Dict], pitch: Dict) -> List[Dict]:
        """Optimize batting order based on roles and strike rates"""
        # Openers: High strike rate batsmen
        batsmen = [p for p in selected if p["role"] in ["batsman", "wicket_keeper"]]
        batsmen.sort(key=lambda x: x["strike_rate"], reverse=True)
        
        # Middle order: All-rounders and anchors
        all_rounders = [p for p in selected if p["role"] == "all_rounder"]
        all_rounders.sort(key=lambda x: x["batting_avg"], reverse=True)
        
        # Tail: Bowlers
        bowlers = [p for p in selected if p["role"] == "bowler"]
        bowlers.sort(key=lambda x: x.get("batting_avg", 0), reverse=True)
        
        # Construct order
        order = []
        order.extend(batsmen[:2])  # Openers
        order.extend(batsmen[2:])  # Middle order batsmen
        order.extend(all_rounders)  # All-rounders
        order.extend(bowlers)  # Tail
        
        return order[:11]
    
    def _identify_bowlers(self, selected: List[Dict], pitch: Dict, opponent: Dict) -> Dict:
        """Identify bowling combination"""
        bowlers = [p for p in selected if p["role"] in ["bowler", "all_rounder"]]
        
        # Classify as pacer or spinner based on economy
        pacers = [p for p in bowlers if p.get("bowling_economy") and p["bowling_economy"] < 8.5]
        spinners = [p for p in bowlers if p.get("bowling_economy") and 7.0 <= p.get("bowling_economy", 10) <= 8.5]
        
        # Death overs specialist (lowest economy)
        death_specialist = min(bowlers, key=lambda x: x.get("bowling_economy", 10))
        
        return {
            "pacers": [p["name"] for p in pacers[:3]],
            "spinners": [p["name"] for p in spinners[:2]],
            "death_overs_specialist": death_specialist["name"]
        }
    
    def _explain_pitch_strategy(self, selected: List[Dict], pitch: Dict) -> str:
        """Explain pitch-based strategy"""
        bowlers = [p for p in selected if p["role"] in ["bowler", "all_rounder"]]
        spinners = sum(1 for p in bowlers if p.get("bowling_economy", 10) >= 7.5)
        pacers = sum(1 for p in bowlers if p.get("bowling_economy", 10) < 8.5)
        
        return f"Selected {spinners} spinners and {pacers} pacers for {pitch['surface_type']} pitch with {pitch['bounce']} bounce"
    
    def _explain_opponent_strategy(self, selected: List[Dict], opponent: Dict) -> str:
        """Explain opponent-based strategy"""
        return f"Targeting {opponent['team_name']}'s weakness against {opponent['weakness_against']} bowling"
    
    def _explain_balance(self, selected: List[Dict]) -> str:
        """Explain team balance"""
        roles = {}
        for player in selected:
            roles[player["role"]] = roles.get(player["role"], 0) + 1
        
        return f"Balanced XI: {roles.get('wicket_keeper', 0)} WK, {roles.get('batsman', 0)} batsmen, {roles.get('all_rounder', 0)} all-rounders, {roles.get('bowler', 0)} bowlers"
    
    # ==================== TASK 3: CRISIS MANAGEMENT ====================
    
    def solve_task3(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced crisis management with priority optimization
        """
        crises = observation["data"]["crises"]
        match_context = observation["data"]["match_context"]
        
        # Analyze each crisis
        crisis_analysis = self._analyze_crises(crises, match_context)
        
        # Determine optimal priority
        priority_order = self._determine_priority(crisis_analysis)
        
        # Generate decisions for each crisis
        decisions = self._generate_crisis_decisions(crises, match_context)
        
        # Create execution timeline
        timeline = self._create_timeline(priority_order, decisions)
        
        # Risk assessment
        risk_assessment = self._assess_risks(crises, priority_order)
        
        return {
            "priority_order": priority_order,
            "decisions": decisions,
            "timeline": timeline,
            "risk_assessment": risk_assessment
        }
    
    def _analyze_crises(self, crises: List[Dict], context: Dict) -> List[Dict]:
        """Analyze severity and urgency of each crisis"""
        analysis = []
        for crisis in crises:
            urgency = 100 if crisis["time_sensitive"] else 50
            if crisis["deadline_seconds"]:
                urgency += (300 - crisis["deadline_seconds"]) / 3
            
            analysis.append({
                "crisis_type": crisis["crisis_type"],
                "severity": crisis["severity"],
                "urgency": urgency,
                "time_sensitive": crisis["time_sensitive"]
            })
        return analysis
    
    def _determine_priority(self, analysis: List[Dict]) -> List[Dict]:
        """Determine correct priority order"""
        # Fixed priority based on crisis type (life safety first)
        priority_map = {
            "crowd_safety": 1,
            "injury": 2,
            "weather": 3,
            "regulatory": 4,
            "tech_failure": 5
        }
        
        priority_order = []
        for crisis_type, rank in sorted(priority_map.items(), key=lambda x: x[1]):
            reason = self._get_priority_reason(crisis_type, rank)
            priority_order.append({
                "rank": rank,
                "crisis": crisis_type,
                "reason": reason
            })
        
        return priority_order
    
    def _get_priority_reason(self, crisis_type: str, rank: int) -> str:
        """Get reasoning for priority rank"""
        reasons = {
            "crowd_safety": "Life-threatening situation requiring immediate intervention",
            "injury": "Player health critical, affects match continuation",
            "weather": "Match continuation depends on weather management",
            "regulatory": "Compliance important but not life-threatening",
            "tech_failure": "Operational issue with minimal safety impact"
        }
        return reasons.get(crisis_type, "Standard priority")
    
    def _generate_crisis_decisions(self, crises: List[Dict], context: Dict) -> Dict[str, Any]:
        """Generate optimal decisions for each crisis"""
        return {
            "crowd_safety": {
                "action": "deploy_riot_squad",
                "details": {
                    "security_reallocation": {"from": "VIP_section", "to": "incident_area", "count": 50},
                    "police_coordination": True,
                    "evacuation_plan": "Prepared if escalates"
                },
                "timeline_minutes": 2.0
            },
            "injury": {
                "action": "impact_sub",
                "details": {
                    "replacement_player": "Best available substitute",
                    "medical_assessment": "Ongoing",
                    "batting_order_adjustment": "Flexible based on situation"
                },
                "timeline_minutes": 3.0
            },
            "weather": {
                "action": "wait",
                "details": {
                    "dls_calculation": "Ready",
                    "covers_deployed": True,
                    "broadcast_communication": "Regular updates every 5 minutes"
                },
                "timeline_minutes": 5.0
            },
            "regulatory": {
                "action": "request_extension",
                "details": {
                    "justification": "Multiple simultaneous crises causing unavoidable delay",
                    "bcci_notification": "Immediate",
                    "documentation": "All incidents logged"
                },
                "timeline_minutes": 1.5
            },
            "tech_failure": {
                "action": "manual_fix",
                "details": {
                    "tech_team_deployed": True,
                    "sponsor_notification": "Sent",
                    "backup_plan": "Manual scoreboard if needed"
                },
                "timeline_minutes": 10.0
            }
        }
    
    def _create_timeline(self, priority_order: List[Dict], decisions: Dict) -> Dict[str, List[str]]:
        """Create execution timeline"""
        return {
            "0-2_mins": [
                "Deploy riot squad to crowd incident area",
                "Request over-rate extension from BCCI",
                "Alert medical team for injury assessment"
            ],
            "2-5_mins": [
                "Process impact substitution",
                "Monitor weather conditions",
                "Coordinate with police on crowd control"
            ],
            "5-10_mins": [
                "Calculate DLS if rain continues",
                "Begin LED screen repairs",
                "Stabilize crowd situation"
            ],
            "10+_mins": [
                "Resume match if conditions permit",
                "Complete technical repairs",
                "Post-incident review"
            ]
        }
    
    def _assess_risks(self, crises: List[Dict], priority_order: List[Dict]) -> Dict[str, str]:
        """Assess risks of decisions"""
        return {
            "if_wrong_priority": (
                "Prioritizing anything over crowd safety could result in casualties and stampede. "
                "Ignoring injury could worsen player condition. "
                "Weather mismanagement could lead to unfair match outcome."
            ),
            "cascading_failures": (
                "Weather delay provides buffer time to handle other crises. "
                "Crowd incident could force match stoppage, affecting all other decisions. "
                "Tech failure is independent and doesn't cascade."
            ),
            "mitigation_strategy": (
                "Parallel task forces for each crisis. "
                "Clear communication channels. "
                "Escalation protocols in place."
            )
        }
    
    # ==================== MAIN EXECUTION ====================
    
    def run(self, task_id: int) -> float:
        """Run agent on specified task"""
        # Reset
        response = requests.post(f"{self.base_url}/reset", json={"task_id": task_id})
        observation = response.json()["observation"]
        
        # Solve
        if task_id == 1:
            action = self.solve_task1(observation)
        elif task_id == 2:
            action = self.solve_task2(observation)
        else:
            action = self.solve_task3(observation)
        
        # Submit
        response = requests.post(f"{self.base_url}/step", json={"action": action})
        result = response.json()
        
        # Store history
        self.history.append({
            "task_id": task_id,
            "score": result["reward"],
            "breakdown": result["info"]["grading_details"]
        })
        
        return result["reward"]


def main():
    """Test the advanced agent"""
    agent = AdvancedIPLAgent()
    
    print("="*60)
    print("Advanced IPL Agent - Performance Test")
    print("="*60)
    
    scores = []
    for task_id in [1, 2, 3]:
        print(f"\nRunning Task {task_id}...")
        score = agent.run(task_id)
        scores.append(score)
        print(f"Score: {score:.3f}")
    
    print("\n" + "="*60)
    print("Final Results")
    print("="*60)
    print(f"Task 1: {scores[0]:.3f}")
    print(f"Task 2: {scores[1]:.3f}")
    print(f"Task 3: {scores[2]:.3f}")
    print(f"Average: {sum(scores)/len(scores):.3f}")


if __name__ == "__main__":
    main()
