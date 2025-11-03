@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title GuskungBot - All in One Manager
color 0B
goto main_menu

REM ========================================
REM 📋 MAIN MENU
REM ========================================


:main_menu
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║          🤖  GuskungBot - All in One Manager  🤖         ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.
echo     ┌──────────────────────────────────────────────────────────┐
echo     │  📋 Main Menu / เมนูหลัก                                 │
echo     └──────────────────────────────────────────────────────────┘
echo.
echo     [1] 🚀 Run Bot / รันบอท
echo     [2] 🔧 Setup / ติดตั้ง Dependencies
echo     [3] 🔨 Build EXE / สร้างไฟล์ EXE
echo     [4] 📖 View README / ดูคู่มือ
echo     [5] 🔍 System Status / ตรวจสอบสถานะ
echo     [6] 🎯 Quick Run / รันเร็ว (ใช้ config เดิม)
echo     [7] ⚡ Run.bat / รัน Run.bat
echo     [8] 📁 Run Batch File / รันไฟล์ BAT อื่นๆ
echo     [0] ❌ Exit / ออก
echo.
echo     ──────────────────────────────────────────────────────────
echo.
set /p choice="     Select option / เลือก: "

if "%choice%"=="1" (
    goto run_bot
)
if "%choice%"=="2" (
    goto setup_bot
)
if "%choice%"=="3" (
    goto build_exe
)
if "%choice%"=="4" (
    if exist README.md (
        echo     [INFO] Opening README.md...
        start notepad README.md
        timeout /t 1 >nul 2>&1
    ) else (
        echo     [❌] README.md not found
        pause
    )
    goto main_menu
)
if "%choice%"=="5" (
    goto system_status
)
if "%choice%"=="6" (
    goto quick_run
)
if "%choice%"=="7" (
    goto run_run_bat
)
if "%choice%"=="8" (
    goto run_batch_file
)
if "%choice%"=="0" (
    cls
    echo.
    echo     [INFO] Thank you for using GuskungBot!
    echo     [INFO] Goodbye! / ลาก่อน!
    timeout /t 2 >nul 2>&1
    exit /b 0
)

echo     [❌] Invalid choice! / ตัวเลือกไม่ถูกต้อง!
timeout /t 2 >nul
goto main_menu

REM ========================================
REM 🔍 SYSTEM STATUS
REM ========================================

:system_status
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║         🔍 System Status / ตรวจสอบสถานะระบบ            ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo     [INFO] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python: Not installed
    set PYTHON_STATUS=❌
) else (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
        echo     [✅] Python: %%v
        set PYTHON_STATUS=✅
    )
)

REM Check Python version
call :check_python_version
if "%PYTHON_OK%"=="false" (
    echo     [⚠️] Python version check: Failed
) else (
    if "%PYTHON_STATUS%"=="✅" (
        echo     [✅] Python version check: OK
    )
)
echo.

REM Check dependencies
call :check_dependencies
if "%DEPS_OK%"=="false" (
    echo     [❌] Dependencies: Missing files
) else (
    echo     [✅] Dependencies: Files OK
)
echo.

REM Check .env file
if exist .env (
    echo     [✅] .env file: Found
    findstr /C:"DISCORD_TOKEN=" .env >nul 2>&1
    if not errorlevel 1 (
        echo     [✅] DISCORD_TOKEN: Configured
    ) else (
        echo     [⚠️] DISCORD_TOKEN: Not set
    )
) else (
    echo     [⚠️] .env file: Not found
)
echo.

REM Check pip packages
echo     [INFO] Checking installed packages...
python -m pip show discord.py >nul 2>&1
if errorlevel 1 (
    echo     [⚠️] discord.py: Not installed
) else (
    echo     [✅] discord.py: Installed
)
python -m pip show python-dotenv >nul 2>&1
if errorlevel 1 (
    echo     [⚠️] python-dotenv: Not installed
) else (
    echo     [✅] python-dotenv: Installed
)
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo     [⚠️] pyinstaller: Not installed
) else (
    echo     [✅] pyinstaller: Installed
)
echo.

echo     ──────────────────────────────────────────────────────────
echo.
echo     [INFO] Press any key to return to main menu...
pause >nul
goto main_menu

REM ========================================
REM 🚀 RUN BOT SECTION
REM ========================================

