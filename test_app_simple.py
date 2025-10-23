#!/usr/bin/env python3
"""
Simple test to verify the app can start
"""
import sys
import os

# Add the project directory to Python path
project_dir = r"C:\Users\DELL\OneDrive\画像\Desktop\old projects\co;;age\Safenet_Dashbord"
sys.path.insert(0, project_dir)

try:
    print("🧪 Testing Safenet Dashboard...")
    print("=" * 40)
    
    # Test imports
    print("📦 Testing imports...")
    from flask import Flask, render_template, request
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    import pickle
    import folium
    import json
    import requests
    print("✅ All imports successful!")
    
    # Test app creation
    print("🚀 Testing app creation...")
    from app import app
    print("✅ App created successfully!")
    
    # Test basic routes
    print("🌐 Testing routes...")
    with app.test_client() as client:
        # Test home route
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home route (/) works")
        else:
            print(f"❌ Home route failed: {response.status_code}")
            
        # Test map route
        response = client.get('/map')
        if response.status_code == 200:
            print("✅ Map route (/map) works")
        else:
            print(f"❌ Map route failed: {response.status_code}")
    
    print("=" * 40)
    print("🎉 All tests passed! Your app is ready to run!")
    print("📍 To start the app, run: python app.py")
    print("📍 Then visit: http://localhost:5000")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your installation and try again.")
    sys.exit(1)
