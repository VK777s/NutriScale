# nutriscale_full.py
"""
NutriScale - Full CLI Implementation (Team-ready)

Features included:
 - Admin & Client portals (multi-user)
 - Food database (CSV) with CRUD using pandas
 - Daily user logs stored persistently (CSV)
 - BMI calculation + category + personalized recommendations
 - Activity-level based calorie goal (Mifflin-St Jeor + multipliers)
 - Macronutrient breakdown (carbs/protein/fat)
 - Smart food recommendations (backtracking / greedy fallback)
 - Food search & sorting (linear, bubble, quick, merge)
 - Syllabus demos: decorators, recursion, lambda, stacks/queues, searching/sorting
 - Export logs to CSV/JSON
 - Case-insensitive matching, input validation, helpful prompts
"""

import os
import sys
import json
import random
from datetime import datetime, date
from typing import List, Tuple

import pandas as pd
import numpy as np

# -------------------------
# Files / Constants
# -------------------------
FOOD_DB_FILE = "food_database.csv"
USER_DB_FILE = "users.csv"            # stores user profiles
LOGS_FILE = "nutriscale_logs.csv"     # daily logs per user
RECOMMENDATIONS_FILE = "custom_recommendations.csv"

# Activity multipliers (Mifflin-St Jeor based TDEE)
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very active": 1.9
}

