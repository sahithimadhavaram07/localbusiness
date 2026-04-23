import sqlite3
import random
import uuid
import math

DATABASE = 'india_biz.db'

# ── 15 CATEGORIES (Hyderabad full set) ─────────────────────────────────────────
CATEGORIES = [
    "Tailors & Boutiques",
    "Tuitions & Coaching",
    "Restaurants & Tiffin",
    "Medical & Pharmacy",
    "Grocery & Kirana",
    "Beauty Salons & Parlours",
    "Mobile & Electronics Repair",
    "Gyms & Fitness",
    "Automobile Services",
    "Hardware & Plumbing",
    "Electrical Services",
    "Catering & Events",
    "Laundry & Dry Cleaning",
    "Printing & Stationery",
    "Nursery & Garden Supplies",
]

# ── 10 CATEGORIES for non-Hyderabad cities ─────────────────────────────────────
CATEGORIES_OTHER = [
    "Restaurants & Tiffin",
    "Medical & Pharmacy",
    "Grocery & Kirana",
    "Beauty Salons & Parlours",
    "Mobile & Electronics Repair",
    "Automobile Services",
    "Gyms & Fitness",
    "Tailors & Boutiques",
    "Tuitions & Coaching",
    "Catering & Events",
]

TIMINGS = [
    "9:00 AM – 9:00 PM", "8:00 AM – 8:00 PM", "10:00 AM – 10:00 PM",
    "7:00 AM – 7:00 PM", "9:00 AM – 6:00 PM", "Open 24 Hours", "8:00 AM – 10:00 PM",
]

PHONES = [
    "9876543210","9123456780","9988776655","9654321098","9871234560",
    "9000112233","9811223344","9776655443","9654445566","9832100987",
    "8876543210","8123456780","8988776655","8654321098","8871234560",
    "7876543210","7123456780","7988776655","7654321098","7871234560",
]

DESCRIPTIONS = {
    "Tailors & Boutiques": "Expert tailoring and stitching services with premium fabric collections. Specialising in traditional and modern wear.",
    "Tuitions & Coaching": "Professional coaching by experienced faculty. Personalized attention for every student to achieve academic excellence.",
    "Restaurants & Tiffin": "Serving authentic local cuisine and fresh home-style tiffin. Hygienic, tasty, and affordable meals daily.",
    "Medical & Pharmacy": "Licensed pharmacy and clinic offering quality medicines, health products, and professional medical consultation.",
    "Grocery & Kirana": "Your neighbourhood grocery store stocking fresh produce, daily essentials, and household items at best prices.",
    "Beauty Salons & Parlours": "Professional beauty treatments including hair styling, skincare, bridal makeup, and grooming services.",
    "Mobile & Electronics Repair": "Fast and reliable repair services for all mobile brands, laptops, and electronics with genuine spare parts.",
    "Gyms & Fitness": "State-of-the-art fitness equipment and expert trainers helping you achieve your health and fitness goals.",
    "Automobile Services": "Comprehensive vehicle servicing, repairs, and maintenance for all two-wheelers and four-wheelers.",
    "Hardware & Plumbing": "Complete hardware, plumbing, and sanitary solutions for residential and commercial construction needs.",
    "Electrical Services": "Certified electricians providing wiring, repairs, installations, and all electrical work for homes and offices.",
    "Catering & Events": "End-to-end event planning and catering for weddings, parties, corporate events, and all celebrations.",
    "Laundry & Dry Cleaning": "Professional laundry and dry cleaning services with quick turnaround, home pickup and delivery available.",
    "Printing & Stationery": "Quality printing services for banners, visiting cards, invitations, flex boards, and all stationery needs.",
    "Nursery & Garden Supplies": "Wide variety of indoor and outdoor plants, seeds, fertilizers, and garden accessories for green enthusiasts.",
}

