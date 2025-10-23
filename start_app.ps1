# PowerShell script to start the Safenet Dashboard
Write-Host "🚀 Starting Safenet Dashboard..." -ForegroundColor Green
Write-Host "📍 Local URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📍 Map URL: http://localhost:5000/map" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

# Change to the project directory
Set-Location "C:\Users\DELL\OneDrive\画像\Desktop\old projects\co;;age\Safenet_Dashbord"

# Run the Python app
python app.py
