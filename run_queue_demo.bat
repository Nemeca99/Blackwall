@echo off
echo Running Queue-Driven Demo...
echo.

cd /d "%~dp0"
python demo/queue_driven_demo.py

echo.
echo Demo completed.
pause
