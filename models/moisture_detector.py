import joblib
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class MoistureDetector:
    def __init__(self, model_path='saved_models/moisture_rf_model.pkl'):
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.stress_classes = ['Healthy', 'Moderate Stress', 'High Stress']
        
        if os.path.exists(self.model_path):
            self.load_model()

    def train(self, X, y):
        """
        Train the Moisture Stress Detection Model.
        X: Feature matrix (NDMI, SAR, NDVI)
        y: Labels (0: Healthy, 1: Moderate Stress, 2: High Stress)
        """
        print("Training Moisture Detector...")
        self.model.fit(X, y)
        self.save_model()

    def predict(self, features):
        """
        Predict moisture stress. 
        Alternatively, this can fallback to rule-based logic if ML confidence is low.
        """
        features = np.array(features).reshape(1, -1)
        pred_idx = self.model.predict(features)[0]
        return self.stress_classes[pred_idx]

    def predict_rule_based(self, ndmi_value):
        """
        A rule-based backup for Moisture Stress based on standard NDMI thresholds.
        """
        if ndmi_value > 0.4:
            return 'Healthy'
        elif 0.2 <= ndmi_value <= 0.4:
            return 'Moderate Stress'
        else:
            return 'High Stress'

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def load_model(self):
        self.model = joblib.load(self.model_path)
