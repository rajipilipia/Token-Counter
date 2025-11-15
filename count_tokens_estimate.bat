@echo off
REM =========================================
REM Claude Token Counter - ESTIMATION METHOD
REM =========================================
REM
REM This batch file uses character-based ESTIMATION method
REM No dependencies required - pure Python
REM Fast but less accurate (~75-85% accuracy)
REM
REM Usage:
REM   1. Drag and drop a file or folder onto this .bat file
REM   2. Or run from command line: count_tokens_estimate.bat "path\to\file.txt"
REM
REM =========================================

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if a path was provided
if "%~1"=="" (
    echo ERROR: No file or folder specified
    echo.
    echo Usage:
    echo   - Drag and drop a file or folder onto this batch file
    echo   - Or run: count_tokens_estimate.bat "path\to\file.txt"
    echo.
    pause
    exit /b 1
)

REM Get the input path
set INPUT_PATH=%~1

REM Check if path exists
if not exist "%INPUT_PATH%" (
    echo ERROR: Path does not exist: %INPUT_PATH%
    echo.
    pause
    exit /b 1
)

REM Run the token counter with estimation method
echo.
echo ========================================
echo Claude Offline Token Counter
echo Method: ESTIMATION (Fast, No Dependencies)
echo ========================================
echo.
echo Input: %INPUT_PATH%
echo.
echo Counting tokens with character estimation...
echo Formula: tokens = characters / 4
echo Accuracy: ~75-85%% for English text
echo.

python offline_token_counter.py "%INPUT_PATH%" --method estimation --verbose

REM Check if successful
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Token counting failed
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Token counting complete!
echo ========================================
echo.
echo NOTE: This is an estimate. For higher accuracy:
echo - Install transformers: pip install transformers
echo - Use count_tokens_xenova.bat
echo.

REM Ask if user wants to save report
set /p SAVE_REPORT="Save report to file? (y/n): "
if /i "%SAVE_REPORT%"=="y" (
    set REPORT_FILE=%INPUT_PATH%_estimate_report.txt
    echo.
    echo Generating report...
    python offline_token_counter.py "%INPUT_PATH%" --method estimation --output "!REPORT_FILE!" --show-files
    echo.
    echo Report saved to: !REPORT_FILE!
    echo.
)

pause
