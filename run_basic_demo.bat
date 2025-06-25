@echo off
cd /d "%~dp0"
echo Running BlackwallV2 Basic Biomimetic Demo...
python -c "import sys; print(f'Python executable: {sys.executable}')"
python demo/basic_biomimetic_demo.py
pause
