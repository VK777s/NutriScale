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

## Default Food Database

| Food             | Calories (kcal) |
| :--------------- | :-------------: |
| Oatmeal          |       150       |
| Eggs             |       155       |
| Chicken Breast   |       200       |
| Rice             |       180       |
| Salad            |       120       |
| Fish             |       220       |
| Apple            |        80       |
| Banana           |       100       |
| Milk             |       130       |
| Yogurt           |        95       |
| Almonds          |       160       |
| Peanut Butter    |       190       |
| Cheese           |       200       |
| Broccoli         |        55       |
| Carrots          |        50       |
| Sweet Potato     |       100       |
| Quinoa           |       120       |
| Lentils          |       115       |
| Tofu             |       150       |
| Turkey           |       180       |
| Spinach          |        25       |
| Avocado          |       160       |
| Strawberries     |        45       |
| Blueberries      |        50       |
| Orange           |        62       |
| Watermelon       |        30       |
| Cucumber         |        16       |
| Tomato           |        20       |
| Beef             |       250       |
| Pork             |       220       |
| Shrimp           |       100       |
| Salmon           |       208       |
| Tuna             |       180       |
| Pasta            |       210       |
| Bread            |        80       |
| Bagel            |       250       |
| Cereal           |       110       |
| Granola          |       120       |
| Honey            |        64       |
| Jam              |        50       |
| Chocolate        |       210       |
| Ice Cream        |       207       |
| Chickpeas        |       120       |
| Black Beans      |       110       |
| Kidney Beans     |       115       |
| Rice Cakes       |        35       |
| Popcorn          |        90       |
| Walnuts          |       180       |
| Cashews          |       160       |
| Sunflower Seeds  |       170       |
| Pumpkin Seeds    |       150       |
| Oats             |       130       |
| Cottage Cheese   |       120       |
| Egg Whites       |        17       |
| Green Peas       |        81       |
| Zucchini         |        20       |
| Mushrooms        |        22       |
| Onions           |        40       |
| Garlic           |        5        |
| Bell Pepper      |        30       |
| Cabbage          |        25       |
| Cauliflower      |        25       |
| Green Beans      |        35       |
| Brussels Sprouts |        38       |
| Asparagus        |        20       |
| Pineapple        |        50       |
| Mango            |        60       |
| Papaya           |        43       |
| Kiwi             |        42       |
| Grapes           |        70       |
| Pear             |        57       |
| Peach            |        59       |
| Plum             |        46       |
| Apricot          |        48       |
| Pomegranate      |        83       |
| Dates            |       277       |
| Raisins          |       299       |
| Figs             |        74       |
| Brown Rice       |       215       |
| Barley           |       193       |
| Millet           |       207       |
| Bulgur           |       150       |
| Buckwheat        |       155       |
| Rye Bread        |        83       |
| Sourdough        |       120       |
| Tortilla         |       140       |
| Avocado Toast    |       190       |
| Hummus           |        75       |
| Falafel          |       150       |
| Tempeh           |       190       |
| Soy Milk         |        80       |
| Coconut Milk     |        45       |
| Green Tea        |        0        |
| Black Coffee     |        5        |
| Protein Shake    |       200       |

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
