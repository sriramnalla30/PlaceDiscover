# Place Search Backend Startup Script
# This script activates the virtual environment and starts the FastAPI server

Write-Host "🚀 Starting Place Search Backend Server..." -ForegroundColor Cyan

# Navigate to project root
Set-Location "D:\gitcode\Projects\Place_Search\Place_Search-Gen_AI"

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# Navigate to backend directory
Set-Location "backend"

# Start the server
Write-Host "🌐 Starting FastAPI server on http://localhost:8002..." -ForegroundColor Green
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload

Write-Host "✅ Server started successfully!" -ForegroundColor Green
Write-Host "📍 API Documentation: http://localhost:8002/docs" -ForegroundColor Cyan
