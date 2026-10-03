@echo off
REM Usage: scripts\run.cmd lab2
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
