# Task 2: Playing XI Selection - Quick Start

## 🚀 Start in 30 Seconds

```bash
# 1. Start server
python app/main.py

# 2. Open browser
http://localhost:8000/task2

# 3. Use the UI
- Select venue and team
- Click "Generate Scenario"
- Select 11 players
- Click "Evaluate"
```

## 🎯 What You'll See

### Scenario Configuration
- **Venue**: Wankhede Stadium, Eden Gardens, M. Chinnaswamy Stadium, Arun Jaitley Stadium
- **Team**: Mumbai Indians, Chennai Super Kings, Royal Challengers Bangalore, Kolkata Knight Riders

### Pitch Report
- Type: batting_friendly / spin_friendly / pace_friendly / balanced
- Pace/Bounce: low / medium / high
- Spin: low / medium / high

### Player Stats
Each player shows:
- Name and role (batsman/bowler/all_rounder/wicket_keeper)
- Batting average and strike rate
- Recent form score (0-100)
- Bowling economy (for bowlers)

### Selection Rules
- Exactly 11 players
- 1 wicket-keeper
- 5-6 batsmen
- 4-5 bowlers
- 2+ all-rounders

## 📊 Scoring

Your team is scored on:
- **Validity** (15%): Correct roles and count
- **Role Balance** (25%): Proper mix of players
- **Pitch Fit** (25%): Players suited to conditions
- **Batting Order** (20%): Logical lineup
- **Opponent Matchup** (15%): Exploiting weaknesses

Score range: 0.000 (worst) to 1.000 (perfect)

## 🧪 Test It

```bash
# Run demo script
python demo_task2.py

# Expected output:
# ✅ Fetches 10 IPL teams
# ✅ Loads Mumbai Indians squad (11 players)
# ✅ Gets pitch report for Wankhede
# ✅ Generates complete scenario
```

## 🔗 API Endpoints

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

# Submit team selection
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "selected_players": ["Rohit Sharma", "Ishan Kishan", ...],
      "batting_order": [...],
      "bowling_plan": [...]
    }
  }'
```

## 💡 Tips

1. **Balance is key**: Don't select all batsmen or all bowlers
2. **Match pitch to players**: Spinners for spin-friendly, pacers for pace-friendly
3. **Check recent form**: Higher form scores = better current performance
4. **Exploit opponent weakness**: If opponent weak against pace, select more pacers
5. **Don't forget wicket-keeper**: Must have exactly 1

## 🐛 Troubleshooting

**"Could not connect to server"**
- Check server is running: `python app/main.py`
- Hard refresh browser: Ctrl+Shift+R
- Try incognito mode

**"Failed to load squad"**
- Click "Generate Scenario" button first
- Check browser console (F12) for errors
- Verify server logs

**Empty player list**
- Click "Generate Scenario" to load data
- Check team name is correct
- Try different team

## 📚 More Info

- **Full Guide**: TASK2_GUIDE.md
- **Implementation Details**: TASK2_SUMMARY.md
- **API Documentation**: API_DOCS.md
- **Overall Status**: CURRENT_STATUS.md

## 🎉 That's It!

Task 2 is ready to use. Have fun selecting your dream IPL team! 🏏
