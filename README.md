# NutriScale: CLI-Based Intelligent Nutrition & Fitness Tracker 🍎

NutriScale is a **Python-based command-line nutrition management system**. It provides a complete solution for tracking dietary intake, logging meals, and visualizing progress toward weight goals.

Unlike GUI-based applications, this version is lightweight and terminal-friendly, suitable for multi-platform usage and team projects.

It helps users maintain a balanced diet by calculating **BMR, daily calorie requirements**, and suggests meal plans based on caloric needs. Users can either accept automated meal suggestions or manually customize meals using a rich food database.

An **Admin Portal** allows management of the food database with CRUD operations.

---

## Project Structure

The project is modularized into three Python files:

| Module                 | Description                                                                                                       |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------- |
| `database_module.py`   | Handles the **food database**, CRUD operations, and **daily logs**.                                               |
| `calculator_module.py` | Calculates **BMI, calorie goals**, and provides **meal combination logic** using backtracking.                    |
| `main_module.py`       | Implements the **CLI menus**, integrates database and calculator modules, and handles **client & admin portals**. |

---

## Features

### 🔑 Client Portal (`main_module.py`)

* **Personalized Profile:** Users input age, weight, height, gender, and target weight to calculate:

  * **BMI**
  * **Recommended daily calories**
  * **Estimated time to reach goal**
* **Meal Suggestions:** Based on calculated calories, the system suggests a combination of foods from the database.
* **Custom Meal Planning:** Users can manually select foods and the program tracks total calories.
* **Daily Logs:** All meals and calories are logged with timestamps for future review.

### 🛠️ Admin Portal (`main_module.py`)

* **Food Database Management (CRUD):**

  * **Create:** Add new foods with calories.
  * **Read:** View all foods in the database.
  * **Update:** Modify calorie values of existing foods.
  * **Delete:** Remove foods from the database.
* **Database Initialization:** Admin can populate the database with a default set of foods.

---

## 🚀 Technical Stack

* **Language:** Python 3.x
* **Database:** CSV-based storage for **foods** and **logs** (`food_database.csv`, `nutriscale_logs.csv`)
* **CLI:** Terminal-based, cross-platform, no GUI dependencies

---

## ⚙️ Installation & Setup

**1. Clone the repository:**

```bash
git clone https://github.com/VK777s/NutriScale.git
cd NutriScale
```

**2. Install dependencies:**

```bash
pip install pandas numpy
```

**3. Run the application:**

```bash
python main_module.py
```

> The program automatically initializes the food database if it does not exist.

---

## How to Use

**Client Portal:**

1. Choose `2` in main menu.
2. Enter your **weight, height, age, gender, and target weight**.
3. See BMI, recommended calories, and meal suggestions.
4. Optionally customize your meal plan manually.
5. Daily logs are saved automatically in `nutriscale_logs.csv`.

**Admin Portal:**

1. Choose `1` in main menu.
2. Use the options to **view, add, update, or delete foods**.
3. Initialize default database if needed.

---

## 📂 Team Collaboration Tips

* Each team member can work independently:

  * **Module 1:** `database_module.py` → database and log management
  * **Module 2:** `calculator_module.py` → calculations & meal combination logic
  * **Module 3:** `main_module.py` → CLI interface, client/admin integration

* Changes in the food database instantly reflect for all users.

---

## ✅ Learning Outcomes

* Handling user input and conditional logic in Python
* Modular programming & decorators
* Collections, searching, and sorting
* Backtracking algorithms for meal suggestions
* File-based data persistence using CSV