:run_bot
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║          🤖  GuskungBot - Discord Bot Runner  🤖          ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo     [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python not found!
    echo.
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  Please install Python 3.8+ from:                    │
    echo     │  https://www.python.org/downloads/                  │
    echo     │                                                      │
    echo     │  ⚠️ IMPORTANT: Check "Add Python to PATH"            │
    echo     │     during installation!                            │
    echo     └─────────────────────────────────────────────────────┘
    echo.
    pause
    goto main_menu
)

REM Check Python version
call :check_python_version
if "%PYTHON_OK%"=="false" (
    echo.
    pause
    goto main_menu
)

echo     [✅] Python detected
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo     [INFO] Version: %%v
echo.

REM Check dependencies
call :check_dependencies
if "%DEPS_OK%"=="false" (
    echo     [❌] Required files missing!
    pause
    goto main_menu
)
echo.

REM Check if .env file exists
set env_exists=false
set has_token=false

if exist .env (
    set env_exists=true
    echo     [✅] .env file found
    
    REM Check if DISCORD_TOKEN exists in .env
    findstr /C:"DISCORD_TOKEN=" .env >nul 2>&1
    if not errorlevel 1 (
        set has_token=true
        echo     [✅] DISCORD_TOKEN found in .env
    ) else (
        echo     [⚠️] DISCORD_TOKEN not found in .env
    )
) else (
    echo     [⚠️] .env file not found
    echo     [INFO] Creating .env file...
    echo DISCORD_TOKEN= > .env
    echo     [✅] .env file created
)

echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📋 Configuration Menu / เมนูการตั้งค่า                │
echo     └─────────────────────────────────────────────────────────┘
echo.

REM Language Selection
:language_menu
echo     Language Selection / เลือกภาษา:
echo     [1] English / อังกฤษ
echo     [2] Thai / ไทย
if "%env_exists%"=="true" (
    echo     [3] Use from .env / ใช้จาก .env
)
echo     [0] Back / กลับ
echo.
set /p lang_choice="     Select / เลือก: "

if "%lang_choice%"=="1" (
    set BOT_LANGUAGE=en
    echo     [✅] Language set to: English
    timeout /t 1 >nul 2>&1
    goto check_token
)
if "%lang_choice%"=="2" (
    set BOT_LANGUAGE=th
    echo     [✅] Language set to: Thai / ภาษาไทย
    timeout /t 1 >nul 2>&1
    goto check_token
)
if "%lang_choice%"=="3" (
    if "%env_exists%"=="true" (
        set BOT_LANGUAGE=
        echo     [✅] Using language from .env
        timeout /t 1 >nul 2>&1
        goto check_token
    ) else (
        echo     [❌] Invalid choice!
        timeout /t 1 >nul 2>&1
        goto language_menu
    )
)
if "%lang_choice%"=="0" (
    goto main_menu
)
echo     [❌] Invalid choice! Please try again.
timeout /t 1 >nul 2>&1
goto language_menu

REM Token Check
:check_token
cls
echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  🔑 Discord Token Configuration                          │
echo     └─────────────────────────────────────────────────────────┘
echo.
if "%has_token%"=="true" (
    echo     [✅] Token found in .env
    echo.
    echo     [1] Use token from .env (Default / ค่าเริ่มต้น)
    echo     [2] Enter new token / ป้อน token ใหม่
    echo     [0] Back / กลับ
    echo.
    set /p token_choice="     Select / เลือก: "
    
    if "!token_choice!"=="" set token_choice=1
    
    if "!token_choice!"=="1" (
        echo     [✅] Using token from .env
        set token_updated=false
        timeout /t 1 >nul 2>&1
        goto continue_setup
    )
    if "!token_choice!"=="2" (
        goto enter_new_token
    )
    if "!token_choice!"=="0" (
        goto main_menu
    )
    set token_updated=false
    goto continue_setup
) else (
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  🔑 Discord Token Required                          │
    echo     │                                                      │
    echo     │  Get your token from:                                │
    echo     │  https://discord.com/developers/applications        │
    echo     └─────────────────────────────────────────────────────┘
    echo.
    goto enter_new_token
)