# -------------------------
# Decorator for logging
# -------------------------
def log_action(func):
    """Simple decorator to show when important functions run"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__}()")
        return func(*args, **kwargs)
    return wrapper

# -------------------------
# Syllabus: Stack & Queue
# -------------------------
class Stack:
    def __init__(self):
        self._s = []
    def push(self, v): self._s.append(v)
    def pop(self):
        return self._s.pop() if self._s else None
    def peek(self): return self._s[-1] if self._s else None
    def is_empty(self): return len(self._s)==0
    def __repr__(self): return f"Stack({self._s})"

class Queue:
    def __init__(self):
        self._q = []
    def enqueue(self, v): self._q.append(v)
    def dequeue(self):
        return self._q.pop(0) if self._q else None
    def is_empty(self): return len(self._q)==0
    def __repr__(self): return f"Queue({self._q})"

# -------------------------
# Syllabus: Searching & Sorting
# -------------------------
def linear_search(lst, key):
    """Case-insensitive linear search (returns indices)"""
    result = []
    for i, v in enumerate(lst):
        try:
            if str(v).lower() == str(key).lower():
                result.append(i)
        except:
            continue
    return result

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    L = merge_sort(arr[:mid])
    R = merge_sort(arr[mid:])
    res = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            res.append(L[i]); i += 1
        else:
            res.append(R[j]); j += 1
    res.extend(L[i:]); res.extend(R[j:])
    return res

# -------------------------
# Utility helpers
# -------------------------
def ensure_food_db():
    if not os.path.exists(FOOD_DB_FILE):
        init_food_database()
    return pd.read_csv(FOOD_DB_FILE)

def ensure_user_db():
    if not os.path.exists(USER_DB_FILE):
        df = pd.DataFrame(columns=["username","name","age","gender","height_cm","weight_kg","target_weight","activity"])
        df.to_csv(USER_DB_FILE, index=False)
    return pd.read_csv(USER_DB_FILE)

def ensure_logs():
    if not os.path.exists(LOGS_FILE):
        df = pd.DataFrame(columns=["date","username","foods","total_calories","weight"])
        df.to_csv(LOGS_FILE, index=False)
    return pd.read_csv(LOGS_FILE)

def ensure_recommendations():
    if not os.path.exists(RECOMMENDATIONS_FILE):
        df = pd.DataFrame(columns=["username", "date_created", "recommendations"])
        df.to_csv(RECOMMENDATIONS_FILE, index=False)
    return pd.read_csv(RECOMMENDATIONS_FILE)


# -------------------------
# Initialize Food DB with variety (80+ items from earlier)
# -------------------------
@log_action
def init_food_database():
    data = [
        {"Food":"Oatmeal","Calories":150},{"Food":"Eggs","Calories":155},
        {"Food":"Chicken Breast","Calories":200},{"Food":"Rice","Calories":180},
        {"Food":"Salad","Calories":120},{"Food":"Fish","Calories":220},
        {"Food":"Apple","Calories":80},{"Food":"Banana","Calories":100},
        {"Food":"Milk","Calories":130},{"Food":"Yogurt","Calories":95},
        {"Food":"Almonds","Calories":160},{"Food":"Peanut Butter","Calories":190},
        {"Food":"Cheese","Calories":200},{"Food":"Broccoli","Calories":55},
        {"Food":"Carrots","Calories":50},{"Food":"Sweet Potato","Calories":100},
        {"Food":"Quinoa","Calories":120},{"Food":"Lentils","Calories":115},
        {"Food":"Tofu","Calories":150},{"Food":"Turkey","Calories":180},
        {"Food":"Spinach","Calories":25},{"Food":"Avocado","Calories":160},
        {"Food":"Strawberries","Calories":45},{"Food":"Blueberries","Calories":50},
        {"Food":"Orange","Calories":62},{"Food":"Watermelon","Calories":30},
        {"Food":"Cucumber","Calories":16},{"Food":"Tomato","Calories":20},
        {"Food":"Beef","Calories":250},{"Food":"Pork","Calories":220},
        {"Food":"Shrimp","Calories":100},{"Food":"Salmon","Calories":208},
        {"Food":"Tuna","Calories":180},{"Food":"Pasta","Calories":210},
        {"Food":"Bread","Calories":80},{"Food":"Bagel","Calories":250},
        {"Food":"Cereal","Calories":110},{"Food":"Granola","Calories":120},
        {"Food":"Honey","Calories":64},{"Food":"Jam","Calories":50},
        {"Food":"Chocolate","Calories":210},{"Food":"Ice Cream","Calories":207},
        {"Food":"Chickpeas","Calories":120},{"Food":"Black Beans","Calories":110},
        {"Food":"Kidney Beans","Calories":115},{"Food":"Rice Cakes","Calories":35},
        {"Food":"Popcorn","Calories":90},{"Food":"Walnuts","Calories":180},
        {"Food":"Cashews","Calories":160},{"Food":"Sunflower Seeds","Calories":170},
        {"Food":"Pumpkin Seeds","Calories":150},{"Food":"Oats","Calories":130},
        {"Food":"Cottage Cheese","Calories":120},{"Food":"Egg Whites","Calories":17},
        {"Food":"Green Peas","Calories":81},{"Food":"Zucchini","Calories":20},
        {"Food":"Mushrooms","Calories":22},{"Food":"Onions","Calories":40},
        {"Food":"Garlic","Calories":5},{"Food":"Bell Pepper","Calories":30},
        {"Food":"Cabbage","Calories":25},{"Food":"Cauliflower","Calories":25},
        {"Food":"Green Beans","Calories":35},{"Food":"Brussels Sprouts","Calories":38},
        {"Food":"Asparagus","Calories":20},{"Food":"Pineapple","Calories":50},
        {"Food":"Mango","Calories":60},{"Food":"Papaya","Calories":43},
        {"Food":"Kiwi","Calories":42},{"Food":"Grapes","Calories":70},
        {"Food":"Pear","Calories":57},{"Food":"Peach","Calories":59},
        {"Food":"Plum","Calories":46},{"Food":"Apricot","Calories":48},
        {"Food":"Pomegranate","Calories":83},{"Food":"Dates","Calories":277},
        {"Food":"Raisins","Calories":299},{"Food":"Figs","Calories":74},
        {"Food":"Brown Rice","Calories":215},{"Food":"Barley","Calories":193},
        {"Food":"Millet","Calories":207},{"Food":"Bulgur","Calories":150},
        {"Food":"Buckwheat","Calories":155},{"Food":"Rye Bread","Calories":83},
        {"Food":"Sourdough","Calories":120},{"Food":"Tortilla","Calories":140},
        {"Food":"Avocado Toast","Calories":190},{"Food":"Hummus","Calories":75},
        {"Food":"Falafel","Calories":150},{"Food":"Tempeh","Calories":190},
        {"Food":"Soy Milk","Calories":80},{"Food":"Coconut Milk","Calories":45},
        {"Food":"Green Tea","Calories":0},{"Food":"Black Coffee","Calories":5},
        {"Food":"Protein Shake","Calories":200}
    ]
    df = pd.DataFrame(data)
    df.to_csv(FOOD_DB_FILE, index=False)
    print("✅ Food database created with variety.")

# -------------------------
# Nutrition Calculations
# -------------------------
@log_action
def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    h_m = height_cm / 100.0
    if h_m <= 0:
        return float('nan')
    return round(weight_kg / (h_m * h_m), 2)

@log_action
def bmi_category_and_recommendation(bmi: float) -> Tuple[str, str]:
    """Return category and recommendation text"""
    if np.isnan(bmi):
        return ("Unknown", "Unable to calculate BMI.")
    if bmi < 18.5:
        cat = "Underweight"
        rec = ("⚠️ You are underweight (BMI < 18.5). "
               "Increase calorie intake with nutrient-dense foods (nuts, dairy, lean proteins). "
               "Aim for modest calorie surplus and resistance training.")
    elif 18.5 <= bmi < 25.0:
        cat = "Healthy"
        rec = ("✅ Healthy weight (BMI 18.5–24.9). Maintain with balanced macronutrients "
               "and regular physical activity.")
    elif 25.0 <= bmi < 30.0:
        cat = "Overweight"
        rec = ("⚠️ Overweight (BMI 25.0–29.9). Consider portion control, reduce refined carbs, "
               "increase daily activity and cardio.")
    else:
        cat = "Obese"
        rec = ("🚨 Obese (BMI ≥ 30.0). Consider consulting a healthcare professional, "
               "focus on whole foods, reduced portions and gradual increased activity.")
    return (cat, rec)

@log_action
def mifflin_st_jeor(weight, height, age, gender):
    """Return BMR (kcal/day)"""
    g = gender.strip().lower()
    if g.startswith('m'):
        bmr = 10*weight + 6.25*height - 5*age + 5
    elif g.startswith('f'):
        bmr = 10*weight + 6.25*height - 5*age - 161
    else:
        # average for non-binary/other
        bmr_m = 10*weight + 6.25*height - 5*age + 5
        bmr_f = 10*weight + 6.25*height - 5*age - 161
        bmr = (bmr_m + bmr_f) / 2.0
    return round(bmr, 2)

@log_action
def tdee_from_activity(bmr, activity_level: str) -> float:
    key = activity_level.strip().lower()
    mult = ACTIVITY_MULTIPLIERS.get(key, 1.2)
    return round(bmr * mult, 0)

@log_action
def recommended_calories(tdee, weight, target_weight):
    # Common simple rule: deficit for loss, surplus for gain
    if target_weight < weight:
        rec = int(round(tdee - 500))
    elif target_weight > weight:
        rec = int(round(tdee + 500))
    else:
        rec = int(round(tdee))
    rec = max(rec, 1000)  # safety floor
    return rec

@log_action
def macronutrient_breakdown(calories: int, protein_ratio=0.25, fat_ratio=0.25, carb_ratio=0.5):
    """
    Default macro split: 50% carbs, 25% protein, 25% fat
    Return grams for each (protein/fat/carbs)
    (1g protein = 4 kcal, 1g carb = 4 kcal, 1g fat = 9 kcal)
    """
    p_cal = calories * protein_ratio
    f_cal = calories * fat_ratio
    c_cal = calories * carb_ratio
    protein_g = round(p_cal / 4)
    fat_g = round(f_cal / 9)
    carbs_g = round(c_cal / 4)
    return {"protein_g": protein_g, "fat_g": fat_g, "carbs_g": carbs_g}

# -------------------------
# Persistence: Users, Food DB, Logs
# -------------------------
@log_action
def create_user_profile(username, name, age, gender, height_cm, weight_kg, target_weight, activity):
    df = ensure_user_db()
    if username.lower() in df['username'].str.lower().tolist():
        print("⚠️ Username exists.")
        return False
    new = {"username": username, "name": name, "age": age, "gender": gender,
           "height_cm": height_cm, "weight_kg": weight_kg, "target_weight": target_weight, "activity": activity}
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(USER_DB_FILE, index=False)
    print("✅ User created.")
    return True

@log_action
def find_user(username):
    df = ensure_user_db()
    mask = df['username'].str.lower() == username.lower()
    if mask.any():
        return df.loc[mask].iloc[0].to_dict()
    return None

# -------------------------
# Admin: View registered users
# -------------------------
@log_action
def view_registered_users():
    df = ensure_user_db()
    if df.empty:
        print("No registered users found.")
        return
    print("\n=== Registered Users ===")
    print(df.to_string(index=False))
    print("========================\n")


@log_action
def update_user_weight(username, new_weight):
    df = ensure_user_db()
    mask = df['username'].str.lower() == username.lower()
    if not mask.any():
        print("⚠️ User not found.")
        return False
    df.loc[mask, 'weight_kg'] = new_weight
    df.to_csv(USER_DB_FILE, index=False)
    return True

@log_action
def save_daily_entry(username, foods: List[Tuple[str,int]], total_calories: int, weight=None):
    """
    Save a daily entry (one row per save). Foods is list of tuples (foodname, calories)
    """
    ensure_logs()
    row = {
        "date": date.today().isoformat(),
        "username": username,
        "foods": "; ".join([f"{f}({c}kcal)" for f,c in foods]),
        "total_calories": total_calories,
        "weight": weight if weight is not None else ""
    }
    logs_df = pd.read_csv(LOGS_FILE)
    logs_df = pd.concat([logs_df, pd.DataFrame([row])], ignore_index=True)
    logs_df.to_csv(LOGS_FILE, index=False)
    print("✅ Daily entry saved.")

@log_action
def export_user_logs(username, fmt="csv"):
    logs = ensure_logs()
    user_logs = logs[logs['username'].str.lower() == username.lower()]
    if user_logs.empty:
        print("No logs for that user.")
        return
    filename = f"{username}_logs_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    if fmt.lower() == "csv":
        path = filename + ".csv"
        user_logs.to_csv(path, index=False)
    else:
        path = filename + ".json"
        user_logs.to_json(path, orient="records", date_format="iso")
    print(f"✅ Exported to {path}")

# -------------------------
# CRUD Food DB ops
# -------------------------
@log_action
def read_food_db():
    return ensure_food_db()

@log_action
def add_food_to_db(food_name, calories):
    df = ensure_food_db()
    df = pd.concat([df, pd.DataFrame([{"Food": food_name, "Calories": int(calories)}])], ignore_index=True)
    df.to_csv(FOOD_DB_FILE, index=False)
    print(f"✅ Added {food_name} ({calories} kcal).")

@log_action
def update_food_db(food_name, calories):
    df = ensure_food_db()
    mask = df['Food'].str.lower() == food_name.lower()
    if not mask.any():
        print("⚠️ Food not found.")
        return False
    df.loc[mask, 'Calories'] = int(calories)
    df.to_csv(FOOD_DB_FILE, index=False)
    print("✅ Updated food.")
    return True

@log_action
def delete_food_from_db(food_name):
    df = ensure_food_db()
    df = df[df['Food'].str.lower() != food_name.lower()]
    df.to_csv(FOOD_DB_FILE, index=False)
    print("✅ Deleted if it existed.")

# -------------------------
# Smart food recommendation (backtracking & greedy)
# -------------------------
def find_combination_close(meals: List[Tuple[str,int]], target: int, tolerance=30):
    """
    Backtracking approach to find a combination of foods whose sum is within tolerance of target.
    meals: list of (name, calories)
    """
    meals_sorted = sorted(meals, key=lambda x: x[1])  # ascending
    best = None
    best_diff = float('inf')

    # recursion helper
    def backtrack(idx, current_list, current_sum):
        nonlocal best, best_diff
        # check
        diff = abs(current_sum - target)
        if diff <= tolerance:
            if diff < best_diff:
                best = current_list.copy()
                best_diff = diff
            # we can still search for exact better combos but prune if perfect
            if diff == 0:
                return True
        # pruning
        if idx >= len(meals_sorted) or current_sum > target + tolerance:
            return False
        # try include
        for i in range(idx, len(meals_sorted)):
            name, cal = meals_sorted[i]
            current_list.append((name, cal))
            if backtrack(i+1, current_list, current_sum+cal):
                return True
            current_list.pop()
        return False

    backtrack(0, [], 0)
    return best

def recommend_foods_for_calories(cal_goal: int, food_df: pd.DataFrame, items=5):
    meals = list(zip(food_df['Food'], food_df['Calories']))
    # try to find combination close to a meal portion (use half-day goal or full-day depending)
    combo = find_combination_close(meals, cal_goal, tolerance=int(0.08*cal_goal))
    if combo:
        return combo
    # fallback: greedy pick items until near target
    sorted_desc = sorted(meals, key=lambda x: x[1], reverse=True)
    total = 0
    chosen = []
    for name, c in sorted_desc:
        if total + c <= cal_goal * 1.05:
            chosen.append((name,c))
            total += c
        if total >= cal_goal*0.9:
            break
    return chosen if chosen else sorted_desc[:min(items, len(sorted_desc))]

# -------------------------
# CLI Menus
# -------------------------
def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def pause():
    input("Press Enter to continue...")

def read_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v

# Admin menu
@log_action
def admin_portal():
    while True:
        clear_console()
        print("=== ADMIN PORTAL ===")
        print("1. View Food Database")
        print("2. Add Food")
        print("3. Update Food")
        print("4. Delete Food")
        print("5. Initialize Default Food DB")
        print("6. View Registered Users")
        print("7. Create Custom Recommendation for User")
        print("8. Back")


        choice = input("Choice: ").strip()
        if choice == "1":
            df = read_food_db()
            print(df.to_string(index=False))
            pause()
        elif choice == "2":
            name = read_nonempty("Food name: ")
            cal = int(input("Calories (kcal): "))
            add_food_to_db(name, cal)
            pause()
        elif choice == "3":
            name = read_nonempty("Food name to update: ")
            cal = int(input("New calories: "))
            update_food_db(name, cal)
            pause()
        elif choice == "4":
            name = read_nonempty("Food name to delete: ")
            delete_food_from_db(name)
            pause()
        elif choice == "5":
            init_food_database()
            pause()
        elif choice == "6":
            view_registered_users()
            pause()
        elif choice == "7":
            create_custom_recommendation()
            pause()
        elif choice == "8":
            break



# Client flows
def register_flow():
    clear_console()
    print("=== USER REGISTRATION ===")
    username = read_nonempty("Username (lowercase recommended): ")
    name = read_nonempty("Full name: ")
    age = int(input("Age: "))
    gender = read_nonempty("Gender (Male/Female/Other): ")
    height_cm = float(input("Height (cm): "))
    weight_kg = float(input("Weight (kg): "))
    target_weight = float(input("Target weight (kg): "))
    print("Activity levels: sedentary / light / moderate / active / very active")
    activity = read_nonempty("Activity level: ").lower()
    create_user_profile(username, name, age, gender, height_cm, weight_kg, target_weight, activity)
    pause()

def login_flow():
    clear_console()
    print("=== USER LOGIN ===")
    username = read_nonempty("Username: ")
    user = find_user(username)
    if not user:
        print("User not found. Please register.")
        pause()
        return None
    print(f"Welcome back, {user['name']}!")
    return user

def client_portal():
    user = login_flow()
    if not user:
        return
    username = user['username']
    # Greet and show last log info if any
    logs = ensure_logs()
    user_logs = logs[logs['username'].str.lower() == username.lower()]
    if not user_logs.empty:
        last = user_logs.iloc[-1]
        print(f"Last log: {last['date']} — {last['total_calories']} kcal — foods: {last['foods']}")
    # calculate metrics
    weight = float(user['weight_kg'])
    height = float(user['height_cm'])
    age = int(user['age'])
    gender = user['gender']
    target_weight = float(user['target_weight'])
    activity = user.get('activity','sedentary')
    bmi = calculate_bmi(weight, height)
    cat, rectext = bmi_category_and_recommendation(bmi)
    bmr = mifflin_st_jeor(weight, height, age, gender)
    tdee = tdee_from_activity(bmr, activity)
    rec_cal = recommended_calories(tdee, weight, target_weight)
    macros = macronutrient_breakdown(rec_cal)
    # Show user-friendly messages
    print(f"\nBMI: {bmi} — {cat}")
    print(rectext)
    # Suggest how much to eat if under/over
    if cat == "Underweight":
        suggestion = f"Aim for a calorie intake around {rec_cal} kcal (or +250–500 kcal surplus) to gain gradually."
    elif cat == "Healthy":
        suggestion = f"Aim to maintain around {rec_cal} kcal to keep weight stable."
    elif cat == "Overweight":
        suggestion = f"Aim for a calorie intake around {rec_cal} kcal (a modest deficit) and try to increase activity."
    else:
        suggestion = f"Aim for supervised calorie reduction and gentle activity; consult a professional if needed."
    print(suggestion)
    print(f"TDEE (est.): {int(tdee)} kcal — Recommended calories: {rec_cal} kcal")
    print("Macro targets (approx): Protein: {protein_g} g, Fat: {fat_g} g, Carbs: {carbs_g} g".format(**macros))
    # motivational
    quotes = [
        "Small steps, big results — keep going!",
        "Consistency beats intensity — log today and win tomorrow.",
        "Hydrate, move, rest — repeat.",
        "You’re one healthy choice away from a better day."
    ]
    print("\n" + random.choice(quotes))

    # Show admin custom recommendation if available
    ensure_recommendations()
    df_rec = pd.read_csv(RECOMMENDATIONS_FILE)
    user_recs = df_rec[df_rec['username'].str.lower() == username.lower()]
    if not user_recs.empty:
        latest = user_recs.iloc[-1]
        print("\n📅 Admin Custom Weekly Plan:")
        print(latest['recommendations'])
        print(f"(Created on {latest['date_created']})")

    # Meal recommendation
    df_food = read_food_db()
    print("\nSmart meal suggestions to match recommended calories:")
    suggestion = recommend_foods_for_calories(rec_cal, df_food)
    total_sug = sum([c for _,c in suggestion]) if suggestion else 0
    for name, c in suggestion:
        print(f" - {name} ({c} kcal)")
    print(f"Suggested total (approx): {total_sug} kcal")
    # allow user to customize today's intake
    customize = input("\nWould you like to customize today's intake? (y/n): ").strip().lower()
    if customize == 'y':
        custom_meal_flow(username, df_food, rec_cal, weight)
    else:
        # save suggested as today's entry if user accepts
        accept = input("Save suggested plan as today's entry? (y/n): ").strip().lower()
        if accept == 'y':
            save_daily_entry(username, suggestion, total_sug, weight)
            # update user weight? offer option
            update = input("Update recorded weight for your profile? (y/n): ").strip().lower()
            if update == 'y':
                new_w = float(input("Enter new weight (kg): "))
                update_user_weight(username, new_w)
        else:
            print("No entry saved.")
    pause()

def custom_meal_flow(username, df_food: pd.DataFrame, calorie_goal: int, curr_weight=None):
    # Show options: search, list top N, add custom food, finish
    selected = []
    total = 0
    while True:
        clear_console()
        print("=== CUSTOM MEAL PLANNER ===")
        print(f"Goal (recommended): {calorie_goal} kcal | Current total: {total} kcal")
        print("Commands: list / search <term> / sort calories asc|desc / addcustom / done")
        cmd = input("Enter command: ").strip()
        if cmd == "list":
            print(df_food[['Food','Calories']].to_string(index=False))
            pause()
        elif cmd.startswith("search"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 1:
                print("Usage: search <term>")
                pause(); continue
            term = parts[1].strip().lower()
            matches = df_food[df_food['Food'].str.lower().str.contains(term)]
            if matches.empty:
                print("No matches.")
            else:
                print(matches[['Food','Calories']].to_string(index=False))
            pause()
        elif cmd.startswith("sort"):
            parts = cmd.split()
            if len(parts) < 3:
                print("Usage: sort calories asc|desc")
                pause(); continue
            key = parts[1]
            order = parts[2]
            if key == "calories":
                if order == "asc":
                    df_sorted = df_food.sort_values(by='Calories', ascending=True)
                else:
                    df_sorted = df_food.sort_values(by='Calories', ascending=False)
                print(df_sorted[['Food','Calories']].to_string(index=False))
            else:
                print("Only sorting by 'calories' is implemented.")
            pause()
        elif cmd == "addcustom":
            name = read_nonempty("Custom food name: ")
            cal = int(input("Calories (kcal): "))
            # add to DB and select it immediately
            add_food_to_db(name, cal)
            selected.append((name, cal)); total += cal
            print(f"Added and selected {name} ({cal} kcal).")
            pause()
        elif cmd == "done":
            break
        else:
            # interpret input as attempt to add a food by exact name
            name_try = cmd
            matches_mask = df_food['Food'].str.lower() == name_try.lower()
            if matches_mask.any():
                row = df_food.loc[matches_mask].iloc[0]
                selected.append((row['Food'], int(row['Calories'])))
                total += int(row['Calories'])
                print(f"Selected {row['Food']} ({row['Calories']} kcal). Total now {total} kcal.")
                # immediate feedback
                if total > calorie_goal * 1.1:
                    print("⚠️ Total exceeds recommended by >10%")
                elif total < calorie_goal * 0.9:
                    print("⚠️ Total below recommended by >10%")
                else:
                    print("✅ Total within recommended range.")
            else:
                print("Unknown command or food. Use 'list' or 'search' or 'addcustom'.")
            pause()
    # end loop
    if selected:
        print("\nFinal selection:")
        for f,c in selected:
            print(f" - {f} ({c} kcal)")
        print("Total:", total, "kcal")
        save_daily_entry(username, selected, total, curr_weight)
    else:
        print("No foods selected. Nothing saved.")

# -------------------------
# Admin: Custom Recommendations
# -------------------------
@log_action
def create_custom_recommendation():
    ensure_recommendations()
    df_users = ensure_user_db()

    if df_users.empty:
        print("⚠️ No users available to recommend for.")
        return

    print("\nAvailable Users:")
    print(df_users[['username', 'name']].to_string(index=False))
    username = input("\nEnter username to create recommendation for: ").strip().lower()

    if username not in df_users['username'].str.lower().tolist():
        print("⚠️ User not found.")
        return

    print("\nEnter weekly meal recommendations (separate each day by ';'):")
    print("Example: Oatmeal+Milk; Salad+Chicken; Fish+Rice; etc.")
    plan = input("Enter meal plan for the week: ").strip()

    df = pd.read_csv(RECOMMENDATIONS_FILE)
    new = {
        "username": username,
        "date_created": date.today().isoformat(),
        "recommendations": plan
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(RECOMMENDATIONS_FILE, index=False)
    print(f"✅ Saved custom recommendation for {username}.")
    pause()


@log_action
def view_recommendations_for_user(username):
    ensure_recommendations()
    df = pd.read_csv(RECOMMENDATIONS_FILE)
    recs = df[df['username'].str.lower() == username.lower()]
    if recs.empty:
        print("No custom recommendations found for this user.")
        return
    print("\n=== Custom Recommendations ===")
    for _, row in recs.iterrows():
        print(f"Date: {row['date_created']}")
        print(f"Plan: {row['recommendations']}")
        print("--------------------------")


# -------------------------
# Main menu
# -------------------------
def main_menu():
    ensure_food_db(); ensure_user_db(); ensure_logs()
    while True:
        clear_console()
        print("=== NUTRISCALE MANAGEMENT PORTAL ===")
        print("1. Admin Portal")
        print("2. Register New User")
        print("3. Client Login")
        print("4. Export My Logs (client must enter username)")
        print("5. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            admin_portal()
        elif choice == "2":
            register_flow()
        elif choice == "3":
            client_portal()
        elif choice == "4":
            username = read_nonempty("Enter username to export logs: ")
            fmt = input("Format (csv/json) [csv]: ").strip().lower() or "csv"
            export_user_logs(username, fmt)
            pause()
        elif choice == "5":
            print("Goodbye — stay consistent!")
            break
        else:
            print("Invalid choice.")
            pause()

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)
