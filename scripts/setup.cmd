@echo off
REM Double-click me, or run "scripts\setup.cmd" in a terminal. Wraps setup.ps1 so no execution-policy changes are needed.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
echo.
pause
