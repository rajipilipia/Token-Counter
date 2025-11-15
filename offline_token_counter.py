#!/usr/bin/env python3
"""
Offline Claude Token Counter
=============================
Counts tokens in text files WITHOUT using the Anthropic API.
No tokens burned, no costs.

Author: Token Counter
License: MIT
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class TokenCountMethod(Enum):
    """Available token counting methods"""
    XENOVA = "xenova"           # Most accurate offline method
    ESTIMATION = "estimation"    # Simple character-based estimation
    AUTO = "auto"               # Try Xenova, fallback to estimation


@dataclass
class FileResult:
    """Result for a single file"""
    file_path: str
    tokens: int
    characters: int
    words: int
    lines: int
    chars_per_token: float
    method: str
    error: Optional[str] = None


@dataclass
class CounterReport:
    """Complete token counting report"""
    directory: str
    total_files: int
    total_tokens: int
    total_characters: int
    total_words: int
    total_lines: int
    avg_tokens_per_file: float
    avg_chars_per_token: float
    method: str
    files: List[FileResult]
    processing_time: float


class OfflineTokenCounter:
    """
    Offline token counter for Claude AI.

    Uses Xenova/claude-tokenizer for accurate offline counting,
    with character-based estimation as fallback.
    """

    def __init__(self, method: TokenCountMethod = TokenCountMethod.AUTO, verbose: bool = False):
        self.method = method
        self.verbose = verbose
        self.tokenizer = None
        self.actual_method = None

        if method in (TokenCountMethod.XENOVA, TokenCountMethod.AUTO):
            self._try_load_xenova()

        if self.tokenizer is None and method == TokenCountMethod.XENOVA:
            print("ERROR: Xenova tokenizer requested but not available", file=sys.stderr)
            print("Install with: pip install transformers", file=sys.stderr)
            sys.exit(1)

        # Set actual method used
        if self.tokenizer is not None:
            self.actual_method = "xenova"
        else:
            self.actual_method = "estimation"

    def _try_load_xenova(self):
        """Try to load Xenova/claude-tokenizer"""
        try:
            from transformers import GPT2TokenizerFast

            if self.verbose:
                print("Loading Xenova/claude-tokenizer...", file=sys.stderr)

            # Try to load from cache first (offline mode)
            try:
                self.tokenizer = GPT2TokenizerFast.from_pretrained(
                    'Xenova/claude-tokenizer',
                    local_files_only=True
                )
                if self.verbose:
                    print("✓ Loaded tokenizer from cache (offline)", file=sys.stderr)
            except Exception:
                # Download if not in cache
                if self.verbose:
                    print("Downloading tokenizer (first time only)...", file=sys.stderr)
                self.tokenizer = GPT2TokenizerFast.from_pretrained(
                    'Xenova/claude-tokenizer'
                )
                if self.verbose:
                    print("✓ Downloaded and cached tokenizer", file=sys.stderr)

        except ImportError:
            if self.verbose:
                print("⚠ transformers library not installed, using estimation method", file=sys.stderr)
                print("  Install with: pip install transformers", file=sys.stderr)
        except Exception as e:
            if self.verbose:
                print(f"⚠ Could not load Xenova tokenizer: {e}", file=sys.stderr)
                print("  Falling back to estimation method", file=sys.stderr)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text using the configured method"""
        if self.tokenizer is not None:
            # Use Xenova tokenizer (most accurate)
            return len(self.tokenizer.encode(text))
        else:
            # Use character-based estimation
            # Claude averages ~3.5-4 characters per token
            return max(1, len(text) // 4)

    def count_file_tokens(self, file_path: Path) -> FileResult:
        """Count tokens for a single file"""
        try:
            # Read file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Count tokens
            tokens = self.count_tokens(content)

            # Calculate metrics
            characters = len(content)
            words = len(content.split())
            lines = content.count('\n') + 1
            chars_per_token = characters / tokens if tokens > 0 else 0

            return FileResult(
                file_path=str(file_path),
                tokens=tokens,
                characters=characters,
                words=words,
                lines=lines,
                chars_per_token=round(chars_per_token, 2),
                method=self.actual_method
            )

        except UnicodeDecodeError as e:
            return FileResult(
                file_path=str(file_path),
                tokens=0,
                characters=0,
                words=0,
                lines=0,
                chars_per_token=0,
                method=self.actual_method,
                error=f"Encoding error: {e}"
            )
        except Exception as e:
            return FileResult(
                file_path=str(file_path),
                tokens=0,
                characters=0,
                words=0,
                lines=0,
                chars_per_token=0,
                method=self.actual_method,
                error=str(e)
            )

    def count_directory_tokens(
        self,
        directory: Path,
        pattern: str = "*.txt",
        limit: Optional[int] = None,
        verbose_progress: bool = False
    ) -> CounterReport:
        """
        Count tokens for all matching files in directory.

        Args:
            directory: Directory to scan
            pattern: File pattern (e.g., "*.txt", "*.md")
            limit: Optional limit on number of files to process
            verbose_progress: Show progress for each file

        Returns:
            CounterReport with detailed statistics
        """
        start_time = time.time()

        # Find all matching files
        if self.verbose:
            print(f"\nScanning directory: {directory}", file=sys.stderr)
            print(f"Pattern: {pattern}", file=sys.stderr)

        files = sorted(directory.rglob(pattern))

        if limit:
            files = files[:limit]

        if self.verbose:
            print(f"Found {len(files)} files\n", file=sys.stderr)

        if len(files) == 0:
            print(f"\nWARNING: No files matching '{pattern}' found in {directory}", file=sys.stderr)
            print(f"Try using --pattern '*.*' to scan all files", file=sys.stderr)
            print(f"Or --pattern '*.{{txt,md,py,js}}' for specific types\n", file=sys.stderr)

        # Process files
        results = []
        total_tokens = 0
        total_chars = 0
        total_words = 0
        total_lines = 0
        errors = 0

        for i, file_path in enumerate(files, 1):
            if verbose_progress or self.verbose:
                print(f"Processing [{i}/{len(files)}]: {file_path.name}", file=sys.stderr)

            result = self.count_file_tokens(file_path)
            results.append(result)

            if result.error:
                errors += 1
                if verbose_progress:
                    print(f"  ⚠ Error: {result.error}", file=sys.stderr)
            else:
                total_tokens += result.tokens
                total_chars += result.characters
                total_words += result.words
                total_lines += result.lines

                if verbose_progress:
                    print(f"  ✓ Tokens: {result.tokens:,}", file=sys.stderr)

        processing_time = time.time() - start_time

        # Calculate averages
        successful_files = len(files) - errors
        avg_tokens = total_tokens / successful_files if successful_files > 0 else 0
        avg_chars_per_token = total_chars / total_tokens if total_tokens > 0 else 0

        if self.verbose:
            print(f"\n✓ Processing complete in {processing_time:.2f} seconds", file=sys.stderr)
            if errors > 0:
                print(f"⚠ {errors} files had errors", file=sys.stderr)

        return CounterReport(
            directory=str(directory),
            total_files=len(files),
            total_tokens=total_tokens,
            total_characters=total_chars,
            total_words=total_words,
            total_lines=total_lines,
            avg_tokens_per_file=round(avg_tokens, 2),
            avg_chars_per_token=round(avg_chars_per_token, 2),
            method=self.actual_method,
            files=results,
            processing_time=round(processing_time, 2)
        )


def format_report(report: CounterReport, show_files: bool = False) -> str:
    """Format report as human-readable text"""
    lines = []
    lines.append("=" * 70)
    lines.append("OFFLINE TOKEN COUNT REPORT")
    lines.append("=" * 70)
    lines.append("")

    # Directory info
    lines.append(f"Directory: {report.directory}")
    lines.append(f"Method: {report.method.upper()}")

    if report.method == "estimation":
        lines.append("  (character-based estimation: ~4 chars per token)")
    else:
        lines.append("  (Xenova/claude-tokenizer - accurate for Claude 2.x)")

    lines.append("")

    # Summary statistics
    lines.append("SUMMARY")
    lines.append("-" * 70)
    lines.append(f"Files Processed:      {report.total_files:,}")
    lines.append(f"Total Tokens:         {report.total_tokens:,}")
    lines.append(f"Total Characters:     {report.total_characters:,}")
    lines.append(f"Total Words:          {report.total_words:,}")
    lines.append(f"Total Lines:          {report.total_lines:,}")
    lines.append("")
    lines.append(f"Avg Tokens/File:      {report.avg_tokens_per_file:,.2f}")
    lines.append(f"Avg Chars/Token:      {report.avg_chars_per_token:.2f}")
    lines.append(f"Processing Time:      {report.processing_time:.2f} seconds")
    lines.append("")

    # Claude context window recommendations
    lines.append("CLAUDE CONTEXT WINDOW USAGE")
    lines.append("-" * 70)

    # Claude model limits
    models = {
        "Claude Sonnet 4.5": 200_000,
        "Claude Opus 4": 200_000,
        "Claude Haiku 3.5": 200_000,
    }

    for model_name, limit in models.items():
        percentage = (report.total_tokens / limit) * 100
        lines.append(f"{model_name:20} ({limit:,} tokens): {percentage:6.2f}% used")

    lines.append("")

    # Recommendations
    lines.append("RECOMMENDATION")
    lines.append("-" * 70)

    if report.total_tokens < 50_000:
        lines.append("✓ LOW token count - Perfect for direct Claude Code usage")
        lines.append("  All files can be fed directly to Claude with plenty of headroom.")
    elif report.total_tokens < 100_000:
        lines.append("✓ MODERATE token count - Good for Claude Code")
        lines.append("  Files can be fed directly, but monitor context usage.")
    elif report.total_tokens < 150_000:
        lines.append("⚠ MODERATE-HIGH token count - Use selectively")
        lines.append("  Consider feeding files in batches or filtering by relevance.")
    else:
        lines.append("⚠ HIGH token count - Requires strategy")
        lines.append("  Recommended approaches:")
        lines.append("  - Feed files in multiple batches")
        lines.append("  - Use file filtering/selection")
        lines.append("  - Summarize less relevant files first")

    lines.append("")

    # Detailed file listing
    if show_files:
        lines.append("DETAILED FILE BREAKDOWN")
        lines.append("-" * 70)
        lines.append(f"{'Tokens':>10} {'Characters':>12} {'Words':>10} {'File'}")
        lines.append("-" * 70)

        # Sort by token count (descending)
        sorted_files = sorted(report.files, key=lambda x: x.tokens, reverse=True)

        for result in sorted_files:
            if result.error:
                lines.append(f"{'ERROR':>10} {'':>12} {'':>10} {result.file_path}")
                lines.append(f"  Error: {result.error}")
            else:
                filename = Path(result.file_path).name
                lines.append(f"{result.tokens:>10,} {result.characters:>12,} {result.words:>10,} {filename}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("")

    # Disclaimer
    if report.method == "estimation":
        lines.append("NOTE: Token counts are estimates based on character count.")
        lines.append("      For exact counts, install transformers library:")
        lines.append("      pip install transformers")
    else:
        lines.append("NOTE: Token counts use Xenova/claude-tokenizer.")
        lines.append("      Highly accurate for Claude 2.x models.")
        lines.append("      Reasonable estimate for Claude 3+ models.")

    lines.append("")

    return "\n".join(lines)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Offline Claude Token Counter - Count tokens without API calls",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count tokens in a single file
  %(prog)s /path/to/file.txt
  %(prog)s "G:/My Drive/document.txt"

  # Count tokens in directory (auto-detect best method)
  %(prog)s /path/to/directory
  %(prog)s "G:/My Drive/Documents"

  # Use specific method
  %(prog)s /path/to/directory --method xenova
  %(prog)s /path/to/directory --method estimation

  # Count specific file types in directory
  %(prog)s /path/to/directory --pattern "*.md"

  # Limit number of files (for testing)
  %(prog)s /path/to/directory --limit 10

  # Show detailed file breakdown
  %(prog)s /path/to/directory --show-files

  # Save report to file
  %(prog)s /path/to/directory --output report.txt

  # Windows paths with spaces (use quotes and forward slashes)
  %(prog)s "G:/My Drive/Documents/file.txt"
  %(prog)s "G:/My Drive/Documents" --verbose

Methods:
  auto        - Try Xenova tokenizer, fallback to estimation (default)
  xenova      - Use Xenova/claude-tokenizer (requires: pip install transformers)
  estimation  - Simple character-based estimation (no dependencies)
        """
    )

    parser.add_argument(
        "path",
        type=str,
        help="File or directory to scan for text files"
    )

    parser.add_argument(
        "--pattern",
        type=str,
        default="*.txt",
        help="File pattern to match (default: *.txt)"
    )

    parser.add_argument(
        "--method",
        type=str,
        choices=["auto", "xenova", "estimation"],
        default="auto",
        help="Token counting method (default: auto)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of files to process (for testing)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file for report (default: stdout)"
    )

    parser.add_argument(
        "--show-files",
        action="store_true",
        help="Show detailed breakdown for each file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose progress information"
    )

    args = parser.parse_args()

    # Convert path (handle Windows paths with spaces)
    path = Path(args.path)

    # Validate path exists
    if not path.exists():
        print(f"ERROR: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Create counter
    method = TokenCountMethod[args.method.upper()]
    counter = OfflineTokenCounter(method=method, verbose=args.verbose)

    # Handle both files and directories
    if path.is_file():
        # Single file mode
        if args.verbose:
            print(f"\nProcessing single file: {path}", file=sys.stderr)

        result = counter.count_file_tokens(path)

        # Create a minimal report for single file
        report = CounterReport(
            directory=str(path.parent),
            total_files=1,
            total_tokens=result.tokens,
            total_characters=result.characters,
            total_words=result.words,
            total_lines=result.lines,
            avg_tokens_per_file=result.tokens,
            avg_chars_per_token=result.chars_per_token,
            method=counter.actual_method,
            files=[result],
            processing_time=0.0
        )

        # Format report
        report_text = format_report(report, show_files=True)

    elif path.is_dir():
        # Directory mode (existing behavior)
        if args.verbose:
            print(f"\nScanning directory: {path}", file=sys.stderr)

        report = counter.count_directory_tokens(
            directory=path,
            pattern=args.pattern,
            limit=args.limit,
            verbose_progress=args.verbose
        )

        # Format report
        report_text = format_report(report, show_files=args.show_files)
    else:
        print(f"ERROR: Path is neither file nor directory: {path}", file=sys.stderr)
        sys.exit(1)

    # Output report
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"\n✓ Report saved to: {args.output}", file=sys.stderr)
    else:
        print(report_text)


if __name__ == "__main__":
    main()
