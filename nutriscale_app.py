# File: nutriscale_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
import random

# Imports for Charting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from datetime import datetime

# --- Core Calculation Logic ---
# (This section is unchanged)
def calculate_bmr(gender, weight_kg, height_cm, age):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    else:
        bmr_male = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        bmr_female = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
        bmr = (bmr_male + bmr_female) / 2
    return bmr

def calculate_tdee(bmr, activity_level):
    multipliers = {
        'Sedentary (little or no exercise)': 1.2,
        'Lightly active (light exercise/sports 1-3 days/week)': 1.375,
        'Moderately active (moderate exercise/sports 3-5 days/week)': 1.55,
        'Very active (hard exercise/sports 6-7 days a week)': 1.725,
        'Extra active (very hard exercise/sports & physical job)': 1.9
    }
    return bmr * multipliers.get(activity_level, 1.2)

def calculate_calorie_target(tdee, current_weight, target_weight):
    if target_weight < current_weight: return tdee - 500
    elif target_weight > current_weight: return tdee + 500
    else: return tdee

# --- Main Application GUI ---

class NutriScaleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NutriScale")
        self.geometry("900x800")
        
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # App state variables
        self.current_user_id = None
        self.current_user_name = "" 
        self.calorie_target = 0
        self.today_total_cal = 0
        
        # Placeholders for chart widgets
        self.chart_canvas_widget = None
        self.fig = None
        
        # --- MODIFIED: Start at the login screen ---
        self.show_login_screen()

    def clear_window(self):
        """Removes all widgets and clears chart figures."""
        for widget in self.winfo_children():
            widget.destroy()
        if self.chart_canvas_widget:
            self.chart_canvas_widget.get_tk_widget().destroy()
            self.chart_canvas_widget = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None

    # --- NEW: Login Screen ---
    def show_login_screen(self):
        """Displays the login screen."""
        self.clear_window()
        self.title("NutriScale - Login")
        self.geometry("400x300")
        
        self.current_user_id = None
        self.current_user_name = ""
        self.calorie_target = 0
        
        frame = ttk.Frame(self, padding="20")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="NutriScale Login", font=("Helvetica", 18, "bold")).pack(pady=10)

        login_frame = ttk.Frame(frame)
        login_frame.pack(pady=10)
        
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.login_user_entry = ttk.Entry(login_frame, width=25)
        self.login_user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.login_pass_entry = ttk.Entry(login_frame, width=25, show="*")
        self.login_pass_entry.grid(row=1, column=1, padx=5, pady=5)
        
        login_btn = ttk.Button(frame, text="Login", command=self.login_user)
        login_btn.pack(pady=10, ipady=4, fill=tk.X)
        
        signup_btn = ttk.Button(frame, text="Don't have an account? Sign Up", 
                                command=self.show_signup_screen, style="Link.TButton")
        signup_btn.pack(pady=5)
        style = ttk.Style()
        style.configure("Link.TButton", borderwidth=0, padding=0, background=self.cget('bg'))

    # --- NEW: Login Logic ---
    def login_user(self):
        """Validates user credentials against the database."""
        username = self.login_user_entry.get()
        password = self.login_pass_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password.")
            return

        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT id, name, calorie_target FROM users WHERE username = ? AND password = ?", 
                      (username, password))
            user_data = c.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return
        finally:
            if conn: conn.close()
            
        if user_data:
            # Login successful
            self.current_user_id = user_data[0]
            self.current_user_name = user_data[1]
            self.calorie_target = user_data[2]
            
            messagebox.showinfo("Login Success", f"Welcome back, {self.current_user_name}!")
            self.geometry("900x800") # Resize for main app
            self.show_client_dashboard()
        else:
            # Login failed
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # --- MODIFIED: Renamed to show_signup_screen ---
    def show_signup_screen(self):
        """Displays the profile creation screen (now for signup)."""
        self.clear_window()
        self.title("NutriScale - Sign Up")
        self.geometry("500x700") # Resize for signup form
        
        frame = ttk.Frame(self, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Create Your NutriScale Profile", font=("Helvetica", 18, "bold")).pack(pady=10)

        # --- NEW: Login Credentials ---
        cred_frame = ttk.LabelFrame(frame, text="Login Credentials", padding=10)
        cred_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(cred_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.signup_user_entry = ttk.Entry(cred_frame, width=30)
        self.signup_user_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(cred_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.signup_pass_entry = ttk.Entry(cred_frame, width=30, show="*")
        self.signup_pass_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        # ----------------------------

        # --- Personal Details ---
        details_frame = ttk.LabelFrame(frame, text="Personal Details", padding=10)
        details_frame.pack(fill=tk.X, pady=10)

        fields = [
            ("Name:", "entry"), ("Age:", "entry"), ("Gender:", ["Male", "Female", "Other"]),
            ("Height (cm):", "entry"), ("Current Weight (kg):", "entry"), ("Target Weight (kg):", "entry"),
            ("Activity Level:", [
                'Sedentary (little or no exercise)', 'Lightly active (light exercise/sports 1-3 days/week)',
                'Moderately active (moderate exercise/sports 3-5 days/week)',
                'Very active (hard exercise/sports 6-7 days a week)',
                'Extra active (very hard exercise/sports & physical job)'
            ])
        ]
        
        self.entries = {}
        for i, (label_text, widget_type) in enumerate(fields):
            row_frame = ttk.Frame(details_frame)
            row_frame.pack(fill=tk.X, pady=5)
            label = ttk.Label(row_frame, text=label_text, width=20)
            label.pack(side=tk.LEFT, padx=5)
            
            if widget_type == "entry":
                widget = ttk.Entry(row_frame)
            elif isinstance(widget_type, list):
                widget = ttk.Combobox(row_frame, values=widget_type, state="readonly")
                widget.config(width=45); widget.set(widget_type[0])
            
            widget.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)
            self.entries[label_text] = widget

        save_button = ttk.Button(frame, text="Create Profile", command=self.save_profile)
        save_button.pack(pady=10, ipady=5, fill=tk.X)
        
        login_btn = ttk.Button(frame, text="Already have an account? Login", 
                               command=self.show_login_screen, style="Link.TButton")
        login_btn.pack(pady=5)

    # --- MODIFIED: save_profile now includes username/password ---
    def save_profile(self):
        """Saves the new user profile to the database."""
        try:
            # 1. Get Login Credentials
            username = self.signup_user_entry.get()
            password = self.signup_pass_entry.get()
            if not username or not password:
                raise ValueError("Username and Password are required.")
                
            # 2. Get Personal Details
            name = self.entries["Name:"].get()
            age = int(self.entries["Age:"].get())
            gender = self.entries["Gender:"].get()
            height_cm = float(self.entries["Height (cm):"].get())
            current_weight_kg = float(self.entries["Current Weight (kg):"].get())
            target_weight_kg = float(self.entries["Target Weight (kg):"].get())
            activity_level = self.entries["Activity Level:"].get()
            
            if not all([name, age, gender, height_cm, current_weight_kg, target_weight_kg, activity_level]):
                raise ValueError("All personal detail fields are required.")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check your inputs.\nError: {e}")
            return

        # 3. Calculate Metrics
        bmr = calculate_bmr(gender, current_weight_kg, height_cm, age)
        tdee = calculate_tdee(bmr, activity_level)
        calorie_target = calculate_calorie_target(tdee, current_weight_kg, target_weight_kg)

        # 4. Save to Database
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("""
                INSERT INTO users (name, username, password, age, gender, height_cm, 
                                 current_weight_kg, target_weight_kg, activity_level, 
                                 bmr, tdee, calorie_target)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, username, password, age, gender, height_cm, 
                  current_weight_kg, target_weight_kg, activity_level, 
                  bmr, tdee, calorie_target))
            
            new_user_id = c.lastrowid
            
            # Log the user's starting weight
            today = date.today().isoformat()
            c.execute("""
                INSERT OR IGNORE INTO weight_logs (user_id, weight_kg, log_date)
                VALUES (?, ?, ?)
            """, (new_user_id, current_weight_kg, today))
            
            conn.commit()
        
        except sqlite3.IntegrityError:
            # This triggers if the username is not UNIQUE
            messagebox.showerror("Sign Up Error", f"The username '{username}' is already taken. Please choose another one.")
            return
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not save profile: {e}")
            return
        finally:
            if conn: conn.close()

        messagebox.showinfo("Profile Created!", 
                            f"Hi {name}, your profile is saved!\n"
                            f"You can now log in.")
        
        # Go back to login screen
        self.show_login_screen()

    # --- MODIFIED: show_client_dashboard ---
    def show_client_dashboard(self):
        """Displays the main dashboard for the logged-in user."""
        self.clear_window()
        self.title("NutriScale - Main Dashboard")
        self.geometry("900x800") # Ensure window is large
        self.today_total_cal = 0 
        
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)
        
        # Use the stored name
        ttk.Label(top_frame, text=f"Welcome, {self.current_user_name}!", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT)
        
        progress_button = ttk.Button(top_frame, text="View Progress Dashboard", command=self.show_progress_dashboard)
        progress_button.pack(side=tk.LEFT, padx=20)
        
        self.summary_label = ttk.Label(top_frame, text="Today's Total: 0 / 0 kcal", font=("Helvetica", 12))
        self.summary_label.pack(side=tk.RIGHT)

        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)
        
        # Log Meal Section (Unchanged)
        log_frame = ttk.LabelFrame(self, text="Log a Meal", padding=15)
        log_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(log_frame, text="Food:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.food_combobox = ttk.Combobox(log_frame, width=30)
        self.food_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.food_combobox['values'] = self.get_all_food_names()
        ttk.Label(log_frame, text="Quantity (g):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.quantity_entry = ttk.Entry(log_frame, width=10)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)
        log_button = ttk.Button(log_frame, text="Log Food", command=self.log_meal)
        log_button.grid(row=0, column=4, padx=10, pady=5)

        # Recommendation Section (Unchanged)
        rec_frame = ttk.LabelFrame(self, text="Food Recommendations", padding=15)
        rec_frame.pack(fill=tk.X, padx=10, pady=5)
        rec_button = ttk.Button(rec_frame, text="Get Suggestions", command=self.get_food_recommendations)
        rec_button.pack(pady=5)
        self.recommend_text = tk.Text(rec_frame, height=7, width=80, wrap=tk.WORD, font=("Helvetica", 10))
        self.recommend_text.pack(expand=True, fill=tk.X, pady=5)
        self.recommend_text.insert(tk.END, "Click 'Get Suggestions'...")
        self.recommend_text.tag_configure('detail', font=('Helvetica', 9, 'italic'), foreground='gray')

        # Today's Logged Meals Section (Unchanged)
        log_list_frame = ttk.LabelFrame(self, text="Today's Log", padding=15)
        log_list_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        cols = ('Food', 'Qty (g)', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fats (g)')
        self.log_tree = ttk.Treeview(log_list_frame, columns=cols, show='headings', height=10)
        for col in cols:
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=100, anchor=tk.CENTER)
        self.log_tree.pack(expand=True, fill=tk.BOTH)
        
        # --- MODIFIED: Log Out button ---
        back_button = ttk.Button(self, text="Log Out", command=self.show_login_screen)
        back_button.pack(pady=10)
        
        self.refresh_log_tree()

    # --- Other Functions (Unchanged) ---
    def get_all_food_names(self):
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT name FROM food_items ORDER BY name ASC")
            foods = [row[0] for row in c.fetchall()]
            return foods
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch food list: {e}")
            return []
        finally:
            if conn: conn.close()

    def log_meal(self):
        food_name = self.food_combobox.get()
        try:
            quantity = float(self.quantity_entry.get())
            if quantity <= 0: raise ValueError("Quantity must be positive.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid quantity (e.g., 150).")
            return
        if not food_name:
            messagebox.showerror("Input Error", "Please select a food from the list.")
            return
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT id FROM food_items WHERE name = ?", (food_name,))
            result = c.fetchone()
            if not result:
                messagebox.showerror("Error", "Food not found in database."); return
            food_id = result[0]
            today = date.today().isoformat()
            c.execute("INSERT INTO meal_logs (user_id, food_id, quantity_grams, log_date) VALUES (?, ?, ?, ?)", 
                      (self.current_user_id, food_id, quantity, today))
            conn.commit()
            self.quantity_entry.delete(0, tk.END)
            self.food_combobox.set('')
            self.refresh_log_tree()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not log meal: {e}")
        finally:
            if conn: conn.close()

    def refresh_log_tree(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        total_cal, total_pro, total_carb, total_fat = 0, 0, 0, 0
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            today = date.today().isoformat()
            c.execute("""
                SELECT f.name, m.quantity_grams, 
                       (f.calories_per_100g * m.quantity_grams / 100),
                       (f.protein_per_100g * m.quantity_grams / 100),
                       (f.carbs_per_100g * m.quantity_grams / 100),
                       (f.fats_per_100g * m.quantity_grams / 100)
                FROM meal_logs m JOIN food_items f ON m.food_id = f.id
                WHERE m.user_id = ? AND m.log_date = ?
            """, (self.current_user_id, today))
            
            for row in c.fetchall():
                formatted_row = (row[0], f"{row[1]:.0f}", f"{row[2]:.1f}", f"{row[3]:.1f}", f"{row[4]:.1f}", f"{row[5]:.1f}")
                self.log_tree.insert('', tk.END, values=formatted_row)
                total_cal += row[2]; total_pro += row[3]; total_carb += row[4]; total_fat += row[5]
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch meal logs: {e}")
        finally:
            if conn: conn.close()
                
        self.today_total_cal = total_cal 
        self.summary_label.config(text=f"Today's Total: {self.today_total_cal:.0f} / {self.calorie_target:.0f} kcal")
        if total_cal > 0:
            summary_values = ('TOTAL', '-', f"{total_cal:.1f}", f"{total_pro:.1f}", f"{total_carb:.1f}", f"{total_fat:.1f}")
            self.log_tree.insert('', tk.END, values=summary_values, tags=('total_row',))
            self.log_tree.tag_configure('total_row', font=('Helvetica', 10, 'bold'))

    def get_food_recommendations(self):
        self.recommend_text.delete('1.0', tk.END)
        remaining_calories = self.calorie_target - self.today_total_cal
        if remaining_calories <= 0:
            self.recommend_text.insert(tk.END, "You've met your calorie target. Great job!"); return
        if remaining_calories > 500:
            target_meal_size = random.randint(350, 500); suggestion_type = "Meal"
        elif remaining_calories > 200:
            target_meal_size = random.randint(150, 250); suggestion_type = "Snack"
        else:
            target_meal_size = remaining_calories; suggestion_type = "Snack"
        self.recommend_text.insert(tk.END, f"Here are some {suggestion_type} ideas (approx. {target_meal_size:.0f} kcal):\n\n")
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT name, calories_per_100g, protein_per_100g FROM food_items WHERE calories_per_100g BETWEEN 50 AND 400 ORDER BY RANDOM() LIMIT 3")
            foods = c.fetchall()
            if not foods:
                self.recommend_text.insert(tk.END, "No food suggestions available."); conn.close(); return
            for name, cal_per_100g, pro_per_100g in foods:
                if cal_per_100g == 0: continue 
                suggested_qty = (target_meal_size / cal_per_100g) * 100
                suggested_pro = (pro_per_100g / 100) * suggested_qty
                self.recommend_text.insert(tk.END, f"• {suggested_qty:.0f}g of {name}\n")
                self.recommend_text.insert(tk.END, f"  (Approx. {target_meal_size:.0f} kcal, {suggested_pro:.1f}g protein)\n\n", ('detail',))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not fetch recommendations: {e}")
        finally:
            if conn: conn.close()

    # --- Progress Dashboard Functions (Unchanged) ---
    def show_progress_dashboard(self):
        self.clear_window()
        self.title("NutriScale - Progress Dashboard")
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(fill=tk.X)
        ttk.Label(top_frame, text="Progress Dashboard", font=("Helvetica", 16, "bold")).pack(side=tk.LEFT, padx=(0, 20))
        log_frame = ttk.Frame(top_frame)
        log_frame.pack(side=tk.LEFT)
        ttk.Label(log_frame, text="Log Today's Weight (kg):").pack(side=tk.LEFT, padx=5)
        self.weight_log_entry = ttk.Entry(log_frame, width=10)
        self.weight_log_entry.pack(side=tk.LEFT, padx=5)
        log_weight_button = ttk.Button(log_frame, text="Log Weight", command=self.log_today_weight)
        log_weight_button.pack(side=tk.LEFT, padx=5)
        back_button = ttk.Button(top_frame, text="Back to Main Dashboard", command=self.show_client_dashboard)
        back_button.pack(side=tk.RIGHT)
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=5)
        chart_frame = ttk.Frame(self, padding=10)
        chart_frame.pack(expand=True, fill=tk.BOTH)
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 7), tight_layout=True)
        self.chart_canvas_widget = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.chart_canvas_widget.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        self.plot_weight_progress()
        self.plot_calorie_progress()
        self.chart_canvas_widget.draw()

    def log_today_weight(self):
        try:
            weight = float(self.weight_log_entry.get())
            if weight <= 0: raise ValueError("Weight must be positive.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid weight (e.g., 70.5)."); return
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            today = date.today().isoformat()
            c.execute("""
                INSERT INTO weight_logs (user_id, weight_kg, log_date) VALUES (?, ?, ?)
                ON CONFLICT(user_id, log_date) DO UPDATE SET weight_kg = excluded.weight_kg
            """, (self.current_user_id, weight, today))
            conn.commit()
            messagebox.showinfo("Success", f"Today's weight of {weight}kg logged.")
            self.weight_log_entry.delete(0, tk.END)
            self.plot_weight_progress()
            self.chart_canvas_widget.draw()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not log weight: {e}")
        finally:
            if conn: conn.close()

    def plot_weight_progress(self):
        self.ax1.clear()
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT log_date, weight_kg FROM weight_logs WHERE user_id = ? ORDER BY log_date ASC LIMIT 30", (self.current_user_id,))
            data = c.fetchall()
            if len(data) < 2:
                self.ax1.set_title("Weight Progress")
                self.ax1.text(0.5, 0.5, "Log weight for 2+ days to see chart.", ha='center', va='center')
                conn.close(); return
            dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in data]
            weights = [row[1] for row in data]
            self.ax1.plot(dates, weights, marker='o', linestyle='-', color='b')
            self.ax1.set_title("Weight Progress (Last 30 Days)")
            self.ax1.set_ylabel("Weight (kg)")
            self.ax1.grid(True)
            self.ax1.xaxis.set_major_formatter(DateFormatter("%m-%d")) 
        except sqlite3.Error as e:
            messagebox.showerror("Chart Error", f"Could not plot weight data: {e}")
        finally:
            if conn: conn.close()

    def plot_calorie_progress(self):
        self.ax2.clear()
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("""
                SELECT m.log_date, SUM(f.calories_per_100g * m.quantity_grams / 100) as total_calories
                FROM meal_logs m JOIN food_items f ON m.food_id = f.id
                WHERE m.user_id = ? GROUP BY m.log_date ORDER BY m.log_date ASC LIMIT 30
            """, (self.current_user_id,))
            data = c.fetchall()
            if len(data) < 1:
                self.ax2.set_title("Calorie Intake")
                self.ax2.text(0.5, 0.5, "No meal data to plot.", ha='center', va='center')
                conn.close(); return
            dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in data]
            calories = [row[1] for row in data]
            self.ax2.bar(dates, calories, color='g', alpha=0.7, label="Calories Eaten")
            self.ax2.axhline(y=self.calorie_target, color='r', linestyle='--', label=f"Target: {self.calorie_target:.0f} kcal")
            self.ax2.set_title("Calorie Intake (Last 30 Days)")
            self.ax2.set_ylabel("Calories (kcal)")
            self.ax2.grid(True, axis='y')
            self.ax2.legend()
            self.ax2.xaxis.set_major_formatter(DateFormatter("%m-%d"))
        except sqlite3.Error as e:
            messagebox.showerror("Chart Error", f"Could not plot calorie data: {e}")
        finally:
            if conn: conn.close()

# --- Run the Application ---
if __name__ == "__main__":
    print("Checking database...")
    from database_setup import create_database
    create_database()
        
    app = NutriScaleApp()
    app.mainloop()