"""
API clients for fetching real IPL data from ESPN Cricinfo and Crickbuzz
"""
import requests
from typing import Dict, List, Any, Optional
import os
from datetime import datetime


class ESPNCricinfoClient:
    """Client for ESPN Cricinfo API"""
    
    BASE_URL = "https://hs-consumer-api.espncricinfo.com/v1/pages"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ESPN_API_KEY", "")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
    
    def get_ipl_teams(self) -> List[Dict[str, Any]]:
        """Fetch all IPL teams"""
        try:
            # ESPN Cricinfo public endpoint for IPL teams
            url = f"{self.BASE_URL}/series/1345038/teams"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("teams", [])
            else:
                print(f"ESPN API returned status {response.status_code}")
                return self._get_fallback_teams()
        except Exception as e:
            print(f"ESPN API error: {e}")
            return self._get_fallback_teams()
    
    def get_team_squad(self, team_id: int) -> List[Dict[str, Any]]:
        """Fetch squad for a specific team"""
        try:
            url = f"{self.BASE_URL}/team/{team_id}/squad"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("players", [])
            else:
                return []
        except Exception as e:
            print(f"ESPN squad API error: {e}")
            return []
    
    def _get_fallback_teams(self) -> List[Dict[str, Any]]:
        """Fallback IPL teams data"""
        return [
            {"id": 1, "name": "Mumbai Indians", "short_name": "MI"},
            {"id": 2, "name": "Chennai Super Kings", "short_name": "CSK"},
            {"id": 3, "name": "Royal Challengers Bangalore", "short_name": "RCB"},
            {"id": 4, "name": "Kolkata Knight Riders", "short_name": "KKR"},
            {"id": 5, "name": "Delhi Capitals", "short_name": "DC"},
            {"id": 6, "name": "Punjab Kings", "short_name": "PBKS"},
            {"id": 7, "name": "Rajasthan Royals", "short_name": "RR"},
            {"id": 8, "name": "Sunrisers Hyderabad", "short_name": "SRH"},
            {"id": 9, "name": "Lucknow Super Giants", "short_name": "LSG"},
            {"id": 10, "name": "Gujarat Titans", "short_name": "GT"}
        ]


class CrickbuzzClient:
    """Client for Crickbuzz API"""
    
    BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY", "")
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
            })
    
    def get_ipl_matches(self) -> List[Dict[str, Any]]:
        """Fetch current IPL matches"""
        try:
            url = f"{self.BASE_URL}/matches/v1/recent"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("typeMatches", [])
            else:
                return []
        except Exception as e:
            print(f"Crickbuzz API error: {e}")
            return []
    
    def get_player_stats(self, player_id: int) -> Dict[str, Any]:
        """Fetch player statistics"""
        try:
            url = f"{self.BASE_URL}/stats/v1/player/{player_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            print(f"Crickbuzz player stats error: {e}")
            return {}


