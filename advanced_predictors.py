import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from utils.crop_soil_data import SOIL_INFO, CROP_INFO

# Paths to models and metadata
SOIL_MODEL_PATH = "model/soil_classifier_model.h5"
SOIL_LABELS_PATH = "model/soil_class_indices.json"

CROP_MODEL_PATH = "model/crop_recommender_model.h5"
CROP_LABELS_PATH = "model/crop_class_indices.json"
CROP_SCALER_PATH = "model/crop_scaler_params.json"

# Cached model and meta references
_soil_model = None
_soil_classes = None

_crop_model = None
_crop_classes = None
_crop_scaler = None

def load_soil_resources():
    global _soil_model, _soil_classes
    if _soil_model is None:
        if not os.path.exists(SOIL_MODEL_PATH):
            raise FileNotFoundError(f"❌ Soil model not found at {SOIL_MODEL_PATH}. Make sure training script was run.")
        if not os.path.exists(SOIL_LABELS_PATH):
            raise FileNotFoundError(f"❌ Soil labels mapping not found at {SOIL_LABELS_PATH}.")
            
        _soil_model = tf.keras.models.load_model(SOIL_MODEL_PATH)
        
        with open(SOIL_LABELS_PATH, "r") as f:
            indices = json.load(f)
        # Reverse mapping: index -> label
        _soil_classes = [None] * len(indices)
        for label, idx in indices.items():
            _soil_classes[idx] = label

def load_crop_resources():
    global _crop_model, _crop_classes, _crop_scaler
    if _crop_model is None:
        if not os.path.exists(CROP_MODEL_PATH):
            raise FileNotFoundError(f"❌ Crop model not found at {CROP_MODEL_PATH}. Make sure training script was run.")
        if not os.path.exists(CROP_LABELS_PATH):
            raise FileNotFoundError(f"❌ Crop labels mapping not found at {CROP_LABELS_PATH}.")
        if not os.path.exists(CROP_SCALER_PATH):
            raise FileNotFoundError(f"❌ Crop scaler parameters not found at {CROP_SCALER_PATH}.")
            
        _crop_model = tf.keras.models.load_model(CROP_MODEL_PATH)
        
        with open(CROP_LABELS_PATH, "r") as f:
            indices = json.load(f)
        # Reverse mapping: index -> label
        _crop_classes = [None] * len(indices)
        for label, idx in indices.items():
            _crop_classes[idx] = label
            
        with open(CROP_SCALER_PATH, "r") as f:
            _crop_scaler = json.load(f)

# === Soil Prediction Interface ===
def predict_soil_class(img_path):
    """
    Predict soil type from image path.
    Returns a dict containing the soil key, clean title, properties, advantages, drawbacks, improvement tips, and recommended crops.
    """
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"❌ Soil image not found at: {img_path}")
        
    load_soil_resources()
    
    # Load and preprocess image (224x224, normalized to [0,1])
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    # Run prediction
    predictions = _soil_model.predict(img_array)
    predicted_idx = np.argmax(predictions[0])
    soil_key = _soil_classes[predicted_idx]
    
    # Retrieve details from static DB
    details = SOIL_INFO.get(soil_key, {
        "title": soil_key.replace("_", " ").title(),
        "properties": "No detailed properties available.",
        "advantages": "No advantage info available.",
        "drawbacks": "No drawback info available.",
        "improvement": "No improvement tips available.",
        "crops": "Unknown crops."
    })
    
    # Pack result
    result = {
        "key": soil_key,
        "title": details["title"],
        "properties": details["properties"],
        "advantages": details["advantages"],
        "drawbacks": details["drawbacks"],
        "improvement": details["improvement"],
        "crops": details["crops"],
        "confidence": float(predictions[0][predicted_idx])
    }
    return result

# === Crop Recommendation Interface ===
def recommend_crop(n, p, k, temp, humidity, ph, rainfall):
    """
    Recommend optimal crop based on soil and climate properties.
    Returns a dict containing the recommended crop, optimal conditions, growth stages list, and fertilizer suggestions.
    """
    load_crop_resources()
    
    # Preprocess/Scale inputs using cached scaler parameters
    raw_vector = np.array([n, p, k, temp, humidity, ph, rainfall], dtype=np.float32)
    s_min = np.array(_crop_scaler["min"], dtype=np.float32)
    s_max = np.array(_crop_scaler["max"], dtype=np.float32)
    
    # Avoid divide by zero
    scaled_vector = (raw_vector - s_min) / (s_max - s_min + 1e-8)
    scaled_vector = np.expand_dims(scaled_vector, axis=0)
    
    # Predict
    predictions = _crop_model.predict(scaled_vector)
    predicted_idx = np.argmax(predictions[0])
    crop_key = _crop_classes[predicted_idx]
    
    # Retrieve details from static DB
    details = CROP_INFO.get(crop_key, {
        "title": crop_key.replace("_", " ").title(),
        "optimal_conditions": "No optimal conditions defined.",
        "growth_stages": "No growth stage data available.",
        "fertilizer": "No fertilizer recommendations available."
    })
    
    # Format growth stages into list
    stages_list = [stage.strip() for stage in details["growth_stages"].split("\n") if stage.strip()]
    
    result = {
        "key": crop_key,
        "title": details["title"],
        "optimal_conditions": details["optimal_conditions"],
        "growth_stages": stages_list,
        "fertilizer": details["fertilizer"],
        "confidence": float(predictions[0][predicted_idx])
    }
    return result
