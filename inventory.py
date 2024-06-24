import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Authentication
def authenticate():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            users = json.load(file)
    else:
        users = {}

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", "Welcome!")
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def register():
        username = simpledialog.askstring("Register", "Enter a username:")
        password = simpledialog.askstring("Register", "Enter a password:", show='*')
        if username and password:
            users[username] = password
            with open("users.json", "w") as file:
                json.dump(users, file)
            messagebox.showinfo("Registration Successful", "You can now log in.")

    login_window = tk.Tk()
    login_window.title("Login")
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    tk.Button(login_window, text="Login", command=login).pack()
    tk.Button(login_window, text="Register", command=register).pack()
    login_window.mainloop()

authenticate()

# Main Inventory Management Application
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        
        # Inventory data
        self.inventory = {}
        if os.path.exists("inventory.json"):
            with open("inventory.json", "r") as file:
                self.inventory = json.load(file)
        
        # GUI setup
        self.setup_gui()
    
    def setup_gui(self):
        self.product_name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()

        tk.Label(self.root, text="Product Name").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.product_name_var).grid(row=0, column=1)
        tk.Label(self.root, text="Quantity").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.quantity_var).grid(row=1, column=1)
        tk.Label(self.root, text="Price").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.price_var).grid(row=2, column=1)
        tk.Button(self.root, text="Add Product", command=self.add_product).grid(row=3, column=0, columnspan=2)
        tk.Button(self.root, text="Edit Product", command=self.edit_product).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Delete Product", command=self.delete_product).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory).grid(row=6, column=0, columnspan=2)
        tk.Button(self.root, text="Low Stock Alert", command=self.low_stock_alert).grid(row=7, column=0, columnspan=2)

    def save_inventory(self):
        with open("inventory.json", "w") as file:
            json.dump(self.inventory, file)

    def add_product(self):
        product_name = self.product_name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()
        if product_name and quantity > 0 and price > 0:
            self.inventory[product_name] = {'quantity': quantity, 'price': price}
            self.save_inventory()
            messagebox.showinfo("Success", "Product added/updated successfully.")
        else:
            messagebox.showerror("Error", "Invalid input data.")

    def edit_product(self):
        product_name = self.product_name_var.get()
        if product_name in self.inventory:
            quantity = simpledialog.askinteger("Edit Product", "Enter new quantity:", initialvalue=self.inventory[product_name]['quantity'])
            price = simpledialog.askfloat("Edit Product", "Enter new price:", initialvalue=self.inventory[product_name]['price'])
            if quantity > 0 and price > 0:
                self.inventory[product_name] = {'quantity': quantity, 'price': price}
                self.save_inventory()
                messagebox.showinfo("Success", "Product edited successfully.")
            else:
                messagebox.showerror("Error", "Invalid input data.")
        else:
            messagebox.showerror("Error", "Product not found.")

    def delete_product(self):
        product_name = self.product_name_var.get()
        if product_name in self.inventory:
            del self.inventory[product_name]
            self.save_inventory()
            messagebox.showinfo("Success", "Product deleted successfully.")
        else:
            messagebox.showerror("Error", "Product not found.")

    def view_inventory(self):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventory")
        for i, (product_name, details) in enumerate(self.inventory.items()):
            tk.Label(inventory_window, text=f"Product: {product_name}, Quantity: {details['quantity']}, Price: {details['price']}").grid(row=i, column=0)

    def low_stock_alert(self):
        alert_window = tk.Toplevel(self.root)
        alert_window.title("Low Stock Alert")
        for i, (product_name, details) in enumerate(self.inventory.items()):
            if details['quantity'] < 10:
                tk.Label(alert_window, text=f"Low Stock: {product_name}, Quantity: {details['quantity']}").grid(row=i, column=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
