"""
Grader for Task 1: Staff Allocation
"""
from typing import Dict, Any


class StaffAllocationGrader:
    """Grade staff allocation decisions"""
    
    # Acceptable deviation thresholds
    SECURITY_TOLERANCE = 0.15  # ±15%
    MEDICAL_TOLERANCE = 0.20   # ±20%
    TICKETING_TOLERANCE = 0.25 # ±25%
    
    # Scoring weights
    WEIGHTS = {
        "security_accuracy": 0.35,
        "medical_accuracy": 0.25,
        "ticketing_accuracy": 0.20,
        "no_overstaffing": 0.10,
        "no_understaffing": 0.10
    }
    
    def calculate_deviation(self, actual: int, optimal: int) -> float:
        """Calculate percentage deviation from optimal"""
        if optimal == 0:
            return 0.0
        return abs(actual - optimal) / optimal
    
    def score_category(self, actual: int, optimal: int, tolerance: float) -> float:
        """Score a single category (0.0 to 1.0)"""
        deviation = self.calculate_deviation(actual, optimal)
        
        if deviation <= tolerance:
            # Within tolerance: full score
            return 1.0
        elif deviation <= tolerance * 2:
            # Beyond tolerance but not terrible: partial score
            return max(0.0, 1.0 - (deviation - tolerance) / tolerance)
        else:
            # Way off: zero score
            return 0.0
    
    def grade(self, action: Dict[str, Any], optimal: Dict[str, int]) -> Dict[str, Any]:
        """
        Grade the staff allocation action
        
        Args:
            action: Agent's allocation decision
            optimal: Optimal allocation from task generator
            
        Returns:
            Dict with score and detailed breakdown
        """
        # Validate action structure
        required_fields = ["security_per_gate", "total_security", "medical_personnel", "ticketing_staff"]
        for field in required_fields:
            if field not in action:
                return {
                    "score": 0.0,
                    "error": f"Missing required field: {field}",
                    "breakdown": {}
                }
        
        # Score each category
        security_score = self.score_category(
            action["total_security"],
            optimal["total_security"],
            self.SECURITY_TOLERANCE
        )
        
        medical_score = self.score_category(
            action["medical_personnel"],
            optimal["medical_personnel"],
            self.MEDICAL_TOLERANCE
        )
        
        ticketing_score = self.score_category(
            action["ticketing_staff"],
            optimal["ticketing_staff"],
            self.TICKETING_TOLERANCE
        )
        
        # Check for overstaffing (total staff > 1.3x optimal)
        total_actual = action["total_security"] + action["medical_personnel"] + action["ticketing_staff"]
        total_optimal = optimal["total_security"] + optimal["medical_personnel"] + optimal["ticketing_staff"]
        overstaffing_ratio = total_actual / total_optimal if total_optimal > 0 else 1.0
        
        overstaffing_score = 1.0 if overstaffing_ratio <= 1.3 else max(0.0, 2.0 - overstaffing_ratio)
        
        # Check for understaffing (total staff < 0.8x optimal)
        understaffing_score = 1.0 if overstaffing_ratio >= 0.8 else max(0.0, overstaffing_ratio / 0.8)
        
        # Calculate weighted final score
        final_score = (
            security_score * self.WEIGHTS["security_accuracy"] +
            medical_score * self.WEIGHTS["medical_accuracy"] +
            ticketing_score * self.WEIGHTS["ticketing_accuracy"] +
            overstaffing_score * self.WEIGHTS["no_overstaffing"] +
            understaffing_score * self.WEIGHTS["no_understaffing"]
        )
        
        return {
            "score": round(final_score, 3),
            "breakdown": {
                "security_score": round(security_score, 3),
                "medical_score": round(medical_score, 3),
                "ticketing_score": round(ticketing_score, 3),
                "overstaffing_score": round(overstaffing_score, 3),
                "understaffing_score": round(understaffing_score, 3),
                "total_staffing_ratio": round(overstaffing_ratio, 3)
            },
            "optimal_values": optimal,
            "agent_values": {
                "total_security": action["total_security"],
                "medical_personnel": action["medical_personnel"],
                "ticketing_staff": action["ticketing_staff"]
            }
        }
