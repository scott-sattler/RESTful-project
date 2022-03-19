@echo off

start cmd.exe /c ""%~dp0\gateway\venv\Scripts\python.exe" "%~dp0\gateway\main.py""
start cmd.exe /c ""%~dp0\frontend\venv\Scripts\python.exe" "%~dp0\frontend\main.py""
start cmd.exe /c ""%~dp0\backend\color_lookup\venv\Scripts\python.exe" "%~dp0\backend\color_lookup\main.py""