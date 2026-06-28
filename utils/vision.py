import os
from PIL import Image

class CropVisionClassifier:
    def __init__(self):
        self.classifier = None
        self.is_ready = False

        self.candidate_labels = [
            "Rice", "Wheat", "Maize (Corn)", "Barley", "Sorghum", "Millet", "Oats", "Rye",
            "Soybeans", "Chickpeas", "Lentils", "Dry Beans", "Peas",
            "Groundnuts (Peanuts)", "Oil Palm", "Rapeseed (Canola)", "Sunflower",
            "Sesame", "Linseed (Flax)", "Potatoes", "Cassava", "Sweet Potatoes",
            "Yams", "Taro", "Tomatoes", "Eggplants", "Bell Peppers", "Cabbage",
            "Broccoli", "Cauliflower", "Kale", "Onions", "Garlic", "Cucumbers",
            "Pumpkins", "Squashes", "Watermelons", "Spinach", "Lettuce",
            "Oranges", "Lemons", "Limes", "Apples", "Pears", "Peaches",
            "Plums", "Cherries", "Bananas", "Mangoes", "Pineapples",
            "Avocados", "Strawberries", "Blueberries", "Almonds",
            "Walnuts", "Pistachios", "Cashews", "Cotton", "Jute",
            "Hemp", "Sugarcane", "Sugar Beet", "Coffee", "Tea",
            "Cocoa", "Tobacco"
        ]

    def load_model(self):
        if self.classifier is None:
            print("\nLoading CLIP model... (First time only)")
            from transformers import pipeline

            self.classifier = pipeline(
                "zero-shot-image-classification",
                model="openai/clip-vit-base-patch32"
            )

            self.is_ready = True
            print("CLIP model loaded successfully.")

    def identify_crop(self, image_path):
        try:
            if self.classifier is None:
                self.load_model()

            image = Image.open(image_path)

            results = self.classifier(
                image,
                candidate_labels=self.candidate_labels
            )

            best_match = results[0]

            return (
                best_match["label"],
                round(best_match["score"] * 100, 2)
            )

        except Exception as e:
            print(e)
            return "Unknown", 0.0