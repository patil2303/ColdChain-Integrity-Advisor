@echo off
echo ============================================================
echo   Cold-Chain Integrity Advisory Platform — MVP
echo   US FDA 21 CFR Part 11 & WHO GDP Operations Tower
echo ============================================================
echo.
echo Starting FastAPI server at http://127.0.0.1:8000 ...
cd /d "%~dp0server"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
