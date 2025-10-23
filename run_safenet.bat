@echo off
echo 🚀 Starting Safenet Dashboard...
echo ================================

cd /d "C:\Users\DELL\OneDrive\画像\Desktop\old projects\co;;age\Safenet_Dashbord"

echo 📍 Current directory: %CD%
echo 📦 Installing/checking requirements...

python -m pip install Flask==2.2.5 numpy==1.26.4 pandas==2.2.1 scikit-learn==1.4.2 folium==0.15.1 requests==2.31.0

echo.
echo 🧪 Testing app...
python -c "import sys; sys.path.insert(0, '.'); from app import app; print('✅ App imported successfully!')"

echo.
echo 🚀 Starting server...
echo 📍 Local URL: http://localhost:5000
echo 📍 Map URL: http://localhost:5000/map
echo 🛑 Press Ctrl+C to stop the server
echo ================================

python app.py

pause
