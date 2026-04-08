"""
Comprehensive terminal test for all IPLOps-Env tasks
Tests the OpenEnv API interface without UI
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test server health"""
    print("\n" + "="*80)
    print("🏥 TESTING SERVER HEALTH")
    print("="*80)
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"✅ Server Status: {data['status']}")
        print(f"   Environment: {data['environment']}")
        print(f"   Version: {data['version']}")
        print(f"   Tasks: {', '.join(data['tasks'])}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_task1():
    """Test Task 1: Staff Allocation"""
    print("\n" + "="*80)
    print("📋 TASK 1: STAFF ALLOCATION")
    print("="*80)
    
    try:
        # Reset
        print("\n1️⃣ Resetting environment...")
        response = requests.post(f"{BASE_URL}/reset", json={"task_id": 1})
        obs = response.json()["observation"]
        
        stadium = obs["data"]["stadium"]
        print(f"   Stadium: {stadium['name']}")
        print(f"   Capacity: {stadium['capacity']:,}")
        print(f"   Expected Crowd: {stadium['expected_crowd_percentage']*100:.0f}%")
        print(f"   Match Type: {stadium['match_type']}")
        
        # Calculate allocation
        expected_crowd = int(stadium["capacity"] * stadium["expected_crowd_percentage"])
        security_ratios = {"league": 2.5, "playoff": 3.5, "final": 5.0}
        security_ratio = security_ratios.get(stadium["match_type"], 3.0)
        
        total_security = int((expected_crowd / 1000) * security_ratio)
        security_per_gate = max(2, total_security // stadium["gates_count"])
        medical_personnel = int((expected_crowd / 1000) * 1.5)
        ticketing_staff = int((expected_crowd / 1000) * 0.8)
        
        action = {
            "security_per_gate": security_per_gate,
            "total_security": total_security,
            "medical_personnel": medical_personnel,
            "ticketing_staff": ticketing_staff
        }
        
        print(f"\n2️⃣ Submitting allocation...")
        print(f"   Total Security: {total_security}")
        print(f"   Medical Personnel: {medical_personnel}")
        print(f"   Ticketing Staff: {ticketing_staff}")
        
        # Step
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
        
        return score >= 0.7
        
    except Exception as e:
        print(f"❌ Task 1 failed: {e}")
        return False


def test_task2():
    """Test Task 2: Playing XI Selection"""
    print("\n" + "="*80)
    print("🏏 TASK 2: PLAYING XI SELECTION")
    print("="*80)
    
    try:
        # Reset
        print("\n1️⃣ Resetting environment...")
        response = requests.post(f"{BASE_URL}/reset", json={"task_id": 2})
        obs = response.json()["observation"]
        
        squad = obs["data"]["squad"]
        pitch = obs["data"]["pitch_report"]
        opponent = obs["data"]["opponent"]
        
        print(f"   Team: {obs['data']['team_name']}")
        print(f"   Squad Size: {len(squad)}")
        print(f"   Venue: {pitch['venue']}")
        print(f"   Pitch Type: {pitch.get('pitch_type', pitch.get('surface_type', 'unknown'))}")
        print(f"   Opponent: {opponent['team_name']}")
        
        # Simple selection by form
        wicket_keepers = [p for p in squad if p["role"] == "wicket_keeper"]
        batsmen = [p for p in squad if p["role"] == "batsman"]
        all_rounders = [p for p in squad if p["role"] == "all_rounder"]
        bowlers = [p for p in squad if p["role"] == "bowler"]
        
        batsmen.sort(key=lambda x: x["recent_form"], reverse=True)
        all_rounders.sort(key=lambda x: x["recent_form"], reverse=True)
        bowlers.sort(key=lambda x: x["recent_form"], reverse=True)
        
        playing_xi = []
        playing_xi.append(wicket_keepers[0]["name"])
        playing_xi.extend([b["name"] for b in batsmen[:4]])
        playing_xi.extend([a["name"] for a in all_rounders[:3]])
        playing_xi.extend([b["name"] for b in bowlers[:3]])
        
        action = {
            "playing_xi": playing_xi[:11],
            "batting_order": playing_xi[:11],
            "bowling_combination": {
                "pacers": [b["name"] for b in bowlers[:2]],
                "spinners": [b["name"] for b in bowlers[2:3]],
                "death_overs_specialist": bowlers[0]["name"] if bowlers else playing_xi[-1]
            }
        }
        
        print(f"\n2️⃣ Submitting Playing XI...")
        print(f"   Selected: {', '.join(playing_xi[:3])}...")
        
        # Step
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
        
        return score >= 0.7
        
    except Exception as e:
        print(f"❌ Task 2 failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_task3():
    """Test Task 3: Crisis Management"""
    print("\n" + "="*80)
    print("🚨 TASK 3: CRISIS MANAGEMENT")
    print("="*80)
    
    try:
        # Reset
        print("\n1️⃣ Resetting environment...")
        response = requests.post(f"{BASE_URL}/reset", json={"task_id": 3})
        obs = response.json()["observation"]
        
        crises = obs["data"]["crises"]
        print(f"   Active Crises: {len(crises)}")
        for crisis in crises:
            crisis_type = crisis.get('type', crisis.get('crisis_type', 'unknown'))
            severity = crisis.get('severity', 'unknown')
            print(f"   • {crisis_type}: {severity}")
        
        # Correct priority order
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
        
        print(f"\n2️⃣ Submitting crisis priorities...")
        print(f"   Priority 1: crowd_safety")
        print(f"   Priority 2: injury")
        print(f"   Priority 3: weather")
        
        # Step
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
        
        return score >= 0.7
        
    except Exception as e:
        print(f"❌ Task 3 failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🧪 IPLOps-Env TERMINAL TEST SUITE")
    print("="*80)
    print("Testing all tasks via OpenEnv API (no UI)")
    
    # Test health
    if not test_health():
        print("\n❌ Server not running. Start with: python app/main.py")
        sys.exit(1)
    
    # Test all tasks
    results = {
        "Task 1": test_task1(),
        "Task 2": test_task2(),
        "Task 3": test_task3()
    }
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    for task, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{task}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*80)
        print("\n✅ All tasks work via terminal/API")
        print("✅ Ready for OpenEnv evaluation")
        print("✅ No UI required")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("="*80)
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
