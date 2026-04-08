"""
Demo script for Task 2: Playing XI Selection
Tests the IPL data API integration
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.api_clients import IPLDataAggregator
from app.tasks.task2_selection import PlayingXITask


async def main():
    print("\n" + "="*60)
    print("🏏 Task 2: Playing XI Selection Demo")
    print("="*60 + "\n")
    
    # Initialize aggregator
    print("📡 Initializing IPL Data Aggregator...")
    aggregator = IPLDataAggregator()
    
    # Test 1: Get IPL teams
    print("\n1️⃣ Fetching IPL Teams...")
    teams = aggregator.espn_client.get_ipl_teams()
    print(f"   Found {len(teams)} teams:")
    for team in teams[:5]:
        print(f"   • {team.get('name', team.get('short_name', 'Unknown'))}")
    
    # Test 2: Get squad for a team
    print("\n2️⃣ Fetching Mumbai Indians Squad...")
    squad = aggregator.get_enriched_squad("Mumbai Indians")
    print(f"   Squad size: {len(squad)} players")
    print(f"   Sample players:")
    for player in squad[:5]:
        role = player.get('role', 'unknown')
        avg = player.get('batting_avg', 0)
        sr = player.get('strike_rate', 0)
        print(f"   • {player['name']} ({role}) - Avg: {avg}, SR: {sr}")
    
    # Test 3: Get pitch report
    print("\n3️⃣ Fetching Pitch Report for Wankhede Stadium...")
    pitch = aggregator.get_pitch_report("Wankhede Stadium")
    print(f"   Type: {pitch.get('type', 'unknown')}")
    print(f"   Pace/Bounce: {pitch.get('pace_bounce', 'unknown')}")
    print(f"   Spin: {pitch.get('spin', 'unknown')}")
    
    # Test 4: Generate full scenario
    print("\n4️⃣ Generating Complete Scenario...")
    task = PlayingXITask()
    scenario = task.generate_scenario()
    
    print(f"\n   Team: {scenario['team_name']}")
    print(f"   Squad Size: {len(scenario['squad'])} players")
    print(f"   Venue: {scenario['pitch_report']['venue']}")
    print(f"   Pitch Type: {scenario['pitch_report']['surface_type']}")
    print(f"   Opponent: {scenario['opponent']['team_name']}")
    print(f"   Opponent Weakness: {scenario['opponent']['weakness_against']}")
    
    print("\n   Instructions:")
    for line in scenario['instructions'].split('\n')[:5]:
        print(f"   {line}")
    
    print("\n" + "="*60)
    print("✅ Task 2 Demo Complete!")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   1. Start server: python app/main.py")
    print("   2. Open UI: http://localhost:8000/task2")
    print("   3. Click 'Generate Scenario' to load real data")
    print("   4. Select 11 players and evaluate!")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
