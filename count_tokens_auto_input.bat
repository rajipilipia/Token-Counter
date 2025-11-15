@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo Claude Token Counter - AUTO METHOD
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    pause
    exit /b 1
)

REM Get path from user
set /p INPUT_PATH="Enter file or folder path: "

REM Remove quotes if user added them
set INPUT_PATH=%INPUT_PATH:"=%

REM Check path exists
if not exist "%INPUT_PATH%" (
    echo ERROR: Path not found: %INPUT_PATH%
    pause
    exit /b 1
)

echo.
echo Path: %INPUT_PATH%
echo Method: AUTO
echo.
echo Counting tokens...
echo.

REM Run counter
python offline_token_counter.py "%INPUT_PATH%" --verbose 2>&1

if errorlevel 1 (
    echo.
    echo ERROR: Failed with exit code %ERRORLEVEL%
    echo.
)

echo.
echo Done.
pause
