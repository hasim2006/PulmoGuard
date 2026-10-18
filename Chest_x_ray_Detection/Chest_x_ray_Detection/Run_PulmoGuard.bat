@echo off
title PulmoGuard - Offline Pneumonia Detection
cd /d "%~dp0"
echo ========================================================
echo       Starting PulmoGuard (100%% Offline Mode)
echo ========================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python chest_xray.py
) else (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" chest_xray.py
)

if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited.
    pause
)
