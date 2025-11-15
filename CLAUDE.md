# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Token Counter is a Python CLI tool that counts Claude AI tokens for text files using Anthropic's official `count_tokens` API. Used to estimate costs and determine feasibility before feeding large document sets to Claude Code.

## Key Commands

### Running the Script
```bash
# Basic usage
uv run python token_counter.py /path/to/directory

# With specific model
uv run python token_counter.py /path/to/directory --model claude-opus-4

# Test with limited files
uv run python token_counter.py /path/to/directory --limit 10

# Save report to file
uv run python token_counter.py /path/to/directory --output report.txt

# Example with email archive
uv run python token_counter.py "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

### Development Commands
```bash
# Install dependencies (CRITICAL: Use uv exclusively, never pip)
uv sync

# Type checking
uvx mypy token_counter.py

# Linting
ruff check token_counter.py

# Format code
ruff format token_counter.py
```

## Architecture

### Core Components

**Single-file architecture** (`token_counter.py`):
- `get_txt_files()` - Recursive directory scanner for .txt files
- `count_tokens_for_file()` - Per-file token counting via Anthropic API
- `count_tokens_batch()` - Batch processor with rate limiting
- `estimate_cost()` - Cost calculation based on model pricing
- `main()` - CLI argument parsing and report generation

### Processing Flow

1. **Directory Scan** - Recursively finds all `.txt` files
2. **Batch Processing** - Processes files in batches of 50 with 0.1s delays
3. **Token Counting** - Uses Anthropic `messages.count_tokens()` API
4. **Cost Estimation** - Calculates cost based on model-specific pricing
5. **Report Generation** - Outputs formatted report with recommendations

### Rate Limiting Strategy

Conservative rate limiting to avoid API throttling:
- Batch size: 50 files per checkpoint
- Delay: 0.1 seconds between batches
- Anthropic API limits:
  - Free tier: 100 requests/minute
  - Build tier: 1,000 requests/minute
  - Scale tier: 8,000 requests/minute

## Configuration

### Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com/settings/keys

Setting API key:
```bash
# Windows Command Prompt
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Linux/Mac
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Model Pricing (as of code)

Token counting uses these pricing tiers:
- `claude-sonnet-4-5`: $3 per 1M input tokens (default)
- `claude-sonnet-3-5`: $3 per 1M input tokens
- `claude-opus-4`: $15 per 1M input tokens
- `claude-haiku-3-5`: $0.80 per 1M input tokens

### Recommendation Thresholds

- **< 100K tokens**: Low - feed directly to Claude Code
- **100K-500K tokens**: Moderate - consider selective loading
- **> 500K tokens**: High - recommend summarization or chunking

## Error Handling

- **UnicodeDecodeError**: Skips files with encoding issues, logs warning
- **API errors**: Logs error per file, continues processing
- **Missing directory**: Exits with error message
- **Missing API key**: Exits with error message
- Uses UTF-8 encoding for all file reads

## Development Standards

### Python Requirements
- Python 3.12+ (specified in `pyproject.toml`)
- Uses `uv` for package management (NEVER use pip)
- Dependencies: `anthropic>=0.39.0`

### Code Quality
- Ruff configuration:
  - Line length: 100 characters
  - Target: Python 3.12
  - Linting rules: E (errors), F (pyflakes), I (isort)
- Type hints throughout
- UTF-8 encoding for file operations
