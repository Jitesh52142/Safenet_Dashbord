#!/usr/bin/env python3
"""
Install all requirements for Safenet Dashboard
"""
import subprocess
import sys
import os

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🚀 Installing Safenet Dashboard requirements...")
    print("=" * 50)
    
    # Core requirements
    requirements = [
        "Flask==2.2.5",
        "numpy==1.26.4", 
        "pandas==2.2.1",
        "scikit-learn==1.4.2",
        "folium==0.15.1",
        "requests==2.31.0",
        "Werkzeug>=2.2.2",
        "Jinja2>=3.0",
        "itsdangerous>=2.0",
        "click>=8.0",
        "python-dateutil>=2.8.2",
        "pytz>=2020.1",
        "tzdata>=2022.7",
        "scipy>=1.6.0",
        "joblib>=1.2.0",
        "threadpoolctl>=2.0.0",
        "branca>=0.6.0",
        "xyzservices",
        "packaging",
        "charset-normalizer<4,>=2",
        "idna<4,>=2.5",
        "urllib3<3,>=1.21.1",
        "certifi>=2017.4.17",
        "MarkupSafe>=2.0",
        "six>=1.5"
    ]
    
    success_count = 0
    total_count = len(requirements)
    
    for req in requirements:
        if install_package(req):
            success_count += 1
    
    print("=" * 50)
    print(f"📊 Installation Summary: {success_count}/{total_count} packages installed successfully")
    
    if success_count == total_count:
        print("🎉 All requirements installed successfully!")
        print("✅ Your app is ready to run!")
    else:
        print("⚠️ Some packages failed to install. Check the errors above.")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
