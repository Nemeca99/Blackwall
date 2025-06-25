@echo off
echo Running Queue Monitor Tool...
echo.

cd /d "%~dp0"
python tools/queue_monitor.py --monitor --interval 3 --pulse 5

echo.
echo Queue Monitor completed.
pause