BIZ_TEMPLATES = {
    "Tailors & Boutiques": [
        "{place} Stitch Hub", "Royal {place} Tailors", "{place} Fashion Boutique",
        "Nizam Tailors {place}", "{place} Silk Boutique", "Traditional {place} Weavers",
        "{place} Designer Wear", "Bridal {place} Studio", "{place} Kurta House",
        "Heritage Stitch {place}", "{place} Alteration Centre", "Star Tailors {place}",
        "{place} Embroidery Works", "Lakshmi Tailors {place}", "{place} Thread & Needle",
        "Elite Boutique {place}", "{place} Cotton House", "Saree Blouse {place}",
        "Classic Tailors {place}", "{place} Kids Wear Studio",
    ],
    "Tuitions & Coaching": [
        "{place} Bright Minds Academy", "Excel Coaching {place}", "{place} IIT Prep Centre",
        "Scholar Hub {place}", "{place} NEET Academy", "Talent Grove {place}",
        "{place} Maths Tuition", "Smart Kids {place}", "{place} English Academy",
        "Top Rank Coaching {place}", "{place} Science Tuition", "Genius Academy {place}",
        "{place} Primary Coaching", "Career Launcher {place}", "{place} SSC Coaching",
        "Narayana Tutorials {place}", "{place} Drawing Classes", "SR Coaching {place}",
        "{place} Commerce Tuition", "Speed Maths {place}",
    ],
    "Restaurants & Tiffin": [
        "{place} Biryani House", "Tiffin Box {place}", "{place} Dosa Corner",
        "Thali House {place}", "{place} Meals Home", "Dum Biryani {place}",
        "{place} Breakfast Point", "Shahi Dining {place}", "{place} Idly Center",
        "Local Tiffins {place}", "{place} Veg Meals", "Pesarattu House {place}",
        "{place} Snack Point", "Cafe Corner {place}", "{place} South Indian Tiffin",
        "Royal Biryani {place}", "{place} Snacks Corner", "Annapurna Meals {place}",
        "{place} Fast Food", "Nawab Kitchen {place}",
    ],
    "Medical & Pharmacy": [
        "{place} Medical Hall", "Apollo Pharmacy {place}", "{place} Health Store",
        "Lifeline Pharmacy {place}", "{place} Clinic & Medical", "MedPlus {place}",
        "{place} Diagnostic Centre", "Care Pharmacy {place}", "{place} General Clinic",
        "Wellness Medical {place}", "{place} Child Clinic", "24hr Pharmacy {place}",
        "{place} Ortho Clinic", "Family Health {place}", "{place} Skin Clinic",
        "Prime Medical {place}", "{place} Eye Clinic", "Sai Pharmacy {place}",
        "{place} ENT Clinic", "Healthpoint {place}",
    ],
    "Grocery & Kirana": [
        "{place} Kirana Stores", "Daily Needs {place}", "{place} Supermart",
        "Fresh Mart {place}", "{place} General Stores", "Big Basket Partner {place}",
        "{place} Organic Store", "Sri Lakshmi Stores {place}", "{place} Provision Store",
        "Ganesh Kirana {place}", "{place} Mini Supermarket", "Ramesh Stores {place}",
        "{place} Grocery Hub", "Morning Fresh {place}", "{place} Staples Store",
        "Value Mart {place}", "{place} Vegetables & Grocery", "Apna Bazar {place}",
        "{place} Food Basket", "Home Needs {place}",
    ],
    "Beauty Salons & Parlours": [
        "{place} Beauty Parlour", "Glam Studio {place}", "{place} Ladies Salon",
        "Naturals Salon {place}", "{place} Gents Parlour", "Jawed Habib {place}",
        "{place} Spa & Salon", "Looks Parlour {place}", "{place} Bridal Makeup Studio",
        "Silk Salon {place}", "{place} Hair Studio", "Pretty Looks {place}",
        "{place} Unisex Salon", "Beauty Zone {place}", "{place} Nail Art Studio",
        "Lotus Parlour {place}", "{place} Threading Centre", "Style Hub {place}",
        "{place} Skin Care Clinic", "Glamour Touch {place}",
    ],
    "Mobile & Electronics Repair": [
        "{place} Mobile Repair", "iCare Service {place}", "{place} Electronics Hub",
        "Smart Fix {place}", "{place} Phone Doctor", "Gadget Care {place}",
        "{place} Laptop Service", "Mobile World {place}", "{place} Screen Repair",
        "TechFix {place}", "{place} Samsung Service", "Mobile Planet {place}",
        "{place} TV Repair", "Digital Care {place}", "{place} Charger & Accessories",
        "Redmi Service {place}", "{place} Apple Repair", "Electro Hub {place}",
        "{place} CCTV Install", "Fast Repair {place}",
    ],
    "Gyms & Fitness": [
        "{place} Fitness Centre", "Iron Body Gym {place}", "{place} CrossFit Studio",
        "Gold Gym {place}", "{place} Yoga Studio", "Power House Gym {place}",
        "{place} Zumba Classes", "Muscle Factory {place}", "{place} Ladies Gym",
        "Fit Zone {place}", "{place} Aerobics Centre", "Body Temple {place}",
        "{place} Martial Arts", "Strength Lab {place}", "{place} MMA Academy",
        "Flex Fitness {place}", "{place} Dance Fitness", "Transform Gym {place}",
        "{place} Pilates Studio", "Active Life {place}",
    ],
    "Automobile Services": [
        "{place} Car Service Centre", "Two Wheeler Service {place}", "{place} Auto Garage",
        "Speed Auto {place}", "{place} Tyre Puncture", "Quick Lube {place}",
        "{place} Bike Wash", "Star Motors {place}", "{place} Denting & Painting",
        "Royal Garage {place}", "{place} Battery Service", "Auto Care {place}",
        "{place} Car Wash", "Mechanic Hub {place}", "{place} Spare Parts",
        "Bike Zone {place}", "{place} AC Service Cars", "Roadside Motors {place}",
        "{place} Truck Service", "Fast Fix Auto {place}",
    ],
    "Hardware & Plumbing": [
        "{place} Hardware Store", "Plumbing Solutions {place}", "{place} Pipe Centre",
        "Build Mart {place}", "{place} Construction Materials", "Sri Hardware {place}",
        "{place} Sanitary Store", "Fix It {place}", "{place} Tools & Equipment",
        "Home Fix {place}", "{place} Paint & Hardware", "Raju Hardware {place}",
        "{place} PVC Pipes", "All Build {place}", "{place} Granite & Tiles",
        "Pro Plumb {place}", "{place} Cement Store", "Iron Works {place}",
        "{place} Door & Window", "Master Build {place}",
    ],
    "Electrical Services": [
        "{place} Electrical Works", "Power Fix {place}", "{place} Wiring Services",
        "Bright Electrical {place}", "{place} Inverter Service", "Switch Gear {place}",
        "{place} Fan & Light", "Volt Care {place}", "{place} Solar Panels",
        "Electrician Hub {place}", "{place} MCB & Panel", "Current Fix {place}",
        "{place} Generator Service", "Plug Point {place}", "{place} AC Wiring",
        "Circuit Masters {place}", "{place} LED Lights Store", "Shock Free {place}",
        "{place} Electric Board", "Power House {place}",
    ],
    "Catering & Events": [
        "{place} Catering Services", "Shadi Caterers {place}", "{place} Event Planners",
        "Royal Feast {place}", "{place} Wedding Caterers", "Grand Events {place}",
        "{place} Tiffin Catering", "Party Hub {place}", "{place} Birthday Planners",
        "Star Caterers {place}", "{place} Corporate Events", "Dream Events {place}",
        "{place} Mandap Decorators", "Nawab Caterers {place}", "{place} Tent House",
        "Food Court {place}", "{place} Stage & Lighting", "Celebrations {place}",
        "{place} Cook on Hire", "Lucky Events {place}",
    ],
    "Laundry & Dry Cleaning": [
        "{place} Laundry Hub", "Wash & Fold {place}", "{place} Dry Cleaners",
        "CleanX {place}", "{place} Steam Press", "Spotless Laundry {place}",
        "{place} Washman", "Quick Wash {place}", "{place} Ironing Centre",
        "Fresh Clothes {place}", "{place} Fabric Care", "Rinse & Shine {place}",
        "{place} Dhobhi Ghat", "White Wash {place}", "{place} Linen Service",
        "Express Laundry {place}", "{place} Sofa Dry Clean", "Soft Touch {place}",
        "{place} Curtain Cleaning", "Urban Laundry {place}",
    ],
    "Printing & Stationery": [
        "{place} Printing Press", "Copy & Print {place}", "{place} Stationery Hub",
        "Digital Print {place}", "{place} Photo Studio", "Xerox Centre {place}",
        "{place} ID Card Print", "Smart Print {place}", "{place} Visiting Cards",
        "Flex Print {place}", "{place} Book Binding", "Print Zone {place}",
        "{place} Sticker Print", "Banner Works {place}", "{place} Office Supplies",
        "Colour Print {place}", "{place} Notebook Store", "Quick Print {place}",
        "{place} Invitation Cards", "Print World {place}",
    ],
    "Nursery & Garden Supplies": [
        "{place} Plant Nursery", "Green Thumb {place}", "{place} Garden Centre",
        "Flower World {place}", "{place} Terrace Garden", "Nature Hub {place}",
        "{place} Seed Store", "Bloom Garden {place}", "{place} Bonsai Centre",
        "Leafy Green {place}", "{place} Fertilizer Store", "Garden Tools {place}",
        "{place} Organic Manure", "Plant Paradise {place}", "{place} Cactus Corner",
        "Grow Well {place}", "{place} Exotic Plants", "Urban Garden {place}",
        "{place} Indoor Plants", "Greenery World {place}",
    ],
}

