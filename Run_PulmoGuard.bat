@echo off
title PulmoGuard - AI-Based Chest X-Ray Detection System
echo ===============================================================
echo     PULMOGUARD: AI-BASED CHEST X-RAY DETECTION SYSTEM
echo     Edge-Native Deep Learning Pediatric & Adult Pneumonia Triage
echo ===============================================================
echo.
cd /d "%~dp0"
if exist "Chest_x_ray_Detection\Chest_x_ray_Detection\chest_xray.py" (
    cd "Chest_x_ray_Detection\Chest_x_ray_Detection"
)
python chest_xray.py
pause
