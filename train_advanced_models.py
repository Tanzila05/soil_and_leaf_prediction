import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Configurations
os.makedirs("model", exist_ok=True)
os.makedirs("dataset_soil", exist_ok=True)

# =====================================================================
# 1. GENERATE SYNTHETIC SOIL DATASET (Sandy, Clayey, Loamy, Silty/Black)
# =====================================================================
print("[*] Generating synthetic soil image dataset...")
soil_classes = {
    "sandy": {"base_color": (210, 180, 140), "noise_level": 25},      # yellowish-beige, coarse texture
    "clayey": {"base_color": (165, 80, 45), "noise_level": 15},       # reddish-brown, smooth
    "loamy": {"base_color": (90, 55, 30), "noise_level": 20},         # dark brown, crumbly
    "silty_black": {"base_color": (35, 35, 35), "noise_level": 18}    # dark grey/black, fine particles
}

samples_per_class = 100
image_size = (224, 224)

for label, config in soil_classes.items():
    class_dir = os.path.join("dataset_soil", label)
    os.makedirs(class_dir, exist_ok=True)
    
    base = np.array(config["base_color"], dtype=np.float32)
    noise_level = config["noise_level"]
    
    for i in range(samples_per_class):
        # Create base color canvas
        img = np.ones((image_size[0], image_size[1], 3), dtype=np.float32) * base
        
        # Add primary high-frequency noise
        noise = np.random.normal(0, noise_level, (image_size[0], image_size[1], 3))
        
        # Add some larger texture patterns by creating a low-frequency noise layer
        small_noise = np.random.normal(0, noise_level * 0.5, (14, 14, 3))
        large_noise = np.array(Image.fromarray((small_noise + 127).astype(np.uint8)).resize(image_size, Image.Resampling.BILINEAR))
        large_noise = (large_noise.astype(np.float32) - 127.0)
        
        # Combine noise components
        final_img = np.clip(img + noise + large_noise, 0, 255).astype(np.uint8)
        
        # Save image
        img_path = os.path.join(class_dir, f"soil_{i}.jpg")
        Image.fromarray(final_img).save(img_path)

print("[+] Soil image generation complete!")

# =====================================================================
# 2. GENERATE SYNTHETIC CROP RECOMMENDATION DATASET
# =====================================================================
print("[*] Generating synthetic crop recommendation dataset...")

# Target ideal environmental/soil values per crop
crop_profiles = {
    "rice":        {"N": 80.0,  "P": 40.0, "K": 40.0, "temp": 25.0, "humidity": 85.0, "pH": 6.0, "rainfall": 240.0},
    "maize":       {"N": 80.0,  "P": 45.0, "K": 20.0, "temp": 26.0, "humidity": 65.0, "pH": 6.2, "rainfall": 80.0},
    "cotton":      {"N": 120.0, "P": 60.0, "K": 20.0, "temp": 28.0, "humidity": 75.0, "pH": 6.8, "rainfall": 75.0},
    "jute":        {"N": 80.0,  "P": 40.0, "K": 40.0, "temp": 30.0, "humidity": 80.0, "pH": 6.5, "rainfall": 180.0},
    "coffee":      {"N": 100.0, "P": 25.0, "K": 30.0, "temp": 23.0, "humidity": 58.0, "pH": 6.2, "rainfall": 160.0},
    "coconut":     {"N": 20.0,  "P": 15.0, "K": 30.0, "temp": 27.0, "humidity": 85.0, "pH": 6.0, "rainfall": 200.0},
    "apple":       {"N": 25.0,  "P": 130.0,"K": 200.0,"temp": 20.0, "humidity": 92.0, "pH": 6.0, "rainfall": 110.0},
    "orange":      {"N": 35.0,  "P": 10.0, "K": 10.0, "temp": 25.0, "humidity": 92.0, "pH": 6.5, "rainfall": 110.0}
}

crops = list(crop_profiles.keys())
num_crops = len(crops)
crop_indices = {crop: idx for idx, crop in enumerate(crops)}

X_data = []
y_data = []

samples_per_crop = 200

