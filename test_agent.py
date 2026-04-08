"""
Example agent to test IPLOps-Env
Run this after starting the server with: python app/main.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_task1():
    """Test Task 1: Staff Allocation"""
    print("\n" + "="*60)
    print("TESTING TASK 1: STAFF ALLOCATION")
    print("="*60)
    
    # Reset environment
    response = requests.post(f"{BASE_URL}/reset", json={"task_id": 1})
    data = response.json()
    
    print("\n📋 Scenario:")
    stadium = data["observation"]["data"]["stadium"]
    print(f"  Stadium: {stadium['name']}")
    print(f"  Capacity: {stadium['capacity']:,}")
    print(f"  Expected Crowd: {stadium['expected_crowd_percentage']*100:.0f}%")
    print(f"  Match Type: {stadium['match_type']}")
    print(f"  Gates: {stadium['gates_count']}")
    
    # Calculate expected crowd
    expected_crowd = int(stadium['capacity'] * stadium['expected_crowd_percentage'])
    
    # Simple allocation logic
    action = {
        "security_per_gate": max(3, expected_crowd // (stadium['gates_count'] * 1000)),
        "total_security": int((expected_crowd / 1000) * 3.5),
        "medical_personnel": int((expected_crowd / 1000) * 1.5),
        "ticketing_staff": int((expected_crowd / 1000) * 0.8),
        "reasoning": "Allocated based on crowd size and safety ratios"
    }
    
    print("\n🤖 Agent Action:")
    print(f"  Security per gate: {action['security_per_gate']}")
    print(f"  Total security: {action['total_security']}")
    print(f"  Medical personnel: {action['medical_personnel']}")
    print(f"  Ticketing staff: {action['ticketing_staff']}")
    
    # Submit action
    response = requests.post(f"{BASE_URL}/step", json={"action": action})
    result = response.json()
    
    print(f"\n🎯 Score: {result['reward']:.3f}")
    print("\n📊 Breakdown:")
    breakdown = result['info']['grading_details']['breakdown']
    for key, value in breakdown.items():
        if isinstance(value, dict):
            continue
        print(f"  {key}: {value:.3f}")
    
    return result['reward']


def test_task2():
    """Test Task 2: Playing XI Selection"""
    print("\n" + "="*60)
    print("TESTING TASK 2: PLAYING XI SELECTION")
    print("="*60)
    
    # Reset environment
    response = requests.post(f"{BASE_URL}/reset", json={"task_id": 2})
    data = response.json()
    
    print("\n📋 Scenario:")
    obs_data = data["observation"]["data"]
    print(f"  Team: {obs_data['team_name']}")
    print(f"  Pitch: {obs_data['pitch_report']['surface_type']}")
    print(f"  Bounce: {obs_data['pitch_report']['bounce']}")
    print(f"  Opponent: {obs_data['opponent']['team_name']}")
    print(f"  Opponent Weakness: {obs_data['opponent']['weakness_against']}")
    
    squad = obs_data['squad']
    pitch = obs_data['pitch_report']
    
    # Simple selection logic
    wicket_keepers = [p for p in squad if p['role'] == 'wicket_keeper']
    batsmen = [p for p in squad if p['role'] == 'batsman']
    all_rounders = [p for p in squad if p['role'] == 'all_rounder']
    bowlers = [p for p in squad if p['role'] == 'bowler']
    
    # Sort by recent form
    batsmen.sort(key=lambda x: x['recent_form'], reverse=True)
    all_rounders.sort(key=lambda x: x['recent_form'], reverse=True)
    bowlers.sort(key=lambda x: x['recent_form'], reverse=True)
    
    # Select XI
    playing_xi = []
    playing_xi.append(wicket_keepers[0]['name'])  # 1 WK
    playing_xi.extend([b['name'] for b in batsmen[:4]])  # 4 batsmen
    playing_xi.extend([a['name'] for a in all_rounders[:3]])  # 3 all-rounders
    playing_xi.extend([b['name'] for b in bowlers[:3]])  # 3 bowlers
    
    action = {
        "playing_xi": playing_xi,
        "batting_order": playing_xi,  # Simple: same as XI
        "bowling_combination": {
            "pacers": [b['name'] for b in bowlers[:2]],
            "spinners": [bowlers[2]['name']] if len(bowlers) > 2 else [],
            "death_overs_specialist": bowlers[0]['name']
        },
        "reasoning": {
            "pitch_strategy": f"Selected for {pitch['surface_type']} conditions",
            "opponent_matchup": f"Targeting opponent weakness: {obs_data['opponent']['weakness_against']}",
            "balance_justification": "1 WK, 4 batsmen, 3 all-rounders, 3 bowlers"
        }
    }
    
    print("\n🤖 Selected XI:")
    for i, player in enumerate(playing_xi, 1):
        print(f"  {i}. {player}")
    
    # Submit action
    response = requests.post(f"{BASE_URL}/step", json={"action": action})
    result = response.json()
    
    print(f"\n🎯 Score: {result['reward']:.3f}")
    print("\n📊 Breakdown:")
    breakdown = result['info']['grading_details']['breakdown']
    for category, details in breakdown.items():
        if isinstance(details, dict) and 'score' in details:
            print(f"  {category}: {details['score']:.3f}")
    
    return result['reward']


def test_task3():
    """Test Task 3: Crisis Management"""
    print("\n" + "="*60)
    print("TESTING TASK 3: CRISIS MANAGEMENT")
    print("="*60)
    
    # Reset environment
    response = requests.post(f"{BASE_URL}/reset", json={"task_id": 3})
    data = response.json()
    
    print("\n📋 Match Context:")
    context = data["observation"]["data"]["match_context"]
    print(f"  Score: {context['current_score']}")
    print(f"  Target: {context['target']}")
    print(f"  Crowd: {context['crowd_size']:,}")
    print(f"  Match Type: {context['match_type']}")
    
    print("\n🚨 Crises:")
    crises = data["observation"]["data"]["crises"]
    for i, crisis in enumerate(crises, 1):
        print(f"  {i}. {crisis['crisis_type']}: {crisis['description'][:80]}...")
    
    # Correct priority order
    action = {
        "priority_order": [
            {"rank": 1, "crisis": "crowd_safety", "reason": "Life-threatening situation, immediate action required"},
            {"rank": 2, "crisis": "injury", "reason": "Player health and match continuation"},
            {"rank": 3, "crisis": "weather", "reason": "Match continuation and DLS calculation"},
            {"rank": 4, "crisis": "regulatory", "reason": "Points penalty but not life-threatening"},
            {"rank": 5, "crisis": "tech_failure", "reason": "Lowest priority, can be handled later"}
        ],
        "decisions": {
            "crowd_safety": {
                "action": "deploy_riot_squad",
                "details": {
                    "security_reallocation": {"from": "VIP_area", "to": "Stand_C", "count": 50},
                    "police_coordination": True,
                    "stop_match": False
                },
                "timeline_minutes": 2.0
            },
            "injury": {
                "action": "impact_sub",
                "details": {
                    "replacement_player": "Substitute Player",
                    "batting_order_change": ["adjusted order"]
                },
                "timeline_minutes": 3.0
            },
            "weather": {
                "action": "wait",
                "details": {
                    "dls_target": 165,
                    "communication": "Waiting for rain to stop, DLS in effect"
                },
                "timeline_minutes": 5.0
            },
            "regulatory": {
                "action": "request_extension",
                "details": {
                    "justification": "Player injury causing delay"
                },
                "timeline_minutes": 1.5
            },
            "tech_failure": {
                "action": "manual_fix",
                "details": {
                    "sponsor_communication": "Technical team working on resolution"
                },
                "timeline_minutes": 10.0
            }
        },
        "timeline": {
            "0-2_mins": ["Deploy riot squad to Stand C", "Request over-rate extension"],
            "2-5_mins": ["Process impact substitution", "Assess weather conditions"],
            "5-10_mins": ["Calculate DLS if needed", "Fix LED screen"]
        },
        "risk_assessment": {
            "if_wrong_priority": "Ignoring crowd safety could lead to stampede and casualties",
            "cascading_failures": "Weather delay gives time to handle other crises"
        }
    }
    
    print("\n🤖 Agent Priority Order:")
    for priority in action["priority_order"]:
        print(f"  {priority['rank']}. {priority['crisis']}: {priority['reason']}")
    
    # Submit action
    response = requests.post(f"{BASE_URL}/step", json={"action": action})
    result = response.json()
    
    print(f"\n🎯 Score: {result['reward']:.3f}")
    print("\n📊 Breakdown:")
    breakdown = result['info']['grading_details']['breakdown']
    for category, details in breakdown.items():
        if isinstance(details, dict) and 'score' in details:
            print(f"  {category}: {details['score']:.3f}")
    
    return result['reward']


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("IPLOps-Env Test Suite")
    print("="*60)
    
    try:
        # Test health endpoint
        response = requests.get(f"{BASE_URL}/health")
        print(f"\n✅ Server is running: {response.json()['status']}")
        
        # Run all tasks
        scores = []
        scores.append(test_task1())
        scores.append(test_task2())
        scores.append(test_task3())
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Task 1 Score: {scores[0]:.3f}")
        print(f"Task 2 Score: {scores[1]:.3f}")
        print(f"Task 3 Score: {scores[2]:.3f}")
        print(f"Average Score: {sum(scores)/len(scores):.3f}")
        print("\n✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server")
        print("Please start the server first with: python app/main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
