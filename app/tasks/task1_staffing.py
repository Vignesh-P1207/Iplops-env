"""
Task 1: Match Day Staff Allocation
Difficulty: Easy
"""
import random
from typing import Dict, Any
from app.models import StadiumInfo, MatchType


class StaffAllocationTask:
    """Generate staff allocation scenarios for IPL match days"""
    
    STADIUMS = [
        {"name": "Wankhede Stadium", "capacity": 33000, "gates": 8, "medical_stations": 4},
        {"name": "Eden Gardens", "capacity": 66000, "gates": 12, "medical_stations": 6},
        {"name": "M. Chinnaswamy Stadium", "capacity": 40000, "gates": 10, "medical_stations": 5},
        {"name": "Feroz Shah Kotla", "capacity": 41000, "gates": 9, "medical_stations": 5},
        {"name": "Rajiv Gandhi Intl Stadium", "capacity": 55000, "gates": 11, "medical_stations": 6},
        {"name": "MA Chidambaram Stadium", "capacity": 50000, "gates": 10, "medical_stations": 5},
        {"name": "Sawai Mansingh Stadium", "capacity": 30000, "gates": 7, "medical_stations": 4},
        {"name": "Punjab Cricket Association", "capacity": 26000, "gates": 6, "medical_stations": 3},
    ]
    
    # Safety standards (per 1000 people)
    SECURITY_RATIO = {
        MatchType.LEAGUE: 2.5,      # 2.5 security per 1000 people
        MatchType.PLAYOFF: 3.5,     # 3.5 security per 1000 people
        MatchType.FINAL: 5.0,       # 5.0 security per 1000 people
    }
    
    MEDICAL_RATIO = 1.5  # 1.5 medical personnel per 1000 people
    TICKETING_RATIO = 0.8  # 0.8 ticketing staff per 1000 people
    
    def __init__(self):
        self.current_scenario = None
    
    def generate_scenario(self) -> Dict[str, Any]:
        """Generate a random staff allocation scenario"""
        stadium = random.choice(self.STADIUMS)
        match_type = random.choice(list(MatchType))
        crowd_percentage = random.uniform(0.65, 0.98)  # 65% to 98% capacity
        
        self.current_scenario = {
            "stadium": StadiumInfo(
                name=stadium["name"],
                capacity=stadium["capacity"],
                expected_crowd_percentage=round(crowd_percentage, 2),
                match_type=match_type,
                gates_count=stadium["gates"],
                medical_stations=stadium["medical_stations"]
            ),
            "instructions": (
                "Allocate staff for this IPL match. Consider:\n"
                "- Security staff per gate and total security\n"
                "- Medical personnel across all stations\n"
                "- Ticketing counter staff\n"
                "Ensure compliance with safety ratios while avoiding over-staffing."
            )
        }
        
        return {
            "stadium": self.current_scenario["stadium"].model_dump(),
            "instructions": self.current_scenario["instructions"]
        }
    
    def get_optimal_allocation(self) -> Dict[str, int]:
        """Calculate optimal staff allocation for grading"""
        if not self.current_scenario:
            raise ValueError("No scenario generated")
        
        stadium = self.current_scenario["stadium"]
        expected_crowd = stadium.capacity * stadium.expected_crowd_percentage
        
        # Calculate optimal values
        security_ratio = self.SECURITY_RATIO[stadium.match_type]
        optimal_security = int((expected_crowd / 1000) * security_ratio)
        optimal_security_per_gate = max(2, optimal_security // stadium.gates_count)
        
        optimal_medical = int((expected_crowd / 1000) * self.MEDICAL_RATIO)
        optimal_ticketing = int((expected_crowd / 1000) * self.TICKETING_RATIO)
        
        return {
            "security_per_gate": optimal_security_per_gate,
            "total_security": optimal_security,
            "medical_personnel": optimal_medical,
            "ticketing_staff": optimal_ticketing,
            "expected_crowd": int(expected_crowd)
        }
