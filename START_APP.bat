@echo off
REM Start Backend Server
echo ===============================================
echo   Place Search - SerpStack Only Backend
echo ===============================================
echo.
echo Starting backend server on http://localhost:8003
echo.
cd backend
start cmd /k "python -m uvicorn main:app --port 8003 --reload"
echo.
echo Backend server started!
echo.
timeout /t 3 /nobreak > nul
echo.
echo Opening frontend in Chrome...
echo.
start chrome.exe "..\frontend\index.html"
echo.
echo ===============================================
echo   Backend: http://localhost:8003
echo   Frontend: Opened in Chrome
echo   API Docs: http://localhost:8003/docs
echo ===============================================
echo.
pause
