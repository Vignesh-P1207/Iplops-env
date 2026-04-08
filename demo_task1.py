"""
Demo: Task 1 - Staff Allocation
Step-by-step demonstration
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("🏏 IPLOps-Env - Task 1 Demo: Match Day Staff Allocation")
print("="*70)

# Step 1: Reset environment to get scenario
print("\n📋 STEP 1: Getting Stadium Scenario...")
print("-"*70)

response = requests.post(f"{BASE_URL}/reset", json={"task_id": 1})
data = response.json()
observation = data["observation"]["data"]

stadium = observation["stadium"]
print(f"\n🏟️  Stadium Information:")
print(f"   Name: {stadium['name']}")
print(f"   Capacity: {stadium['capacity']:,} people")
print(f"   Expected Crowd: {stadium['expected_crowd_percentage']*100:.0f}%")
print(f"   Match Type: {stadium['match_type'].upper()}")
print(f"   Gates: {stadium['gates_count']}")
print(f"   Medical Stations: {stadium['medical_stations']}")

expected_crowd = int(stadium['capacity'] * stadium['expected_crowd_percentage'])
print(f"\n👥 Expected Crowd: {expected_crowd:,} people")

# Step 2: Calculate staff allocation
print("\n" + "-"*70)
print("🤖 STEP 2: Agent Calculating Staff Allocation...")
print("-"*70)

# Safety ratios
security_ratios = {"league": 2.5, "playoff": 3.5, "final": 5.0}
security_ratio = security_ratios[stadium['match_type']]

# Calculate allocations
total_security = int((expected_crowd / 1000) * security_ratio)
security_per_gate = max(2, total_security // stadium['gates_count'])
medical_personnel = int((expected_crowd / 1000) * 1.5)
ticketing_staff = int((expected_crowd / 1000) * 0.8)

action = {
    "security_per_gate": security_per_gate,
    "total_security": total_security,
    "medical_personnel": medical_personnel,
    "ticketing_staff": ticketing_staff,
    "reasoning": f"Allocated for {expected_crowd:,} expected crowd at {stadium['match_type']} match"
}

print(f"\n📊 Agent's Allocation:")
print(f"   Security per Gate: {action['security_per_gate']} officers")
print(f"   Total Security: {action['total_security']} officers")
print(f"   Medical Personnel: {action['medical_personnel']} staff")
print(f"   Ticketing Staff: {action['ticketing_staff']} staff")
print(f"\n💡 Reasoning: {action['reasoning']}")

# Step 3: Submit action and get score
print("\n" + "-"*70)
print("📤 STEP 3: Submitting Action to Environment...")
print("-"*70)

response = requests.post(f"{BASE_URL}/step", json={"action": action})
result = response.json()

reward = result['reward']
grading = result['info']['grading_details']

print(f"\n🎯 FINAL SCORE: {reward:.3f} / 1.000")

# Show detailed breakdown
print("\n" + "="*70)
print("📊 DETAILED GRADING BREAKDOWN")
print("="*70)

breakdown = grading['breakdown']
print(f"\n✅ Security Accuracy:      {breakdown['security_score']:.3f} (Weight: 35%)")
print(f"✅ Medical Accuracy:       {breakdown['medical_score']:.3f} (Weight: 25%)")
print(f"✅ Ticketing Accuracy:     {breakdown['ticketing_score']:.3f} (Weight: 20%)")
print(f"✅ No Overstaffing:        {breakdown['overstaffing_score']:.3f} (Weight: 10%)")
print(f"✅ No Understaffing:       {breakdown['understaffing_score']:.3f} (Weight: 10%)")

print(f"\n📈 Total Staffing Ratio:   {breakdown['total_staffing_ratio']:.3f}x optimal")

# Show optimal values
print("\n" + "-"*70)
print("📋 COMPARISON: Agent vs Optimal")
print("-"*70)

optimal = grading['optimal_values']
agent = grading['agent_values']

print(f"\n{'Category':<20} {'Agent':<15} {'Optimal':<15} {'Difference':<15}")
print("-"*65)
print(f"{'Total Security':<20} {agent['total_security']:<15} {optimal['total_security']:<15} {agent['total_security']-optimal['total_security']:+<15}")
print(f"{'Medical Personnel':<20} {agent['medical_personnel']:<15} {optimal['medical_personnel']:<15} {agent['medical_personnel']-optimal['medical_personnel']:+<15}")
print(f"{'Ticketing Staff':<20} {agent['ticketing_staff']:<15} {optimal['ticketing_staff']:<15} {agent['ticketing_staff']-optimal['ticketing_staff']:+<15}")

# Final verdict
print("\n" + "="*70)
if reward >= 0.95:
    print("🏆 EXCELLENT! Near-perfect allocation!")
elif reward >= 0.85:
    print("✅ GREAT! Very good allocation with minor room for improvement.")
elif reward >= 0.70:
    print("👍 GOOD! Solid allocation, some optimization possible.")
else:
    print("⚠️  NEEDS IMPROVEMENT: Review safety ratios and staffing guidelines.")

print("="*70 + "\n")
