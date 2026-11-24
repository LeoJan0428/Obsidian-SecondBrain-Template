@echo off
REM ==============================================================================
REM 🔗 SecondBrain AgentOS Windows Environment and Junction Setup Script
REM ==============================================================================

echo [AgentOS] Configuring Windows Git and Directory Junctions...

cd /d "%~dp0"

REM 1. Configure Git core settings for Windows compatibility and security
echo [AgentOS] Configuring Git settings...
git config core.hooksPath 00-AgentOS/hooks
set "HOOKS_DIR=%CD:\=/%/00-AgentOS/hooks"
git config --global core.hooksPath "%HOOKS_DIR%"
git config core.quotepath false
git config --global core.quotepath false
git config core.autocrlf input
git config --global core.autocrlf input
echo [AgentOS] Git local and global core.hooksPath set to "%HOOKS_DIR%".
echo [AgentOS] Git local and global core.quotepath set to false (UTF-8 Chinese paths enabled).
echo [AgentOS] Git local and global core.autocrlf set to input (LF preserved).

REM 2. Verify canonical skills directory
if not exist "00-AgentOS\skills" (
    echo [ERROR] Canonical directory 00-AgentOS\skills not found!
    exit /b 1
)

REM 3. Antigravity (.agents\skills)
if not exist ".agents" mkdir ".agents"
if exist ".agents\skills" (
    echo [.agents\skills] Junction already exists.
) else (
    mklink /J ".agents\skills" "00-AgentOS\skills"
    echo [.agents\skills] Junction created successfully.
)

REM 4. Claude Code (.claude\skills)
if not exist ".claude" mkdir ".claude"
if exist ".claude\skills" (
    echo [.claude\skills] Junction already exists.
) else (
    mklink /J ".claude\skills" "00-AgentOS\skills"
    echo [.claude\skills] Junction created successfully.
)

REM 5. Cursor (.cursor\skills)
if not exist ".cursor" mkdir ".cursor"
if exist ".cursor\skills" (
    echo [.cursor\skills] Junction already exists.
) else (
    mklink /J ".cursor\skills" "00-AgentOS\skills"
    echo [.cursor\skills] Junction created successfully.
)

REM 6. Global Antigravity Customizations (%USERPROFILE%\.gemini\config)
if not exist "%USERPROFILE%\.gemini\config" mkdir "%USERPROFILE%\.gemini\config"
if exist "%USERPROFILE%\.gemini\config\skills" (
    echo [%USERPROFILE%\.gemini\config\skills] Junction already exists.
) else (
    mklink /J "%USERPROFILE%\.gemini\config\skills" "%CD%\00-AgentOS\skills"
    echo [%USERPROFILE%\.gemini\config\skills] Junction created successfully.
)
if exist "%USERPROFILE%\.gemini\config\AGENTS.md" del /f /q "%USERPROFILE%\.gemini\config\AGENTS.md"
mklink /H "%USERPROFILE%\.gemini\config\AGENTS.md" "%CD%\AGENTS.md" >nul 2>&1 || copy /Y "%CD%\AGENTS.md" "%USERPROFILE%\.gemini\config\AGENTS.md" >nul
echo [%USERPROFILE%\.gemini\config\AGENTS.md] Synced with Vault AGENTS.md.

echo [AgentOS] All Skills Junctions and Git Hooks are active and synchronized!
