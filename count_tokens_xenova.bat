@echo off
REM =========================================
REM Claude Token Counter - XENOVA METHOD
REM =========================================
REM
REM This batch file uses the XENOVA tokenizer method
REM Most accurate offline method (requires: pip install transformers)
REM
REM Usage:
REM   1. Drag and drop a file or folder onto this .bat file
REM   2. Or run from command line: count_tokens_xenova.bat "path\to\file.txt"
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

REM Check if transformers library is installed
python -c "import transformers" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo XENOVA TOKENIZER NOT INSTALLED
    echo ========================================
    echo.
    echo The transformers library is required for Xenova method.
    echo.
    set /p INSTALL="Install transformers now? (y/n): "
    if /i "!INSTALL!"=="y" (
        echo.
        echo Installing transformers...
        pip install transformers
        echo.
        if errorlevel 1 (
            echo Installation failed. Please try manually: pip install transformers
            pause
            exit /b 1
        )
        echo Installation complete!
        echo.
    ) else (
        echo.
        echo Please install manually: pip install transformers
        echo Or use count_tokens_estimate.bat for no-dependency option
        echo.
        pause
        exit /b 1
    )
)

REM Check if a path was provided
if "%~1"=="" (
    echo ERROR: No file or folder specified
    echo.
    echo Usage:
    echo   - Drag and drop a file or folder onto this batch file
    echo   - Or run: count_tokens_xenova.bat "path\to\file.txt"
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

REM Run the token counter with Xenova method
echo.
echo ========================================
echo Claude Offline Token Counter
echo Method: XENOVA (Most Accurate)
echo ========================================
echo.
echo Input: %INPUT_PATH%
echo.
echo Counting tokens with Xenova tokenizer...
echo.

python offline_token_counter.py "%INPUT_PATH%" --method xenova --verbose

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

REM Ask if user wants to save detailed report
set /p SAVE_REPORT="Save detailed report to file? (y/n): "
if /i "%SAVE_REPORT%"=="y" (
    set REPORT_FILE=%INPUT_PATH%_xenova_report.txt
    echo.
    echo Generating detailed report...
    python offline_token_counter.py "%INPUT_PATH%" --method xenova --output "!REPORT_FILE!" --show-files
    echo.
    echo Report saved to: !REPORT_FILE!
    echo.
)

pause
