@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title GuskungBot - Quick Runner
color 0B

cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║          🤖  GuskungBot - Quick Runner  🤖               ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo     [INFO] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python not found!
    echo.
    echo     Please install Python 3.8+ from:
    echo     https://www.python.org/downloads/
    echo.
    echo     ⚠️ IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
    echo     [✅] Python: %%v
)
echo.

REM Check .env file
if not exist .env (
    echo     [❌] .env file not found!
    echo     [INFO] Please run Setup first or use all_in_one.bat
    echo.
    pause
    exit /b 1
)

echo     [✅] .env file found
echo.

REM Check DISCORD_TOKEN
findstr /C:"DISCORD_TOKEN=" .env >nul 2>&1
if errorlevel 1 (
    echo     [❌] DISCORD_TOKEN not found in .env!
    echo     [INFO] Please edit .env file and add your DISCORD_TOKEN
    echo.
    pause
    exit /b 1
)

echo     [✅] Configuration loaded
echo.

REM Load BOT_LANGUAGE from .env
set BOT_LANGUAGE=
for /f "tokens=2 delims==" %%a in ('findstr /C:"BOT_LANGUAGE=" .env 2^>nul') do (
    set BOT_LANGUAGE=%%a
)

if not "!BOT_LANGUAGE!"=="" (
    echo     [INFO] Language: !BOT_LANGUAGE!
    echo.
)

REM Check dependencies
if not exist main.py (
    echo     [❌] main.py not found!
    pause
    exit /b 1
)

echo     ──────────────────────────────────────────────────────────
echo     🚀 Starting Bot
echo     ──────────────────────────────────────────────────────────
echo.
echo     [INFO] Press Ctrl+C to stop the bot
echo.
echo     ──────────────────────────────────────────────────────────
echo.

REM Run the bot
python main.py

REM Check exit status
if errorlevel 1 (
    echo.
    echo     ──────────────────────────────────────────────────────────
    echo     ❌ Bot stopped due to an error!
    echo     ──────────────────────────────────────────────────────────
    echo.
    echo     Common issues / ปัญหาที่พบบ่อย:
    echo     - Invalid Discord Token / Token ไม่ถูกต้อง
    echo     - Missing dependencies / ขาด dependencies
    echo     - Network connection issues / ปัญหาเครือข่าย
    echo.
    pause
    exit /b 1
)

echo.
echo     ──────────────────────────────────────────────────────────
echo     ✅ Bot stopped normally
echo     ──────────────────────────────────────────────────────────
echo.
pause
exit /b 0

