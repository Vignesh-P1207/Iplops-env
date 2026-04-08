"""
Comprehensive IPL stadium and pitch data
"""
from typing import Dict, Any, List


class StadiumDatabase:
    """Complete database of all IPL stadiums with detailed pitch characteristics"""
    
    STADIUMS = {
        "Wankhede Stadium, Mumbai": {
            "city": "Mumbai",
            "capacity": 33108,
            "pitch_type": "batting_friendly",
            "pace_bounce": "high",
            "spin_assistance": "low",
            "avg_first_innings": 185,
            "avg_second_innings": 165,
            "dew_factor": "high",
            "boundary_size": "small",
            "characteristics": ["High scoring", "Favors pacers early", "Dew helps chasing"],
            "best_for": ["Power hitters", "Fast bowlers", "Death bowlers"]
        },
        "M. A. Chidambaram Stadium, Chennai": {
            "city": "Chennai",
            "capacity": 50000,
            "pitch_type": "spin_friendly",
            "pace_bounce": "low",
            "spin_assistance": "very_high",
            "avg_first_innings": 155,
            "avg_second_innings": 145,
            "dew_factor": "medium",
            "boundary_size": "medium",
            "characteristics": ["Slow and low", "Spinners dominate", "Difficult to score"],
            "best_for": ["Spinners", "Anchor batsmen", "Death specialists"]
        },
        "Eden Gardens, Kolkata": {
            "city": "Kolkata",
            "capacity": 66000,
            "pitch_type": "balanced",
            "pace_bounce": "medium",
            "spin_assistance": "high",
            "avg_first_innings": 170,
            "avg_second_innings": 160,
            "dew_factor": "very_high",
            "boundary_size": "large",
            "characteristics": ["Dew heavy", "Spinners effective", "Big boundaries"],
            "best_for": ["All-rounders", "Spinners", "Boundary riders"]
        },
        "M. Chinnaswamy Stadium, Bangalore": {
            "city": "Bangalore",
            "capacity": 40000,
            "pitch_type": "batting_friendly",
            "pace_bounce": "very_high",
            "spin_assistance": "low",
            "avg_first_innings": 195,
            "avg_second_innings": 180,
            "dew_factor": "medium",
            "boundary_size": "very_small",
            "characteristics": ["Highest scoring", "Flat pitch", "Small boundaries"],
            "best_for": ["Power hitters", "Aggressive batsmen", "Death bowlers"]
        },
        "Arun Jaitley Stadium, Delhi": {
            "city": "Delhi",
            "capacity": 41820,
            "pitch_type": "balanced",
            "pace_bounce": "medium",
            "spin_assistance": "medium",
            "avg_first_innings": 175,
            "avg_second_innings": 165,
            "dew_factor": "high",
            "boundary_size": "medium",
            "characteristics": ["True bounce", "Even contest", "Dew factor"],
            "best_for": ["Balanced teams", "Quality bowlers", "Consistent batsmen"]
        },
        "Rajiv Gandhi International Stadium, Hyderabad": {
            "city": "Hyderabad",
            "capacity": 55000,
            "pitch_type": "spin_friendly",
            "pace_bounce": "low",
            "spin_assistance": "high",
            "avg_first_innings": 160,
            "avg_second_innings": 150,
            "dew_factor": "medium",
            "boundary_size": "large",
            "characteristics": ["Slow pitch", "Two-paced", "Spinners key"],
            "best_for": ["Spinners", "Smart batsmen", "Variations"]
        },
        "Punjab Cricket Association Stadium, Mohali": {
            "city": "Mohali",
            "capacity": 26000,
            "pitch_type": "pace_friendly",
            "pace_bounce": "high",
            "spin_assistance": "low",
            "avg_first_innings": 180,
            "avg_second_innings": 170,
            "dew_factor": "medium",
            "boundary_size": "medium",
            "characteristics": ["Pace and bounce", "Seam movement", "Good for batting"],
            "best_for": ["Fast bowlers", "Stroke makers", "Swing bowlers"]
        },
        "Sawai Mansingh Stadium, Jaipur": {
            "city": "Jaipur",
            "capacity": 30000,
            "pitch_type": "batting_friendly",
            "pace_bounce": "medium",
            "spin_assistance": "medium",
            "avg_first_innings": 185,
            "avg_second_innings": 175,
            "dew_factor": "high",
            "boundary_size": "small",
            "characteristics": ["High scoring", "Flat pitch", "Dew heavy"],
            "best_for": ["Aggressive batsmen", "Death bowlers", "All-rounders"]
        },
        "Narendra Modi Stadium, Ahmedabad": {
            "city": "Ahmedabad",
            "capacity": 132000,
            "pitch_type": "balanced",
            "pace_bounce": "medium",
            "spin_assistance": "medium",
            "avg_first_innings": 175,
            "avg_second_innings": 165,
            "dew_factor": "high",
            "boundary_size": "very_large",
            "characteristics": ["Huge boundaries", "Even pitch", "World's largest"],
            "best_for": ["Fitness", "Running between wickets", "Boundary riders"]
        },
        "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": {
            "city": "Lucknow",
            "capacity": 50000,
            "pitch_type": "balanced",
            "pace_bounce": "medium",
            "spin_assistance": "medium",
            "avg_first_innings": 170,
            "avg_second_innings": 160,
            "dew_factor": "high",
            "boundary_size": "medium",
            "characteristics": ["New venue", "True pitch", "Dew factor"],
            "best_for": ["Balanced teams", "Quality bowlers", "Smart batsmen"]
        },
        "Maharashtra Cricket Association Stadium, Pune": {
            "city": "Pune",
            "capacity": 37000,
            "pitch_type": "spin_friendly",
            "pace_bounce": "low",
            "spin_assistance": "high",
            "avg_first_innings": 165,
            "avg_second_innings": 155,
            "dew_factor": "medium",
            "boundary_size": "medium",
            "characteristics": ["Slow and low", "Spinners dominate", "Difficult to score"],
            "best_for": ["Spinners", "Anchor batsmen", "Smart bowling"]
        },
        "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam": {
            "city": "Visakhapatnam",
            "capacity": 27000,
            "pitch_type": "pace_friendly",
            "pace_bounce": "high",
            "spin_assistance": "low",
            "avg_first_innings": 175,
            "avg_second_innings": 165,
            "dew_factor": "high",
            "boundary_size": "medium",
            "characteristics": ["Pace and bounce", "Sea breeze", "Good for batting"],
            "best_for": ["Fast bowlers", "Stroke makers", "Swing bowlers"]
        },
        "Himachal Pradesh Cricket Association Stadium, Dharamsala": {
            "city": "Dharamsala",
            "capacity": 23000,
            "pitch_type": "pace_friendly",
            "pace_bounce": "very_high",
            "spin_assistance": "low",
            "avg_first_innings": 170,
            "avg_second_innings": 160,
            "dew_factor": "low",
            "boundary_size": "medium",
            "characteristics": ["High altitude", "Pace and bounce", "Scenic venue"],
            "best_for": ["Fast bowlers", "Power hitters", "Swing bowlers"]
        },
        "Holkar Cricket Stadium, Indore": {
            "city": "Indore",
            "pitch_type": "batting_friendly",
            "capacity": 30000,
            "pace_bounce": "medium",
            "spin_assistance": "low",
            "avg_first_innings": 190,
            "avg_second_innings": 180,
            "dew_factor": "medium",
            "boundary_size": "small",
            "characteristics": ["Flat pitch", "High scoring", "Batsman's paradise"],
            "best_for": ["Aggressive batsmen", "Power hitters", "Death bowlers"]
        }
    }
    
    @classmethod
    def get_all_stadiums(cls) -> List[str]:
        """Get list of all stadium names"""
        return list(cls.STADIUMS.keys())
    
    @classmethod
    def get_stadium_info(cls, stadium_name: str) -> Dict[str, Any]:
        """Get detailed information about a stadium"""
        return cls.STADIUMS.get(stadium_name, cls.STADIUMS["Wankhede Stadium, Mumbai"])
    
    @classmethod
    def get_pitch_report(cls, stadium_name: str, match_time: str = "night", weather: str = "clear") -> Dict[str, Any]:
        """Generate dynamic pitch report based on conditions"""
        stadium = cls.get_stadium_info(stadium_name)
        
        # Adjust characteristics based on conditions
        dew_impact = "high" if match_time == "night" and stadium["dew_factor"] in ["high", "very_high"] else stadium["dew_factor"]
        
        return {
            "venue": stadium_name,
            "city": stadium["city"],
            "pitch_type": stadium["pitch_type"],
            "pace_bounce": stadium["pace_bounce"],
            "spin_assistance": stadium["spin_assistance"],
            "dew_factor": dew_impact,
            "boundary_size": stadium["boundary_size"],
            "avg_first_innings": stadium["avg_first_innings"],
            "avg_second_innings": stadium["avg_second_innings"],
            "match_time": match_time,
            "weather": weather,
            "characteristics": stadium["characteristics"],
            "best_for": stadium["best_for"],
            "recommendation": cls._get_team_recommendation(stadium)
        }
    
    @classmethod
    def _get_team_recommendation(cls, stadium: Dict[str, Any]) -> str:
        """Get team composition recommendation based on pitch"""
        if stadium["pitch_type"] == "spin_friendly":
            return "Select 3 spinners, 2 pacers. Focus on anchor batsmen and smart runners."
        elif stadium["pitch_type"] == "pace_friendly":
            return "Select 3-4 pacers, 1-2 spinners. Focus on stroke makers and power hitters."
        elif stadium["pitch_type"] == "batting_friendly":
            return "Select quality death bowlers. Focus on power hitters and aggressive batsmen."
        else:
            return "Select balanced attack with 2 spinners, 3 pacers. Mix of aggression and stability."


# Initialize database
stadium_db = StadiumDatabase()
