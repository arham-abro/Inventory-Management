import json
import os

# Directory and file for storing inventory and revenue
DATA_DIR = "V2"
DATA_FILE = os.path.join(DATA_DIR, "inventory_data.json")

def ensure_data_folder():
    """Ensure the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_data():
    """Load inventory and revenue from the JSON file."""
    ensure_data_folder()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"inventory": {}, "total_revenue": 0.0}

def save_data(data):
    """Save inventory and revenue to the JSON file."""
    ensure_data_folder()
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def main():
    data = load_data()
    inventory = data["inventory"]
    total_revenue = data["total_revenue"]

    def add_product():
        product_name = input("Enter product name: ")
        category = input("Enter category (e.g., electronics, clothing): ")
        try:
            price = float(input("Enter price of product: "))
            stock = int(input("Enter initial stock quantity: "))
        except ValueError:
            print("Invalid input for price or stock. Please try again.")
            return
        if product_name in inventory:
            print(f"Product {product_name} already exists in inventory!")
        else:
            inventory[product_name] = {'category': category, 'price': price, 'stock': stock}
            print(f"Product {product_name} added successfully!")
            save_data(data)

    def view_products():
        if not inventory:
            print("Inventory is empty.")
        else:
            for name, details in inventory.items():
                print(f"{name}: Category: {details['category']}, Price: {details['price']}, Stock: {details['stock']}")

    def update_stock():
        product_name = input("Enter product name to update stock: ")
        if product_name not in inventory:
            print(f"Product {product_name} not found in inventory.")
            return
        try:
            quantity_change = int(input("Enter quantity to add/subtract: "))
            inventory[product_name]['stock'] += quantity_change
            print(f"Updated stock for {product_name}: {inventory[product_name]['stock']}")
            save_data(data)
        except ValueError:
            print("Invalid input for quantity. Please enter a valid number.")

    def update_price():
        product_name = input("Enter product name to update price: ")
        if product_name not in inventory:
            print(f"Product {product_name} not found in inventory.")
            return
        try:
            new_price = float(input("Enter new price: "))
            inventory[product_name]['price'] = new_price
            print(f"Updated price for {product_name}: {inventory[product_name]['price']}")
            save_data(data)
        except ValueError:
            print("Invalid input for price. Please enter a valid number.")

    def process_sale():
        nonlocal total_revenue
        product_name = input("Enter product name to purchase: ")
        if product_name not in inventory:
            print(f"Product {product_name} not found in inventory.")
            return
        try:
            quantity = int(input("Enter quantity to purchase: "))
            if quantity <= 0:
                print("Quantity should be greater than zero.")
                return
            stock = inventory[product_name]['stock']
            price = inventory[product_name]['price']
            if quantity > stock:
                print(f"Insufficient stock for {product_name}. Available stock: {stock}.")
                return
            total_cost = price * quantity
            inventory[product_name]['stock'] -= quantity
            total_revenue += total_cost
            print(f"Sale successful! Total cost: {total_cost:.2f}")
            # Update total revenue in data and save it
            data["total_revenue"] = total_revenue
            save_data(data)
        except ValueError:
            print("Invalid input for quantity. Please enter a valid number.")

    def view_revenue():
        print(f"Total revenue: {total_revenue:.2f}")

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Add a new product")
        print("2. View all products")
        print("3. Update stock")
        print("4. Update price")
        print("5. Process a sale")
        print("6. View total revenue")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_stock()
        elif choice == '4':
            update_price()
        elif choice == '5':
            process_sale()
        elif choice == '6':
            view_revenue()
        elif choice == '7':
            print("Saving data and exiting the system...")
            data["total_revenue"] = total_revenue  # Save final revenue before exiting
            save_data(data)
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
