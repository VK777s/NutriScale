# File: database_setup.py
import sqlite3
from datetime import date

def create_database():
    """
    Creates or updates the database and tables for the NutriScale app.
    """
    try:
        conn = sqlite3.connect('nutriscale.db')
        c = conn.cursor()

        # 1. Users Table (UPDATED)
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE, 
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            height_cm REAL NOT NULL,
            current_weight_kg REAL NOT NULL,
            target_weight_kg REAL NOT NULL,
            activity_level TEXT NOT NULL,
            bmr REAL,
            tdee REAL,
            calorie_target REAL
        )
        ''')

        # 2. Food Database Table (Unchanged)
        c.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            calories_per_100g REAL NOT NULL,
            protein_per_100g REAL NOT NULL,
            carbs_per_100g REAL NOT NULL,
            fats_per_100g REAL NOT NULL
        )
        ''')

        # 3. Meal Logs Table (Unchanged)
        c.execute('''
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            quantity_grams REAL NOT NULL,
            log_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (food_id) REFERENCES food_items (id)
        )
        ''')
        
        # 4. Weight Logs Table (Unchanged)
        c.execute('''
        CREATE TABLE IF NOT EXISTS weight_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight_kg REAL NOT NULL,
            log_date DATE NOT NULL,
            UNIQUE(user_id, log_date),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Add sample food items (Unchanged)
        sample_foods = [
            ('Chicken Breast', 165, 31, 0, 3.6),
            ('Brown Rice (Cooked)', 112, 2.6, 23.5, 0.9),
            ('Broccoli', 55, 3.7, 11.2, 0.6),
            ('Olive Oil', 884, 0, 0, 100),
            ('Apple', 52, 0.3, 14, 0.2),
            ('Salmon', 208, 20, 0, 13)
        ]
        
        c.executemany('''
        INSERT OR IGNORE INTO food_items (name, calories_per_100g, protein_per_100g, carbs_per_100g, fats_per_100g) 
        VALUES (?, ?, ?, ?, ?)
        ''', sample_foods)

        conn.commit()
        print("Database 'nutriscale.db' created/updated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()