# ── INDIA STATES & CITIES ──────────────────────────────────────────────────────
# Format: state_name, code, capital, region, [(city_name, lat, lng, is_major), ...]
INDIA_DATA = [
    ("Andhra Pradesh", "AP", "Amaravati", "South", [
        ("Visakhapatnam", 17.6868, 83.2185, 1),
        ("Vijayawada", 16.5062, 80.6480, 1),
        ("Tirupati", 13.6288, 79.4192, 0),
        ("Guntur", 16.3067, 80.4365, 0),
    ]),
    ("Telangana", "TS", "Hyderabad", "South", [
        ("Hyderabad", 17.3850, 78.4867, 1),
        ("Warangal", 17.9689, 79.5941, 0),
        ("Nizamabad", 18.6726, 78.0941, 0),
    ]),
    ("Karnataka", "KA", "Bengaluru", "South", [
        ("Bengaluru", 12.9716, 77.5946, 1),
        ("Mysuru", 12.2958, 76.6394, 1),
        ("Mangaluru", 12.9141, 74.8560, 0),
        ("Hubballi", 15.3647, 75.1240, 0),
    ]),
    ("Tamil Nadu", "TN", "Chennai", "South", [
        ("Chennai", 13.0827, 80.2707, 1),
        ("Coimbatore", 11.0168, 76.9558, 1),
        ("Madurai", 9.9252, 78.1198, 0),
        ("Tiruchirappalli", 10.7905, 78.7047, 0),
    ]),
    ("Kerala", "KL", "Thiruvananthapuram", "South", [
        ("Thiruvananthapuram", 8.5241, 76.9366, 1),
        ("Kochi", 9.9312, 76.2673, 1),
        ("Kozhikode", 11.2588, 75.7804, 0),
    ]),
    ("Maharashtra", "MH", "Mumbai", "West", [
        ("Mumbai", 19.0760, 72.8777, 1),
        ("Pune", 18.5204, 73.8567, 1),
        ("Nagpur", 21.1458, 79.0882, 1),
        ("Nashik", 19.9975, 73.7898, 0),
    ]),
    ("Gujarat", "GJ", "Gandhinagar", "West", [
        ("Ahmedabad", 23.0225, 72.5714, 1),
        ("Surat", 21.1702, 72.8311, 1),
        ("Vadodara", 22.3072, 73.1812, 0),
        ("Rajkot", 22.3039, 70.8022, 0),
    ]),
    ("Rajasthan", "RJ", "Jaipur", "North", [
        ("Jaipur", 26.9124, 75.7873, 1),
        ("Jodhpur", 26.2389, 73.0243, 0),
        ("Udaipur", 24.5854, 73.7125, 0),
        ("Kota", 25.2138, 75.8648, 0),
    ]),
    ("Uttar Pradesh", "UP", "Lucknow", "North", [
        ("Lucknow", 26.8467, 80.9462, 1),
        ("Kanpur", 26.4499, 80.3319, 1),
        ("Agra", 27.1767, 78.0081, 1),
        ("Varanasi", 25.3176, 82.9739, 0),
        ("Noida", 28.5355, 77.3910, 1),
    ]),
    ("Delhi", "DL", "New Delhi", "North", [
        ("New Delhi", 28.6139, 77.2090, 1),
        ("Dwarka", 28.5921, 77.0460, 0),
        ("Rohini", 28.7041, 77.1025, 0),
        ("Lajpat Nagar", 28.5657, 77.2435, 0),
    ]),
    ("Haryana", "HR", "Chandigarh", "North", [
        ("Gurugram", 28.4595, 77.0266, 1),
        ("Faridabad", 28.4089, 77.3178, 0),
        ("Ambala", 30.3782, 76.7767, 0),
    ]),
    ("Punjab", "PB", "Chandigarh", "North", [
        ("Chandigarh", 30.7333, 76.7794, 1),
        ("Amritsar", 31.6340, 74.8723, 1),
        ("Ludhiana", 30.9010, 75.8573, 0),
    ]),
    ("Madhya Pradesh", "MP", "Bhopal", "Central", [
        ("Bhopal", 23.2599, 77.4126, 1),
        ("Indore", 22.7196, 75.8577, 1),
        ("Jabalpur", 23.1815, 79.9864, 0),
        ("Gwalior", 26.2183, 78.1828, 0),
    ]),
    ("Odisha", "OD", "Bhubaneswar", "East", [
        ("Bhubaneswar", 20.2961, 85.8245, 1),
        ("Cuttack", 20.4625, 85.8828, 0),
        ("Rourkela", 22.2604, 84.8536, 0),
    ]),
    ("West Bengal", "WB", "Kolkata", "East", [
        ("Kolkata", 22.5726, 88.3639, 1),
        ("Howrah", 22.5958, 88.2636, 0),
        ("Siliguri", 26.7271, 88.3953, 0),
        ("Durgapur", 23.5204, 87.3119, 0),
    ]),
    ("Bihar", "BR", "Patna", "East", [
        ("Patna", 25.5941, 85.1376, 1),
        ("Gaya", 24.7955, 85.0002, 0),
        ("Muzaffarpur", 26.1209, 85.3647, 0),
    ]),
    ("Assam", "AS", "Dispur", "Northeast", [
        ("Guwahati", 26.1445, 91.7362, 1),
        ("Dibrugarh", 27.4728, 94.9120, 0),
    ]),
    ("Himachal Pradesh", "HP", "Shimla", "North", [
        ("Shimla", 31.1048, 77.1734, 1),
        ("Dharamshala", 32.2190, 76.3234, 0),
    ]),
    ("Goa", "GA", "Panaji", "West", [
        ("Panaji", 15.4909, 73.8278, 1),
        ("Margao", 15.2832, 73.9862, 0),
    ]),
    ("Jammu & Kashmir", "JK", "Srinagar", "North", [
        ("Srinagar", 34.0837, 74.7973, 1),
        ("Jammu", 32.7266, 74.8570, 0),
    ]),
    ("Jharkhand", "JH", "Ranchi", "East", [
        ("Ranchi", 23.3441, 85.3096, 1),
        ("Jamshedpur", 22.8046, 86.2029, 0),
    ]),
    ("Chhattisgarh", "CG", "Raipur", "Central", [
        ("Raipur", 21.2514, 81.6296, 1),
        ("Bilaspur", 22.0796, 82.1391, 0),
    ]),
    ("Uttarakhand", "UK", "Dehradun", "North", [
        ("Dehradun", 30.3165, 78.0322, 1),
        ("Haridwar", 29.9457, 78.1642, 0),
    ]),
]