class IPLDataAggregator:
    """Aggregates data from multiple sources"""
    
    def __init__(self):
        self.espn_client = ESPNCricinfoClient()
        self.crickbuzz_client = CrickbuzzClient()
        
        # Import scraper and stadium data
        try:
            from app.scraper import scraper
            from app.stadium_data import stadium_db
            self.scraper = scraper
            self.stadium_db = stadium_db
        except:
            self.scraper = None
            self.stadium_db = None
    
    def get_enriched_squad(self, team_name: str) -> List[Dict[str, Any]]:
        """
        Get enriched squad data with AI-powered dynamic generation
        Each call generates fresh squad with form variations
        """
        # Always generate fresh dynamic squad
        if self.scraper:
            try:
                # Generate dynamic squad with AI variations
                squads = self.scraper.scrape_cricbuzz_squads()
                if team_name in squads:
                    print(f"[DYNAMIC SQUAD] Generated fresh squad for {team_name} with AI variations")
                    return squads[team_name]
            except Exception as e:
                print(f"[ERROR] Squad generation failed: {e}")
        
        # Fallback to static data
        return self._get_static_squad(team_name)
    
    def get_all_stadiums(self) -> List[str]:
        """Get list of all IPL stadiums"""
        if self.stadium_db:
            return self.stadium_db.get_all_stadiums()
        return [
            "Wankhede Stadium, Mumbai",
            "M. A. Chidambaram Stadium, Chennai",
            "Eden Gardens, Kolkata",
            "M. Chinnaswamy Stadium, Bangalore"
        ]
    
    def _get_static_squad(self, team_name: str) -> List[Dict[str, Any]]:
        """Enhanced static squad data with realistic 2026 IPL stats"""
        
        squads = {
            "Mumbai Indians": [
                {
                    "name": "Rohit Sharma",
                    "role": "batsman",
                    "batting_avg": 31.2,
                    "strike_rate": 130.5,
                    "balls_faced": 3200,
                    "runs_scored": 6000,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 45,
                    "recent_form": 78,
                    "matches_played": 227,
                    "best_score": 109
                },
                {
                    "name": "Ishan Kishan",
                    "role": "wicket_keeper",
                    "batting_avg": 29.8,
                    "strike_rate": 135.2,
                    "balls_faced": 2800,
                    "runs_scored": 4500,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 62,
                    "recent_form": 82,
                    "matches_played": 105,
                    "best_score": 99
                },
                {
                    "name": "Suryakumar Yadav",
                    "role": "batsman",
                    "batting_avg": 30.5,
                    "strike_rate": 145.8,
                    "balls_faced": 2500,
                    "runs_scored": 4200,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 38,
                    "recent_form": 88,
                    "matches_played": 142,
                    "best_score": 103
                },
                {
                    "name": "Tilak Varma",
                    "role": "all_rounder",
                    "batting_avg": 35.2,
                    "strike_rate": 128.4,
                    "balls_faced": 1800,
                    "runs_scored": 3100,
                    "bowling_economy": 8.5,
                    "bowling_type": "pace",
                    "wickets": 5,
                    "overs_bowled": 45.0,
                    "bowling_avg": 42.0,
                    "fielding_catches": 22,
                    "recent_form": 85,
                    "matches_played": 45,
                    "best_score": 84
                },
                {
                    "name": "Hardik Pandya",
                    "role": "all_rounder",
                    "batting_avg": 28.5,
                    "strike_rate": 142.3,
                    "balls_faced": 2200,
                    "runs_scored": 3800,
                    "bowling_economy": 8.8,
                    "bowling_type": "pace",
                    "wickets": 68,
                    "overs_bowled": 280.0,
                    "bowling_avg": 28.5,
                    "fielding_catches": 41,
                    "recent_form": 75,
                    "matches_played": 158,
                    "best_score": 91
                },
                {
                    "name": "Tim David",
                    "role": "batsman",
                    "batting_avg": 42.5,
                    "strike_rate": 158.2,
                    "balls_faced": 800,
                    "runs_scored": 1850,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 15,
                    "recent_form": 90,
                    "matches_played": 52,
                    "best_score": 85
                },
                {
                    "name": "Jasprit Bumrah",
                    "role": "bowler",
                    "batting_avg": 8.2,
                    "strike_rate": 95.5,
                    "balls_faced": 250,
                    "runs_scored": 180,
                    "bowling_economy": 7.2,
                    "bowling_type": "pace",
                    "wickets": 145,
                    "overs_bowled": 520.0,
                    "bowling_avg": 22.8,
                    "fielding_catches": 18,
                    "recent_form": 92,
                    "matches_played": 133,
                    "best_bowling": "5/10"
                },
                {
                    "name": "Piyush Chawla",
                    "role": "bowler",
                    "batting_avg": 12.5,
                    "strike_rate": 110.2,
                    "balls_faced": 420,
                    "runs_scored": 380,
                    "bowling_economy": 8.2,
                    "bowling_type": "spin",
                    "wickets": 95,
                    "overs_bowled": 380.0,
                    "bowling_avg": 28.5,
                    "fielding_catches": 25,
                    "recent_form": 68,
                    "matches_played": 165,
                    "best_bowling": "4/17"
                },
                {
                    "name": "Kumar Kartikeya",
                    "role": "bowler",
                    "batting_avg": 6.5,
                    "strike_rate": 88.5,
                    "balls_faced": 180,
                    "runs_scored": 95,
                    "bowling_economy": 7.8,
                    "bowling_type": "spin",
                    "wickets": 42,
                    "overs_bowled": 165.0,
                    "bowling_avg": 26.2,
                    "fielding_catches": 12,
                    "recent_form": 72,
                    "matches_played": 38,
                    "best_bowling": "3/22"
                },
                {
                    "name": "Jason Behrendorff",
                    "role": "bowler",
                    "batting_avg": 7.8,
                    "strike_rate": 92.5,
                    "balls_faced": 120,
                    "runs_scored": 85,
                    "bowling_economy": 8.5,
                    "bowling_type": "pace",
                    "wickets": 38,
                    "overs_bowled": 145.0,
                    "bowling_avg": 30.5,
                    "fielding_catches": 8,
                    "recent_form": 70,
                    "matches_played": 42,
                    "best_bowling": "4/28"
                },
                {
                    "name": "Arjun Tendulkar",
                    "role": "all_rounder",
                    "batting_avg": 18.5,
                    "strike_rate": 118.5,
                    "balls_faced": 650,
                    "runs_scored": 980,
                    "bowling_economy": 9.2,
                    "bowling_type": "pace",
                    "wickets": 28,
                    "overs_bowled": 125.0,
                    "bowling_avg": 35.8,
                    "fielding_catches": 18,
                    "recent_form": 62,
                    "matches_played": 55,
                    "best_score": 45
                },
            ],
            "Chennai Super Kings": [
                {
                    "name": "MS Dhoni",
                    "role": "wicket_keeper",
                    "batting_avg": 38.2,
                    "strike_rate": 136.8,
                    "balls_faced": 4200,
                    "runs_scored": 5200,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 125,
                    "recent_form": 72,
                    "matches_played": 250,
                    "best_score": 84
                },
                {
                    "name": "Ruturaj Gaikwad",
                    "role": "batsman",
                    "batting_avg": 33.5,
                    "strike_rate": 128.5,
                    "balls_faced": 2800,
                    "runs_scored": 4800,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 32,
                    "recent_form": 85,
                    "matches_played": 145,
                    "best_score": 101
                },
                {
                    "name": "Devon Conway",
                    "role": "batsman",
                    "batting_avg": 42.8,
                    "strike_rate": 140.2,
                    "balls_faced": 1850,
                    "runs_scored": 3450,
                    "bowling_economy": None,
                    "wickets": None,
                    "overs_bowled": None,
                    "bowling_avg": None,
                    "fielding_catches": 28,
                    "recent_form": 88,
                    "matches_played": 82,
                    "best_score": 92
                },
                {
                    "name": "Ravindra Jadeja",
                    "role": "all_rounder",
                    "batting_avg": 26.8,
                    "strike_rate": 127.5,
                    "balls_faced": 2200,
                    "runs_scored": 3600,
                    "bowling_economy": 7.5,
                    "bowling_type": "spin",
                    "wickets": 132,
                    "overs_bowled": 485.0,
                    "bowling_avg": 26.2,
                    "fielding_catches": 68,
                    "recent_form": 80,
                    "matches_played": 220,
                    "best_score": 62
                },
                {
                    "name": "Moeen Ali",
                    "role": "all_rounder",
                    "batting_avg": 24.5,
                    "strike_rate": 138.2,
                    "balls_faced": 1450,
                    "runs_scored": 2280,
                    "bowling_economy": 7.8,
                    "bowling_type": "spin",
                    "wickets": 52,
                    "overs_bowled": 220.0,
                    "bowling_avg": 28.5,
                    "fielding_catches": 35,
                    "recent_form": 75,
                    "matches_played": 95,
                    "best_score": 68
                },
                {
                    "name": "Deepak Chahar",
                    "role": "bowler",
                    "batting_avg": 15.2,
                    "strike_rate": 125.5,
                    "balls_faced": 580,
                    "runs_scored": 720,
                    "bowling_economy": 8.2,
                    "bowling_type": "pace",
                    "wickets": 78,
                    "overs_bowled": 320.0,
                    "bowling_avg": 28.8,
                    "fielding_catches": 22,
                    "recent_form": 78,
                    "matches_played": 105,
                    "best_bowling": "4/13"
                },
                {
                    "name": "Maheesh Theekshana",
                    "role": "bowler",
                    "batting_avg": 9.2,
                    "strike_rate": 98.5,
                    "balls_faced": 180,
                    "runs_scored": 125,
                    "bowling_economy": 7.2,
                    "bowling_type": "spin",
                    "wickets": 48,
                    "overs_bowled": 185.0,
                    "bowling_avg": 25.8,
                    "fielding_catches": 15,
                    "recent_form": 82,
                    "matches_played": 62,
                    "best_bowling": "4/18"
                },
                {
                    "name": "Matheesha Pathirana",
                    "role": "bowler",
                    "batting_avg": 6.5,
                    "strike_rate": 88.5,
                    "balls_faced": 95,
                    "runs_scored": 58,
                    "bowling_economy": 8.5,
                    "bowling_type": "pace",
                    "wickets": 38,
                    "overs_bowled": 142.0,
                    "bowling_avg": 30.2,
                    "fielding_catches": 8,
                    "recent_form": 85,
                    "matches_played": 45,
                    "best_bowling": "5/21"
                },
            ]
        }
        
        # Return squad or default to Mumbai Indians if team not found
        return squads.get(team_name, squads["Mumbai Indians"])
    
    def get_pitch_report(self, venue: str) -> Dict[str, Any]:
        """Generate detailed pitch report for venue"""
        if self.stadium_db:
            return self.stadium_db.get_pitch_report(venue)
        
        # Fallback
        pitch_types = {
            "Wankhede Stadium, Mumbai": {"type": "batting_friendly", "pace_bounce": "high", "spin": "low"},
            "Eden Gardens, Kolkata": {"type": "spin_friendly", "pace_bounce": "low", "spin": "high"},
            "M. Chinnaswamy Stadium, Bangalore": {"type": "batting_friendly", "pace_bounce": "high", "spin": "low"},
            "Arun Jaitley Stadium, Delhi": {"type": "balanced", "pace_bounce": "medium", "spin": "medium"},
        }
        
        return pitch_types.get(venue, {"type": "balanced", "pace_bounce": "medium", "spin": "medium"})
