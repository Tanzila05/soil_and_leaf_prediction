# Static database of agronomic information for Soil Types and Crops

SOIL_INFO = {
    "sandy": {
        "title": "Sandy Soil",
        "properties": "High sand content with large, coarse particles. Excellent aeration but very low water retention and rapid nutrient leaching.",
        "advantages": "Warms up quickly in the spring, easy to till and cultivate, and low risk of waterlogging.",
        "drawbacks": "Dries out very quickly. Fails to hold nutrients, requiring frequent watering and organic fertilization.",
        "improvement": "Incorporate heavy amounts of organic compost, peat moss, or well-rotted manure to build structure. Apply mulching to prevent moisture loss. Add clay or silt if possible.",
        "crops": "Potato, Carrot, Groundnut, Watermelon, Beetroot, Radish."
    },
    "clayey": {
        "title": "Clayey Soil",
        "properties": "Extremely fine particles that compact tightly. High nutrient density but poor aeration and very slow water drainage.",
        "advantages": "Retains moisture and essential plant nutrients exceptionally well. Highly fertile when managed correctly.",
        "drawbacks": "Prone to waterlogging, becomes sticky and hard to work when wet, and dries into rock-hard crusts during summer. Slow to warm up in spring.",
        "improvement": "Add coarse river sand and composted organic matter to improve drainage. Apply gypsum (calcium sulfate) to aggregate clay particles. Avoid working the soil when wet to prevent compaction.",
        "crops": "Paddy (Rice), Wheat, Sugarcane, Broccoli, Cabbage."
    },
    "loamy": {
        "title": "Loamy Soil",
        "properties": "A near-perfect balance of sand, silt, and clay with rich organic humus. The gold standard for agricultural soils.",
        "advantages": "Maintains an ideal balance of moisture retention and drainage. Highly fertile, crumbly texture, and rich in beneficial microbes.",
        "drawbacks": "Relatively few drawbacks. Can erode under heavy rains if not covered, and requires regular replenishment of organic matter.",
        "improvement": "Maintain its superior structure by adding regular compost, practicing crop rotation, and using cover crops to prevent erosion.",
        "crops": "Tomato, Pepper, Corn, Cotton, Jute, Beans, and most fruits/vegetables."
    },
    "silty_black": {
        "title": "Silty / Black Cotton Soil",
        "properties": "Rich in fine silt and clay particles, with a high concentration of dark organic humus. Extremely fertile and mineral-rich.",
        "advantages": "Exceptional water-holding capacity and highly rich in calcium, magnesium, carbonate, and potassium.",
        "drawbacks": "Expands and becomes sticky when wet, and develops deep, wide cracks when dry. Prone to surface erosion and waterlogging.",
        "improvement": "Improve aeration by carrying out deep tillage before the monsoons. Add organic compost to enhance drainage and break the density. Install drainage channels.",
        "crops": "Cotton, Wheat, Soybean, Chickpea, Sorghum, Safflower."
    }
}