# ── HYDERABAD SPECIFIC: FULL 20-PLACES CONFIG ──────────────────────────────────
HYD_PLACES = [
    # (name, zone, famous_for, description, lat, lng)
    ("Secunderabad",  "North",  "Twin city, Railway Hub, Clock Tower", "Major commercial and railway hub", 17.4399, 78.4983),
    ("Trimulgherry",  "North",  "Cantonment Area, Old Churches",       "Historic military cantonment",     17.4573, 78.5063),
    ("Malkajgiri",    "North",  "Malkajgiri Lake, Temples",            "Residential suburb with scenic lake",17.4564, 78.5311),
    ("Alwal",         "North",  "Alwal Lake, Defense establishments",  "Quiet suburb near defense area",   17.4875, 78.5131),
    ("Mehdipatnam",   "South",  "Bustling markets, Transport hub",     "Major commercial transport junction",17.3880, 78.4369),
    ("Tolichowki",    "South",  "IT Hub, Film industry",               "Mix of IT offices and film industry",17.3990, 78.4200),
    ("Attapur",       "South",  "Residential Area, Lakes",             "Peaceful residential locality",    17.3620, 78.4250),
    ("Rajendranagar", "South",  "IARI Campus, Green spaces",           "Agricultural research hub",        17.3262, 78.4355),
    ("LB Nagar",      "East",   "Commercial Hub, Metro station",       "Eastern commercial center",        17.3463, 78.5522),
    ("Uppal",         "East",   "Uppal Stadium, IT offices",           "Known for cricket stadium and IT", 17.4063, 78.5592),
    ("Hayathnagar",   "East",   "Hayathnagar Lake, Open spaces",       "Growing suburb with lakes",        17.3255, 78.5942),
    ("Ghatkesar",     "East",   "Ghatkesar Lake, Pharma industries",   "Pharmaceutical hub",               17.4457, 78.6930),
    ("Kukatpally",    "West",   "KPHB Colony, Shopping Malls",         "Largest residential locality",     17.4947, 78.3996),
    ("Miyapur",       "West",   "Metro terminus, Residential hub",     "Western metro terminus",           17.4967, 78.3580),
    ("Kondapur",      "West",   "Cyber City, Tech Parks",              "Heart of Hyderabad IT corridor",   17.4700, 78.3543),
    ("Manikonda",     "West",   "Golconda Fort view, IT Hub",          "Emerging tech hub",                17.3990, 78.3887),
    ("Charminar",     "Central","Charminar Monument, Laad Bazaar",     "Historic heart of old Hyderabad",  17.3616, 78.4747),
    ("Banjara Hills", "Central","High-end restaurants, Embassies",     "Upscale neighbourhood",            17.4150, 78.4470),
    ("Jubilee Hills", "Central","Film Industry, Fine dining",          "Celebrity residential area",       17.4239, 78.4083),
    ("Abids",         "Central","Book market, Shopping",               "Historic commercial district",     17.3841, 78.4758),
]

