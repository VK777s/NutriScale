# 🥗 NutriScale: CLI-Based Intelligent Nutrition & Fitness Tracker

**NutriScale** is a Python-based **command-line nutrition management system** that helps users track meals, calculate calorie needs, and maintain fitness goals — all from the terminal.

It’s a complete, syllabus-aligned project combining **data structures, file handling, decorators, recursion, and algorithms**.  
Built for **academic submissions, teamwork**, and real-world demonstration of Python proficiency.

---

## 📦 Overview

NutriScale enables users to:
- Calculate **BMI**, **BMR**, and **TDEE** using personal data  
- Get **health-based recommendations** (e.g., if BMI is low, the app advises eating more)  
- Track **daily calorie intake** and **nutritional balance**  
- Create **custom meals** from a food database  
- Log data automatically to CSV files for long-term progress tracking  
- Allow admins to **manage food items and view registered users**

All interactions are through a clean and friendly **CLI interface**, with menus, validation, and logging.

---

## 🧩 Project Structure

| File | Description |
|------|--------------|
| `nutriscale_full.py` | Complete CLI app (Admin + Client) |
| `food_database.csv` | Stores food names and calorie data |
| `users.csv` | Stores user profiles and goals |
| `nutriscale_logs.csv` | Daily log of user food intake |

---

## 🌟 Key Features

### 👤 **Client Portal**

- **User Registration & Login**  
  Users can sign up with their details — name, age, height, weight, gender, and activity level.

- **BMI & Health Insights**  
  Calculates BMI and provides category feedback:
  - 🟢 *Healthy (18.5–24.9)* — Great job maintaining balance!
  - 🟡 *Underweight (<18.5)* — You should eat more; increase calories gradually.
  - 🔴 *Overweight (25–29.9)* — Try moderate calorie control and regular exercise.
  - ⚠️ *Obese (>30)* — Consider consulting a doctor and following a calorie deficit diet.

- **Personalized Calorie & Macronutrient Goals**  
  Based on the user’s BMR, activity level, and goal (gain or lose weight).

- **Meal Customization**  
  Users can search for foods from the database and build custom meal plans.

- **Smart Food Recommendations**  
  Suggests balanced foods using backtracking and greedy algorithms.

- **Daily Progress Tracker**  
  Every day’s meal and calorie intake is saved to a CSV file (`nutriscale_logs.csv`).

- **Data Export**  
  Users can export their logs in `.csv` or `.json` formats.

---

### 🧑‍💼 **Admin Portal**

The admin has access to manage the food database and registered users.

**Features include:**
- ➕ **Add new foods** with their calorie count  
- ✏️ **Update** existing food data  
- 🗑️ **Delete** unwanted foods  
- 📋 **View all foods** currently stored in the database  
- 👥 **View all registered users** (with details from `users.csv`)  
- 🧹 **Initialize** or reset the database (optional)

---

## 🧠 Technical Highlights

- **Language:** Python 3.x  
- **Core Concepts Used:**
  - Decorators (for logging function calls)
  - File Handling (CSV read/write)
  - Backtracking & Sorting algorithms
  - Stacks and Queues (for food suggestion history)
  - Recursion (used in search/sort)
  - Pandas for efficient CSV handling
- **Libraries:**  
  - `pandas` – data handling  
  - `numpy` – calculations  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VK777s/NutriScale.git
cd NutriScale
```

## ✅ Learning Outcomes

* Handling user input and conditional logic in Python
* Modular programming & decorators
* Collections, searching, and sorting
* Backtracking algorithms for meal suggestions
* File-based data persistence using CSV