CROP_INFO = {
    "rice": {
        "title": "Paddy (Rice)",
        "optimal_conditions": "Nitrogen-rich clayey/loamy soil with standing water. Thrives in high humidity (>80%), temperatures between 22-30°C, and heavy rainfall (>200 mm).",
        "growth_stages": "1. Nursery Bed Sowing (0-25 days)\n2. Transplanting to Flooded Fields (25-30 days)\n3. Tillering & Stem Elongation (30-60 days)\n4. Panicle Initiation & Heading (60-90 days)\n5. Flowering & Grain Filling (90-115 days)\n6. Ripening & Harvesting (115-130 days)",
        "fertilizer": "Urea (for Nitrogen) split in 3 doses, Single Super Phosphate (SSP) during transplanting, and Muriate of Potash (MOP) for potassium."
    },
    "maize": {
        "title": "Maize (Corn)",
        "optimal_conditions": "Well-drained deep loamy soil. Requires moderate rainfall (60-110 mm), warm days (24-30°C), and moderate nitrogen/phosphorus levels.",
        "growth_stages": "1. Sowing & Germination (0-10 days)\n2. Early Vegetative Growth (V1-V8) (10-35 days)\n3. Rapid Stalk Elongation (V9-VT) (35-55 days)\n4. Tasseling & Pollination (Silking) (55-65 days)\n5. Milk & Dough Kernels (65-85 days)\n6. Dent Stage & Harvest (85-110 days)",
        "fertilizer": "Di-ammonium Phosphate (DAP) at sowing, Urea top-dressing at knee-high stage, and Zinc Sulfate to prevent white bud disease."
    },
    "cotton": {
        "title": "Cotton",
        "optimal_conditions": "Deep black soils or well-drained clayey-loams. Requires warm temperatures (22-32°C), moderate rainfall, and high nitrogen combined with low moisture during boll opening.",
        "growth_stages": "1. Sowing & Seedling Emergence (0-12 days)\n2. Leaf and Canopy Development (12-40 days)\n3. Square (Flower Bud) Appearance (40-65 days)\n4. Flowering & Boll Set (65-90 days)\n5. Boll Maturation & Opening (90-130 days)\n6. Defoliation & Picking/Harvest (130-160 days)",
        "fertilizer": "NPK balanced mix, Urea splits during squaring, and foliar Boron spray to boost boll retention."
    },
    "jute": {
        "title": "Jute",
        "optimal_conditions": "Alluvial, loamy, fertile soil. Needs a hot and humid climate (temperature 24-35°C, humidity 70-90%) and high seasonal rainfall.",
        "growth_stages": "1. Broadcast Sowing & Emergence (0-7 days)\n2. Interculture (Weeding & Thinning) (15-35 days)\n3. Active Stem Elongation (35-90 days)\n4. Flowering stage (Harvest time for fiber quality) (90-120 days)\n5. Retting (Soaking stems in slow water) (120-140 days)\n6. Stripping, Washing, and Fiber Drying (140-145 days)",
        "fertilizer": "Ammonium Sulfate or Urea for leaf growth, Single Super Phosphate (SSP) for root anchoring."
    },
    "coffee": {
        "title": "Coffee",
        "optimal_conditions": "Rich, acidic, organic-heavy, well-drained volcanic/loamy soil on sloped terrain. Prefers cooler highland temperatures (18-24°C) and stable rainfall.",
        "growth_stages": "1. Seed Germination in Nursery (0-60 days)\n2. Planting & Vegetative Growth (3-4 years to first crop)\n3. Seasonal Blossom (triggered by rains)\n4. Pinhead & Green Berry development (1-5 months)\n5. Berry Ripening (Cherry stage - Red color) (6-9 months)\n6. Harvesting & Processing (Pulping & Drying)",
        "fertilizer": "Nitrogen-potassium rich granular fertilizers, Magnesium Sulfate, and agricultural lime (Dolomite) to adjust soil pH."
    },
    "coconut": {
        "title": "Coconut",
        "optimal_conditions": "Coastal sandy or loamy soils. Extremely high humidity (>75%), high rainfall (>180 mm), warm coastal breeze, and high tolerance to soil salinity.",
        "growth_stages": "1. Seednut Germination in Nursery (0-6 months)\n2. Seedling Stage & Transplanting (6-18 months)\n3. Stem/Trunk Initiation & Growth (2-5 years)\n4. Inflorescence (Flowering) Commencement (5-7 years)\n5. Continuous Fruit Set & Nut Development (12 months per nut)\n6. Year-round Harvesting",
        "fertilizer": "Organic compost mixed with Neem cake, Muriate of Potash (MOP) for palm health, and common salt (NaCl) which is highly beneficial for coconut palms."
    },
    "apple": {
        "title": "Apple",
        "optimal_conditions": "Cool temperate climate (requires chilling hours). Deep, well-drained, slightly acidic sandy-loam or loamy soil. High potassium and phosphorus requirement.",
        "growth_stages": "1. Winter Dormancy & Chilling\n2. Bud Break & Green Tip (Spring)\n3. Pink Bud & Blossom (Full Bloom)\n4. Petal Fall & Fruit Set\n5. Mid-summer Fruit Development\n6. Ripening, Coloration & Harvesting (Late Summer/Autumn)",
        "fertilizer": "Calcium Nitrate for cell wall strength, Potassium Nitrate for fruit color and size, and Borax spray during bloom."
    },
    "orange": {
        "title": "Sweet Orange / Citrus",
        "optimal_conditions": "Deep, loamy, well-drained soil with pH 6.0-7.0. Subtropical climate with moderate rainfall and high sunlight exposure.",
        "growth_stages": "1. Shoot Flushes & Bud Initiation\n2. Heavy Spring Blossom\n3. Fruit Set & June Drop (natural thinning)\n4. Fruit Expansion (Summer)\n5. Color Break (Green to Orange transition)\n6. Harvesting & Post-harvest Pruning",
        "fertilizer": "Citrus-specific NPK fertilizer, monthly Zinc Sulfate foliar spray, and Iron Chelates to prevent chlorosis (yellowing of leaves)."
    }
}
