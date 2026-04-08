"""
Task 2: Playing XI Selection
Difficulty: Medium
Uses real IPL squad data from API clients
"""
import random
from typing import Dict, Any, List
from app.models import PlayerStats, PitchReport, OpponentProfile, PlayerRole, SurfaceType
from app.api_clients import IPLDataAggregator


class PlayingXITask:
    """Generate Playing XI selection scenarios with real IPL data"""
    
    def __init__(self):
        self.current_scenario = None
        self.aggregator = IPLDataAggregator()
    
    def generate_scenario(self) -> Dict[str, Any]:
        """Generate a Playing XI selection scenario using API data"""
        # Get available teams
        teams = self.aggregator.espn_client.get_ipl_teams()
        team = random.choice(teams)
        team_name = team.get("name", "Mumbai Indians")
        
        # Get squad from aggregator (uses API or fallback)
        squad = self.aggregator.get_enriched_squad(team_name)
        
        # Generate pitch conditions
        venues = ["Wankhede Stadium", "Eden Gardens", "M. Chinnaswamy Stadium", "Arun Jaitley Stadium"]
        venue = random.choice(venues)
        pitch = self.aggregator.get_pitch_report(venue)
        
        # Add more pitch details
        pitch_report = {
            "venue": venue,
            "surface_type": pitch.get("type", "balanced"),
            "bounce": pitch.get("pace_bounce", "medium"),
            "spin_factor": pitch.get("spin", "medium"),
            "match_time": random.choice(["day", "night", "day_night"]),
            "dew_factor": random.choice(["low", "medium", "high"]),
            "expected_score_range": (160, 180)
        }
        
        # Generate opponent profile
        opponent_teams = [t for t in teams if t.get("name") != team_name]
        opponent = random.choice(opponent_teams) if opponent_teams else {"name": "Chennai Super Kings"}
        
        opponent_profile = {
            "team_name": opponent.get("name", "Chennai Super Kings"),
            "weakness_against": random.choice(["spin", "pace", "swing"]),
            "top_order_strength": random.choice(["weak", "medium", "strong"]),
            "tail_weakness": random.choice([True, False]),
            "top_batsmen": [
                {"name": "Player A", "avg_strike_rate": random.uniform(125, 145)},
                {"name": "Player B", "avg_strike_rate": random.uniform(120, 140)},
            ],
            "death_bowling_strength": random.uniform(60, 90)
        }
        
        self.current_scenario = {
            "team_name": team_name,
            "squad": squad,
            "pitch_report": pitch_report,
            "opponent": opponent_profile,
            "instructions": (
                f"Select the best Playing XI for {team_name} from the {len(squad)}-player squad.\n"
                "Your selection must include:\n"
                "- Exactly 11 players\n"
                "- 1 wicket-keeper\n"
                "- 5-6 specialist batsmen\n"
                "- 4-5 bowlers (at least 2 pacers, 1 spinner)\n"
                "- At least 2 all-rounders\n"
                f"Pitch: {pitch_report['surface_type']} at {venue}\n"
                f"Opponent: {opponent_profile['team_name']} (weak against {opponent_profile['weakness_against']})\n"
                "Consider pitch conditions, opponent weaknesses, and recent form."
            )
        }
        
        return {
            "team_name": team_name,
            "squad": squad,
            "pitch_report": pitch_report,
            "opponent": opponent_profile,
            "instructions": self.current_scenario["instructions"]
        }
    
    def get_scenario_context(self) -> Dict[str, Any]:
        """Return current scenario for grading"""
        return self.current_scenario
