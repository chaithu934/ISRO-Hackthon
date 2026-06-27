import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

class CropClassifier:
    def __init__(self, model_path='saved_models/crop_rf_model.pkl'):
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.target_names = ['Rice', 'Cotton', 'Maize', 'Wheat', 'Sugarcane']
        
        # Load model if it exists
        if os.path.exists(self.model_path):
            self.load_model()

    def train(self, X, y):
        """
        Train the Crop Classification Model.
        X: Feature matrix (NDVI, NDMI, SAR, Red, Green, Blue, NIR, SWIR, etc.)
        y: Labels (0: Rice, 1: Cotton, 2: Maize, 3: Wheat, 4: Sugarcane)
        """
        print("Training Crop Classifier...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred, target_names=self.target_names))
        
        self.save_model()

    def predict(self, features):
        """
        Predict crop type from features.
        """
        # Ensure features are in 2D array format for sklearn
        features = np.array(features).reshape(1, -1)
        pred_idx = self.model.predict(features)[0]
        confidence = np.max(self.model.predict_proba(features)[0])
        
        return {
            'crop_name': self.target_names[pred_idx],
            'confidence': round(confidence * 100, 2)
        }

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        self.model = joblib.load(self.model_path)
        print(f"Model loaded from {self.model_path}")