:enter_new_token
echo     Please enter your Discord Bot Token:
echo     (You can get it from https://discord.com/developers/applications)
echo.
set /p new_token="     Token: "
if "!new_token!"=="" (
    echo     [❌] Token cannot be empty!
    echo.
    timeout /t 1 >nul 2>&1
    goto enter_new_token
)
set DISCORD_TOKEN=!new_token!
set token_updated=true
echo     [✅] Token received!
timeout /t 1 >nul 2>&1
goto continue_setup

:continue_setup
cls
echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  💾 Saving Configuration                                 │
echo     └─────────────────────────────────────────────────────────┘
echo.

REM Save to .env
if "%token_updated%"=="true" (
    echo     [INFO] Saving configuration...
    (
        echo DISCORD_TOKEN=!DISCORD_TOKEN!
        if not "%BOT_LANGUAGE%"=="" (
            echo BOT_LANGUAGE=%BOT_LANGUAGE%
        )
    ) > .env
    echo     [✅] Configuration saved successfully!
) else (
    if not "%BOT_LANGUAGE%"=="" (
        if exist .env (
            findstr /C:"BOT_LANGUAGE=" .env >nul 2>&1
            if errorlevel 1 (
                echo BOT_LANGUAGE=%BOT_LANGUAGE% >> .env
                echo     [✅] Language preference saved
            ) else (
                powershell -Command "$content = Get-Content .env -Raw; $content = $content -replace 'BOT_LANGUAGE=.*', 'BOT_LANGUAGE=%BOT_LANGUAGE%'; Set-Content .env -Value $content -NoNewline"
                echo     [✅] Language preference updated
            )
        )
    )
)

echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📦 Checking Dependencies                                │
echo     └─────────────────────────────────────────────────────────┘
echo.

if exist requirements.txt (
    echo     [INFO] Checking and installing dependencies...
    echo     [INFO] This may take a few moments...
    python -m pip install -q -r requirements.txt --upgrade 2>nul
    if errorlevel 1 (
        echo     [⚠️] Some dependencies may need manual installation
        echo     [INFO] Trying to install without quiet mode...
        python -m pip install -r requirements.txt --upgrade
    ) else (
        echo     [✅] Dependencies ready
    )
) else (
    echo     [⚠️] requirements.txt not found
    echo     [INFO] Skipping dependency check
)

echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  🚀 Starting Bot                                        │
echo     └─────────────────────────────────────────────────────────┘
echo.

REM Verify .env exists
if not exist .env (
    echo     [❌] .env file not found!
    pause
    goto main_menu
)

REM Verify DISCORD_TOKEN exists
findstr /C:"DISCORD_TOKEN=" .env >nul 2>&1
if errorlevel 1 (
    echo     [❌] DISCORD_TOKEN not found in .env!
    pause
    goto main_menu
)

echo     [✅] Configuration loaded
if not "%BOT_LANGUAGE%"=="" (
    echo     [INFO] Language: %BOT_LANGUAGE%
)
echo.
echo     [INFO] Starting bot...
echo     [INFO] Press Ctrl+C to stop the bot
echo.
echo     ──────────────────────────────────────────────────────────
echo.

REM Set environment variable
if not "%BOT_LANGUAGE%"=="" (
    set BOT_LANGUAGE=%BOT_LANGUAGE%
)

REM Run the bot
python main.py

REM Check exit status
if errorlevel 1 (
    echo.
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  ❌ Bot stopped due to an error!                     │
    echo     └─────────────────────────────────────────────────────┘
    echo.
    echo     Common issues / ปัญหาที่พบบ่อย:
    echo     - Invalid Discord Token / Token ไม่ถูกต้อง
    echo     - Missing dependencies / ขาด dependencies
    echo     - Network connection issues / ปัญหาเครือข่าย
    echo.
    echo     [INFO] Check the error message above
    echo.
    pause
)

goto main_menu

REM ========================================
REM 🔧 SETUP SECTION
REM ========================================

:setup_bot
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║        🔧  GuskungBot - Setup Wizard  🔧                 ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo     [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python not found!
    echo.
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  Please install Python 3.8+ from:                     │
    echo     │  https://www.python.org/downloads/                  │
    echo     │                                                      │
    echo     │  ⚠️ IMPORTANT: Check "Add Python to PATH"            │
    echo     │     during installation!                             │
    echo     └─────────────────────────────────────────────────────┘
    echo.
    pause
    goto main_menu
)

REM Check Python version
call :check_python_version
if "%PYTHON_OK%"=="false" (
    pause
    goto main_menu
)

echo     [✅] Python found
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo     [INFO] Version: %%v
echo.

REM Upgrade pip
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📦 Upgrading pip                                        │
echo     └─────────────────────────────────────────────────────────┘
echo.
echo     [INFO] Upgrading pip to latest version...
python -m pip install --upgrade pip -q
if errorlevel 1 (
    echo     [⚠️] Failed to upgrade pip, continuing...
    python -m pip install --upgrade pip
) else (
    echo     [✅] pip upgraded successfully
)
echo.

REM Install dependencies
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📦 Installing Dependencies                              │
echo     └─────────────────────────────────────────────────────────┘
echo.

if exist requirements.txt (
    echo     [INFO] Installing dependencies from requirements.txt...
    echo     [INFO] This may take a few minutes...
    echo     [INFO] Please wait...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo     [❌] Failed to install some dependencies!
        echo     [INFO] Try running as Administrator
        echo     [INFO] Or try: python -m pip install -r requirements.txt --user
        pause
        goto main_menu
    ) else (
        echo.
        echo     [✅] All dependencies installed successfully!
    )
) else (
    echo     [⚠️] requirements.txt not found
    echo     [INFO] Skipping dependency installation
)
echo.

