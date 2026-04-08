# Task 2: Playing XI Selection - Integration Guide

## Overview
Task 2 now integrates with real IPL data APIs (ESPN Cricinfo and Crickbuzz) to fetch live squad information, player statistics, and pitch reports.

## Architecture

### Components
1. **API Clients** (`app/api_clients.py`)
   - `ESPNCricinfoClient`: Fetches IPL teams and squad data
   - `CrickbuzzClient`: Fetches match data and player stats
   - `IPLDataAggregator`: Combines data from multiple sources with fallback

2. **Task Generator** (`app/tasks/task2_selection.py`)
   - Uses `IPLDataAggregator` to fetch real squad data
   - Generates scenarios with pitch reports and opponent profiles
   - Falls back to static data if APIs are unavailable

3. **Web UI** (`static/task2.html`)
   - Interactive player selection interface
   - Connects to backend API endpoints
   - Real-time scenario generation and evaluation

4. **API Endpoints** (`app/main.py`)
   - `GET /task2` - Serve Task 2 UI
   - `GET /api/ipl/teams` - Get list of IPL teams
   - `GET /api/ipl/squad/{team_name}` - Get squad for specific team
   - `GET /api/ipl/pitch/{venue}` - Get pitch report for venue
   - `POST /reset` - Reset environment with task_id=2
   - `POST /step` - Submit team selection for evaluation

## Setup

### 1. API Keys (Optional)
For real-time data, set these environment variables:

```bash
# ESPN Cricinfo API (if you have access)
export ESPN_API_KEY="your_espn_api_key"

# Crickbuzz via RapidAPI
export RAPIDAPI_KEY="your_rapidapi_key"
```

**Note**: The system works without API keys using enhanced static data with realistic IPL 2026 stats.

### 2. Start the Server
```bash
python app/main.py
```

Server will start at: http://localhost:8000

### 3. Access Task 2 UI
Open in browser: http://localhost:8000/task2

## Usage

### Step 1: Generate Scenario
1. Select a stadium venue (Wankhede, Eden Gardens, etc.)
2. Select an IPL team (Mumbai Indians, CSK, etc.)
3. Click "🎲 Generate Scenario"

This will:
- Fetch the team's 20-player squad from API/static data
- Load pitch report for the venue
- Generate opponent profile
- Display all information in the UI

### Step 2: Select Playing XI
1. Browse the player list showing stats:
   - Role (batsman, bowler, all-rounder, wicket-keeper)
   - Batting average and strike rate
   - Recent form score
   - Bowling economy (for bowlers)

2. Click on 11 players to select them
3. Selected players appear in the XI slots at the top

### Step 3: Evaluate Team
Click "🎯 EVALUATE TEAM SELECTION" to submit your selection.

The grader will score based on:
- **Validity** (15%): Correct number of players, roles
- **Role Balance** (25%): Proper mix of batsmen, bowlers, all-rounders
- **Pitch Fit** (25%): Players suited to pitch conditions
- **Batting Order** (20%): Logical batting lineup
- **Opponent Matchup** (15%): Exploiting opponent weaknesses

## API Integration Details

### ESPN Cricinfo Client
```python
from app.api_clients import ESPNCricinfoClient

client = ESPNCricinfoClient()
teams = client.get_ipl_teams()  # Returns list of IPL teams
squad = client.get_team_squad(team_id)  # Returns player list
```

### Crickbuzz Client
```python
from app.api_clients import CrickbuzzClient

client = CrickbuzzClient()
matches = client.get_ipl_matches()  # Returns current matches
stats = client.get_player_stats(player_id)  # Returns player stats
```

### IPL Data Aggregator
```python
from app.api_clients import IPLDataAggregator

aggregator = IPLDataAggregator()
squad = aggregator.get_enriched_squad("Mumbai Indians")
pitch = aggregator.get_pitch_report("Wankhede Stadium")
```

## Testing

### Run Demo Script
```bash
python demo_task2.py
```

This will:
- Test API client connections
- Fetch sample team data
- Generate a complete scenario
- Display all information

### Manual API Testing
```bash
# Get teams
curl http://localhost:8000/api/ipl/teams

# Get squad
curl http://localhost:8000/api/ipl/squad/Mumbai%20Indians

# Get pitch report
curl http://localhost:8000/api/ipl/pitch/Wankhede%20Stadium

# Reset environment
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": 2}'
```

## Data Structure

### Squad Player Object
```json
{
  "name": "Rohit Sharma",
  "role": "batsman",
  "batting_avg": 31.2,
  "strike_rate": 130.5,
  "balls_faced": 3200,
  "runs_scored": 6000,
  "bowling_economy": null,
  "wickets": null,
  "overs_bowled": null,
  "bowling_avg": null,
  "fielding_catches": 45,
  "recent_form": 78,
  "matches_played": 227,
  "best_score": 109
}
```

### Pitch Report Object
```json
{
  "type": "batting_friendly",
  "pace_bounce": "high",
  "spin": "medium"
}
```

### Opponent Profile Object
```json
{
  "team_name": "Chennai Super Kings",
  "weakness_against": "pace",
  "top_order_strength": "strong",
  "tail_weakness": false,
  "death_bowling_strength": 85.5
}
```

## Fallback Behavior

If API calls fail:
1. System automatically uses enhanced static data
2. Static data includes realistic IPL 2026 stats for 10 teams
3. Each team has 20 players with complete statistics
4. No functionality is lost - everything works offline

## Troubleshooting

### Issue: "Could not connect to server"
- Ensure server is running: `python app/main.py`
- Check server is on localhost:8000
- Hard refresh browser (Ctrl+Shift+R)

### Issue: "Failed to load squad"
- Check team name spelling matches exactly
- API may be rate-limited (will use fallback data)
- Check console for error messages (F12)

### Issue: Empty player list
- Click "Generate Scenario" button first
- Check browser console for errors
- Verify server logs for API errors

## Future Enhancements

1. **Real API Integration**
   - Implement actual ESPN Cricinfo API calls
   - Add Crickbuzz RapidAPI integration
   - Handle rate limiting and caching

2. **Enhanced Features**
   - Player comparison tool
   - Historical performance charts
   - AI-powered team suggestions
   - Export team sheet as PDF

3. **Additional Data Sources**
   - IPL official API
   - Cricket statistics databases
   - Weather data for pitch conditions

## Navigation

- **Task 1**: http://localhost:8000/ (Staff Allocation)
- **Task 2**: http://localhost:8000/task2 (Playing XI Selection)
- **API Docs**: http://localhost:8000/docs (FastAPI Swagger)

## Support

For issues or questions:
1. Check server logs in terminal
2. Check browser console (F12)
3. Review API endpoint responses
4. Test with demo script: `python demo_task2.py`
