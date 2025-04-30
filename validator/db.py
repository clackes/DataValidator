# validator/db.py
import os
import sqlite3
import json

def save_to_sqlite(self, db_path="./output/validation_data.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS valid_customers (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            birth_date TEXT,
            phone_number TEXT,
            address TEXT,
            city TEXT,
            postal_code TEXT,
            state TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invalid_customers (
            id TEXT,
            name TEXT,
            email TEXT,
            birth_date TEXT,
            phone_number TEXT,
            address TEXT,
            city TEXT,
            postal_code TEXT,
            state TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            errors TEXT
        )
    ''')

    for customer in self.valid_customers:
        cursor.execute('''
            INSERT OR REPLACE INTO valid_customers (
                id, name, email, birth_date, phone_number, address,
                city, postal_code, state, country, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer.id,
            customer.name,
            customer.email,
            str(customer.birth_date),
            customer.phone_number,
            customer.address,
            customer.city,
            customer.postal_code,
            customer.state,
            customer.country,
            customer.latitude,
            customer.longitude
        ))

    for item in self.invalid_customers:
        invalid_entry = item['data']
        errors = item['error']
        cursor.execute('''
            INSERT INTO invalid_customers (
                id, name, email, birth_date, phone_number, address,
                city, postal_code, state, country, latitude, longitude, errors
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            invalid_entry.get("id"),
            invalid_entry.get("name"),
            invalid_entry.get("email"),
            invalid_entry.get("birth_date"),
            invalid_entry.get("phone_number"),
            invalid_entry.get("address"),
            invalid_entry.get("city"),
            invalid_entry.get("postal_code"),
            invalid_entry.get("state"),
            invalid_entry.get("country"),
            invalid_entry.get("latitude"),
            invalid_entry.get("longitude"),
            json.dumps(errors, ensure_ascii=False)
        ))

    conn.commit()
    conn.close()
    print(f"✅ Dati salvati su database SQLite in: {db_path}")