REM Create .env file
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📝 Creating .env file                                    │
echo     └─────────────────────────────────────────────────────────┘
echo.

if not exist .env (
    echo     [INFO] Creating .env file...
    echo DISCORD_TOKEN= > .env
    echo BOT_LANGUAGE=th >> .env
    echo     [✅] .env file created
    echo.
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  ⚠️ IMPORTANT: Edit .env file and add your            │
    echo     │     DISCORD_TOKEN!                                   │
    echo     │                                                      │
    echo     │  Get your token from:                                │
    echo     │  https://discord.com/developers/applications        │
    echo     └─────────────────────────────────────────────────────┘
) else (
    echo     [✅] .env file already exists
    echo     [INFO] Current .env will be preserved
)
echo.

REM Setup complete
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  ✅ Setup Complete!                                       │
echo     └─────────────────────────────────────────────────────────┘
echo.
echo     Next steps / ขั้นตอนต่อไป:
echo     1. Edit .env file and add your DISCORD_TOKEN
echo     2. Choose [1] Run Bot from main menu
echo.
echo     ──────────────────────────────────────────────────────────
echo.
pause
goto main_menu

REM ========================================
REM 🔨 BUILD EXE SECTION
REM ========================================

:build_exe
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║           🔨  GuskungBot - Build EXE  🔨                ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo     [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python not found!
    echo     [INFO] Please install Python first
    pause
    goto main_menu
)

REM Check Python version
call :check_python_version
if "%PYTHON_OK%"=="false" (
    pause
    goto main_menu
)

echo     [✅] Python found
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo     [INFO] Version: %%v
echo.

REM Check if PyInstaller is installed
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📦 Checking PyInstaller                                │
echo     └─────────────────────────────────────────────────────────┘
echo.
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo     [INFO] PyInstaller not found, installing...
    python -m pip install pyinstaller -q
    if errorlevel 1 (
        echo     [❌] Failed to install PyInstaller!
        echo     [INFO] Trying without quiet mode...
        python -m pip install pyinstaller
        if errorlevel 1 (
            pause
            goto main_menu
        )
    )
    echo     [✅] PyInstaller installed successfully
) else (
    echo     [✅] PyInstaller found
)
echo.

REM Check if main.py exists
if not exist main.py (
    echo     [❌] main.py not found!
    pause
    goto main_menu
)

REM Check required files
call :check_dependencies
if "%DEPS_OK%"=="false" (
    echo     [⚠️] Some required files may be missing
    echo     [INFO] Continuing anyway...
)
echo.

REM Clean previous builds
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  🧹 Cleaning Previous Builds                            │
echo     └─────────────────────────────────────────────────────────┘
echo.
if exist build (
    echo     [INFO] Removing build folder...
    rmdir /s /q build 2>nul
    echo     [✅] Build folder cleaned
)
if exist dist (
    echo     [INFO] Removing dist folder...
    rmdir /s /q dist 2>nul
    echo     [✅] Dist folder cleaned
)
if exist *.spec (
    echo     [INFO] Removing spec files...
    del /q *.spec 2>nul
    echo     [✅] Spec files cleaned
)
echo.

echo     ┌─────────────────────────────────────────────────────────┐
echo     │  🔨 Building EXE                                        │
echo     └─────────────────────────────────────────────────────────┘
echo.
echo     [INFO] This will create a standalone EXE file
echo     [INFO] All dependencies will be included
echo     [INFO] Building... (This may take 2-5 minutes)
echo.
echo     [⏳] Please wait...
echo.

