@echo off
title GREENRIDE Sustainable Community Mobility Platform
cls
echo =====================================================================
echo   GREENRIDE - Sustainable Community Mobility Platform
echo   Technofest Demonstration Edition (Varanasi Corridors)
echo =====================================================================
echo.
echo [1/2] Verifying Python environment...
py --version
if %errorlevel% neq 0 (
    echo Error: Python is required to run the GreenRide backend server.
    pause
    exit /b 1
)

echo.
echo [2/2] Launching server on http://localhost:8000 ...
start "" "http://localhost:8000"
py backend/run.py
pause

