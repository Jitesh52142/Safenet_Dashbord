# Safenet Dashboard - Vercel Deployment Guide

## 🚀 Quick Deployment to Vercel

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- Git repository (GitHub, GitLab, or Bitbucket)

### Step 1: Prepare Your Repository
1. **Push your code to a Git repository** (GitHub recommended)
2. **Ensure all files are committed:**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository
4. Vercel will automatically detect it's a Python Flask app
5. Click "Deploy"

#### Option B: Deploy via Vercel CLI
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```
2. In your project directory, run:
   ```bash
   vercel
   ```
3. Follow the prompts to link your project

### Step 3: Configure Environment Variables (if needed)
If your app uses environment variables:
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add any required variables (like API keys)

### Step 4: Test Your Deployment
1. Once deployed, Vercel will provide you with a URL
2. Test the following endpoints:
   - `/` - Main form
   - `/map` - Map view
   - `/predict` - Risk assessment (POST)

## 📁 Project Structure
```
Safenet_Dashbord/
├── app.py                 # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── data/                 # Data files
│   ├── prefinal.csv
│   └── with_time_new.csv
├── models/               # ML models
│   ├── log_model.pkl
│   └── rf_model.pkl
├── locations/            # Location data
│   └── locations.json
├── static/               # Static assets
│   └── css/
│       └── style.css
└── templates/            # HTML templates
    ├── index.html
    ├── map.html
    ├── folium_map.html
    └── result.html
```

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

### requirements.txt
```
Flask==2.2.5
numpy==1.26.4
pandas==2.2.1
scikit-learn==1.4.2
folium==0.15.1
requests==2.31.0
```

## 🚨 Important Notes

### File Size Limits
- Vercel has a 50MB limit for serverless functions
- Your ML models and data files should be within this limit
- If files are too large, consider:
  - Using external storage (AWS S3, Google Cloud Storage)
  - Compressing files
  - Using smaller model files

### API Key Security
- The OpenCage API key is currently hardcoded in `app.py`
- For production, move it to environment variables:
  ```python
  API_KEY = os.environ.get('OPENCAGE_API_KEY', 'your-default-key')
  ```

### Performance Considerations
- Vercel serverless functions have a 10-second execution limit
- ML model loading might be slow on cold starts
- Consider caching models or using faster alternatives

## 🧪 Testing Locally

### Run the app locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Test endpoints:
- Open http://localhost:5000 in your browser
- Test the risk assessment form
- Check the map functionality

## 🔄 Updating Your Deployment

1. Make changes to your code
2. Commit and push to your repository:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Vercel will automatically redeploy your app

## 📊 Monitoring

- Check Vercel dashboard for deployment status
- Monitor function logs for any errors
- Use Vercel Analytics for performance insights

## 🆘 Troubleshooting

### Common Issues:
1. **Import errors**: Ensure all dependencies are in `requirements.txt`
2. **File not found**: Check file paths are relative to project root
3. **Timeout errors**: Optimize model loading or reduce file sizes
4. **Memory issues**: Consider using smaller models or external storage

### Debug Steps:
1. Check Vercel function logs
2. Test locally first
3. Verify all files are committed to repository
4. Check environment variables are set correctly

## 🎯 Next Steps

1. **Security**: Move API keys to environment variables
2. **Performance**: Optimize model loading
3. **Monitoring**: Set up error tracking
4. **Backup**: Regular data backups
5. **Scaling**: Consider database for larger datasets

---

**Your app is now ready for deployment on Vercel! 🎉**