REM Build standalone EXE
python -m PyInstaller --onefile ^
    --console ^
    --name "GuskungBot" ^
    --hidden-import=discord ^
    --hidden-import=discord.ext.commands ^
    --hidden-import=discord.app_commands ^
    --hidden-import=discord.ext ^
    --hidden-import=dotenv ^
    --hidden-import=asyncio ^
    --hidden-import=bad_words ^
    --hidden-import=i18n ^
    --collect-all discord ^
    --collect-all dotenv ^
    --add-data "i18n.py;." ^
    --add-data "bad_words.py;." ^
    --add-data "language_chooser.py;." ^
    main.py

if errorlevel 1 (
    echo.
    echo     ┌─────────────────────────────────────────────────────┐
    echo     │  ❌ Build failed!                                    │
    echo     └─────────────────────────────────────────────────────┘
    echo.
    echo     [INFO] Check the error messages above
    echo     [INFO] Common issues:
    echo     - Missing dependencies
    echo     - Incorrect Python version
    echo     - File permissions
    echo.
    pause
    goto main_menu
)

echo.
echo     ┌─────────────────────────────────────────────────────────┐
echo     │  ✅ Build Successful!                                     │
echo     └─────────────────────────────────────────────────────────┘
echo.
echo     [✅] EXE file created: dist\GuskungBot.exe
echo.

REM Copy .env if exists
if exist .env (
    echo     [INFO] Copying .env file to dist folder...
    if not exist dist mkdir dist
    copy /Y .env dist\ >nul 2>&1
    if not errorlevel 1 (
        echo     [✅] .env file copied
    ) else (
        echo     [⚠️] Failed to copy .env file
    )
) else (
    echo     [⚠️] .env file not found
    echo     [INFO] Creating .env template in dist folder...
    if not exist dist mkdir dist
    echo DISCORD_TOKEN= > dist\.env
    echo BOT_LANGUAGE=th >> dist\.env
    echo     [✅] .env template created
)
echo.

echo     ┌─────────────────────────────────────────────────────────┐
echo     │  📋 Next Steps                                           │
echo     └─────────────────────────────────────────────────────────┘
echo.
echo     1. Go to dist folder
echo     2. Edit .env file and add your DISCORD_TOKEN
echo     3. Run GuskungBot.exe
echo.
echo     [INFO] This is a standalone EXE - no Python needed!
echo     [INFO] You can distribute this folder to other Windows PCs
echo.

REM Ask if user wants to open dist folder
echo     [INFO] Would you like to open the dist folder? (Y/N)
set /p open_folder="     Your choice: "

if /i "!open_folder!"=="Y" (
    if exist dist (
        echo     [INFO] Opening dist folder...
        explorer dist
    )
)

echo.
echo     ──────────────────────────────────────────────────────────
echo.
pause
goto main_menu

REM ========================================
REM 🎯 QUICK RUN SECTION
REM ========================================

:quick_run
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║        🎯  GuskungBot - Quick Run  🎯                     ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo     [❌] Python not found!
    pause
    goto main_menu
)

REM Verify .env exists
if not exist .env (
    echo     [❌] .env file not found!
    echo     [INFO] Please run Setup first or use option [1] Run Bot
    pause
    goto main_menu
)

REM Verify DISCORD_TOKEN exists
findstr /C:"DISCORD_TOKEN=" .env >nul 2>&1
if errorlevel 1 (
    echo     [❌] DISCORD_TOKEN not found in .env!
    echo     [INFO] Please run Setup first or use option [1] Run Bot
    pause
    goto main_menu
)

echo     [✅] Configuration found, starting bot...
echo     [INFO] Using settings from .env file
echo     [INFO] Press Ctrl+C to stop the bot
echo.
echo     ──────────────────────────────────────────────────────────
echo.

REM Load language from .env if exists
set BOT_LANGUAGE=
for /f "tokens=2 delims==" %%a in ('findstr /C:"BOT_LANGUAGE=" .env 2^>nul') do (
    set BOT_LANGUAGE=%%a
)

REM Run the bot
python main.py

if errorlevel 1 (
    echo.
    echo     [❌] Bot stopped due to an error!
    pause
)

goto main_menu

REM ========================================
REM ⚡ RUN Run.bat SECTION
REM ========================================

:run_run_bat
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║                                                          ║
echo     ║        ⚡  GuskungBot - Run Run.bat  ⚡                  ║
echo     ║                                                          ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Run.bat exists
if not exist Run.bat (
    echo     [❌] Run.bat not found!
    echo     [INFO] Run.bat should be in the same directory
    echo.
    pause
    goto main_menu
)

