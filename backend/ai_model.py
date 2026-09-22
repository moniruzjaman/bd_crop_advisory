
"""
Symptom-First CNN Classifier
No disease names in training labels - only symptoms
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
from typing import Dict

class SymptomClassifier:
    """
    CNN-based symptom classifier
    Input: RGB image (224x224)
    Output: Symptom category with confidence
    """

    SYMPTOM_CLASSES = [
        "healthy",
        "leaf_spot", 
        "yellowing",
        "wilt",
        "mosaic",
        "leaf_distortion",
        "galls",
        "necrosis_blight",
        "root_problem",
        "stem_damage",
        "panicle_ear_problem"
    ]

    def __init__(self, model_path: str = None):
        self.img_size = (224, 224)
        self.confidence_threshold = 0.6

        # Initialize model (placeholder for actual trained model)
        # In production, load: self.model = keras.models.load_model(model_path)
        self.model = self._build_model()

    def _build_model(self):
        """Build CNN architecture for symptom classification"""
        model = keras.Sequential([
            keras.layers.Input(shape=(224, 224, 3)),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(len(self.SYMPTOM_CLASSES), activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    async def classify(self, image_file) -> Dict:
        """
        Classify image symptom
        Returns: {"symptom": str, "confidence": float, "all_probabilities": dict}
        """
        try:
            # Read and preprocess image
            contents = await image_file.read()
            image = Image.open(io.BytesIO(contents))

            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize
            image = image.resize(self.img_size)

            # Normalize
            img_array = keras.preprocessing.image.img_to_array(image)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            predictions = self.model.predict(img_array, verbose=0)[0]

            # Get top prediction
            top_idx = np.argmax(predictions)
            confidence = float(predictions[top_idx])
            symptom = self.SYMPTOM_CLASSES[top_idx]

            # Build probability dictionary
            all_probs = {
                cls: float(prob) 
                for cls, prob in zip(self.SYMPTOM_CLASSES, predictions)
            }

            # Mark low certainty
            certainty_flag = confidence < self.confidence_threshold

            return {
                "symptom": symptom,
                "confidence": round(confidence, 4),
                "certainty": "low" if certainty_flag else "medium" if confidence < 0.8 else "high",
                "all_probabilities": all_probs,
                "requires_human_review": certainty_flag
            }

        except Exception as e:
            return {
                "symptom": "unknown",
                "confidence": 0.0,
                "error": str(e),
                "requires_human_review": True
            }

    def get_symptom_description(self, symptom: str) -> Dict:
        """Get Bangla description of symptom"""
        descriptions = {
            "healthy": {"en": "Plant appears healthy", "bn": "গাছ সুস্থ দেখাচ্ছে"},
            "leaf_spot": {"en": "Spots on leaves", "bn": "পাতায় দাগ দেখা যাচ্ছে"},
            "yellowing": {"en": "Yellowing of leaves", "bn": "পাতা হলুদ হয়ে গেছে"},
            "wilt": {"en": "Wilting/plant drooping", "bn": "গাছ শুকিয়ে/নুয়ে গেছে"},
            "mosaic": {"en": "Mosaic pattern on leaves", "bn": "পাতায় মোজাইক প্যাটার্ন"},
            "leaf_distortion": {"en": "Twisted/deformed leaves", "bn": "পাতা বাঁকা/বিকৃত"},
            "galls": {"en": "Swelling or galls", "bn": "গাছে ফোলা/গাল দেখা যাচ্ছে"},
            "necrosis_blight": {"en": "Dead/burnt tissue", "bn": "পাতা/কাণ্ড পোড়া/মরে গেছে"},
            "root_problem": {"en": "Root damage symptoms", "bn": "গোড়ায় সমস্যা"},
            "stem_damage": {"en": "Stem/culm damage", "bn": "কাণ্ডে ক্ষতি"},
            "panicle_ear_problem": {"en": "Grain/fruit problem", "bn": "শীষ/ফলে সমস্যা"}
        }
        return descriptions.get(symptom, {"en": "Unknown", "bn": "অজানা"})
