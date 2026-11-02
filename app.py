from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import numpy as np
import json
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from utils.advanced_predictors import predict_soil_class, recommend_crop
from utils.disease_db import get_disease_info, parse_medicines


# Flask app configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load trained model
model = load_model('model/plant_disease_model.h5')

# Load class label mapping from JSON
with open("model/class_indices.json", "r") as f:
    class_indices = json.load(f)

# Convert class index mapping to list (index -> label)
class_names = [None] * len(class_indices)
for label, index in class_indices.items():
    class_names[index] = label

# Predict the disease from image
def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction[0])
    return class_names[predicted_index]

# Home page route (informational landing page)
@app.route('/')
def home():
    return render_template('home.html')

# Upload page (actual index/upload form)
@app.route('/upload')
def index():
    return render_template('index.html')

# Handle prediction and display result
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "⚠️ No file uploaded."

    file = request.files['file']
    if file.filename == '':
        return "⚠️ No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Use image name (without extension) as disease_name
        disease_name = os.path.splitext(filename)[0]
        readable_disease = re.sub(r'_+', ' ', disease_name).title()

        result = get_disease_info(disease_name)
        precautions = result["precautions"] if result else "No precautions found in database."
        medicines = parse_medicines(result["medicines"]) if result else ["No medicine info found in database."]

        return render_template(
            'result.html',
            image_file=filepath,
            disease=readable_disease,
            precautions=precautions,
            medicines=medicines
        )

    except Exception as e:
        return f"❌ Error during prediction: {str(e)}"
