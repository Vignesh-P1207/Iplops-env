"""
Test script for GPT-4 integration in team selection
"""
import os
from app.team_selector import IntelligentTeamSelector
from app.scraper import IPLSquadScraper

def test_algorithmic_selection():
    """Test algorithmic selection (no API key)"""
    print("\n" + "="*80)
    print("TEST 1: ALGORITHMIC SELECTION (No API Key)")
    print("="*80)
    
    # Ensure no API key
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("HF_TOKEN", None)
    
    # Create selector
    selector = IntelligentTeamSelector()
    
    # Generate test squad
    scraper = IPLSquadScraper()
    squad = scraper._generate_dynamic_squad("Mumbai Indians")
    
    # Test pitch report
    pitch_report = {
        "venue": "Wankhede Stadium",
        "pitch_type": "batting_friendly",
        "characteristics": ["High scoring", "Flat pitch"],
        "pace_bounce": "medium",
        "spin_assistance": "low"
    }
    
    # Test opponent
    opponent_profile = {
        "team_name": "Chennai Super Kings",
        "weakness_against": "pace",
        "death_bowling_strength": 65
    }
    
    # Select team
    result = selector.select_playing_xi(squad, pitch_report, opponent_profile)
    
    # Verify results
    assert len(result["selected_players"]) == 11, "Should select 11 players"
    assert result["selection_method"] == "Algorithmic", "Should use algorithmic method"
    assert "batting_order" in result, "Should have batting order"
    assert "bowling_plan" in result, "Should have bowling plan"
    
    print("\n✅ ALGORITHMIC SELECTION TEST PASSED")
    print(f"   Selected: {', '.join(result['selected_players'][:3])}...")
    print(f"   Method: {result['selection_method']}")
    print(f"   Team Strength: {result['team_strength']['overall']:.2%}")
    
    return result


def test_gpt4_selection():
    """Test GPT-4 selection (with API key)"""
    print("\n" + "="*80)
    print("TEST 2: GPT-4 SELECTION (With API Key)")
    print("="*80)
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("HF_TOKEN")
    
    if not api_key:
        print("\n⚠️  SKIPPED: No API key found")
        print("   Set OPENAI_API_KEY or HF_TOKEN to test GPT-4 mode")
        return None
    
    # Create selector
    selector = IntelligentTeamSelector()
    
    if not selector.client:
        print("\n⚠️  SKIPPED: OpenAI client not initialized")
        return None
    
    # Generate test squad
    scraper = IPLSquadScraper()
    squad = scraper._generate_dynamic_squad("Chennai Super Kings")
    
    # Test pitch report
    pitch_report = {
        "venue": "M. A. Chidambaram Stadium",
        "pitch_type": "spin_friendly",
        "characteristics": ["Slow", "Turning"],
        "pace_bounce": "low",
        "spin_assistance": "high"
    }
    
    # Test opponent
    opponent_profile = {
        "team_name": "Mumbai Indians",
        "weakness_against": "spin",
        "death_bowling_strength": 70
    }
    
    try:
        # Select team
        result = selector.select_playing_xi(squad, pitch_report, opponent_profile)
        
        # Verify results
        assert len(result["selected_players"]) == 11, "Should select 11 players"
        assert result["selection_method"] == "GPT-4 AI", "Should use GPT-4 method"
        assert "batting_order" in result, "Should have batting order"
        assert "bowling_plan" in result, "Should have bowling plan"
        
        print("\n✅ GPT-4 SELECTION TEST PASSED")
        print(f"   Selected: {', '.join(result['selected_players'][:3])}...")
        print(f"   Method: {result['selection_method']}")
        print(f"   Strategy: {result['reasoning'].get('strategy', 'N/A')}")
        print(f"   Team Strength: {result['team_strength']['overall']:.2%}")
        
        if "gpt_reasoning" in result["reasoning"]:
            print(f"   GPT Reasoning: {result['reasoning']['gpt_reasoning'][:100]}...")
        
        return result
        
    except Exception as e:
        print(f"\n❌ GPT-4 TEST FAILED: {e}")
        print("   Falling back to algorithmic selection")
        return None


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("🧪 TESTING GPT-4 INTEGRATION")
    print("="*80)
    
    # Test 1: Algorithmic (always works)
    result1 = test_algorithmic_selection()
    
    # Test 2: GPT-4 (if API key available)
    result2 = test_gpt4_selection()
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"✅ Algorithmic Selection: PASSED")
    print(f"{'✅' if result2 else '⚠️ '} GPT-4 Selection: {'PASSED' if result2 else 'SKIPPED (no API key)'}")
    print("\n" + "="*80)
    print("🎉 ALL TESTS COMPLETE")
    print("="*80)
    
    if not result2:
        print("\n💡 TIP: Set OPENAI_API_KEY to test GPT-4 mode:")
        print("   export OPENAI_API_KEY='sk-...'")
        print("   python test_gpt4_integration.py")


if __name__ == "__main__":
    main()
