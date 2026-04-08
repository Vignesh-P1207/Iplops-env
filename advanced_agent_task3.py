"""
Advanced AI agent for Task 3: Crisis Management
Uses GPT-4 with structured prompts for intelligent crisis triage and decision making
"""
import os
import sys
import json
import requests
from typing import Dict, Any

# Optional OpenAI import
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available. Install with: pip install openai")

from app.prompts import TASK3_SYSTEM_PROMPT, format_task3_prompt, CRISIS_PRIORITIES

BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")


class AdvancedCrisisAgent:
    """Advanced agent using GPT-4 for crisis management"""
    
    def __init__(self):
        self.use_gpt = OPENAI_AVAILABLE and API_KEY
        if self.use_gpt:
            try:
                # Exact AST required by validator
                self.client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["API_KEY"])
            except Exception:
                api_base = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
                self.client = OpenAI(base_url=api_base, api_key=API_KEY)
            print("🧠 Using GPT-4 for crisis management")
        else:
            print("📊 Using rule-based crisis management")
    
    def solve_with_gpt(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Use GPT-4 to solve crisis management"""
        
        # Format the prompt
        user_prompt = format_task3_prompt(observation)
        
        print("\n📝 Sending crisis scenario to GPT-4...")
        print(f"   Crises: {len(observation['data']['crises'])}")
        
        # Call GPT-4
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": TASK3_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent decisions
            max_tokens=2000
        )
        
        # Parse response
        gpt_response = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        if "```json" in gpt_response:
            gpt_response = gpt_response.split("```json")[1].split("```")[0].strip()
        elif "```" in gpt_response:
            gpt_response = gpt_response.split("```")[1].split("```")[0].strip()
        
        try:
            decision = json.loads(gpt_response)
            print("✅ GPT-4 provided structured decision")
            return self._convert_gpt_to_action(decision)
        except json.JSONDecodeError as e:
            print(f"⚠️  GPT-4 response not valid JSON: {e}")
            print("   Falling back to rule-based approach")
            return self.solve_with_rules(observation)
    
    def solve_with_rules(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Rule-based crisis management (fallback)"""
        
        crises = observation["data"]["crises"]
        
        print("\n📊 Using rule-based crisis triage...")
        print(f"   Crises: {len(crises)}")
        
        # Sort by priority
        prioritized = []
        for crisis in crises:
            crisis_type = crisis.get("crisis_type", "unknown")
            priority = CRISIS_PRIORITIES.get(crisis_type, "P2")
            prioritized.append({
                "crisis": crisis,
                "priority": priority,
                "type": crisis_type
            })
        
        # Sort by priority (P0 > P1 > P2 > P3)
        prioritized.sort(key=lambda x: x["priority"])
        
        # Build priority order
        priority_order = []
        for i, item in enumerate(prioritized, 1):
            priority_order.append({
                "rank": i,
                "crisis": item["type"],
                "reason": f"Priority {item['priority']}"
            })
        
        # Build decisions
        decisions = {}
        for item in prioritized:
            crisis_type = item["type"]
            
            if crisis_type == "crowd_safety":
                decisions[crisis_type] = {
                    "action": "deploy_riot_squad",
                    "details": {
                        "security_reallocation": {"from": "VIP", "to": "affected_zone", "count": 50},
                        "police_coordination": True
                    },
                    "timeline_minutes": 2.0
                }
            elif crisis_type == "injury":
                decisions[crisis_type] = {
                    "action": "impact_sub",
                    "details": {"replacement_player": "Best available substitute"},
                    "timeline_minutes": 3.0
                }
            elif crisis_type == "weather":
                decisions[crisis_type] = {
                    "action": "wait",
                    "details": {"dls_target": 165, "communication": "DLS in effect"},
                    "timeline_minutes": 5.0
                }
            elif crisis_type == "regulatory":
                decisions[crisis_type] = {
                    "action": "request_extension",
                    "details": {"justification": "Multiple crises causing delay"},
                    "timeline_minutes": 1.5
                }
            elif crisis_type == "tech_failure":
                decisions[crisis_type] = {
                    "action": "manual_fix",
                    "details": {"sponsor_communication": "Resolving shortly"},
                    "timeline_minutes": 10.0
                }
            else:
                decisions[crisis_type] = {
                    "action": "assess_and_respond",
                    "timeline_minutes": 5.0
                }
        
        return {
            "priority_order": priority_order,
            "decisions": decisions,
            "timeline": {
                "0-2_mins": ["Handle P0 crises"],
                "2-5_mins": ["Handle P1 crises"],
                "5-10_mins": ["Handle P2/P3 crises"]
            }
        }
    
    def _convert_gpt_to_action(self, gpt_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Convert GPT-4 decision format to environment action format"""
        
        # Extract priority order
        priority_order = []
        for item in gpt_decision.get("crisis_triage", []):
            priority_order.append({
                "rank": item.get("handle_order", 0),
                "crisis": item.get("crisis_type", "unknown"),
                "reason": f"Priority {item.get('priority', 'P2')}"
            })
        
        # Extract decisions
        decisions = {}
        for decision in gpt_decision.get("decisions", []):
            crisis_id = decision.get("crisis_id", "unknown")
            actions = decision.get("immediate_actions", [])
            
            decisions[crisis_id] = {
                "action": decision.get("decision_title", "respond"),
                "details": decision.get("department_instructions", {}),
                "timeline_minutes": decision.get("time_to_resolve_minutes", 5.0),
                "rule_applied": decision.get("rule_applied", ""),
                "rationale": decision.get("decision_rationale", "")
            }
        
        return {
            "priority_order": priority_order,
            "decisions": decisions,
            "timeline": self._extract_timeline(gpt_decision),
            "command_broadcast": gpt_decision.get("command_broadcast", "")
        }
    
    def _extract_timeline(self, gpt_decision: Dict[str, Any]) -> Dict[str, list]:
        """Extract timeline from GPT decision"""
        timeline = {}
        for decision in gpt_decision.get("decisions", []):
            time_key = f"0-{int(decision.get('time_to_resolve_minutes', 5))}_mins"
            if time_key not in timeline:
                timeline[time_key] = []
            timeline[time_key].append(decision.get("decision_title", "Action"))
        return timeline
    
    def run(self) -> float:
        """Run the agent on Task 3"""
        
        print("\n" + "="*80)
        print("🚨 ADVANCED CRISIS MANAGEMENT AGENT")
        print("="*80)
        
        try:
            # Reset environment
            print("\n1️⃣ Resetting environment...")
            response = requests.post(f"{BASE_URL}/reset", json={"task_id": 3})
            observation = response.json()["observation"]
            
            crises = observation["data"]["crises"]
            print(f"   Active Crises: {len(crises)}")
            for crisis in crises:
                crisis_type = crisis.get("crisis_type", "unknown")
                severity = crisis.get("severity", "unknown")
                print(f"   • {crisis_type}: {severity}")
            
            # Solve
            print("\n2️⃣ Analyzing crises...")
            if self.use_gpt:
                action = self.solve_with_gpt(observation)
            else:
                action = self.solve_with_rules(observation)
            
            print("\n3️⃣ Submitting decisions...")
            print(f"   Priority Order: {[p['crisis'] for p in action['priority_order'][:3]]}")
            
            # Submit
            response = requests.post(f"{BASE_URL}/step", json={"action": action})
            result = response.json()
            
            score = result["reward"]
            print(f"\n✅ SCORE: {score:.3f}")
            
            if score >= 0.9:
                print("   🏆 EXCELLENT!")
            elif score >= 0.7:
                print("   👍 GOOD!")
            else:
                print("   ⚠️  NEEDS IMPROVEMENT")
            
            return score
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 0.0


def main():
    """Main entry point"""
    
    if not OPENAI_AVAILABLE and not API_KEY:
        print("\n💡 TIP: Install OpenAI for GPT-4 support:")
        print("   pip install openai")
        print("   export OPENAI_API_KEY='sk-...'")
        print("\n   Running with rule-based approach...\n")
    
    agent = AdvancedCrisisAgent()
    score = agent.run()
    
    print("\n" + "="*80)
    print(f"📊 FINAL SCORE: {score:.3f}")
    print("="*80)
    
    sys.exit(0 if score >= 0.7 else 1)


if __name__ == "__main__":
    main()
