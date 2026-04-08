"""
Grader for Task 2: Playing XI Selection
ENHANCED VERSION - Fixed spinner/pacer detection, improved pitch scoring
"""
from typing import Dict, Any, List


class PlayingXIGrader:
    """Grade Playing XI selection decisions"""

    WEIGHTS = {
        "team_balance": 0.30,
        "pitch_fit": 0.40,
        "opponent_matchup": 0.30
    }

    def __init__(self):
        self.squad_lookup = {}

    def _is_spinner(self, player: Dict) -> bool:
        """Determine if a player is a spinner using bowling_type field first, then economy heuristic."""
        bowling_type = player.get("bowling_type", "")
        if bowling_type == "spin":
            return True
        if bowling_type == "pace":
            return False
        economy = player.get("bowling_economy")
        if economy is not None and player["role"] in ["bowler", "all_rounder"]:
            return 6.5 <= economy <= 9.0
        return False

    def _is_pacer(self, player: Dict) -> bool:
        """Determine if a player is a pacer using bowling_type field first, then economy heuristic."""
        bowling_type = player.get("bowling_type", "")
        if bowling_type == "pace":
            return True
        if bowling_type == "spin":
            return False
        economy = player.get("bowling_economy")
        if economy is not None and player["role"] in ["bowler", "all_rounder"]:
            return economy < 8.5
        return False

    def _can_bowl(self, player: Dict) -> bool:
        return player.get("bowling_economy") is not None

    def validate_structure(self, action: Dict[str, Any], squad: List[Dict]) -> tuple:
        self.squad_lookup = {p["name"]: p for p in squad}

        if "playing_xi" not in action:
            return False, "Missing 'playing_xi' field"
        if "batting_order" not in action:
            return False, "Missing 'batting_order' field"
        if "bowling_combination" not in action:
            return False, "Missing 'bowling_combination' field"

        playing_xi = action["playing_xi"]
        batting_order = action["batting_order"]

        if len(playing_xi) != 11:
            return False, f"Must select exactly 11 players, got {len(playing_xi)}"

        for player in playing_xi:
            if player not in self.squad_lookup:
                return False, f"Player '{player}' not in squad"

        if set(batting_order) != set(playing_xi):
            return False, "Batting order must contain same players as playing XI"

        if len(batting_order) != 11:
            return False, "Batting order must have exactly 11 players"

        return True, ""

    def score_team_balance(self, playing_xi: List[str]) -> Dict[str, Any]:
        """Score team balance (0.0 to 1.0) - MINIMUM 5 BOWLERS REQUIRED"""
        players = [self.squad_lookup[name] for name in playing_xi]

        wicket_keepers = sum(1 for p in players if p["role"] == "wicket_keeper")
        batsmen = sum(1 for p in players if p["role"] == "batsman")
        bowlers = sum(1 for p in players if p["role"] == "bowler")
        all_rounders = sum(1 for p in players if p["role"] == "all_rounder")

        bowling_options = sum(1 for p in players if self._can_bowl(p))
        pacers = sum(1 for p in players if self._is_pacer(p))
        spinners = sum(1 for p in players if self._is_spinner(p))

        score = 1.0
        issues = []

        if bowling_options < 5:
            score -= 0.5
            issues.append(f"CRITICAL: Need minimum 5 bowling options, got {bowling_options}")
        elif bowling_options == 5:
            issues.append(f"Acceptable: {bowling_options} bowling options (minimum met)")
        else:
            issues.append(f"Good: {bowling_options} bowling options")

        if wicket_keepers != 1:
            score -= 0.3
            issues.append(f"Need 1 wicket-keeper, got {wicket_keepers}")

        total_batsmen = batsmen + wicket_keepers
        if total_batsmen < 4 or total_batsmen > 7:
            score -= 0.2
            issues.append(f"Need 4-7 batsmen, got {total_batsmen}")

        total_bowlers = bowlers + all_rounders
        if total_bowlers < 4 or total_bowlers > 7:
            score -= 0.2
            issues.append(f"Need 4-7 bowlers, got {total_bowlers}")

        if all_rounders < 2:
            score -= 0.1
            issues.append(f"Recommended: at least 2 all-rounders, got {all_rounders}")

        if pacers < 2:
            score -= 0.1
            issues.append(f"Recommended: at least 2 pacers, got {pacers}")

        if spinners < 1:
            score -= 0.1
            issues.append(f"Recommended: at least 1 spinner, got {spinners}")

        return {
            "score": max(0.0, score),
            "composition": {
                "wicket_keepers": wicket_keepers,
                "batsmen": batsmen,
                "bowlers": bowlers,
                "all_rounders": all_rounders,
                "bowling_options": bowling_options,
                "pacers": pacers,
                "spinners": spinners
            },
            "issues": issues
        }

    def score_pitch_fit(self, playing_xi: List[str], pitch: Dict[str, Any]) -> Dict[str, Any]:
        """Score how well the XI fits the pitch conditions"""
        players = [self.squad_lookup[name] for name in playing_xi]
        surface_type = pitch.get("surface_type") or pitch.get("type", "balanced")

        spinners = [p for p in players if self._is_spinner(p)]
        pacers = [p for p in players if self._is_pacer(p)]

        batsmen_sr = [
            p["strike_rate"]
            for p in players
            if p["role"] in ["batsman", "wicket_keeper", "all_rounder"] and p.get("strike_rate")
        ]
        avg_strike_rate = sum(batsmen_sr) / len(batsmen_sr) if batsmen_sr else 0

        score = 0.5
        feedback = []

        if surface_type == "spin_friendly":
            if len(spinners) >= 3:
                score += 0.4
                feedback.append(f"Excellent: {len(spinners)} spinners for spin-friendly pitch")
            elif len(spinners) >= 2:
                score += 0.3
                feedback.append(f"Good: {len(spinners)} spinners for spin-friendly pitch")
            else:
                score -= 0.2
                feedback.append(f"Issue: Only {len(spinners)} spinner(s) on spin-friendly pitch")
            if avg_strike_rate < 135:
                score += 0.1
                feedback.append("Good: Anchor batsmen suit spin conditions")

        elif surface_type == "pace_friendly":
            if len(pacers) >= 4:
                score += 0.4
                feedback.append(f"Excellent: {len(pacers)} pacers for pace-friendly pitch")
            elif len(pacers) >= 3:
                score += 0.3
                feedback.append(f"Good: {len(pacers)} pacers for pace-friendly pitch")
            else:
                score -= 0.2
                feedback.append(f"Issue: Only {len(pacers)} pacer(s) on pace-friendly pitch")
            if avg_strike_rate > 135:
                score += 0.1
                feedback.append("Good: Aggressive batsmen suit pace-friendly pitch")

        elif surface_type == "batting_friendly":
            if len(pacers) >= 2 and len(spinners) >= 1:
                score += 0.3
                feedback.append("Good: Mixed bowling attack for batting track")
            if avg_strike_rate > 140:
                score += 0.2
                feedback.append("Good: Power hitters for batting-friendly pitch")

        else:  # balanced
            if len(spinners) >= 1 and len(pacers) >= 2:
                score += 0.4
                feedback.append("Good: Balanced bowling attack")
            else:
                score -= 0.1
                feedback.append("Issue: Unbalanced bowling attack")

        return {
            "score": max(0.0, min(1.0, score)),
            "spinners_count": len(spinners),
            "pacers_count": len(pacers),
            "avg_strike_rate": round(avg_strike_rate, 2),
            "feedback": feedback
        }

    def score_opponent_matchup(self, playing_xi: List[str], opponent: Dict[str, Any], pitch: Dict[str, Any]) -> Dict[str, Any]:
        """Score how well the XI exploits opponent weaknesses"""
        players = [self.squad_lookup[name] for name in playing_xi]
        weakness = opponent.get("weakness_against", "pace")

        score = 0.5
        feedback = []

        spinners = sum(1 for p in players if self._is_spinner(p))
        pacers = sum(1 for p in players if self._is_pacer(p))

        if weakness == "spin":
            if spinners >= 3:
                score += 0.45
                feedback.append(f"Excellent: {spinners} spinners vs spin-weak opponent")
            elif spinners >= 2:
                score += 0.3
                feedback.append(f"Good: {spinners} spinners vs spin-weak opponent")
            else:
                score -= 0.1
                feedback.append(f"Missed: Opponent weak against spin, only {spinners} spinner(s)")
        elif weakness == "pace":
            if pacers >= 4:
                score += 0.45
                feedback.append(f"Excellent: {pacers} pacers vs pace-weak opponent")
            elif pacers >= 3:
                score += 0.3
                feedback.append(f"Good: {pacers} pacers vs pace-weak opponent")
            else:
                score -= 0.1
                feedback.append(f"Missed: Opponent weak against pace, only {pacers} pacer(s)")
        elif weakness == "swing":
            if pacers >= 2:
                score += 0.3
                feedback.append("Good: Pace attack vs swing-weak opponent")
            else:
                score -= 0.1
                feedback.append("Missed: Opponent weak against swing")

        death_specialists = [p for p in players if self._can_bowl(p) and p.get("bowling_economy", 10) < 8.5]
        if opponent.get("death_bowling_strength", 75) > 75 and len(death_specialists) >= 2:
            score += 0.05
            feedback.append(f"Good: {len(death_specialists)} death bowling specialists selected")

        return {
            "score": max(0.0, min(1.0, score)),
            "feedback": feedback
        }

    def grade(self, action: Dict[str, Any], scenario: Dict[str, Any]) -> Dict[str, Any]:
        squad = scenario["squad"]
        pitch = scenario["pitch_report"]
        opponent = scenario["opponent"]

        valid, error = self.validate_structure(action, squad)
        if not valid:
            return {"score": 0.01, "error": error, "breakdown": {}}

        balance_result = self.score_team_balance(action["playing_xi"])
        pitch_result = self.score_pitch_fit(action["playing_xi"], pitch)
        opponent_result = self.score_opponent_matchup(action["playing_xi"], opponent, pitch)

        final_score = (
            balance_result["score"] * self.WEIGHTS["team_balance"] +
            pitch_result["score"] * self.WEIGHTS["pitch_fit"] +
            opponent_result["score"] * self.WEIGHTS["opponent_matchup"]
        )

        final_score = max(0.01, min(0.98, final_score))
        return {
            "score": round(final_score, 3),
            "breakdown": {
                "team_balance": {
                    "score": round(balance_result["score"], 3),
                    "weight": self.WEIGHTS["team_balance"],
                    "composition": balance_result["composition"],
                    "issues": balance_result["issues"]
                },
                "pitch_fit": {
                    "score": round(pitch_result["score"], 3),
                    "weight": self.WEIGHTS["pitch_fit"],
                    "spinners": pitch_result["spinners_count"],
                    "pacers": pitch_result["pacers_count"],
                    "feedback": pitch_result["feedback"]
                },
                "opponent_matchup": {
                    "score": round(opponent_result["score"], 3),
                    "weight": self.WEIGHTS["opponent_matchup"],
                    "feedback": opponent_result["feedback"]
                }
            },
            "selected_xi": action["playing_xi"]
        }
