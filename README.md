# Token Counter

Count Claude AI tokens for text files with two powerful methods:

1. **API-Based Counter** (`token_counter.py`) - 100% accurate using Anthropic's official API
2. **Offline Counter** (`offline_token_counter.py`) - ⭐ **NEW!** Count tokens locally without API calls

## Quick Comparison

| Feature | Offline Counter ⭐ | API Counter |
|---------|-------------------|-------------|
| **API Calls** | Zero | Yes |
| **Cost** | Free | ~$0.003 per 1K tokens |
| **Accuracy** | 75-95% | 100% |
| **Speed** | Very Fast | Slower (rate limited) |
| **Internet** | Not required* | Required |
| **Best For** | Quick estimates, development | Production, billing |

*First run downloads tokenizer (~500KB), then fully offline

## Features

### Both Counters
- Count tokens for all `.txt` files in a directory (or any file pattern)
- Supports all Claude models (Sonnet, Opus, Haiku)
- Detailed reporting with context window recommendations
- Windows path support (handles spaces properly)

### Offline Counter Specific
- ✅ **Zero API calls** - No tokens burned
- ✅ **Two methods** - Xenova tokenizer OR character estimation
- ✅ **Standalone** - Minimal dependencies
- ✅ **Fast** - Process thousands of files quickly

### API Counter Specific
- ✅ **100% accurate** - Official Anthropic API
- ✅ **Cost estimates** - Based on official pricing
- ✅ **Rate limiting** - Avoids API throttling

## Installation

### Quick Start (Offline Counter - Recommended)

```bash
# Clone repository
git clone https://github.com/rajipilipia/Token-Counter.git
cd Token-Counter

# Option 1: With Xenova tokenizer (most accurate offline)
pip install transformers
python offline_token_counter.py /path/to/directory

# Option 2: Pure estimation (no dependencies)
python offline_token_counter.py /path/to/directory --method estimation
```

### Full Setup (Both Counters)

```bash
# Clone repository
git clone https://github.com/rajipilipia/Token-Counter.git
cd Token-Counter

# For offline counter (optional)
pip install transformers

# For API counter (requires API key)
uv sync
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Offline Counter (Recommended for Quick Estimates)

```bash
# Basic usage - auto-detect best method
python offline_token_counter.py /path/to/directory

# Your email directory example
python offline_token_counter.py "G:/My Drive/Google AI Studio/Logan Stone/Rock Center_TSQ/CPM/context/Emails"

# With options
python offline_token_counter.py /path/to/directory --show-files --verbose
python offline_token_counter.py /path/to/directory --method estimation  # No dependencies
python offline_token_counter.py /path/to/directory --pattern "*.md"     # Markdown files
python offline_token_counter.py /path/to/directory --limit 10            # Test first
python offline_token_counter.py /path/to/directory --output report.txt  # Save report
```

**See [OFFLINE_USAGE.md](OFFLINE_USAGE.md) for complete offline counter documentation.**

### API Counter (For 100% Accuracy)

```bash
# Basic usage
uv run python token_counter.py /path/to/directory

# With options
uv run python token_counter.py /path/to/directory --model claude-opus-4
uv run python token_counter.py /path/to/directory --limit 10
uv run python token_counter.py /path/to/directory --output report.txt

# Your email directory example
uv run python token_counter.py "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

**See [QUICK_START.md](QUICK_START.md) for complete API counter documentation.**

## Output

### Offline Counter Report Example

```
======================================================================
OFFLINE TOKEN COUNT REPORT
======================================================================

Directory: /path/to/emails
Method: XENOVA
  (Xenova/claude-tokenizer - accurate for Claude 2.x)

SUMMARY
----------------------------------------------------------------------
Files Processed:      1,825
Total Tokens:         312,450
Total Characters:     1,249,800
Total Words:          234,567

Avg Tokens/File:      171.21
Avg Chars/Token:      4.00
Processing Time:      3.45 seconds

CLAUDE CONTEXT WINDOW USAGE
----------------------------------------------------------------------
Claude Sonnet 4.5    (200,000 tokens): 156.23% used
Claude Opus 4        (200,000 tokens): 156.23% used

RECOMMENDATION
----------------------------------------------------------------------
⚠ HIGH token count - Requires strategy
  Recommended approaches:
  - Feed files in multiple batches
  - Use file filtering/selection
  - Summarize less relevant files first
======================================================================
```

### API Counter Report Example

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

### Offline Counter

1. Scans directory recursively for text files
2. **Method 1 (Xenova)**: Uses `Xenova/claude-tokenizer` from Hugging Face
   - Downloads tokenizer once (~500KB)
   - Highly accurate for Claude 2.x (~95%)
   - Reasonable estimate for Claude 3+ (~80%)
3. **Method 2 (Estimation)**: Character-based calculation
   - Formula: `tokens = characters / 4`
   - No dependencies, instant results
   - ~75-85% accuracy
4. Generates detailed report with recommendations

### API Counter

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

## Which Counter Should I Use?

### Use Offline Counter When:
- ✅ You want quick estimates without burning API tokens
- ✅ Processing large directories (thousands of files)
- ✅ Development/testing phase
- ✅ Cost is a concern
- ✅ You don't have internet access

### Use API Counter When:
- ✅ You need 100% accurate counts
- ✅ Billing/production requirements
- ✅ Official cost estimates are needed
- ✅ Small number of files
- ✅ Accuracy is critical

**Recommended workflow:** Use offline counter for initial estimates, then API counter for final verification if needed.

## Token Counting Methods Explained

### Xenova Tokenizer (Offline - Most Accurate)
- Based on Claude 2.x official tokenizer
- ~95% accuracy for Claude 2.x
- ~80% accuracy for Claude 3+
- ~75% accuracy for Claude 4
- Requires: `pip install transformers`

### Character Estimation (Offline - Simple)
- Formula: `tokens ≈ characters / 4`
- ~75-85% accuracy for English text
- No dependencies required
- Instant calculation

### API Method (Online - Perfect)
- Uses Anthropic's official `count_tokens` endpoint
- 100% accurate for all Claude models
- Requires API key
- Costs: ~$0.003 per 1K tokens counted

## Notes

- **Offline counter**: Token counts are estimates (75-95% accurate)
- **API counter**: Token counts are exact (100% accurate)
- Both skip files with encoding issues
- Both use UTF-8 encoding by default
- Both handle Windows paths with spaces

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
