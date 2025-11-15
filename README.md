# Token Counter

Python script to count Claude AI tokens for text files using Anthropic's official API.

## Features

- Count tokens for all `.txt` files in a directory
- Uses official Anthropic API for accurate counting
- Generates cost estimates based on model pricing
- Supports all Claude models (Sonnet, Opus, Haiku)
- Rate limiting to avoid API throttling
- Detailed reporting with recommendations

## Installation

### Prerequisites

- Python 3.12+
- `uv` package manager
- Anthropic API key

### Setup

```bash
# Clone repository
git clone https://github.com/rajipilipia/Token-Counter.git
cd Token-Counter

# Install dependencies with uv
uv sync
```

### API Key

Set your Anthropic API key as environment variable:

```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Basic Usage

```bash
uv run python token_counter.py /path/to/directory
```

### With Options

```bash
# Use specific model
uv run python token_counter.py /path/to/directory --model claude-opus-4

# Test with limited files
uv run python token_counter.py /path/to/directory --limit 10

# Save report to file
uv run python token_counter.py /path/to/directory --output report.txt
```

### Example

```bash
# Count tokens for email archive
uv run python token_counter.py "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

## Output

The script generates a report with:

- Total files processed
- Total token count
- Average tokens per file
- Cost estimate (based on input tokens)
- Recommendation (whether to feed to Claude Code)

Example output:

```
TOKEN COUNT REPORT
==================

Directory: /path/to/emails
Model: claude-sonnet-4-5

Files Processed: 1,825
Total Tokens: 312,450
Average Tokens per File: 171

Cost Estimate:
- Input tokens: 312,450
- Cost: $0.9374

RECOMMENDATION:
Moderate token count - consider selective loading
```

## Supported Models

- `claude-sonnet-4-5` (default) - $3 per 1M input tokens
- `claude-sonnet-3-5` - $3 per 1M input tokens
- `claude-opus-4` - $15 per 1M input tokens
- `claude-haiku-3-5` - $0.80 per 1M input tokens

## How It Works

1. Scans directory recursively for `.txt` files
2. Sends each file content to Anthropic's `count_tokens` API
3. Aggregates results with rate limiting
4. Calculates cost estimates based on official pricing
5. Provides recommendations based on token count thresholds

## Rate Limits

The script uses conservative rate limiting:

- Batch size: 50 files
- Delay: 0.1 seconds between batches

Anthropic API rate limits by tier:

- Free: 100 requests/minute
- Build: 1,000 requests/minute
- Scale: 8,000 requests/minute

## Notes

- Token counts are estimates (official API method)
- Actual usage may differ slightly when sending to Claude
- Skips files with encoding issues
- Uses UTF-8 encoding for all files

## Development

### Type Checking

```bash
uvx mypy token_counter.py
```

### Linting

```bash
ruff check token_counter.py
```

## License

MIT

## Author

Raji Pilipia
