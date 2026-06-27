import os
from PIL import Image

class CropVisionClassifier:
    def __init__(self):
        print("\n========================================================")
        print("🤖 INITIALIZING TRUE ML VISION CLASSIFIER (CLIP)")
        print("Note: First time startup will download ~600MB of AI weights.")
        print("========================================================\n")
        
        try:
            from transformers import pipeline
            self.classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
            self.is_ready = True
            print("✅ Vision Classifier successfully loaded into memory!")
        except Exception as e:
            print(f"❌ Failed to load Vision Classifier: {e}")
            self.is_ready = False

        # The 66 crops requested for ISRO Hackathon
        self.candidate_labels = [
            "Rice", "Wheat", "Maize (Corn)", "Barley", "Sorghum", "Millet", "Oats", "Rye", "Soybeans", 
            "Chickpeas", "Lentils", "Dry Beans", "Peas", "Groundnuts (Peanuts)", "Oil Palm", 
            "Rapeseed (Canola)", "Sunflower", "Sesame", "Linseed (Flax)", "Potatoes", "Cassava", 
            "Sweet Potatoes", "Yams", "Taro", "Tomatoes", "Eggplants", "Bell Peppers", "Cabbage", 
            "Broccoli", "Cauliflower", "Kale", "Onions", "Garlic", "Cucumbers", "Pumpkins", "Squashes", 
            "Watermelons", "Spinach", "Lettuce", "Oranges", "Lemons", "Limes", "Apples", "Pears", 
            "Peaches", "Plums", "Cherries", "Bananas", "Mangoes", "Pineapples", "Avocados", 
            "Strawberries", "Blueberries", "Almonds", "Walnuts", "Pistachios", "Cashews", "Cotton", 
            "Jute", "Hemp", "Sugarcane", "Sugar Beet", "Coffee", "Tea", "Cocoa", "Tobacco"
        ]

    def identify_crop(self, image_path):
        """
        Uses Zero-Shot Image Classification to mathematically match the image against the 66 crop labels.
        """
        if not self.is_ready:
            return "AI Not Ready", 0.0

        try:
            image = Image.open(image_path)
            # The Hugging Face pipeline does all the heavy lifting!
            results = self.classifier(image, candidate_labels=self.candidate_labels)
            
            # 'results' is a sorted list of dictionaries from highest to lowest confidence
            best_match = results[0]
            crop_name = best_match['label']
            confidence = round(best_match['score'] * 100, 2)
            
            return crop_name, confidence
        except Exception as e:
            print(f"Vision Classification Error: {e}")
            return "Unknown Error", 0.0
