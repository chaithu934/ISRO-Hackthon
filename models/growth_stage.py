import joblib
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class GrowthStagePredictor:
    def __init__(self, model_path='saved_models/growth_stage_rf_model.pkl'):
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.stages = ['Seedling', 'Vegetative', 'Flowering', 'Grain Filling', 'Harvest']
        
        if os.path.exists(self.model_path):
            self.load_model()

    def train(self, X, y):
        """
        Train the Growth Stage Prediction Model.
        X: Feature matrix (NDVI time-series, accumulated degree days, crop type)
        y: Labels (0 to 4 mapping to self.stages)
        """
        print("Training Growth Stage Predictor...")
        self.model.fit(X, y)
        self.save_model()

    def predict(self, features):
        """
        Predict current growth stage.
        """
        features = np.array(features).reshape(1, -1)
        pred_idx = self.model.predict(features)[0]
        return self.stages[pred_idx]

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)

    def load_model(self):
        self.model = joblib.load(self.model_path)
