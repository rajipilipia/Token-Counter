# Quick Start Guide

## Set API Key

Get your Anthropic API key from: https://console.anthropic.com/settings/keys

### Windows (Command Prompt)
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Windows (PowerShell)
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Linux/Mac
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## Run Token Counter

### Test with 10 files
```bash
cd "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\Token-Counter"
uv run python token_counter.py "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails" --limit 10
```

### Full scan (1,825 files)
```bash
cd "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\Token-Counter"
uv run python token_counter.py "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails" --output email_tokens_report.txt
```

## Expected Results

Based on directory analysis:
- Files: 1,825 .txt files
- Size: 1.04 MB
- Estimated tokens: ~312,000 tokens
- Estimated cost: ~$0.94 (using Sonnet 4.5)

## Recommendations

Token count thresholds:
- < 100K tokens: Low - feed directly to Claude Code
- 100K-500K tokens: Moderate - selective loading recommended
- > 500K tokens: High - summarization or chunking needed

With ~312K estimated tokens, you're in the moderate range.
Consider:
1. Loading most recent emails only
2. Filtering by date range
3. Filtering by stakeholder
4. Creating summaries by category
