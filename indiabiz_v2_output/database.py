import sqlite3
from flask import g
import os

DATABASE = 'india_biz.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ("customer","business_owner","admin")),
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            code TEXT UNIQUE NOT NULL,
            capital TEXT,
            region TEXT
        );

        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            is_major INTEGER DEFAULT 0,
            FOREIGN KEY (state_id) REFERENCES states(id),
            UNIQUE(state_id, name)
        );

        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            zone TEXT,
            famous_for TEXT,
            description TEXT,
            lat REAL DEFAULT 17.3850,
            lng REAL DEFAULT 78.4867,
            image_url TEXT,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        );

        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_uid TEXT UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            place_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            lat REAL,
            lng REAL,
            timing TEXT,
            status TEXT DEFAULT "pending" CHECK(status IN ("pending","approved","rejected")),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id),
            FOREIGN KEY (place_id) REFERENCES places(id)
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            notes TEXT,
            status TEXT DEFAULT "pending" CHECK(status IN ("pending","confirmed","cancelled","completed")),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses(id),
            FOREIGN KEY (customer_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Seed admin
    existing = db.execute("SELECT id FROM users WHERE email='admin@indiabiz.com'").fetchone()
    if not existing:
        db.execute(
            "INSERT INTO users (name,email,password,role,phone) VALUES (?,?,?,?,?)",
            ('Admin', 'admin@indiabiz.com', 'admin123', 'admin', '9000000000')
        )
        db.commit()

    db.commit()
    db.close()
