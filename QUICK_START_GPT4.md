# Quick Start: GPT-4 Team Selection

## 🚀 30-Second Setup

### Without GPT-4 (Free, Works Now)

```bash
python app/main.py
```

Open http://localhost:8000/task2.html → Click "🎲 Load Match & AI Select Team"

Look for **📊 Algorithmic** badge (blue)

### With GPT-4 (Requires API Key)

```bash
export OPENAI_API_KEY="sk-..."
python app/main.py
```

Open http://localhost:8000/task2.html → Click "🎲 Load Match & AI Select Team"

Look for **🧠 GPT-4 AI** badge (green)

## 🧪 Test It

```bash
python test_gpt4_integration.py
```

Expected:
- ✅ Algorithmic test passes
- ⚠️ GPT-4 test skipped (if no API key)

## 📊 What You'll See

### Algorithmic Mode (No API Key)
```
📊 Using algorithmic selection (no OpenAI API key)
📊 TOP 15 PLAYERS BY SCORE:
 1. Tim David | Score: 0.953 | Form:1.00 Pitch:0.95 | BATSMAN
 ...
✅ Selected 11 players
Team Strength: 96.93%
```

### GPT-4 Mode (With API Key)
```
🧠 Using OpenAI GPT-4 for intelligent team selection...
✅ GPT-4 selected 11 players
💡 Strategy: Spin-heavy attack with power hitters
Team Strength: 94.50%
```

## 🎨 UI Indicators

| Badge | Color | Meaning |
|-------|-------|---------|
| 🧠 GPT-4 AI | Green | Using OpenAI GPT-4 |
| 📊 Algorithmic | Blue | Using multi-criteria scoring |

## 💰 Cost

- **Algorithmic**: Free
- **GPT-4**: ~$0.03 per team selection

## 📚 More Info

- Full guide: `GPT4_INTEGRATION.md`
- Summary: `GPT4_COMPLETE.md`
- Status: `CURRENT_STATUS.md`

## ✅ Status

**COMPLETE** - Both modes working and tested!
