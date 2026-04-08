"""
AI-powered Playing XI selector using OpenAI GPT for intelligent team selection
"""
from typing import Dict, List, Any, Tuple
import random
import os
import json


class IntelligentTeamSelector:
    """Select optimal Playing XI using OpenAI GPT-4 for decision making"""
    
    def __init__(self):
        # Selection criteria weights for algorithmic fallback
        self.weights = {
            "recent_form": 0.25,      # 25% - Current performance
            "batting_avg": 0.15,      # 15% - Career stats
            "strike_rate": 0.10,      # 10% - Scoring ability
            "pitch_suitability": 0.35, # 35% - Match conditions (MOST IMPORTANT)
            "opponent_matchup": 0.15   # 15% - Exploit weaknesses
        }
        
        self.use_openai = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")
        if self.use_openai:
            try:
                from openai import OpenAI
                api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
                api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")
                self.client = OpenAI(base_url=api_base, api_key=api_key)
                print("[AI] OpenAI client initialized - will use GPT for team selection")
            except Exception as e:
                print(f"[AI] OpenAI not available: {e}, using algorithmic selection")
                self.client = None
        else:
            self.client = None
            print("[AI] No API key found, using algorithmic selection")
    
    def select_playing_xi(
        self,
        squad: List[Dict[str, Any]],
        pitch_report: Dict[str, Any],
        opponent_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Select optimal Playing XI using GPT-4 AI or algorithmic fallback
        """
        
        print("\n" + "="*80)
        print("🤖 AI TEAM SELECTION")
        print("="*80)
        print(f"📍 Venue: {pitch_report.get('venue', 'Unknown')}")
        print(f"🏟️  Pitch: {pitch_report.get('surface_type') or pitch_report.get('pitch_type', 'unknown').upper()}")
        print(f"🎯 Opponent: {opponent_profile.get('team_name', 'Unknown')}")
        print(f"👥 Squad Size: {len(squad)} players")
        
        # Try GPT-4 selection first
        if self.client:
            try:
                print("🧠 Using OpenAI GPT-4 for intelligent team selection...")
                return self._select_with_gpt(squad, pitch_report, opponent_profile)
            except Exception as e:
                print(f"⚠️  GPT selection failed: {e}")
                print("📊 Falling back to algorithmic selection...")
        else:
            print("📊 Using algorithmic selection (no OpenAI API key)")
        
        # Fallback to algorithmic selection
        return self._select_algorithmically(squad, pitch_report, opponent_profile)

    
    def _select_with_gpt(
        self,
        squad: List[Dict[str, Any]],
        pitch_report: Dict[str, Any],
        opponent_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Use GPT-4 to select the team"""
        
        # Prepare squad data for GPT
        squad_summary = []
        for i, player in enumerate(squad, 1):
            squad_summary.append({
                "id": i,
                "name": player["name"],
                "role": player["role"],
                "batting_avg": player.get("batting_avg"),
                "strike_rate": player.get("strike_rate"),
                "recent_form": player.get("recent_form"),
                "bowling_economy": player.get("bowling_economy"),
                "wickets": player.get("wickets"),
                "injury_status": player.get("injury_status", "fit")
            })
        
        # Create prompt for GPT
        prompt = f"""You are an expert IPL cricket team selector. Select the best Playing XI from the squad below.

MATCH CONDITIONS:
- Venue: {pitch_report.get('venue')}
- Pitch Type: {pitch_report.get('pitch_type')}
- Pitch Characteristics: {', '.join(pitch_report.get('characteristics', []))}
- Opponent: {opponent_profile.get('team_name')}
- Opponent Weakness: {opponent_profile.get('weakness_against')}

SQUAD (20 players):
{json.dumps(squad_summary, indent=2)}

SELECTION RULES:
1. Select EXACTLY 11 players
2. Must include 1 wicket-keeper
3. Must have MINIMUM 5 bowling options (bowlers + all-rounders who can bowl)
4. Prefer players with high recent_form
5. Match player types to pitch (spinners for spin-friendly, pacers for pace-friendly, power hitters for batting-friendly)
6. Exploit opponent weakness
7. Avoid injured players (injury_status: "doubtful")

Respond with ONLY a JSON object in this exact format:
{{
  "selected_player_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "reasoning": "Brief explanation of why these 11 players were selected",
  "key_strategy": "Main strategy for this pitch and opponent"
}}"""
        
        # Call GPT-4
        response = self.client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4"),
            messages=[
                {"role": "system", "content": "You are an expert IPL cricket analyst and team selector."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse GPT response
        gpt_response = response.choices[0].message.content.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in gpt_response:
            gpt_response = gpt_response.split("```json")[1].split("```")[0].strip()
        elif "```" in gpt_response:
            gpt_response = gpt_response.split("```")[1].split("```")[0].strip()
        
        selection_data = json.loads(gpt_response)
        
        # Get selected players
        selected_ids = selection_data["selected_player_ids"]
        selected_players = [squad[id-1] for id in selected_ids]
        
        print(f"✅ GPT-4 selected {len(selected_players)} players")
        print(f"💡 Strategy: {selection_data.get('key_strategy', 'N/A')}")
        
        # Create batting order and bowling plan
        batting_order = self._create_batting_order(selected_players)
        bowling_plan = self._create_bowling_plan(selected_players, pitch_report, opponent_profile)
        
        return {
            "selected_players": [p["name"] for p in selected_players],
            "selected_players_full": selected_players,
            "batting_order": batting_order,
            "bowling_plan": bowling_plan,
            "reasoning": {
                "pitch_analysis": f"{pitch_report.get('pitch_type')} pitch at {pitch_report.get('venue')}",
                "team_composition": f"{len([p for p in selected_players if p['role']=='batsman'])} batsmen, {len([p for p in selected_players if p['role']=='bowler'])} bowlers",
                "key_players": [p["name"] for p in selected_players[:3]],
                "strategy": selection_data.get("key_strategy", "Balanced approach"),
                "opponent_weakness": f"Opponent weak against {opponent_profile.get('weakness_against')}",
                "gpt_reasoning": selection_data.get("reasoning", "")
            },
            "team_strength": self._calculate_team_strength(selected_players, pitch_report),
            "selection_method": "GPT-4 AI",
            "selection_criteria": {
                "method": "OpenAI GPT-4",
                "model": os.getenv("MODEL_NAME", "gpt-4"),
                "approach": "Natural language AI analysis"
            }
        }

    
    def _select_algorithmically(
        self,
        squad: List[Dict[str, Any]],
        pitch_report: Dict[str, Any],
        opponent_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback algorithmic selection with multi-criteria analysis"""
        
        print("\n📊 ALGORITHMIC SELECTION - MULTI-CRITERIA ANALYSIS")
        print("-" * 80)
        
        # Score each player
        scored_players = []
        for player in squad:
            score = self._calculate_player_score(player, pitch_report, opponent_profile)
            scored_players.append({**player, "selection_score": score})
        
        scored_players.sort(key=lambda x: x["selection_score"], reverse=True)
        
        print("\n📊 TOP 15 PLAYERS BY SCORE:")
        for i, p in enumerate(scored_players[:15], 1):
            breakdown = p.get("score_breakdown", {})
            print(f"{i:2d}. {p['name']:25s} | Score: {p['selection_score']:.3f} | "
                  f"Form:{breakdown.get('form', 0):.2f} Pitch:{breakdown.get('pitch', 0):.2f} | {p['role'].upper()}")
        
        # Select balanced team
        selected = self._select_balanced_team(scored_players, pitch_report)
        
        batting_order = self._create_batting_order(selected)
        bowling_plan = self._create_bowling_plan(selected, pitch_report, opponent_profile)
        
        return {
            "selected_players": [p["name"] for p in selected],
            "selected_players_full": selected,
            "batting_order": batting_order,
            "bowling_plan": bowling_plan,
            "reasoning": {
                "pitch_analysis": f"{pitch_report.get('pitch_type')} pitch at {pitch_report.get('venue')}",
                "team_composition": f"{sum(1 for p in selected if p['role']=='batsman')} batsmen, {sum(1 for p in selected if p['role']=='bowler')} bowlers",
                "key_players": [p["name"] for p in selected[:3]],
                "strategy": pitch_report.get("recommendation", "Balanced approach"),
                "opponent_weakness": f"Opponent weak against {opponent_profile.get('weakness_against')}"
            },
            "team_strength": self._calculate_team_strength(selected, pitch_report),
            "selection_method": "Algorithmic",
            "selection_criteria": {
                "method": "Multi-criteria scoring",
                "form_weight": f"{self.weights['recent_form']*100:.0f}%",
                "pitch_weight": f"{self.weights['pitch_suitability']*100:.0f}%",
                "approach": "Form + Pitch + Stats based"
            }
        }
    
    def _calculate_player_score(
        self,
        player: Dict[str, Any],
        pitch_report: Dict[str, Any],
        opponent_profile: Dict[str, Any]
    ) -> float:
        """Calculate player score using multi-criteria analysis"""
        
        score = 0.0
        breakdown = {}
        
        # Recent Form (25%)
        form = player.get("recent_form", 50)
        form_score = 1.0 if form > 85 else 0.85 if form > 75 else 0.70 if form > 65 else 0.55 if form > 55 else 0.40
        score += form_score * self.weights["recent_form"]
        breakdown["form"] = form_score
        
        # Batting Average (15%)
        avg = player.get("batting_avg", 20)
        avg_score = 1.0 if avg > 35 else 0.85 if avg > 30 else 0.70 if avg > 25 else 0.55 if avg > 20 else 0.40
        score += avg_score * self.weights["batting_avg"]
        breakdown["avg"] = avg_score
        
        # Strike Rate (10%)
        sr = player.get("strike_rate", 120)
        sr_score = 1.0 if sr > 145 else 0.85 if sr > 135 else 0.70 if sr > 125 else 0.55 if sr > 115 else 0.40
        score += sr_score * self.weights["strike_rate"]
        breakdown["sr"] = sr_score
        
        # Pitch Suitability (35%) - MOST IMPORTANT
        pitch_score = self._calculate_pitch_suitability(player, pitch_report)
        score += pitch_score * self.weights["pitch_suitability"]
        breakdown["pitch"] = pitch_score
        
        # Opponent Matchup (15%)
        matchup_score = self._calculate_opponent_matchup(player, opponent_profile)
        score += matchup_score * self.weights["opponent_matchup"]
        breakdown["opponent"] = matchup_score
        
        # Bonuses
        if player.get("role") == "all_rounder":
            score += 0.05
        if player.get("matches", 0) > 100:
            score += 0.03
        if player.get("injury_status") == "doubtful":
            score -= 0.15
        wickets = player.get("wickets")
        if wickets and wickets > 40:
            score += 0.04
        
        player["score_breakdown"] = breakdown
        return min(1.0, max(0.0, score))
    
    def _calculate_pitch_suitability(self, player: Dict[str, Any], pitch_report: Dict[str, Any]) -> float:
        """Calculate pitch suitability - dynamic based on pitch type"""
        
        pitch_type = pitch_report.get("surface_type") or pitch_report.get("pitch_type", "balanced")
        role = player.get("role", "batsman")
        bowling_economy = player.get("bowling_economy")
        strike_rate = player.get("strike_rate", 120)
        batting_avg = player.get("batting_avg", 20)
        
        score = 0.5
        
        if pitch_type == "spin_friendly":
            if role in ["bowler", "all_rounder"] and bowling_economy:
                score = 0.95 if 7.0 <= bowling_economy <= 8.5 else 0.85 if bowling_economy < 7.0 else 0.70 if bowling_economy < 9.0 else 0.50
            elif role in ["batsman", "wicket_keeper"]:
                score = 0.90 if strike_rate < 130 and batting_avg > 30 else 0.75 if strike_rate < 135 else 0.60
        
        elif pitch_type == "pace_friendly":
            if role in ["bowler", "all_rounder"] and bowling_economy:
                wickets = player.get("wickets", 0)
                score = 0.95 if bowling_economy < 8.5 and wickets > 40 else 0.85 if bowling_economy < 9.0 and wickets > 25 else 0.70 if bowling_economy < 9.5 else 0.55
            elif role in ["batsman", "wicket_keeper"]:
                score = 0.90 if strike_rate > 140 and batting_avg > 25 else 0.80 if strike_rate > 135 else 0.65
        
        elif pitch_type == "batting_friendly":
            if role in ["bowler", "all_rounder"] and bowling_economy:
                score = 0.95 if bowling_economy < 7.5 else 0.85 if bowling_economy < 8.0 else 0.70 if bowling_economy < 8.5 else 0.50
            elif role in ["batsman", "wicket_keeper"]:
                score = 0.95 if strike_rate > 145 else 0.85 if strike_rate > 135 else 0.70
        
        else:  # balanced
            if role == "all_rounder":
                score = 0.90
            elif role in ["bowler", "all_rounder"] and bowling_economy:
                score = 0.80 if bowling_economy < 8.5 else 0.65
            elif role in ["batsman", "wicket_keeper"]:
                score = 0.85 if 130 < strike_rate < 145 and batting_avg > 28 else 0.70
        
        return min(1.0, score)
    
    def _calculate_opponent_matchup(self, player: Dict[str, Any], opponent_profile: Dict[str, Any]) -> float:
        """Calculate opponent matchup advantage"""
        
        weakness = opponent_profile.get("weakness_against", "spin")
        role = player.get("role", "batsman")
        
        if role in ["bowler", "all_rounder"] and player.get("bowling_economy"):
            if weakness == "spin" and player.get("bowling_economy", 10) < 8.5:
                return 0.9
            elif weakness == "pace" and player.get("wickets", 0) > 30:
                return 0.9
            else:
                return 0.7
        
        if role in ["batsman", "wicket_keeper"]:
            return 0.8 if opponent_profile.get("death_bowling_strength", 75) < 70 else 0.7
        
        return 0.65
    
    def _select_balanced_team(self, scored_players: List[Dict[str, Any]], pitch_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select 11 players with role balance - MINIMUM 5 BOWLERS"""
        
        selected = []
        role_counts = {"batsman": 0, "bowler": 0, "all_rounder": 0, "wicket_keeper": 0}
        
        pitch_type = pitch_report.get("surface_type") or pitch_report.get("pitch_type", "balanced")
        
        # Dynamic composition based on pitch
        if pitch_type == "spin_friendly":
            required = {"wicket_keeper": 1, "batsman": 3, "all_rounder": 3, "bowler": 4}
            print(f"[PITCH] Spin-friendly: More spinners and all-rounders")
        elif pitch_type == "pace_friendly":
            required = {"wicket_keeper": 1, "batsman": 3, "all_rounder": 2, "bowler": 5}
            print(f"[PITCH] Pace-friendly: More fast bowlers")
        elif pitch_type == "batting_friendly":
            required = {"wicket_keeper": 1, "batsman": 4, "all_rounder": 2, "bowler": 4}
            print(f"[PITCH] Batting-friendly: Power hitters + quality bowlers")
        else:
            required = {"wicket_keeper": 1, "batsman": 3, "all_rounder": 3, "bowler": 4}
            print(f"[PITCH] Balanced: Standard composition")
        
        # Select wicket-keeper first
        for player in scored_players:
            if player["role"] == "wicket_keeper" and role_counts["wicket_keeper"] < required["wicket_keeper"]:
                selected.append(player)
                role_counts["wicket_keeper"] += 1
                print(f"[SELECTED] WK: {player['name']} (Score: {player['selection_score']:.3f})")
                break
        
        # Select by score with role balance
        for player in scored_players:
            if len(selected) >= 11:
                break
            role = player["role"]
            if player not in selected and role_counts[role] < required[role]:
                selected.append(player)
                role_counts[role] += 1
                print(f"[SELECTED] {role.upper()}: {player['name']} (Score: {player['selection_score']:.3f})")
        
        # Fill remaining slots
        for player in scored_players:
            if len(selected) >= 11:
                break
            if player not in selected:
                selected.append(player)
                print(f"[SELECTED] FILL: {player['name']} (Score: {player['selection_score']:.3f})")
        
        # Validate minimum 5 bowlers
        bowling_count = sum(1 for p in selected if p.get("bowling_economy") is not None)
        
        if bowling_count < 5:
            print(f"[WARNING] Only {bowling_count} bowlers. Adjusting...")
            batsmen_indices = [i for i, p in enumerate(selected) if p["role"] == "batsman" and p.get("bowling_economy") is None]
            available_bowlers = [p for p in scored_players if p not in selected and p.get("bowling_economy") is not None]
            available_bowlers.sort(key=lambda x: x["selection_score"], reverse=True)
            
            replacements_needed = 5 - bowling_count
            for i in range(min(replacements_needed, len(batsmen_indices), len(available_bowlers))):
                old_player = selected[batsmen_indices[i]]
                new_player = available_bowlers[i]
                selected[batsmen_indices[i]] = new_player
                print(f"[REPLACED] {old_player['name']} -> {new_player['name']} (bowling option)")
        
        print(f"[FINAL] {bowling_count} bowling options, Composition: {role_counts}")
        return selected[:11]
    
    def _create_batting_order(self, selected: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create optimal batting order"""
        
        openers = []
        middle_order = []
        finishers = []
        tail = []
        
        for player in selected:
            role = player["role"]
            sr = player.get("strike_rate", 120)
            avg = player.get("batting_avg", 20)
            
            if role in ["batsman", "wicket_keeper"]:
                if avg > 30 and sr < 135:
                    openers.append(player)
                elif sr > 140:
                    finishers.append(player)
                else:
                    middle_order.append(player)
            elif role == "all_rounder":
                middle_order.append(player)
            else:
                tail.append(player)
        
        openers.sort(key=lambda x: x.get("batting_avg", 0), reverse=True)
        middle_order.sort(key=lambda x: x.get("recent_form", 0), reverse=True)
        finishers.sort(key=lambda x: x.get("strike_rate", 0), reverse=True)
        
        batting_order = openers[:2] + middle_order[:4] + finishers[:2] + tail[:3]
        
        return [
            {
                "position": i + 1,
                "player_name": player["name"],
                "role": player["role"],
                "reasoning": self._get_batting_position_reasoning(i + 1, player)
            }
            for i, player in enumerate(batting_order[:11])
        ]
    
    def _get_batting_position_reasoning(self, position: int, player: Dict[str, Any]) -> str:
        """Get reasoning for batting position"""
        if position <= 2:
            return f"Opener - Avg: {player.get('batting_avg', 0):.1f}, SR: {player.get('strike_rate', 0):.1f}"
        elif position <= 5:
            return f"Middle order - Form: {player.get('recent_form', 0)}, Avg: {player.get('batting_avg', 0):.1f}"
        elif position <= 7:
            return f"Finisher - SR: {player.get('strike_rate', 0):.1f}, Power hitter"
        else:
            return f"Tail - Bowling all-rounder"
    
    def _create_bowling_plan(
        self,
        selected: List[Dict[str, Any]],
        pitch_report: Dict[str, Any],
        opponent_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create bowling strategy"""
        
        bowlers = [p for p in selected if p.get("bowling_economy") is not None]
        bowlers.sort(key=lambda x: x.get("bowling_economy", 10))
        
        plan = []
        for i, bowler in enumerate(bowlers[:6]):
            if i < 2:
                phase = "powerplay"
                overs = 2.0
            elif i < 4:
                phase = "middle"
                overs = 3.0
            else:
                phase = "death"
                overs = 2.0
            
            plan.append({
                "bowler_name": bowler["name"],
                "overs_allocated": overs,
                "phase": phase,
                "economy": bowler.get("bowling_economy", 0),
                "reasoning": f"Economy: {bowler.get('bowling_economy', 0):.1f}, Wickets: {bowler.get('wickets', 0)}"
            })
        
        return plan
    
    def _calculate_team_strength(self, selected: List[Dict[str, Any]], pitch_report: Dict[str, Any]) -> Dict[str, float]:
        """Calculate team strength metrics (normalized 0.0-1.0)"""
        
        # Calculate raw strengths
        batting_strength = sum(p.get("batting_avg", 0) * p.get("strike_rate", 0) / 100 for p in selected) / len(selected)
        
        # Bowling strength - only count players who can bowl
        bowlers = [p for p in selected if p.get("bowling_economy")]
        if bowlers:
            bowling_strength = sum(1 / p.get("bowling_economy", 10) for p in bowlers) / len(bowlers)
        else:
            bowling_strength = 0.5  # Default if no bowlers
        
        form_strength = sum(p.get("recent_form", 0) for p in selected) / len(selected)
        
        # Normalize all values to 0.0-1.0 range
        batting_normalized = min(batting_strength / 50, 1.0)
        bowling_normalized = min(bowling_strength / 0.15, 1.0)  # Economy ~7-8 = good
        form_normalized = form_strength / 100
        
        # Overall is weighted average, also capped at 1.0
        overall = (batting_normalized + bowling_normalized + form_normalized) / 3
        
        return {
            "batting": batting_normalized,
            "bowling": bowling_normalized,
            "form": form_normalized,
            "overall": min(overall, 1.0)  # Ensure overall never exceeds 1.0
        }


# Initialize selector
team_selector = IntelligentTeamSelector()