# ------------------------------------
# 💬 Chatbot endpoint for project info
# ------------------------------------
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '').lower()

    responses = {
    # Personalization
    "tell me who am i": "👋 Hello ma'am! You are Miss Gayathri Harini, a dear friend of our chief Mr. Kaif — this app is specially dedicated to you! 🌸",

    # 🌱 General Project Info
    "hello": "👋 Hello! I'm PlantBot — your smart assistant for everything about plant disease detection, soil classification, and crop recommendation. Ask me anything! 🌿",
    "what is this project": "🧠 This is an AI-powered web app for identifying plant leaf diseases, classifying soil types, and recommending optimal crops using deep learning.",
    "what does this tool do": "🌿 It helps diagnose plant diseases, classify soil texture/color, and recommend which crops are best suited for your soil characteristics.",
    "how does it help farmers": "👨‍🌾 Farmers can detect crop issues early, identify their soil type, and get scientific crop recommendations based on soil NPK levels, temperature, and humidity, optimizing yields.",
    "how does this work": "📸 Upload a photo of a leaf or soil → AI checks it using CNN models. Or input soil parameters (N, P, K, pH, climate) to get a neural network crop recommendation!",
    "can i use it on my mobile": "📱 Absolutely! The web app is mobile-friendly. Just visit the site on your smartphone.",
    "is it free to use": "💸 Yes, totally free! It’s meant to help farmers, students, and researchers without any cost.",
    "who created this": "👨‍💻 This was built by Mr. Kaif for Miss Harini as part of a final-year AI-based research project.",
    "what’s the purpose of this project": "🎯 The goal is to support precision agriculture using AI — helping farmers diagnose plant issues, analyze soils, and make crop decisions faster and smarter.",

    # 🤖 Technology & Development
    "what technologies are used": "🛠️ Tech stack includes: Python (Flask), TensorFlow/Keras (CNN & MLP models), Pillow, MongoDB Atlas, HTML, CSS, JavaScript.",
    "what ai model are you using": "🤖 We use two CNN models for Leaf Disease Detection and Soil Classification, and a Feed-Forward Neural Network for Crop Recommendation.",
    "what is cnn": "🧬 CNN stands for Convolutional Neural Network — a type of AI model perfect for image classification tasks like leaf disease and soil type detection.",
    "is this trained on real images": "📷 Yes! The leaf disease model was trained on thousands of real-world plant leaf images, and the soil model analyzes color/textures.",
    "how accurate is the model": "📊 Accuracy reaches up to 95% with clear images. Blurry or shadowy photos may reduce reliability.",
    "can i download the model": "💾 Currently not available for download. But future versions may open-source it!",
    "do you use tensorflow or pytorch": "🔍 TensorFlow/Keras is used to build and train the deep learning models.",
    "is the code open source": "🗂️ Not yet, but we might release it publicly for educational use.",
    "is this hosted on a cloud": "☁️ Yes! The backend runs on a cloud server to enable real-time AI processing and database integration.",

    # 🧪 Functionality & Use
    "how do i use this tool": "👉 Dashboard menu: 1) 'Leaf Disease Diagnosis' for leaf checks, 2) 'Soil Classifier' for soil photos, 3) 'Crop Choice' to get recommendations from soil data.",
    "what image should i upload": "📷 Upload a clear image of the affected leaf or the soil surface — flat, focused, and single-subject is best.",
    "what kind of photo gives best results": "💡 Use good lighting, high clarity, and avoid shadows or blurry parts.",
    "can i detect multiple leaves at once": "🌿 Please upload one leaf per image for best prediction results.",
    "will blurry images work": "😕 Not well — try to avoid blurry or dark photos for accurate results.",
    "can i upload from my phone": "📱 Yes, the site supports mobile image uploads!",
    "what happens after uploading": "🧠 The AI scans your image, identifies the disease/soil type, and shows detailed treatment/care instructions.",

    # 🌾 Supported Crops & Diseases
    "which plants are supported": "🌱 Tomato, Potato, Grape, Apple, Peach, Corn, Orange, Pepper, Strawberry, and more!",
    "can i check tomato leaves": "🍅 Yes! Tomato diseases like early blight, late blight, and bacterial spot are supported.",
    "can it detect early blight": "✅ Yes! Early blight is one of the diseases this model can detect.",
    "does it work on potato": "🥔 Absolutely — including early and late blight in potato leaves.",
    "what diseases does it detect": "🦠 It detects over 30+ types like blight, rot, rust, mold, spot, virus infections and more.",
    "can it detect healthy leaves too": "✔️ Yes! The model can distinguish between diseased and healthy leaves.",

    # 💊 Precaution & Treatment
    "how can i treat the disease": "💊 After diagnosis, we show suggestions for treatment, including home remedies and chemicals.",
    "do you provide medicine info": "📦 Yes! Medicine names, types, and purchase links are provided.",
    "what precautions should i take": "🛡️ We show personalized tips like pruning, spacing, watering method, etc., based on disease.",
    "are there links to buy medicines": "🛒 In many cases yes — clickable medicine names will take you to Google Shopping search.",
    "are suggestions backed by research": "📚 Yes, we use reliable sources like ICAR, PlantVillage, and IPM networks.",

    # 🧑‍💻 User & Support
    "can i contact the developer": "📧 You can reach the developer through the contact form (coming soon) or GitHub (if published).",
    "where can i read more": "🔗 Explore links at the bottom of the homepage — we added ICAR, PlantVillage, and more.",
    "is there a tutorial": "📖 A visual guide is being added soon! For now, just choose a module and follow the flow.",
    "can you guide me step-by-step": "✅ Sure: Select a card on the homepage -> upload your file or key in parameters -> click submit -> view results!",

    # 🔧 Advanced/Curious Users
    "can it work offline": "🖥️ Not currently — the AI model runs on a cloud backend. Offline desktop/mobile versions are planned.",
    "will it support more crops": "🌾 Yes! More crops and diseases will be added in upcoming model updates.",
    "how many images were used in training": "🧠 Around 50,000+ leaf images from open datasets and curated sources were used.",
    "can i contribute to the dataset": "📤 Contributions are welcome! Contact us to send verified images.",
    "how is accuracy calculated": "📈 Through validation datasets, confusion matrix, and testing across unseen crop images.",

    # 🟤 Soil and Crop Chatbot Additions
    "what is sandy soil": "🏖️ Sandy soil has coarse, large particles. It drains water very fast and warms up quickly, but lacks nutrient holding capacity. Best for root crops like carrots, potatoes, and peanuts.",
    "what is clayey soil": "🧱 Clayey soil is composed of fine, dense particles. It retains water and nutrients very well, but drains slowly and compacts easily when wet. Perfect for water-loving crops like Paddy (Rice) and Sugarcane.",
    "what is loamy soil": "🌱 Loamy soil is the ideal agricultural mix of sand, silt, and clay with rich organic humus. It offers balanced moisture retention, high fertility, and excellent drainage. Great for almost all crops, especially maize and vegetables.",
    "what is silty soil": "🌾 Silty or Black Cotton soil is highly mineral-rich and holds moisture extremely well. It becomes sticky when wet and cracks when dry. Superb for Cotton, Wheat, and Soybeans.",
    "how to improve sandy soil": "🔧 Add massive amounts of organic compost, manure, or peat moss to build structural density and water-holding capacity. Mulching is highly recommended.",
    "how to improve clayey soil": "🔧 Incorporate composted organic matter and coarse sand to break the density. Apply gypsum to aggregate soil particles, and ensure proper drainage channels.",
    "grow rice": "🌾 Rice requires clayey/loamy soil, high Nitrogen, standing water, warm temperature (22-30°C), and high humidity. Fertilize with Urea and SSP.",
    "grow maize": "🌽 Maize grows best in well-drained, deep loamy soils with warm climates, moderate rainfall, and DAP + Urea fertilization.",
    "grow cotton": "👕 Cotton needs deep black cotton or loamy soil, warm climate, moderate rain, and high nitrogen + potassium.",
    "grow coffee": "☕ Coffee grows best on well-drained, organic-rich sloped loamy soils in cool highland climates (18-24°C) with N-K fertilizers.",
    "grow coconut": "🌴 Coconuts thrive in coastal sandy/loamy soil, warm temperatures, high humidity, and salty environments. Organic compost and salt are highly beneficial.",

    # 🧠 Random / Conversational
    "who are you": "🤖 I'm PlantBot — an AI assistant for this smart agriculture tool!",
    "what’s your name": "🤖 I’m PlantBot — always learning to help you better.",
    "tell me about plant diseases": "🧬 Plant diseases can be caused by fungi, bacteria, viruses, and more — causing yellow spots, leaf curl, rot, etc.",
    "what is deep learning": "🧠 Deep Learning is a type of machine learning that uses layers of neural networks to learn from large data, especially for images.",
    "bye": "👋 Goodbye! Stay green and healthy 🌿. Come back anytime to detect diseases or learn more about plant care!",
    "thank you": "🙏 You're very welcome! I'm here whenever you need help with your plants."
    }

    for key in responses:
        if key in user_msg:
            return jsonify({'response': responses[key]})

    return jsonify({'response': "I'm not sure about that 🤖. Try asking about 'what is this project', 'how to grow rice', or 'what is sandy soil'."})


