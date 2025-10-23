# 🛡️ Safenet Dashboard

A Flask-based safety risk assessment application that uses machine learning to predict risk levels based on various environmental and demographic factors.

## 🌟 Features

- **Risk Assessment**: ML-powered risk prediction using Random Forest and Logistic Regression models
- **Interactive Maps**: Folium-based mapping with location markers
- **Real-time Analysis**: Process environmental data to assess safety levels
- **User-friendly Interface**: Clean, responsive web interface
- **Location Services**: Integration with OpenCage API for location data

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run_local.py
```

Visit `http://localhost:5000` to access the application.

### Deploy to Vercel
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 How It Works

1. **Data Input**: Users provide environmental and demographic data
2. **Preprocessing**: Time features are encoded and additional features are engineered
3. **ML Prediction**: Two models predict isolation and risk levels
4. **Hybrid Assessment**: Combines ML predictions with rule-based classification
5. **Risk Classification**: 
   - 🟢 Low Risk (0)
   - 🟡 Medium Risk (1) 
   - 🔴 High Risk (2)

## 🏗️ Project Structure

```
Safenet_Dashbord/
├── app.py                 # Main Flask application
├── vercel.json           # Vercel deployment config
├── requirements.txt      # Python dependencies
├── run_local.py         # Local development server
├── data/                # Training and test data
├── models/              # Trained ML models
├── locations/           # Location data
├── static/              # CSS and static assets
└── templates/           # HTML templates
```

## 🔧 Configuration

The app uses the following key parameters:
- **OpenCage API**: For geocoding services
- **ML Models**: Pre-trained Random Forest and Logistic Regression models
- **Risk Factors**: Crowd density, signal strength, gender ratio, time, population

## 📱 Usage

1. **Access the Dashboard**: Navigate to the main page
2. **Input Data**: Fill in the risk assessment form with:
   - Tower ID and coordinates
   - Signal strength
   - Population demographics
   - Crowd density
   - Time of day
3. **Get Assessment**: Submit to receive risk level prediction
4. **View Map**: Check the interactive map for location details

## 🛠️ Dependencies

- Flask 2.2.5
- NumPy 1.26.4
- Pandas 2.2.1
- Scikit-learn 1.4.2
- Folium 0.15.1
- Requests 2.31.0

## 📄 License

This project is part of the Safenet Dashboard system for safety risk assessment.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions, please refer to the deployment guide or create an issue in the repository.

---

**Built with ❤️ for community safety**
