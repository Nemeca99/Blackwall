@echo off
echo Running Queue Monitor Demo with Test Data...
echo.

cd /d "%~dp0"
python tools/queue_monitor.py --add 5 --queue input --pulse 3 --beats 10

echo.
echo Adding more test items with delay...
python tools/queue_monitor.py --add 2 --queue input --beats 5

echo.
echo Final queue statistics:
python tools/queue_monitor.py

echo.
echo Queue Monitor Demo completed.
pause
