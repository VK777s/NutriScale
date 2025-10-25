# NutriScale: A Python-Based Diet & Nutrition Tracker 🍎

NutriScale is a full-featured, GUI-based nutrition management system built with Python, Tkinter, and Matplotlib. It provides a complete solution for users to track their dietary intake, log meals, and visualize progress toward their weight goals.

It also features a separate, comprehensive admin panel for managing the application's food database and user accounts.

## Screenshots

| Client Login | Client Dashboard | Progress Charts | Admin Panel |
| :---: | :---: | :---: | :---: |
| 

[Image of Login Screen]
(https://i.imgur.com/your-login-screenshot.png) | (https://i.imgur.com/your-dashboard-screenshot.png) | 

[Image of Charts]
(https://i.imgur.com/your-charts-screenshot.png) | (https://i.imgur.com/your-admin-screenshot.png) |
*(Note: Replace these links with your own screenshots after uploading!)*

---

## Features

The project is split into two main applications: the **Client Portal** and the **Admin Panel**.

### 🔑 Client Portal (`nutriscale_app.py`)

* **Secure Authentication:** Users can create a secure account (username/password) and log in.
* **Personalized Profile:** On signup, users provide their age, weight, height, and activity level to calculate:
    * Basal Metabolic Rate (BMR)
    * Total Daily Energy Expenditure (TDEE)
    * A target daily calorie goal (deficit/surplus).
* **Daily Meal Logging:** Users can search the food database, enter a quantity (in grams), and log it to their daily journal.
* **Smart Food Recommendations:** A recommendation engine suggests meal/snack ideas (with quantities) based on the user's remaining calories for the day.
* **Progress Dashboard:** Users can visualize their progress with two dynamic charts:
    * A line chart tracking weight changes over time.
    * A bar chart comparing daily calorie intake against their target.

### 🛠️ Admin Panel (`admin_app.py`)

* **Tabbed Interface:** A clean, tabbed GUI for simple management.
* **Food Database Management (CRUD):**
    * **Create:** Add new food items with full nutritional data (calories, protein, carbs, fats).
    * **Read:** View the entire food database in a sortable list.
    * **Update:** Select a food to auto-fill its data, make changes, and save.
    * **Delete:** Remove food items from the database.
* **User Management:**
    * View a list of all registered users and their profile details (username, name, goals, etc.).
    * Delete users from the system. This also performs a "cascading delete" to remove all of their associated meal logs and weight history.

---

## 🚀 Technical Stack

* **Language:** Python 3.x
* **GUI:** Tkinter (via `ttk` for modern styling)
* **Database:** SQLite 3 (for all user, food, and log data)
* **Data Visualization:** Matplotlib (embedded directly into the Tkinter GUI)

---

## ⚙️ Installation & Setup

To run this project, you'll need Python 3 and one external library.

**1. Clone the repository:**
```bash
git clone https://github.com/VK777s/NutriScale.git
cd NutriScale

**2. Install dependencies:**
 The project requires matplotlib. You can install it using pip:
```bash
pip install matplotlib
