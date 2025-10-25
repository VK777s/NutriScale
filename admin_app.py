# File: admin_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AdminApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NutriScale Admin Panel")
        self.geometry("900x600") # Made wider for new column
        
        style = ttk.Style(self)
        style.theme_use('clam')
        
        notebook = ttk.Notebook(self)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text='Food Database Management')
        notebook.add(tab2, text='User Management')
        notebook.pack(expand=True, fill='both')

        self.create_food_tab(tab1)
        self.create_user_tab(tab2)
        
        self.load_food_database()
        self.load_users()

    # ==========================================
    # ========= TAB 1: FOOD MANAGEMENT =========
    # ==========================================
    
    def create_food_tab(self, parent_tab):
        # (This function is unchanged)
        form_frame = ttk.LabelFrame(parent_tab, text="Add / Edit Food Item (per 100g)", padding=15)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(form_frame, text="Food Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Calories:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.cal_entry = ttk.Entry(form_frame, width=10)
        self.cal_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(form_frame, text="Protein (g):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.pro_entry = ttk.Entry(form_frame, width=10)
        self.pro_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(form_frame, text="Carbs (g):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.carb_entry = ttk.Entry(form_frame, width=10)
        self.carb_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(form_frame, text="Fats (g):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fat_entry = ttk.Entry(form_frame, width=10)
        self.fat_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.selected_food_id = None
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=0, column=2, rowspan=5, padx=20, sticky=tk.N)
        add_btn = ttk.Button(button_frame, text="Add New Food", command=self.add_food)
        add_btn.pack(fill=tk.X, pady=5, ipady=4)
        update_btn = ttk.Button(button_frame, text="Update Selected", command=self.update_food)
        update_btn.pack(fill=tk.X, pady=5, ipady=4)
        delete_btn = ttk.Button(button_frame, text="Delete Selected", command=self.delete_food)
        delete_btn.pack(fill=tk.X, pady=5, ipady=4)
        clear_btn = ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields)
        clear_btn.pack(fill=tk.X, pady=5, ipady=4)
        tree_frame = ttk.LabelFrame(parent_tab, text="Food Database", padding=15)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        cols = ('ID', 'Name', 'Calories', 'Protein', 'Carbs', 'Fats')
        self.food_tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=10)
        for col in cols: self.food_tree.heading(col, text=col)
        self.food_tree.column('ID', width=40, anchor=tk.CENTER)
        self.food_tree.column('Name', width=200)
        self.food_tree.column('Calories', width=80, anchor=tk.E)
        self.food_tree.column('Protein', width=80, anchor=tk.E)
        self.food_tree.column('Carbs', width=80, anchor=tk.E)
        self.food_tree.column('Fats', width=80, anchor=tk.E)
        self.food_tree.pack(expand=True, fill=tk.BOTH)
        self.food_tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    # --- Food helper functions (Unchanged) ---
    def get_form_data(self):
        try:
            name = self.name_entry.get()
            if not name: raise ValueError("Name is required.")
            calories = float(self.cal_entry.get())
            protein = float(self.pro_entry.get())
            carbs = float(self.carb_entry.get())
            fats = float(self.fat_entry.get())
            return name, calories, protein, carbs, fats
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}\nPlease check all fields.")
            return None
    def load_food_database(self):
        for item in self.food_tree.get_children(): self.food_tree.delete(item)
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("SELECT id, name, calories_per_100g, protein_per_100g, carbs_per_100g, fats_per_100g FROM food_items ORDER BY name ASC")
            for row in c.fetchall():
                formatted_row = (row[0], row[1], f"{row[2]:.1f}", f"{row[3]:.1f}", f"{row[4]:.1f}", f"{row[5]:.1f}")
                self.food_tree.insert('', tk.END, values=formatted_row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load food database: {e}")
        finally:
            if conn: conn.close()
        self.clear_fields()
    def add_food(self):
        data = self.get_form_data()
        if data is None: return
        name, calories, protein, carbs, fats = data
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("INSERT INTO food_items (name, calories_per_100g, protein_per_100g, carbs_per_100g, fats_per_100g) VALUES (?, ?, ?, ?, ?)",
                      (name, calories, protein, carbs, fats))
            conn.commit()
            messagebox.showinfo("Success", f"'{name}' added to the database.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"A food item with the name '{name}' already exists.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not add food: {e}")
        finally:
            if conn: conn.close()
        self.load_food_database()
    def update_food(self):
        if self.selected_food_id is None:
            messagebox.showerror("Error", "No food item selected."); return
        data = self.get_form_data()
        if data is None: return
        name, calories, protein, carbs, fats = data
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("UPDATE food_items SET name = ?, calories_per_100g = ?, protein_per_100g = ?, carbs_per_100g = ?, fats_per_100g = ? WHERE id = ?",
                      (name, calories, protein, carbs, fats, self.selected_food_id))
            conn.commit()
            messagebox.showinfo("Success", f"'{name}' updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not update food: {e}")
        finally:
            if conn: conn.close()
        self.load_food_database()
    def delete_food(self):
        if self.selected_food_id is None:
            messagebox.showerror("Error", "No food item selected."); return
        name = self.name_entry.get()
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            return
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("DELETE FROM food_items WHERE id = ?", (self.selected_food_id,))
            conn.commit()
            messagebox.showinfo("Success", f"'{name}' was deleted.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not delete food: {e}")
        finally:
            if conn: conn.close()
        self.load_food_database()
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.cal_entry.delete(0, tk.END)
        self.pro_entry.delete(0, tk.END)
        self.carb_entry.delete(0, tk.END)
        self.fat_entry.delete(0, tk.END)
        self.selected_food_id = None
        if self.food_tree.selection():
            self.food_tree.selection_remove(self.food_tree.selection()[0])
    def on_tree_select(self, event):
        try:
            selected_item = self.food_tree.selection()[0]
            item_data = self.food_tree.item(selected_item, 'values')
            food_id, name, cal, pro, carb, fat = item_data
            self.clear_fields()
            self.selected_food_id = int(food_id)
            self.name_entry.insert(0, name)
            self.cal_entry.insert(0, cal)
            self.pro_entry.insert(0, pro)
            self.carb_entry.insert(0, carb)
            self.fat_entry.insert(0, fat)
        except IndexError:
            pass

    # ========================================
    # ========= TAB 2: USER MANAGEMENT =========
    # ========================================
    
    # --- MODIFIED: create_user_tab ---
    def create_user_tab(self, parent_tab):
        """Creates all widgets for the user management tab."""
        frame = ttk.Frame(parent_tab, padding=10)
        frame.pack(expand=True, fill='both')
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill='x', pady=5)
        ttk.Label(top_frame, text="All Registered Users", font=("Helvetica", 14, "bold")).pack(side=tk.LEFT)
        refresh_btn = ttk.Button(top_frame, text="Refresh List", command=self.load_users)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        delete_btn = ttk.Button(top_frame, text="Delete Selected User", command=self.delete_user)
        delete_btn.pack(side=tk.RIGHT, padx=5)

        tree_frame = ttk.Frame(frame)
        tree_frame.pack(expand=True, fill='both', pady=10)
        
        # --- NEW Column 'Username' ---
        cols = ('ID', 'Username', 'Name', 'Age', 'Gender', 'Current (kg)', 'Target (kg)', 'Cal Target')
        self.user_tree = ttk.Treeview(tree_frame, columns=cols, show='headings')
        
        for col in cols: self.user_tree.heading(col, text=col)
        self.user_tree.column('ID', width=40, anchor=tk.CENTER)
        self.user_tree.column('Username', width=100)
        self.user_tree.column('Name', width=120)
        self.user_tree.column('Age', width=40, anchor=tk.CENTER)
        self.user_tree.column('Gender', width=60)
        self.user_tree.column('Current (kg)', width=80, anchor=tk.E)
        self.user_tree.column('Target (kg)', width=80, anchor=tk.E)
        self.user_tree.column('Cal Target', width=80, anchor=tk.E)

        self.user_tree.pack(expand=True, fill='both')

    # --- MODIFIED: load_users ---
    def load_users(self):
        """Clears and reloads all users from the DB into the user tree."""
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            # --- Updated SELECT query ---
            c.execute("""
                SELECT id, username, name, age, gender, 
                       current_weight_kg, target_weight_kg, calorie_target 
                FROM users ORDER BY username ASC
            """)
            for row in c.fetchall():
                # Format numbers for display
                formatted_row = list(row)
                formatted_row[5] = f"{row[5]:.1f}" # Current Wt
                formatted_row[6] = f"{row[6]:.1f}" # Target Wt
                formatted_row[7] = f"{row[7]:.0f}" # Calorie Target
                self.user_tree.insert('', tk.END, values=formatted_row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load users: {e}")
        finally:
            if conn: conn.close()

    # --- MODIFIED: delete_user (to get correct user_name) ---
    def delete_user(self):
        """Deletes a selected user AND all their associated logs."""
        try:
            selected_item = self.user_tree.selection()[0]
            item_data = self.user_tree.item(selected_item, 'values')
            user_id = item_data[0]
            user_name = item_data[1] # Using username for confirm message
        except IndexError:
            messagebox.showerror("Error", "No user selected. Please click a user in the list to delete.")
            return

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user_name}' (ID: {user_id})?\n\nThis will also delete ALL their meal logs and weight history.\nThis action is permanent and cannot be undone."):
            return

        try:
            conn = sqlite3.connect('nutriscale.db')
            c = conn.cursor()
            c.execute("DELETE FROM meal_logs WHERE user_id = ?", (user_id,))
            c.execute("DELETE FROM weight_logs WHERE user_id = ?", (user_id,))
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            messagebox.showinfo("Success", f"User '{user_name}' and all their data has been deleted.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not delete user: {e}")
        finally:
            if conn: conn.close()
        
        self.load_users()

# --- Run the Application ---
if __name__ == "__main__":
    try:
        open('nutriscale.db')
    except FileNotFoundError:
        print("Database not found! Please run database_setup.py first.")
    app = AdminApp()
    app.mainloop()