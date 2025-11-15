# Windows Usage Guide - Offline Token Counter

## Quick Start for Windows Users

This guide shows you how to easily count Claude AI tokens on Windows using **drag-and-drop batch files**.

## Prerequisites

- **Python 3.12+** installed ([Download here](https://www.python.org/downloads/))
- Make sure to check "Add Python to PATH" during installation

## Three Easy Methods

### Method 1: AUTO (Recommended) - `count_tokens.bat`

**Best for:** Most users - automatically chooses best available method

**How to use:**
1. Drag and drop ANY file or folder onto `count_tokens.bat`
2. Wait for results
3. Optionally save detailed report

**Features:**
- Tries Xenova tokenizer first (most accurate)
- Falls back to estimation if Xenova not installed
- Works with any path

### Method 2: XENOVA - `count_tokens_xenova.bat`

**Best for:** Maximum accuracy (~95% for Claude 2.x, ~80% for Claude 3+)

**Requirements:**
- Requires `transformers` library
- Batch file will offer to install it automatically

**How to use:**
1. Drag and drop ANY file or folder onto `count_tokens_xenova.bat`
2. If prompted, choose "y" to install transformers
3. Wait for results

### Method 3: ESTIMATION - `count_tokens_estimate.bat`

**Best for:** Quick estimates, no installation needed

**Features:**
- No dependencies required (pure Python)
- Very fast
- ~75-85% accuracy

**How to use:**
1. Drag and drop ANY file or folder onto `count_tokens_estimate.bat`
2. Get instant results

## Step-by-Step Instructions

### Option A: Drag and Drop (Easiest!)

1. **Find your file or folder** in Windows Explorer
   - Example: `G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails`

2. **Drag and drop** onto one of the batch files:
   - `count_tokens.bat` (auto-detect method)
   - `count_tokens_xenova.bat` (most accurate)
   - `count_tokens_estimate.bat` (fastest, no dependencies)

3. **View results** in the console window

4. **Save report** (optional)
   - When prompted, type `y` and press Enter
   - Report will be saved next to your input file/folder

### Option B: Command Line

Open Command Prompt or PowerShell in the Token-Counter folder:

```cmd
REM Count tokens in a single file
count_tokens.bat "G:\My Drive\document.txt"

REM Count tokens in a folder
count_tokens.bat "G:\My Drive\Emails"

REM Use specific methods
count_tokens_xenova.bat "G:\My Drive\Emails"
count_tokens_estimate.bat "G:\My Drive\Emails"
```

### Option C: Right-Click "Send To" (Advanced)

Create a shortcut in your SendTo folder for even easier access:

1. Press `Win + R` and type: `shell:sendto`
2. Create a shortcut to `count_tokens.bat` in that folder
3. Now you can right-click any file/folder → Send To → count_tokens

## Your Email Directory Example

For your specific path: `G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails`

### Quick Estimate (No Dependencies)

```cmd
count_tokens_estimate.bat "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

### Most Accurate Count

```cmd
count_tokens_xenova.bat "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

### Auto-Detect Best Method

```cmd
count_tokens.bat "G:\My Drive\Google AI Studio\Logan Stone\Rock Center_TSQ\CPM\context\Emails"
```

## What You'll See

### Example Output

```
========================================
Claude Offline Token Counter
========================================

Input: G:\My Drive\Emails
Method: AUTO (Xenova or Estimation)

Counting tokens...

Scanning directory: G:\My Drive\Emails
Pattern: *.txt
Found 1,825 files

Processing [1/1825]: email001.txt
  ✓ Tokens: 234
Processing [2/1825]: email002.txt
  ✓ Tokens: 156
...

======================================================================
OFFLINE TOKEN COUNT REPORT
======================================================================

Directory: G:\My Drive\Emails
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

========================================
Token counting complete!
========================================

Save report to file? (y/n):
```

## Path Formats

Windows batch files handle paths automatically, but here are tips:

### ✅ GOOD - These all work:

```cmd
REM Drag and drop - handles everything automatically
(Just drag and drop!)

REM With quotes (recommended for paths with spaces)
count_tokens.bat "G:\My Drive\Emails"
count_tokens.bat "C:\Users\YourName\Documents\file.txt"

REM Without quotes (if no spaces)
count_tokens.bat G:\Projects\code
count_tokens.bat C:\data\emails
```

### ⚠️ Important Notes:

- The batch files automatically handle all path formats
- Spaces in paths are handled automatically when you drag and drop
- Forward slashes (/) or backslashes (\) both work

## File Types Supported

By default, batch files count tokens in `.txt` files.

**To count other file types:**

Use Python directly from command line:

```cmd
REM Count markdown files
python offline_token_counter.py "G:\My Drive\Docs" --pattern "*.md"

REM Count Python files
python offline_token_counter.py "G:\Projects\code" --pattern "*.py"

REM Count all text-based files
python offline_token_counter.py "G:\Projects" --pattern "*.*"
```

## Troubleshooting

### "Python is not installed or not in PATH"

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart Command Prompt and try again

### "transformers not installed" (Xenova method)

**Solution 1 - Auto install:**
- The `count_tokens_xenova.bat` will offer to install it
- Just type `y` when prompted

**Solution 2 - Manual install:**
```cmd
pip install transformers
```

**Solution 3 - Use estimation instead:**
- Use `count_tokens_estimate.bat` (no dependencies)

### "Path does not exist"

**Possible causes:**
1. Google Drive not synced locally
2. Typo in path
3. Network drive not connected

**Solution:**
1. Check if path exists in Windows Explorer
2. Make sure Google Drive is syncing (if using Google Drive)
3. Verify drive letter is correct

### Very slow for large directories

**Solution:**
1. Test with limited files first:
   ```cmd
   python offline_token_counter.py "path" --limit 100
   ```
2. Use estimation method (much faster):
   ```cmd
   count_tokens_estimate.bat "path"
   ```

### Encoding errors for some files

**Solution:**
- The script automatically skips files with encoding errors
- Check the error messages to see which files were skipped
- Most common with non-UTF-8 files

## Saving Reports

All batch files will ask if you want to save a detailed report.

**Report includes:**
- Total token count
- Per-file breakdown
- Context window usage
- Recommendations

**Report location:**
- Saved next to your input file/folder
- Named: `{input_path}_token_report.txt`

**Example:**
- Input: `G:\My Drive\Emails`
- Report: `G:\My Drive\Emails_token_report.txt`

## Advanced Options

For more control, use Python directly:

```cmd
REM Show verbose progress
python offline_token_counter.py "path" --verbose

REM Show per-file breakdown
python offline_token_counter.py "path" --show-files

REM Limit number of files (testing)
python offline_token_counter.py "path" --limit 10

REM Save to specific file
python offline_token_counter.py "path" --output "my_report.txt"

REM Combine options
python offline_token_counter.py "G:\My Drive\Emails" --method xenova --show-files --output "email_tokens.txt" --verbose
```

## Understanding Token Counts

### What do the numbers mean?

**Total Tokens:** How many Claude AI tokens your files contain

**Context Window Usage:**
- < 50,000 tokens: ✅ Perfect for Claude Code (< 25% of context)
- 50,000-100,000: ✅ Good (25-50% of context)
- 100,000-150,000: ⚠️ Moderate (50-75% of context)
- \> 150,000: ⚠️ High (> 75% of context) - Consider batching

### For your email example (~312,450 tokens):

This exceeds Claude's 200K context window, so you should:
1. **Feed files in batches** - Split into multiple sessions
2. **Filter by relevance** - Only feed important emails
3. **Summarize first** - Ask Claude to summarize, then work with summaries

## Batch File Comparison

| Feature | count_tokens.bat | count_tokens_xenova.bat | count_tokens_estimate.bat |
|---------|-----------------|------------------------|--------------------------|
| **Method** | Auto-detect | Xenova only | Estimation only |
| **Accuracy** | Best available | Highest (~80-95%) | Good (~75-85%) |
| **Dependencies** | Optional | Required (transformers) | None |
| **Speed** | Medium | Medium | Very Fast |
| **Best For** | Most users | Maximum accuracy | Quick estimates |

## Tips for Best Results

1. **Start with estimation** for quick overview
   - Use `count_tokens_estimate.bat`
   - Gets instant results

2. **Install transformers** for accurate counts
   - Let `count_tokens_xenova.bat` install it
   - First run downloads tokenizer (~500KB)

3. **Test with --limit** for large directories
   - Test with 10-100 files first
   - Verify results before full run

4. **Use --show-files** to find largest files
   - See which files consume most tokens
   - Helps with selective loading

5. **Save reports** for future reference
   - Type 'y' when prompted
   - Compare different directories

## Next Steps

After counting tokens:

1. **Review the recommendation** in the report
2. **Plan your Claude Code usage:**
   - Low tokens (< 50K): Feed all files
   - Moderate (50-100K): Feed selectively
   - High (> 100K): Batch or filter
3. **Start using Claude Code** with your files!

## Support

For issues:
1. Check this guide first
2. Review error messages
3. Try `--verbose` flag for more details
4. See [OFFLINE_USAGE.md](OFFLINE_USAGE.md) for advanced usage

Happy token counting! 🚀
