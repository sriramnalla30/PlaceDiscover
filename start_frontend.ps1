# Place Search Frontend Startup Script  
# This script starts an HTTP server for the frontend

Write-Host "🚀 Starting Place Search Frontend Server..." -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location "D:\gitcode\Projects\Place_Search\Place_Search-Gen_AI\frontend"

# Start HTTP server
Write-Host "🌐 Starting HTTP server on http://localhost:3000..." -ForegroundColor Green
python -m http.server 3000

Write-Host "✅ Frontend server started!" -ForegroundColor Green
Write-Host "📍 Open: http://localhost:3000" -ForegroundColor Cyan
