# GPT-4 AI Integration for Team Selection

## Overview

The IPLOps environment now supports **real AI-powered team selection** using OpenAI's GPT-4 model. The system intelligently falls back to algorithmic selection if GPT-4 is unavailable.

## How It Works

### Selection Flow

1. **GPT-4 First**: If OpenAI API key is configured, the system uses GPT-4 for natural language analysis
2. **Algorithmic Fallback**: If GPT-4 is unavailable, uses sophisticated multi-criteria scoring algorithm
3. **UI Indication**: The UI clearly shows which method was used (🧠 GPT-4 AI or 📊 Algorithmic)

### GPT-4 Selection Process

When GPT-4 is available:

1. **Context Preparation**: System sends match conditions, pitch report, opponent profile, and full squad to GPT-4
2. **AI Analysis**: GPT-4 analyzes all factors using natural language reasoning
3. **Selection**: GPT-4 returns 11 player IDs with reasoning and strategy
4. **Display**: UI shows GPT-4's reasoning and selected team

### Algorithmic Selection Process

When GPT-4 is unavailable:

1. **Multi-Criteria Scoring**: Each player scored on 5 criteria:
   - Recent Form (25%)
   - Pitch Suitability (35%) - Most important
   - Batting Average (15%)
   - Strike Rate (10%)
   - Opponent Matchup (15%)

2. **Dynamic Composition**: Team composition changes based on pitch type
3. **Minimum 5 Bowlers**: Enforced automatically
4. **Role Balance**: Ensures proper mix of batsmen, bowlers, all-rounders, wicket-keeper

## Configuration

### Option 1: OpenAI API (Recommended)

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-..."

# Optional: Custom API base URL
export API_BASE_URL="https://api.openai.com/v1"

# Optional: Custom model name (default: gpt-4)
export MODEL_NAME="gpt-4"
```

### Option 2: Hugging Face Inference API

```bash
# Use HF token as fallback
export HF_TOKEN="hf_..."
export API_BASE_URL="https://api-inference.huggingface.co/models/..."
export MODEL_NAME="your-model-name"
```

### Option 3: No API Key (Algorithmic Only)

If no API key is set, the system automatically uses the algorithmic selection method.

## Testing

### Test with GPT-4

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Start server
python app/main.py

# Open browser
# Navigate to http://localhost:8000/task2.html
# Click "🎲 Load Match & AI Select Team"
# Look for "🧠 GPT-4 AI" badge in AI Recommendation panel
```

### Test Algorithmic Fallback

```bash
# Don't set any API key
unset OPENAI_API_KEY
unset HF_TOKEN

# Start server
python app/main.py

# Open browser
# Navigate to http://localhost:8000/task2.html
# Click "🎲 Load Match & AI Select Team"
# Look for "📊 Algorithmic" badge in AI Recommendation panel
```

## UI Features

### Selection Method Badge

- **🧠 GPT-4 AI** (Green): Using OpenAI GPT-4 for selection
- **📊 Algorithmic** (Blue): Using multi-criteria scoring algorithm

### GPT-4 Reasoning Display

When GPT-4 is used, the UI shows:
- Purple gradient box with GPT-4's reasoning
- Key strategy explanation
- Selection criteria weights
- Team strength metrics

### Algorithmic Display

When algorithmic selection is used:
- Selection criteria weights (Form 25%, Pitch 35%, etc.)
- Top 15 players by score in server logs
- Detailed pitch-based composition logic

## API Response Format

Both methods return the same format:

```json
{
  "selected_players": ["Player 1", "Player 2", ...],
  "selected_players_full": [...],
  "batting_order": [...],
  "bowling_plan": [...],
  "reasoning": {
    "pitch_analysis": "...",
    "team_composition": "...",
    "key_players": [...],
    "strategy": "...",
    "opponent_weakness": "...",
    "gpt_reasoning": "..." // Only for GPT-4
  },
  "team_strength": {
    "batting": 0.85,
    "bowling": 0.78,
    "form": 0.82,
    "overall": 0.82
  },
  "selection_method": "GPT-4 AI" or "Algorithmic",
  "selection_criteria": {
    "method": "OpenAI GPT-4" or "Multi-criteria scoring",
    "form_weight": "25%",
    "pitch_weight": "35%",
    ...
  }
}
```

## Advantages

### GPT-4 Selection
- Natural language reasoning
- Contextual understanding
- Flexible decision making
- Explains reasoning in human terms

### Algorithmic Selection
- Fast and deterministic
- No API costs
- Transparent scoring
- Proven multi-criteria analysis

## Server Logs

### GPT-4 Mode
```
[AI] OpenAI client initialized - will use GPT for team selection
🧠 Using OpenAI GPT-4 for intelligent team selection...
✅ GPT-4 selected 11 players
💡 Strategy: Spin-heavy attack with power hitters
```

### Algorithmic Mode
```
[AI] No API key found, using algorithmic selection
📊 Using algorithmic selection (no OpenAI API key)
📊 ALGORITHMIC SELECTION - MULTI-CRITERIA ANALYSIS
📊 TOP 15 PLAYERS BY SCORE:
 1. Player Name              | Score: 0.856 | Form:0.85 Pitch:0.95 | BOWLER
...
```

## Cost Considerations

- **GPT-4**: ~$0.03 per team selection (500 tokens)
- **Algorithmic**: Free, no API costs

For development/testing, use algorithmic mode. For production with budget, use GPT-4.

## Troubleshooting

### GPT-4 Not Working

1. Check API key is set: `echo $OPENAI_API_KEY`
2. Check server logs for error messages
3. Verify API key has GPT-4 access
4. Check API rate limits

### Always Using Algorithmic

1. Verify environment variable is set before starting server
2. Check server startup logs for "[AI] OpenAI client initialized"
3. If you see "[AI] No API key found", the variable isn't set

### Invalid Selections

1. Check server logs for detailed scoring
2. Verify squad has enough players of each role
3. Check pitch report is valid
4. Ensure minimum 5 bowlers rule is enforced

## Future Enhancements

- [ ] Support for other LLM providers (Anthropic Claude, Google Gemini)
- [ ] Fine-tuned models specifically for cricket
- [ ] Historical performance learning
- [ ] A/B testing between GPT-4 and algorithmic
- [ ] Hybrid mode: GPT-4 + algorithmic validation