def jitter(lat, lng, scale=0.008):
    return round(lat + random.uniform(-scale, scale), 6), round(lng + random.uniform(-scale, scale), 6)

def make_uid(state_code, city_abbr, seq):
    return f"{state_code}-{city_abbr[:3].upper()}-{seq:05d}"

def seed():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    print("🌱 Starting India-wide seed...")

    # ── Create owner users ─────────────────────────────────────────────────────
    owner_ids = []
    for i in range(1, 101):
        email = f"owner{i}@indiabiz.com"
        existing = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            owner_ids.append(existing['id'])
        else:
            db.execute(
                "INSERT INTO users (name, email, password, role, phone) VALUES (?,?,?,?,?)",
                (f"Owner {i}", email, "owner123", "business_owner", PHONES[i % len(PHONES)])
            )
            db.commit()
            owner_ids.append(db.execute("SELECT last_insert_rowid()").fetchone()[0])
    print(f"  ✅ {len(owner_ids)} owner accounts ready")

    # ── Clear old seed businesses ──────────────────────────────────────────────
    db.execute("DELETE FROM businesses WHERE owner_id IN (SELECT id FROM users WHERE email LIKE 'owner%@indiabiz.com')")
    db.execute("DELETE FROM places")
    db.execute("DELETE FROM cities")
    db.execute("DELETE FROM states")
    db.commit()

    biz_seq = 1
    owner_idx = 0
    total_biz = 0

    for (state_name, state_code, capital, region, cities_list) in INDIA_DATA:
        # Insert state
        db.execute(
            "INSERT OR IGNORE INTO states (name, code, capital, region) VALUES (?,?,?,?)",
            (state_name, state_code, capital, region)
        )
        db.commit()
        state_id = db.execute("SELECT id FROM states WHERE code=?", (state_code,)).fetchone()['id']

        for (city_name, city_lat, city_lng, is_major) in cities_list:
            db.execute(
                "INSERT OR IGNORE INTO cities (state_id, name, lat, lng, is_major) VALUES (?,?,?,?,?)",
                (state_id, city_name, city_lat, city_lng, is_major)
            )
            db.commit()
            city_id = db.execute(
                "SELECT id FROM cities WHERE state_id=? AND name=?", (state_id, city_name)
            ).fetchone()['id']

            is_hyderabad = (city_name == "Hyderabad")

            if is_hyderabad:
                # ── Seed all 20 Hyderabad places with all 15 categories × 20 businesses ──
                for (pname, zone, famous, desc, plat, plng) in HYD_PLACES:
                    db.execute(
                        "INSERT INTO places (city_id, name, zone, famous_for, description, lat, lng) VALUES (?,?,?,?,?,?,?)",
                        (city_id, pname, zone, famous, desc, plat, plng)
                    )
                    db.commit()
                    place_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

                    place_pending = 0
                    for cat_idx, category in enumerate(CATEGORIES):
                        templates = BIZ_TEMPLATES[category]
                        for biz_idx in range(20):
                            biz_name = templates[biz_idx % len(templates)].replace("{place}", pname)
                            if cat_idx >= 13 and biz_idx >= 17 and place_pending < 8:
                                status = "pending"
                                place_pending += 1
                            else:
                                status = "approved"

                            lat, lng = jitter(plat, plng)
                            uid = make_uid(state_code, pname, biz_seq)
                            biz_seq += 1
                            owner_id = owner_ids[owner_idx % len(owner_ids)]
                            owner_idx += 1
                            phone = PHONES[biz_idx % len(PHONES)]
                            email = f"biz{biz_seq}@{pname.lower().replace(' ', '')}.com"
                            address = f"{biz_name}, {pname}, Hyderabad"
                            timing = TIMINGS[biz_idx % len(TIMINGS)]
                            db.execute(
                                '''INSERT INTO businesses
                                   (business_uid, owner_id, place_id, name, category, description, phone, email, address, lat, lng, timing, status)
                                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                (uid, owner_id, place_id, biz_name, category, DESCRIPTIONS[category],
                                 phone, email, address, lat, lng, timing, status)
                            )
                            total_biz += 1
                    db.commit()
                print(f"  ✅ Hyderabad — 20 places × 15 categories × 20 businesses seeded")

            else:
                # ── Other cities: 2 places, 10 categories, 2 businesses each ──
                # Generic place names: City Centre + New Town / Suburb
                place_configs = [
                    (f"{city_name} Central", city_lat + 0.01, city_lng + 0.01),
                    (f"{city_name} New Town", city_lat - 0.01, city_lng - 0.01),
                ]
                for (pname, plat, plng) in place_configs:
                    db.execute(
                        "INSERT INTO places (city_id, name, zone, famous_for, description, lat, lng) VALUES (?,?,?,?,?,?,?)",
                        (city_id, pname, "Central", f"Business hub of {city_name}", f"Key commercial area in {city_name}", plat, plng)
                    )
                    db.commit()
                    place_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

                    for cat_idx, category in enumerate(CATEGORIES_OTHER):
                        templates = BIZ_TEMPLATES[category]
                        for biz_idx in range(2):
                            biz_name = templates[biz_idx % len(templates)].replace("{place}", city_name)
                            lat, lng = jitter(plat, plng, 0.005)
                            uid = make_uid(state_code, city_name, biz_seq)
                            biz_seq += 1
                            owner_id = owner_ids[owner_idx % len(owner_ids)]
                            owner_idx += 1
                            phone = PHONES[biz_seq % len(PHONES)]
                            email = f"biz{biz_seq}@{city_name.lower().replace(' ', '')}.com"
                            address = f"{biz_name}, {pname}, {city_name}"
                            timing = TIMINGS[biz_seq % len(TIMINGS)]
                            db.execute(
                                '''INSERT INTO businesses
                                   (business_uid, owner_id, place_id, name, category, description, phone, email, address, lat, lng, timing, status)
                                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                (uid, owner_id, place_id, biz_name, category, DESCRIPTIONS[category],
                                 phone, email, address, lat, lng, timing, "approved")
                            )
                            total_biz += 1
                    db.commit()

    print(f"\n🎉 India-wide seeding complete!")
    print(f"   Total businesses : {total_biz}")
    print(f"   States covered   : {len(INDIA_DATA)}")
    db.close()

if __name__ == "__main__":
    seed()
