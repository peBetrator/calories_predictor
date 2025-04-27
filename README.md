# Calories Predictor

A simple iOS app that predicts the number of calories burned during exercise, using live Apple Watch sensor data and a custom-trained machine learning model.

## Features

- 🤖 **Machine Learning**:
  - Research notebook (`ML research.ipynb`) for model building, feature engineering, and performance evaluation.
  - Linear Regression model trained on exercise and biometric data.
  - Script to export trained model to CoreML format (`CaloriesPredictorFromCSV.mlmodel`) for direct iOS integration.

- 📱 **iOS App**:
  - SwiftUI-based simple interface.
  - Fetches real-time exercise metrics (heart rate, body temperature, weight, height, workout duration) from Apple Watch using HealthKit.
  - Predicts calories burned using an on-device Core ML model.

## Repository Structure

```
├── ML
│   ├── ML research.ipynb                - Research notebook for model development and evaluation
│   └── export_mlmodel.py                - Train and export ML model to Core ML format
└── CaloriesPrediction
    ├── CaloriesPredictionApp.swift      - SwiftUI app entry point
    ├── ContentView.swift                - Main UI for user inputs and predictions
    ├── HealthManager.swift              - Fetch exercise and biometric data from HealthKit
    └── Info.plist                       - App configuration (permissions for HealthKit, etc.)
```

## Requirements

The following versions are recommended for full compatibility:

| Tool / Library | Version |
|:--------------|:--------|
| **Python**         | 3.9     |
| **coremltools**    | 8.2     |
| **scikit-learn**   | 1.2.2   |

Other packages and system libraries can use their **latest LTS (Long-Term Support)** versions unless stated otherwise.

## How It Works

### Machine Learning Part

- **Data Preparation**:
  - Merge `exercise.csv` (user features) and `calories.csv` (target calories) by `User_ID`.
  - Encode categorical features (gender).
  - Prepare features: `Gender`, `Age`, `Height`, `Weight`, `Duration`, `Heart_Rate`, `Body_Temp`.

- **Model Training**:
  - Train a `LinearRegression` model using scikit-learn.
  - Test predictions on sample data.

- **Model Export**:
  - Export the trained model to `.mlmodel` format via `coremltools` for iOS use.

```bash
pip install pandas coremltools scikit-learn
python export_mlmodel.py
```
This will generate `CaloriesPredictorFromCSV.mlmodel`.