for crop, profile in crop_profiles.items():
    idx = crop_indices[crop]
    for _ in range(samples_per_crop):
        # Generate metrics with normal distribution around ideal conditions
        n = np.random.normal(profile["N"], 8.0)
        p = np.random.normal(profile["P"], 5.0)
        k = np.random.normal(profile["K"], 10.0)
        t = np.random.normal(profile["temp"], 2.0)
        h = np.random.normal(profile["humidity"], 4.0)
        ph = np.random.normal(profile["pH"], 0.3)
        r = np.random.normal(profile["rainfall"], 15.0)
        
        # Ensure values stay positive and within reasonable physiological boundaries
        n = max(0.0, n)
        p = max(0.0, p)
        k = max(0.0, k)
        t = max(5.0, min(50.0, t))
        h = max(10.0, min(100.0, h))
        ph = max(3.5, min(9.5, ph))
        r = max(0.0, r)
        
        X_data.append([n, p, k, t, h, ph, r])
        y_data.append(idx)

X_data = np.array(X_data, dtype=np.float32)
y_data = np.array(y_data, dtype=np.int32)

# Save min-max scaler parameters to normalize during prediction
x_min = X_data.min(axis=0)
x_max = X_data.max(axis=0)

scaler_params = {
    "min": x_min.tolist(),
    "max": x_max.tolist(),
    "features": ["N", "P", "K", "temperature", "humidity", "pH", "rainfall"]
}

with open("model/crop_scaler_params.json", "w") as f:
    json.dump(scaler_params, f)

# Normalize data
X_data_scaled = (X_data - x_min) / (x_max - x_min + 1e-8)

print("[+] Crop recommendation data generation complete!")

# =====================================================================
# 3. TRAIN SOIL IMAGE CLASSIFIER MODEL (CNN)
# =====================================================================
print("[*] Training Soil Image Classifier Model (CNN)...")

soil_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_soil_gen = soil_datagen.flow_from_directory(
    "dataset_soil",
    target_size=image_size,
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_soil_gen = soil_datagen.flow_from_directory(
    "dataset_soil",
    target_size=image_size,
    batch_size=16,
    class_mode='categorical',
    subset='validation'
)

# Save soil class labels mapping
with open("model/soil_class_indices.json", "w") as f:
    json.dump(train_soil_gen.class_indices, f)

# Build a compact CNN for soil classification (speed and efficiency on CPU)
soil_model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(image_size[0], image_size[1], 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(train_soil_gen.num_classes, activation='softmax')
])

soil_model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train CNN (5 epochs is sufficient since textures/colors are simple)
soil_model.fit(
    train_soil_gen,
    validation_data=val_soil_gen,
    epochs=5
)

soil_model.save("model/soil_classifier_model.h5")
print("[+] Saved soil classifier model to 'model/soil_classifier_model.h5'")

# =====================================================================
# 4. TRAIN CROP RECOMMENDATION TABULAR MODEL
# =====================================================================
print("[*] Training Crop Recommendation Tabular Model...")

# Split crop data into train/val
indices = np.arange(X_data_scaled.shape[0])
np.random.shuffle(indices)
split_idx = int(0.8 * X_data_scaled.shape[0])

train_idx, val_idx = indices[:split_idx], indices[split_idx:]
X_train, y_train = X_data_scaled[train_idx], y_data[train_idx]
X_val, y_val = X_data_scaled[val_idx], y_data[val_idx]

# Save crop class labels mapping
with open("model/crop_class_indices.json", "w") as f:
    json.dump(crop_indices, f)

# Build a Feed-Forward Neural Network
crop_model = Sequential([
    Dense(32, activation='relu', input_shape=(7,)),
    Dense(16, activation='relu'),
    Dense(num_crops, activation='softmax')
])

crop_model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train NN
crop_model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=20,
    batch_size=8,
    verbose=1
)

crop_model.save("model/crop_recommender_model.h5")
print("[+] Saved crop recommender model to 'model/crop_recommender_model.h5'")

print("[+] All advanced models have been trained and saved successfully!")
