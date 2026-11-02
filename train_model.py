from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import tensorflow as tf
import os
import json

# Paths
dataset_path = "dataset"
model_save_path = "model/plant_disease_model.h5"
class_index_path = "model/class_indices.json"

# Create model folder if not exists
os.makedirs("model", exist_ok=True)

# Image properties
img_height, img_width = 224, 224
batch_size = 16
epochs = 15

# Load datasets using tf.keras.utils.image_dataset_from_directory
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# Get class names
class_names = train_ds.class_names
num_classes = len(class_names)

# Print and save class indices for reference in app.py
print("\n✅ Class Index Mapping:")
for index, class_name in enumerate(class_names):
    print(f"  {index}: {class_name}")

# Save class index mapping to file for app reference
class_indices = {class_name: index for index, class_name in enumerate(class_names)}
with open(class_index_path, 'w') as f:
    json.dump(class_indices, f)

# Normalize pixel values
def normalize(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label

train_ds = train_ds.map(normalize)
val_ds = val_ds.map(normalize)

# Data augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
])

train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y))

# CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train model
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

# Save model
model.save(model_save_path)
print(f"\n✅ Model trained and saved to: {model_save_path}")
print(f"✅ Class indices saved to: {class_index_path}")
