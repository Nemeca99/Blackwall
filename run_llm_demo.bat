@echo off
echo BlackwallV2 LLM Integration Demo
echo ===============================
echo.
echo Please select a demo mode:
echo 1. Interactive Demo (chat with LLM)
echo 2. Batch Processing Demo (evaluate performance)
echo 3. Connection Test Only (verify API works)
echo.

set /p mode="Enter your choice (1-3, default: 1): "

cd /d "%~dp0"

if "%mode%"=="2" (
    echo.
    echo Starting Batch Processing Demo...
    python run_llm_demo.py --batch
) else if "%mode%"=="3" (
    echo.
    echo Running Connection Test Only...
    python run_llm_demo.py --test
) else (
    echo.
    echo Starting Interactive Demo...
    python run_llm_demo.py --interactive
)

pause
