from sweets.inventory import InventoryManager
from sweets.sweet import Sweet

inventory = InventoryManager()

def print_menu():
    print("\n===== Sweet Shop Management =====")
    print("1. Add Sweet")
    print("2. View All Sweets")
    print("3. Delete Sweet")
    print("4. Restock Sweet")
    print("5. Search Sweets")
    print("6. Purchase Sweet")
    print("0. Exit")

def add_sweet():
    try:
        id = int(input("Enter Sweet ID: "))
        name = input("Enter Sweet Name: ")
        category = input("Enter Category (e.g., Chocolate, Pastry): ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        sweet = Sweet(id, name, category, price, quantity)
        inventory.add_sweet(sweet)
        print("Sweet added successfully.")
    except ValueError as e:
        print("Error:", e)

def view_sweets():
    sweets = inventory.get_all_sweets()
    if not sweets:
        print("No sweets available.")
    else:
        print("\n--- Available Sweets ---")
        for sweet in sweets:
            print(sweet)

def delete_sweet():
    id = int(input("Enter Sweet ID to delete: "))
    inventory.delete_sweet(id)
    print(" Sweet deleted (if ID existed).")

def restock_sweet():
    id = int(input("Enter Sweet ID to restock: "))
    quantity = int(input("Enter quantity to add: "))
    try:
        inventory.restock_sweet(id, quantity)
        print(" Sweet restocked.")
    except ValueError as e:
        print("Error:", e)

def search_sweets():
    print("Search by:")
    print("1. Name")
    print("2. Category")
    print("3. Price Range")
    choice = input("Enter choice: ")
    
    if choice == "1":
        name = input("Enter sweet name to search: ")
        results = inventory.search_by_name(name)
    elif choice == "2":
        category = input("Enter category to search: ")
        results = inventory.search_by_category(category)
    elif choice == "3":
        min_price = float(input("Enter min price: "))
        max_price = float(input("Enter max price: "))
        results = inventory.search_by_price_range(min_price, max_price)
    else:
        print("Invalid choice.")
        return

    if not results:
        print("🔍 No matching sweets found.")
    else:
        print("\n--- Search Results ---")
        for sweet in results:
            print(sweet)

def purchase_sweet():
    id = int(input("Enter Sweet ID to purchase: "))
    quantity = int(input("Enter quantity to purchase: "))
    try:
        inventory.purchase_sweet(id, quantity)
        print(" Purchase successful.")
    except ValueError as e:
        print("Error:", e)

# ==== Main Loop ====
while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        add_sweet()
    elif choice == "2":
        view_sweets()
    elif choice == "3":
        delete_sweet()
    elif choice == "4":
        restock_sweet()
    elif choice == "5":
        search_sweets()
    elif choice == "6":
        purchase_sweet()
    elif choice == "0":
        print("Exiting Sweet Shop System. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

    def purchase_sweet():
        id = int(input("Enter Sweet ID to purchase: "))
        quantity = int(input("Enter quantity to purchase: "))
        try:
            inventory.purchase_sweet(id, quantity)
            print("Purchase successful.")
        except ValueError as e:
            print("Error:", e)

