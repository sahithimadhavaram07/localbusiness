from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import init_db, get_db, close_db
import sqlite3, math, random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'india_biz_secret_2025'

# ── City Specialities & Tourist Places ─────────────────────────────────────────
CITY_INFO = {
    "Hyderabad": {
        "tagline": "City of Pearls & Biryani",
        "specialities": [
            {
                "name": "Hyderabadi Dum Biryani",
                "emoji": "🍛",
                "desc": "Slow-cooked aromatic rice with spiced meat, the crown jewel of Hyderabadi cuisine.",
                "where": [
                    {"place": "Paradise Restaurant", "area": "Secunderabad / MG Road", "tip": "The original since 1953 — always a queue!"},
                    {"place": "Bawarchi", "area": "RTC Cross Roads", "tip": "No-frills, massive portions, loyal locals."},
                ]
            },
            {
                "name": "Irani Chai & Osmania Biscuits",
                "emoji": "☕",
                "desc": "Thick, milky tea from old-city Irani cafés paired with buttery Osmania biscuits.",
                "where": [
                    {"place": "Nimrah Café & Bakery", "area": "Charminar", "tip": "Step back in time — open since 1939."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Charminar",
                "emoji": "🕌",
                "desc": "Iconic 16th-century monument at the heart of the old city. Climb to the top for a panoramic view of the bazaars.",
                "area": "Charminar, Central Hyderabad",
                "tip": "Visit early morning to avoid crowds and great photography light."
            },
            {
                "name": "Golconda Fort",
                "emoji": "🏰",
                "desc": "Magnificent medieval fort famous for its acoustic clap-and-echo feature and sweeping hilltop views.",
                "area": "Ibrahim Bagh, West Hyderabad",
                "tip": "Don't miss the Sound & Light Show in the evenings."
            },
        ]
    },
    "Bengaluru": {
        "tagline": "Silicon Valley of India",
        "specialities": [
            {
                "name": "Masala Dosa",
                "emoji": "🫓",
                "desc": "Crispy rice-lentil crepe stuffed with spiced potato filling — Bangalore's iconic breakfast.",
                "where": [
                    {"place": "CTR (Central Tiffin Room)", "area": "Malleshwaram", "tip": "Open since 1920s — arrive before 9 AM to beat the queue."},
                    {"place": "Vidyarthi Bhavan", "area": "Gandhi Bazaar, Basavanagudi", "tip": "Sunday-only full service; small, legendary, cash only."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Lalbagh Botanical Garden",
                "emoji": "🌿",
                "desc": "A 240-acre garden with a 3,000-year-old rock and a stunning glass house modelled on London's Crystal Palace.",
                "area": "Lalbagh Road, South Bengaluru",
                "tip": "Flower shows happen twice a year during Republic Day and Independence Day."
            },
            {
                "name": "Bangalore Palace",
                "emoji": "🏯",
                "desc": "Tudor-style royal palace built in 1887 with ornate wood carvings, floral motifs, and regal interiors.",
                "area": "Vasanth Nagar, Central Bengaluru",
                "tip": "Audio guides available; photography inside requires an extra fee."
            },
        ]
    },
    "Chennai": {
        "tagline": "Gateway of the South",
        "specialities": [
            {
                "name": "Chettinad Chicken Curry",
                "emoji": "🍗",
                "desc": "Fiery, aromatic curry bursting with rare spices — the pride of Tamil cuisine.",
                "where": [
                    {"place": "Ponnusamy Hotel", "area": "Egmore", "tip": "Legendary no-nonsense spot; lunch hours fill up fast."},
                    {"place": "Anjappar Chettinad", "area": "Anna Nagar", "tip": "Multiple branches; great for large group dining."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Marina Beach",
                "emoji": "🏖️",
                "desc": "One of the world's longest natural urban beaches stretching 13 km along the Bay of Bengal.",
                "area": "Marina, Central Chennai",
                "tip": "Best visited at sunrise or sunset; avoid afternoons in summer."
            },
            {
                "name": "Kapaleeshwarar Temple",
                "emoji": "🛕",
                "desc": "Ancient Dravidian temple dedicated to Lord Shiva, famous for its colourful gopuram (tower).",
                "area": "Mylapore, South Chennai",
                "tip": "Photography of the gopuram from outside is stunning at golden hour."
            },
        ]
    },
    "Mumbai": {
        "tagline": "City of Dreams",
        "specialities": [
            {
                "name": "Vada Pav",
                "emoji": "🍔",
                "desc": "Mumbai's street-food soul — a spiced potato fritter inside a pav bun with chutneys.",
                "where": [
                    {"place": "Ashok Vada Pav", "area": "Dadar Station (West)", "tip": "The original dadar stall — locals swear by it."},
                    {"place": "Anand Vada Pav", "area": "Vile Parle", "tip": "Famous for extra-crispy batter and tangy garlic chutney."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Gateway of India",
                "emoji": "🏛️",
                "desc": "Iconic 1924 arch monument overlooking the Arabian Sea — the symbol of Mumbai.",
                "area": "Apollo Bunder, Colaba",
                "tip": "Take a ferry from here to Elephanta Caves for a half-day trip."
            },
            {
                "name": "Chhatrapati Shivaji Maharaj Terminus",
                "emoji": "🚂",
                "desc": "UNESCO World Heritage Victorian-Gothic railway station — a stunning blend of Indian and European architecture.",
                "area": "Fort, South Mumbai",
                "tip": "Best photographed at dusk when the lights come on; photography permitted outside."
            },
        ]
    },
    "New Delhi": {
        "tagline": "Heart of India",
        "specialities": [
            {
                "name": "Butter Chicken",
                "emoji": "🍲",
                "desc": "Creamy tomato-based chicken curry invented in Delhi — now beloved worldwide.",
                "where": [
                    {"place": "Moti Mahal Delux", "area": "Daryaganj", "tip": "The birthplace of butter chicken since the 1950s."},
                    {"place": "Gulati Restaurant", "area": "Pandara Road, India Gate", "tip": "Classic Mughlai; try the dal makhani alongside."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Red Fort",
                "emoji": "🏰",
                "desc": "Majestic Mughal-era red sandstone fort and UNESCO site; venue of the Prime Minister's Independence Day address.",
                "area": "Chandni Chowk, Old Delhi",
                "tip": "Combine with a street-food walk through Chandni Chowk right outside."
            },
            {
                "name": "Qutub Minar",
                "emoji": "🗼",
                "desc": "World's tallest brick minaret at 73 m, built in 1193 — a masterpiece of Indo-Islamic architecture.",
                "area": "Mehrauli, South Delhi",
                "tip": "The surrounding complex has beautiful ruins perfect for an afternoon stroll."
            },
        ]
    },
    "Kolkata": {
        "tagline": "City of Joy",
        "specialities": [
            {
                "name": "Rosogolla",
                "emoji": "🍮",
                "desc": "Soft spongy cheese balls soaked in light sugar syrup — Kolkata's most iconic sweet.",
                "where": [
                    {"place": "K.C. Das", "area": "Esplanade / multiple branches", "tip": "The family that invented it in 1868; look for the original Esplanade shop."},
                    {"place": "Balaram Mullick & Radharaman Mullick", "area": "Paddapukur Road, Bhowanipore", "tip": "Old-school sweet shop with incredible variety of Bengali mishti."},
                ]
            },
        ],
        "tourist_places": [
            {
                "name": "Victoria Memorial",
                "emoji": "🏛️",
                "desc": "Grand white marble hall built in 1921 — part museum, part majestic garden; a defining Kolkata landmark.",
                "area": "Queens Way, Maidan",
                "tip": "The evening sound-and-light show is spectacular; check timings in advance."
            },
            {
                "name": "Howrah Bridge",
                "emoji": "🌉",
                "desc": "Iconic cantilever bridge over the Hooghly River — one of the busiest bridges in the world.",
                "area": "Howrah, Kolkata",
                "tip": "Best viewed from a boat on the Hooghly River at sunrise or from Mullick Ghat."
            },
        ]
    },
}

def get_city_info(city_name):
    return CITY_INFO.get(city_name, None)
app.teardown_appcontext(close_db)

with app.app_context():
    init_db()

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = math.sin(math.radians(lat2-lat1)/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(math.radians(lng2-lng1)/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

def get_nearby_businesses(lat, lng, radius=10, category=''):
    db = get_db()
    sql = '''SELECT b.*, p.name as place_name, p.lat as place_lat, p.lng as place_lng,
                    c.name as city_name, s.name as state_name
             FROM businesses b JOIN places p ON b.place_id=p.id
             JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id
             WHERE b.status="approved"'''
    rows = db.execute(sql + (' AND b.category=?' if category else ''), (category,) if category else ()).fetchall()
    out = []
    for row in rows:
        blat = row['lat'] if row['lat'] else row['place_lat']
        blng = row['lng'] if row['lng'] else row['place_lng']
        if blat and blng:
            dist = haversine(lat, lng, blat, blng)
            if dist <= radius:
                r = dict(row); r['distance'] = round(dist, 2); out.append(r)
    out.sort(key=lambda x: x['distance'])
    return out

@app.route('/')
def index():
    db = get_db()
    states = db.execute('SELECT * FROM states ORDER BY name').fetchall()
    return render_template('index.html', states=states)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email, password, role = request.form['email'], request.form['password'], request.form['role']
        lat, lng = request.form.get('lat','').strip(), request.form.get('lng','').strip()
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email=? AND password=? AND role=?', (email, password, role)).fetchone()
        if user:
            session.update({'user_id': user['id'], 'user_name': user['name'], 'role': user['role']})
            if role == 'customer' and lat and lng:
                try: session['lat'] = float(lat); session['lng'] = float(lng)
                except: pass
            if role == 'admin': return redirect(url_for('admin_dashboard'))
            if role == 'business_owner': return redirect(url_for('owner_dashboard'))
            return redirect(url_for('customer_home') if session.get('lat') else url_for('set_location'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name, email, password, role = request.form['name'], request.form['email'], request.form['password'], request.form['role']
        phone = request.form.get('phone','')
        db = get_db()
        if db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone():
            flash('Email already registered.', 'error')
        else:
            db.execute('INSERT INTO users (name, email, password, role, phone) VALUES (?,?,?,?,?)', (name, email, password, role, phone))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('index'))

@app.route('/set-location', methods=['GET','POST'])
def set_location():
    if 'user_id' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        lat, lng = request.form.get('lat','').strip(), request.form.get('lng','').strip()
        if lat and lng:
            try: session['lat'] = float(lat); session['lng'] = float(lng); return redirect(url_for('customer_home'))
            except: flash('Invalid location.', 'error')
    return render_template('set_location.html')

@app.route('/home')
def customer_home():
    if 'user_id' not in session: return redirect(url_for('login'))
    if session.get('role') != 'customer': return redirect(url_for('explore'))
    if not session.get('lat'): return redirect(url_for('set_location'))
    lat, lng = session['lat'], session['lng']
    category = request.args.get('category','')
    radius   = float(request.args.get('radius', 10))
    businesses = get_nearby_businesses(lat, lng, radius, category)
    db = get_db()
    categories = db.execute('SELECT DISTINCT category FROM businesses WHERE status="approved" ORDER BY category').fetchall()
    return render_template('customer_home.html', businesses=businesses, lat=lat, lng=lng,
                           radius=radius, category=category, categories=categories)

@app.route('/search')
def search():
    q, uid = request.args.get('q','').strip(), request.args.get('uid','').strip()
    db = get_db(); results = []; searched = False
    if uid:
        searched = True
        biz = db.execute('''SELECT b.*, p.name as place_name, c.name as city_name, s.name as state_name
            FROM businesses b JOIN places p ON b.place_id=p.id JOIN cities c ON p.city_id=c.id
            JOIN states s ON c.state_id=s.id WHERE b.business_uid=? AND b.status="approved"''', (uid.upper(),)).fetchone()
        if biz: results = [dict(biz)]
        else: flash(f'No business found with ID: {uid.upper()}', 'error')
    elif q:
        searched = True
        like = f'%{q}%'
        rows = db.execute('''SELECT b.*, p.name as place_name, c.name as city_name, s.name as state_name
            FROM businesses b JOIN places p ON b.place_id=p.id JOIN cities c ON p.city_id=c.id
            JOIN states s ON c.state_id=s.id WHERE b.status="approved"
            AND (b.name LIKE ? OR b.category LIKE ? OR p.name LIKE ? OR c.name LIKE ? OR b.business_uid LIKE ?)
            ORDER BY b.name LIMIT 60''', (like, like, like, like, like)).fetchall()
        results = [dict(r) for r in rows]
    return render_template('search.html', results=results, q=q, uid=uid, searched=searched)

@app.route('/explore')
def explore():
    db = get_db()
    states = db.execute('SELECT * FROM states ORDER BY name').fetchall()
    return render_template('explore.html', states=states)

@app.route('/nearby')
def nearby():
    lat = request.args.get('lat', type=float); lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 10, type=float); category = request.args.get('category','')
    db = get_db()
    businesses = get_nearby_businesses(lat, lng, radius, category) if lat and lng else []
    categories = db.execute('SELECT DISTINCT category FROM businesses WHERE status="approved" ORDER BY category').fetchall()
    return render_template('nearby.html', businesses=businesses, lat=lat, lng=lng,
                           radius=radius, category=category, categories=categories)

@app.route('/state/<int:state_id>')
def state_page(state_id):
    db = get_db()
    state = db.execute('SELECT * FROM states WHERE id=?', (state_id,)).fetchone()
    if not state: return redirect(url_for('explore'))
    cities = db.execute('''SELECT c.*, COUNT(DISTINCT b.id) as biz_count FROM cities c
        LEFT JOIN places p ON p.city_id=c.id LEFT JOIN businesses b ON b.place_id=p.id AND b.status="approved"
        WHERE c.state_id=? GROUP BY c.id ORDER BY c.name''', (state_id,)).fetchall()
    return render_template('state.html', state=state, cities=cities)

@app.route('/city/<int:city_id>')
def city_page(city_id):
    db = get_db()
    city = db.execute('SELECT c.*, s.name as state_name, s.id as state_id FROM cities c JOIN states s ON c.state_id=s.id WHERE c.id=?', (city_id,)).fetchone()
    if not city: return redirect(url_for('explore'))
    city_info = get_city_info(city['name'])
    if city['name'] == 'Hyderabad':
        zones = db.execute('''SELECT p.zone, COUNT(DISTINCT p.id) as place_count, COUNT(DISTINCT b.id) as biz_count
            FROM places p LEFT JOIN businesses b ON b.place_id=p.id AND b.status="approved"
            WHERE p.city_id=? GROUP BY p.zone''', (city_id,)).fetchall()
        return render_template('city_hyderabad.html', city=city, zones=zones, city_info=city_info)
    places = db.execute('''SELECT p.*, COUNT(DISTINCT b.id) as biz_count FROM places p
        LEFT JOIN businesses b ON b.place_id=p.id AND b.status="approved"
        WHERE p.city_id=? GROUP BY p.id ORDER BY p.name''', (city_id,)).fetchall()
    cats = db.execute('''SELECT b.category, COUNT(*) as cnt FROM businesses b JOIN places p ON b.place_id=p.id
        WHERE p.city_id=? AND b.status="approved" GROUP BY b.category ORDER BY b.category''', (city_id,)).fetchall()
    return render_template('city.html', city=city, places=places, categories=cats, city_info=city_info)

@app.route('/city/<int:city_id>/zone/<zone_name>')
def zone(city_id, zone_name):
    db = get_db()
    city = db.execute('SELECT c.*, s.name as state_name FROM cities c JOIN states s ON c.state_id=s.id WHERE c.id=?', (city_id,)).fetchone()
    places = db.execute('SELECT * FROM places WHERE city_id=? AND zone=?', (city_id, zone_name)).fetchall()
    return render_template('zone.html', city=city, zone=zone_name, places=places)

@app.route('/place/<int:place_id>')
def place(place_id):
    db = get_db()
    p = db.execute('''SELECT p.*, c.name as city_name, c.id as city_id, s.name as state_name, s.id as state_id
        FROM places p JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id WHERE p.id=?''', (place_id,)).fetchone()
    if not p: return redirect(url_for('explore'))
    rows = db.execute('SELECT category, COUNT(*) as count FROM businesses WHERE place_id=? AND status="approved" GROUP BY category ORDER BY category', (place_id,)).fetchall()
    # Load highlights grouped by category
    raw_h = db.execute(
        'SELECT * FROM area_specialities WHERE place_name=? ORDER BY category, id',
        (p['name'],)
    ).fetchall()
    highlights = {}
    cat_order = ['Food', 'Shopping', 'Heritage', 'Experience', 'Market']
    for h in raw_h:
        hd = dict(h)
        cat = hd['category']
        highlights.setdefault(cat, []).append(hd)
    highlights = {k: highlights[k] for k in cat_order if k in highlights}
    return render_template('place.html', place=p,
        categories=[{'name': r['category'], 'count': r['count']} for r in rows],
        highlights=highlights if highlights else None)

@app.route('/place/<int:place_id>/category/<path:category>')
def place_category(place_id, category):
    db = get_db()
    p = db.execute('SELECT p.*, c.name as city_name, c.id as city_id FROM places p JOIN cities c ON p.city_id=c.id WHERE p.id=?', (place_id,)).fetchone()
    if not p: return redirect(url_for('explore'))
    businesses = db.execute('SELECT * FROM businesses WHERE place_id=? AND category=? AND status="approved" ORDER BY name', (place_id, category)).fetchall()
    return render_template('category.html', place=p, category=category, businesses=businesses)

@app.route('/business/<int:biz_id>')
def business_detail(biz_id):
    db = get_db()
    biz = db.execute('''SELECT b.*, p.name as place_name, p.zone, p.id as place_id_val,
        c.name as city_name, c.id as city_id, s.name as state_name FROM businesses b
        JOIN places p ON b.place_id=p.id JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id
        WHERE b.id=?''', (biz_id,)).fetchone()
    if not biz: return redirect(url_for('explore'))
    reviews = db.execute('SELECT r.*, u.name as customer_name FROM reviews r JOIN users u ON r.user_id=u.id WHERE r.business_id=?', (biz_id,)).fetchall()
    return render_template('business_detail.html', biz=biz, reviews=reviews)

@app.route('/book/<int:biz_id>', methods=['GET','POST'])
def book_appointment(biz_id):
    if 'user_id' not in session or session['role'] != 'customer':
        flash('Please login as customer to book.', 'error'); return redirect(url_for('login'))
    db = get_db(); biz = db.execute('SELECT * FROM businesses WHERE id=?', (biz_id,)).fetchone()
    if request.method == 'POST':
        db.execute('INSERT INTO appointments (business_id, customer_id, date, time, notes, status) VALUES (?,?,?,?,?,?)',
            (biz_id, session['user_id'], request.form['date'], request.form['time'], request.form.get('notes',''), 'pending'))
        db.commit(); flash('Appointment booked!', 'success'); return redirect(url_for('business_detail', biz_id=biz_id))
    return render_template('book_appointment.html', biz=biz)

@app.route('/my-appointments')
def my_appointments():
    if 'user_id' not in session: return redirect(url_for('login'))
    db = get_db()
    appts = db.execute('''SELECT a.*, b.name as biz_name, b.category, b.business_uid, p.name as place_name, c.name as city_name
        FROM appointments a JOIN businesses b ON a.business_id=b.id JOIN places p ON b.place_id=p.id
        JOIN cities c ON p.city_id=c.id WHERE a.customer_id=? ORDER BY a.date DESC''', (session['user_id'],)).fetchall()
    return render_template('my_appointments.html', appts=appts)

@app.route('/review/<int:biz_id>', methods=['POST'])
def add_review(biz_id):
    if 'user_id' not in session or session['role'] != 'customer': return redirect(url_for('login'))
    db = get_db()
    db.execute('INSERT INTO reviews (business_id, user_id, rating, comment) VALUES (?,?,?,?)',
        (biz_id, session['user_id'], request.form['rating'], request.form['comment']))
    db.commit(); flash('Review submitted!', 'success'); return redirect(url_for('business_detail', biz_id=biz_id))

@app.route('/owner/dashboard')
def owner_dashboard():
    if session.get('role') != 'business_owner': return redirect(url_for('login'))
    db = get_db()
    bizs = db.execute('''SELECT b.*, p.name as place_name, c.name as city_name FROM businesses b
        JOIN places p ON b.place_id=p.id JOIN cities c ON p.city_id=c.id WHERE b.owner_id=?''', (session['user_id'],)).fetchall()
    appts = db.execute('''SELECT a.*, b.name as biz_name, u.name as customer_name, u.phone as customer_phone
        FROM appointments a JOIN businesses b ON a.business_id=b.id JOIN users u ON a.customer_id=u.id
        WHERE b.owner_id=? ORDER BY a.date DESC''', (session['user_id'],)).fetchall()
    return render_template('owner_dashboard.html', businesses=bizs, appointments=appts)

@app.route('/owner/add-business', methods=['GET','POST'])
def add_business():
    if session.get('role') != 'business_owner': return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        place_id = request.form['place_id']
        sc = db.execute('SELECT s.code FROM states s JOIN cities c ON c.state_id=s.id JOIN places p ON p.city_id=c.id WHERE p.id=?', (place_id,)).fetchone()
        state_code = sc['code'] if sc else 'IN'
        seq = random.randint(90000, 99999)
        uid = f"{state_code}-USR-{seq:05d}"
        while db.execute("SELECT id FROM businesses WHERE business_uid=?", (uid,)).fetchone():
            seq = random.randint(90000, 99999); uid = f"{state_code}-USR-{seq:05d}"
        db.execute('''INSERT INTO businesses (business_uid, owner_id, place_id, name, category, description,
            phone, email, address, lat, lng, timing, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (uid, session['user_id'], place_id, request.form['name'], request.form['category'],
             request.form['description'], request.form['phone'], request.form.get('email',''),
             request.form['address'], request.form.get('lat',0), request.form.get('lng',0),
             request.form['timing'], 'pending'))
        db.commit(); flash(f'Submitted for review! Your Business ID: {uid}', 'success')
        return redirect(url_for('owner_dashboard'))
    states = db.execute('SELECT * FROM states ORDER BY name').fetchall()
    cities = [dict(c) for c in db.execute('SELECT * FROM cities ORDER BY name').fetchall()]
    places = [dict(p) for p in db.execute('''SELECT p.*, c.name as city_name, s.name as state_name
        FROM places p JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id
        ORDER BY s.name, c.name, p.name''').fetchall()]
    CATS = sorted(["Tailors & Boutiques","Tuitions & Coaching","Restaurants & Tiffin","Medical & Pharmacy",
        "Grocery & Kirana","Beauty Salons & Parlours","Mobile & Electronics Repair","Gyms & Fitness",
        "Automobile Services","Hardware & Plumbing","Electrical Services","Catering & Events",
        "Laundry & Dry Cleaning","Printing & Stationery","Nursery & Garden Supplies"])
    return render_template('add_business.html', places=places, states=states, cities=cities, categories=CATS)

@app.route('/owner/appointment/<int:appt_id>/update', methods=['POST'])
def update_appointment(appt_id):
    db = get_db()
    db.execute('UPDATE appointments SET status=? WHERE id=?', (request.form['status'], appt_id))
    db.commit(); return redirect(url_for('owner_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    db = get_db()
    search, uid_s = request.args.get('search','').strip(), request.args.get('uid','').strip()
    page, per_page = int(request.args.get('page',1)), 20
    pending = db.execute('''SELECT b.*, u.name as owner_name, p.name as place_name, c.name as city_name, s.name as state_name
        FROM businesses b JOIN users u ON b.owner_id=u.id JOIN places p ON b.place_id=p.id
        JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id
        WHERE b.status="pending" ORDER BY b.created_at DESC''').fetchall()
    base = '''SELECT b.*, u.name as owner_name, p.name as place_name, c.name as city_name, s.name as state_name
        FROM businesses b JOIN users u ON b.owner_id=u.id JOIN places p ON b.place_id=p.id
        JOIN cities c ON p.city_id=c.id JOIN states s ON c.state_id=s.id WHERE b.status="approved"'''
    params = []
    if uid_s: base += ' AND b.business_uid=?'; params.append(uid_s.upper())
    elif search:
        like = f'%{search}%'; base += ' AND (b.name LIKE ? OR b.category LIKE ? OR p.name LIKE ? OR c.name LIKE ? OR s.name LIKE ? OR b.business_uid LIKE ?)'; params += [like]*6
    total = db.execute(base.replace('b.*, u.name as owner_name, p.name as place_name, c.name as city_name, s.name as state_name','COUNT(*)'), params).fetchone()[0]
    approved = db.execute(base + ' ORDER BY b.created_at DESC LIMIT ? OFFSET ?', params + [per_page, (page-1)*per_page]).fetchall()
    users = db.execute('SELECT * FROM users WHERE role != "admin"').fetchall()
    stats = {'total_users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
             'total_businesses': db.execute('SELECT COUNT(*) FROM businesses').fetchone()[0],
             'total_appointments': db.execute('SELECT COUNT(*) FROM appointments').fetchone()[0],
             'total_states': db.execute('SELECT COUNT(*) FROM states').fetchone()[0],
             'total_cities': db.execute('SELECT COUNT(*) FROM cities').fetchone()[0],
             'pending_count': len(pending)}
    return render_template('admin_dashboard.html', pending=pending, approved=approved, users=users,
        stats=stats, page=page, total_pages=max(1,(total+per_page-1)//per_page),
        search=search, uid_search=uid_s, total_approved=total)

@app.route('/admin/verify/<int:biz_id>/<action>')
def verify_business(biz_id, action):
    if session.get('role') != 'admin': return redirect(url_for('login'))
    db = get_db()
    db.execute('UPDATE businesses SET status=? WHERE id=?', ('approved' if action=='approve' else 'rejected', biz_id))
    db.commit(); flash(f'Business {"approved" if action=="approve" else "rejected"}!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/cities/<int:state_id>')
def api_cities(state_id):
    db = get_db()
    return jsonify([dict(c) for c in db.execute('SELECT * FROM cities WHERE state_id=? ORDER BY name', (state_id,)).fetchall()])

@app.route('/api/places/<int:city_id>')
def api_places(city_id):
    db = get_db()
    return jsonify([dict(p) for p in db.execute('SELECT * FROM places WHERE city_id=? ORDER BY name', (city_id,)).fetchall()])

if __name__ == '__main__':
    app.run(debug=True)
