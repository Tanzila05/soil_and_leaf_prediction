import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import json
import re
import os

# === Config ===
MODEL_PATH = "model/plant_disease_model.h5"
CLASS_INDEX_PATH = "model/class_indices.json"

# === Validate required files ===
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found at '{MODEL_PATH}'")

if not os.path.exists(CLASS_INDEX_PATH):
    raise FileNotFoundError(f"❌ Class index file not found at '{CLASS_INDEX_PATH}'")

# === Load model and class index mapping ===
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_INDEX_PATH, "r") as f:
    class_indices = json.load(f)

# Reverse mapping: index → class name
num_classes = len(class_indices)
class_names = [None] * num_classes
for label, index in class_indices.items():
    if 0 <= index < num_classes:
        class_names[index] = label
    else:
        print(f"⚠️ Warning: Class index {index} out of valid range.")

# === Prediction Function ===
def predict_disease(img_path):
    """Predict plant disease from image path"""
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"❌ Image not found at: {img_path}")

    # Load and preprocess image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction[0])

    if predicted_index >= len(class_names) or class_names[predicted_index] is None:
        raise ValueError("❌ Predicted index is out of range or not mapped.")

    predicted_class = class_names[predicted_index]
    readable_name = re.sub(r'_+', ' ', predicted_class).title()

    return readable_name

# === Optional Test Run ===
if __name__ == "__main__":
    test_img = "static/uploads/test_leaf.jpg"  # Replace with valid test image path
    try:
        result = predict_disease(test_img)
        print("🩺 Predicted Disease:", result)
    except Exception as e:
        print("❌ Error:", e)
