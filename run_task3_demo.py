"""
Demo script for Task 3: Crisis Management
Shows detailed crisis scenario and AI decision making
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def run_task3_demo():
    """Run Task 3 with detailed output"""
    
    print("\n" + "="*80)
    print("🚨 TASK 3: IPL MATCH CRISIS MANAGEMENT")
    print("="*80)
    print("You are the Match Operations AI - handling multiple simultaneous crises")
    
    try:
        # Reset environment
        print("\n1️⃣ Loading Crisis Scenario...")
        response = requests.post(f"{BASE_URL}/reset", json={"task_id": 3})
        observation = response.json()["observation"]
        
        data = observation["data"]
        crises = data["crises"]
        match_state = data.get("match_state", {})
        
        # Display match context
        print("\n" + "="*80)
        print("MATCH CONTEXT")
        print("="*80)
        print(f"🏏 Match: {match_state.get('batting_team', 'Team A')} vs {match_state.get('bowling_team', 'Team B')}")
        print(f"🏟️  Venue: {match_state.get('venue', 'Stadium')}")
        print(f"📊 Score: {match_state.get('score', '0/0')} | Over: {match_state.get('current_over', '0.0')}")
        print(f"🎯 Target: {match_state.get('target', 'N/A')}")
        print(f"🌤️  Weather: {match_state.get('weather', 'Clear')}")
        
        # Display all crises
        print("\n" + "="*80)
        print(f"⚠️  SIMULTANEOUS CRISES DETECTED: {len(crises)}")
        print("="*80)
        
        for i, crisis in enumerate(crises, 1):
            severity = crisis.get("severity", 50)
            crisis_type = crisis.get("crisis_type", "unknown")
            
            # Emoji based on severity
            if severity > 80:
                emoji = "🔴"
                level = "CRITICAL"
            elif severity > 60:
                emoji = "🟠"
                level = "HIGH"
            else:
                emoji = "🟡"
                level = "MEDIUM"
            
            print(f"\n{emoji} CRISIS {chr(64+i)}: {crisis_type.upper().replace('_', ' ')}")
            print(f"   Severity: {severity}/100 ({level})")
            print(f"   Description: {crisis.get('description', 'No description')}")
            print(f"   Affected Zone: {crisis.get('affected_zone', 'Unknown')}")
            print(f"   Reported By: {crisis.get('reported_by', 'Unknown')}")
            print(f"   Time: {crisis.get('time_reported', 'Unknown')}")
        
        # AI Decision Making
        print("\n" + "="*80)
        print("🤖 AI CRISIS TRIAGE & DECISION MAKING")
        print("="*80)
        
        print("\n⏳ Analyzing all crises...")
        print("   Priority Framework: P0 (Life/Safety) > P1 (Match Integrity) > P2 (Operations) > P3 (Communication)")
        
        # Create action (correct priority order)
        action = {
            "priority_order": [
                {"rank": 1, "crisis": "crowd_safety", "reason": "Life-threatening, requires immediate action"},
                {"rank": 2, "crisis": "injury", "reason": "Player health and match impact"},
                {"rank": 3, "crisis": "weather", "reason": "Match continuation critical"},
                {"rank": 4, "crisis": "regulatory", "reason": "Compliance important but not urgent"},
                {"rank": 5, "crisis": "tech_failure", "reason": "Lowest priority, minimal impact"}
            ],
            "decisions": {
                "crowd_safety": {
                    "action": "deploy_riot_squad",
                    "details": {
                        "security_reallocation": {"from": "VIP", "to": "Stand_C", "count": 50},
                        "police_coordination": True
                    },
                    "timeline_minutes": 2.0
                },
                "injury": {
                    "action": "impact_sub",
                    "details": {"replacement_player": "Best available substitute"},
                    "timeline_minutes": 3.0
                },
                "weather": {
                    "action": "wait",
                    "details": {"dls_target": 165, "communication": "DLS in effect"},
                    "timeline_minutes": 5.0
                },
                "regulatory": {
                    "action": "request_extension",
                    "details": {"justification": "Multiple crises causing delay"},
                    "timeline_minutes": 1.5
                },
                "tech_failure": {
                    "action": "manual_fix",
                    "details": {"sponsor_communication": "Resolving shortly"},
                    "timeline_minutes": 10.0
                }
            },
            "timeline": {
                "0-2_mins": ["Deploy security to Stand C", "Request regulatory extension"],
                "2-5_mins": ["Process injury substitution", "Monitor weather"],
                "5-10_mins": ["Apply DLS if needed", "Fix technical issues"]
            },
            "risk_assessment": {
                "if_wrong_priority": "Crowd safety failure could cause casualties",
                "cascading_failures": "Weather delay provides buffer for other issues"
            }
        }
        
        # Display priority order
        print("\n✅ PRIORITY ORDER DETERMINED:")
        print("-" * 80)
        for item in action["priority_order"]:
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][item["rank"]-1]
            print(f"{rank_emoji} Priority {item['rank']}: {item['crisis'].upper().replace('_', ' ')}")
            print(f"   Reason: {item['reason']}")
        
        # Display decisions
        print("\n✅ DECISIONS FOR EACH CRISIS:")
        print("-" * 80)
        
        for crisis_type, decision in action["decisions"].items():
            print(f"\n🎯 {crisis_type.upper().replace('_', ' ')}:")
            print(f"   Action: {decision['action'].upper().replace('_', ' ')}")
            print(f"   Timeline: {decision['timeline_minutes']} minutes")
            if decision.get('details'):
                print(f"   Details: {json.dumps(decision['details'], indent=6)}")
        
        # Display timeline
        print("\n✅ EXECUTION TIMELINE:")
        print("-" * 80)
        for timeframe, actions in action["timeline"].items():
            print(f"\n⏰ {timeframe}:")
            for act in actions:
                print(f"   • {act}")
        
        # Display risk assessment
        print("\n✅ RISK ASSESSMENT:")
        print("-" * 80)
        for risk_type, assessment in action["risk_assessment"].items():
            print(f"   • {risk_type.replace('_', ' ').title()}: {assessment}")
        
        # Submit action
        print("\n" + "="*80)
        print("📤 SUBMITTING DECISIONS TO MATCH REFEREE...")
        print("="*80)
        
        response = requests.post(f"{BASE_URL}/step", json={"action": action})
        result = response.json()
        
        score = result["reward"]
        info = result.get("info", {})
        
        # Display results
        print(f"\n🎯 FINAL SCORE: {score:.3f} / 1.000")
        
        if score >= 0.9:
            print("   🏆 EXCELLENT! Crisis handled perfectly!")
        elif score >= 0.7:
            print("   👍 GOOD! Effective crisis management!")
        elif score >= 0.5:
            print("   ⚠️  ACCEPTABLE - Some improvements needed")
        else:
            print("   ❌ POOR - Critical errors in crisis handling")
        
        # Breakdown
        if info:
            print("\n" + "="*80)
            print("📊 GRADING BREAKDOWN")
            print("="*80)
            
            breakdown = info.get("breakdown", {})
            for category, details in breakdown.items():
                cat_score = details.get("score", 0)
                weight = details.get("weight", 0)
                
                print(f"\n{category.replace('_', ' ').title()}:")
                print(f"   Score: {cat_score:.3f} (Weight: {weight*100:.0f}%)")
                
                if "issues" in details and details["issues"]:
                    print(f"   Issues:")
                    for issue in details["issues"]:
                        print(f"      • {issue}")
        
        print("\n" + "="*80)
        print("✅ CRISIS MANAGEMENT COMPLETE")
        print("="*80)
        
        print("\n💡 Key Takeaways:")
        print("   • Crowd safety MUST always be Priority #1 (life-threatening)")
        print("   • Player injury is Priority #2 (health + match impact)")
        print("   • Weather/DLS is Priority #3 (match integrity)")
        print("   • Regulatory compliance is Priority #4")
        print("   • Technical failures are Priority #5 (lowest impact)")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Server not running")
        print("   Start with: python app/main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_task3_demo()
