@echo off
REM ─────────────────────────────────────────────────────────
REM  Chocoberry Dashboard — Daily Sync Launcher
REM  This file is run by Windows Task Scheduler every night.
REM ─────────────────────────────────────────────────────────

cd /d "C:\Users\GEO\Desktop\Dashboard"
py scripts\daily_sync.py >> logs\daily_sync_bat.log 2>&1