echo     [INFO] Running Run.bat...
echo     [INFO] Opening in separate window...
echo     [INFO] The window will stay open after execution
echo.
start "GuskungBot - Run.bat" cmd /k "cd /d %~dp0 && echo. && echo     ======================================== && echo     Running: Run.bat && echo     ======================================== && echo. && Run.bat && echo. && echo     ======================================== && echo     Execution completed. && echo     ======================================== && echo. && pause"
timeout /t 1 >nul
echo     [✅] Run.bat launched in separate window
echo     [INFO] Window will stay open
echo     [INFO] You can continue using this menu
echo.

goto batch_run_done

REM ========================================
REM 📁 RUN BATCH FILE SECTION
REM ========================================

:run_batch_file
cls
echo.
echo     ╔══════════════════════════════════════════════════════════╗
echo     ║         📁  Run Batch File / รันไฟล์ BAT                ║
echo     ╚══════════════════════════════════════════════════════════╝
echo.

REM Find all .bat files in current directory
set /a count=0
set /a index=1
echo     [INFO] Scanning for batch files...
echo.

REM Create list of batch files
for %%f in (*.bat) do (
    if /i not "%%~nxf"=="all_in_one.bat" (
        echo     [!index!] %%~nxf
        set /a count+=1
        set /a index+=1
    )
)

if %count%==0 (
    echo     [⚠️] No other batch files found in current directory
    echo.
    pause
    goto main_menu
)

echo     [0] Back / กลับ
echo.
set /p batch_choice="     Select batch file / เลือกไฟล์: "

REM Run selected batch file
set /a batch_index=1
set batch_file=
for %%f in (*.bat) do (
    if /i not "%%~nxf"=="all_in_one.bat" (
        if "!batch_choice!"=="!batch_index!" (
            set batch_file=%%f
            goto run_selected_batch
        )
        set /a batch_index+=1
    )
)

REM Check if batch file was found
if "!batch_choice!"=="0" (
    goto main_menu
)

if not defined batch_file (
    echo     [❌] Invalid choice!
    timeout /t 2 >nul
    goto run_batch_file
)

:run_selected_batch
if not exist "!batch_file!" (
    echo     [❌] Batch file not found: !batch_file!
    pause
    goto main_menu
)

echo     [INFO] Running !batch_file!...
echo     [INFO] Opening in separate window...
echo     [INFO] The window will stay open after execution
echo.
start "Batch Runner: !batch_file!" cmd /k "cd /d %~dp0 && echo. && echo     ======================================== && echo     Running: !batch_file! && echo     ======================================== && echo. && !batch_file! && echo. && echo     ======================================== && echo     Execution completed. && echo     ======================================== && echo. && pause"
timeout /t 1 >nul
echo     [✅] Batch file launched in separate window
echo     [INFO] Window will stay open
echo     [INFO] You can continue using this menu
goto batch_run_done

:batch_run_done
echo.
echo     ──────────────────────────────────────────────────────────
echo     [INFO] Batch file execution completed
echo     ──────────────────────────────────────────────────────────
echo.
pause
goto main_menu

REM ========================================
REM 🎨 ENHANCED FUNCTIONS
REM ========================================

REM Check Python version compatibility
:check_python_version
set PYTHON_OK=true
for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
    for /f "tokens=1,2 delims=." %%a in ("%%v") do (
        if %%a LSS 3 (
            echo     [❌] Python version too old! Required: 3.8+
            echo     [INFO] Your version: %%v
            set PYTHON_OK=false
            exit /b
        )
        if %%a EQU 3 (
            if %%b LSS 8 (
                echo     [❌] Python version too old! Required: 3.8+
                echo     [INFO] Your version: %%v
                set PYTHON_OK=false
                exit /b
            )
        )
        set PYTHON_OK=true
    )
)
exit /b

REM Check if dependencies are installed
:check_dependencies
set DEPS_OK=true
if not exist main.py (
    echo     [❌] main.py not found!
    set DEPS_OK=false
    exit /b
)
if not exist i18n.py (
    echo     [⚠️] i18n.py not found!
)
if not exist bad_words.py (
    echo     [⚠️] bad_words.py not found!
)
if not exist requirements.txt (
    echo     [⚠️] requirements.txt not found!
    set DEPS_OK=false
    exit /b
)
exit /b
