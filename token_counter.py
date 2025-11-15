#!/usr/bin/env python3
"""Count Claude AI tokens for text files using Anthropic API."""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

import anthropic


def get_txt_files(directory: Path) -> List[Path]:
    """Recursively find all .txt files in directory."""
    return sorted(directory.rglob("*.txt"))


def count_tokens_for_file(
    client: anthropic.Anthropic,
    file_path: Path,
    model: str
) -> int:
    """Count tokens for a single file using Anthropic API."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        response = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": content}]
        )

        return response.input_tokens

    except UnicodeDecodeError:
        print(f"Warning: Could not read {file_path} (encoding issue)", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return 0


def count_tokens_batch(
    client: anthropic.Anthropic,
    files: List[Path],
    model: str,
    batch_size: int = 50,
    delay: float = 0.1
) -> Dict[str, Any]:
    """Count tokens for multiple files with rate limiting."""
    total_tokens = 0
    file_tokens = {}

    for i, file_path in enumerate(files, 1):
        tokens = count_tokens_for_file(client, file_path, model)
        file_tokens[str(file_path)] = tokens
        total_tokens += tokens

        if i % batch_size == 0:
            print(f"Processed {i}/{len(files)} files...", file=sys.stderr)
            time.sleep(delay)

    return {
        "total_tokens": total_tokens,
        "file_count": len(files),
        "avg_tokens_per_file": total_tokens / len(files) if files else 0,
        "file_tokens": file_tokens
    }


def estimate_cost(tokens: int, model: str) -> float:
    """Estimate cost based on token count and model."""
    pricing = {
        "claude-sonnet-4-5": 0.003,  # $3 per 1M input tokens
        "claude-sonnet-3-5": 0.003,
        "claude-opus-4": 0.015,      # $15 per 1M input tokens
        "claude-haiku-3-5": 0.0008,  # $0.80 per 1M input tokens
    }

    cost_per_1k = pricing.get(model, 0.003)
    return (tokens / 1000) * cost_per_1k


def main():
    parser = argparse.ArgumentParser(
        description="Count Claude AI tokens for text files"
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing .txt files"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-5",
        help="Claude model to use for token counting (default: claude-sonnet-4-5)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of files to process (for testing)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output report to file (default: stdout)"
    )

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"Scanning directory: {args.directory}", file=sys.stderr)
    files = get_txt_files(args.directory)

    if not files:
        print(f"No .txt files found in {args.directory}", file=sys.stderr)
        sys.exit(0)

    if args.limit:
        files = files[:args.limit]

    print(f"Found {len(files)} .txt files", file=sys.stderr)
    print(f"Counting tokens using model: {args.model}", file=sys.stderr)
    print("", file=sys.stderr)

    results = count_tokens_batch(client, files, args.model)

    report = f"""
TOKEN COUNT REPORT
==================

Directory: {args.directory}
Model: {args.model}

Files Processed: {results['file_count']:,}
Total Tokens: {results['total_tokens']:,}
Average Tokens per File: {results['avg_tokens_per_file']:.0f}

Cost Estimate:
- Input tokens: {results['total_tokens']:,}
- Cost: ${estimate_cost(results['total_tokens'], args.model):.4f}

RECOMMENDATION:
"""

    if results['total_tokens'] < 100000:
        report += "Worth feeding to Claude Code (low token count)\n"
    elif results['total_tokens'] < 500000:
        report += "Moderate token count - consider selective loading\n"
    else:
        report += "High token count - recommend summarization or selective loading\n"

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