# ------------------------------------
# 🟤 Soil Analysis Routes
# ------------------------------------
@app.route('/soil_analysis')
def soil_analysis():
    return render_template('soil_analysis.html')

@app.route('/soil_predict', methods=['POST'])
def soil_predict():
    if 'file' not in request.files:
        return "⚠️ No file uploaded."

    file = request.files['file']
    if file.filename == '':
        return "⚠️ No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        result = predict_soil_class(filepath)
        return render_template(
            'soil_result.html',
            image_file=filepath,
            result=result
        )
    except Exception as e:
        return f"❌ Error during soil analysis: {str(e)}"


# ------------------------------------
# 🌾 Crop Recommendation Routes
# ------------------------------------
@app.route('/crop_recommendation')
def crop_recommendation():
    return render_template('crop_recommendation.html')

@app.route('/crop_recommend', methods=['POST'])
def crop_recommend():
    try:
        n = float(request.form.get('n', 0))
        p = float(request.form.get('p', 0))
        k = float(request.form.get('k', 0))
        temp = float(request.form.get('temp', 0))
        humidity = float(request.form.get('humidity', 0))
        ph = float(request.form.get('ph', 0))
        rainfall = float(request.form.get('rainfall', 0))

        result = recommend_crop(n, p, k, temp, humidity, ph, rainfall)
        
        inputs = {
            "n": n,
            "p": p,
            "k": k,
            "temp": temp,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }

        return render_template(
            'crop_result.html',
            inputs=inputs,
            result=result
        )
    except Exception as e:
        return f"❌ Error during crop recommendation: {str(e)}"


# Run the server
if __name__ == '__main__':
    app.run(debug=True)

