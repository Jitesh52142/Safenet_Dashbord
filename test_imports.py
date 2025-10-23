#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""
import sys
import os

print("Testing imports...")

try:
    print("✅ Importing Flask...")
    from flask import Flask, render_template, request
    print("✅ Importing pandas...")
    import pandas as pd
    print("✅ Importing numpy...")
    import numpy as np
    print("✅ Importing sklearn...")
    from sklearn.preprocessing import StandardScaler
    print("✅ Importing pickle...")
    import pickle
    print("✅ Importing folium...")
    import folium
    print("✅ Importing json...")
    import json
    print("✅ Importing requests...")
    import requests
    
    print("\n🎉 All imports successful!")
    print("✅ Your app should work correctly!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install missing dependencies with: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
