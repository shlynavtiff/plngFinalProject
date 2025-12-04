import csv
import os
from datetime import datetime

menu_items = {}
item_counter = 1

VALID_CATEGORIES = ["Appetizer", "Main Dish", "Dessert", "Beverage"]
VALID_STATUS = ["Available", "Out of Stock"]


def save_menu_to_csv(filename="menu_items.csv"):
    """Save all menu items to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "item_id",
                    "item_name",
                    "category",
                    "price",
                    "prep_time",
                    "status",
                    "description",
                ]
            )

            for item_id, item in menu_items.items():
                writer.writerow(
                    [
                        item["item_id"],
                        item["item_name"],
                        item["category"],
                        item["price"],
                        item["prep_time"],
                        item["status"],
                        item["description"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving menu: {e}")
        return False


def load_menu_from_csv(filename="menu_items.csv"):
    """Load menu items from CSV file"""
    global menu_items, item_counter

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with empty menu.")
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            menu_items = {}
            max_item_id = 0

            for row in reader:
                item_id = int(row["item_id"])
                max_item_id = max(max_item_id, item_id)

                menu_items[item_id] = {
                    "item_id": item_id,
                    "item_name": row["item_name"],
                    "category": row["category"],
                    "price": float(row["price"]),
                    "prep_time": int(row["prep_time"]),
                    "status": row["status"],
                    "description": row["description"],
                }

            item_counter = max_item_id + 1

        print(f"Loaded {len(menu_items)} menu items from {filename}")
        return True
    except Exception as e:
        print(f"Error loading menu: {e}")
        return False


def add_menu_item(
    item_name, category, price, prep_time=10, description="", status="Available"
):
    """

    Args:
        item_name: Name of the food/beverage
        category: Category (Appetizer, Main Dish, Dessert, Beverage)
        price: Price in pesos
        prep_time: Preparation time in minutes (default: 10)
        description: Item description
        status: Available or Out of Stock

    """
    global menu_items, item_counter

    if not item_name or not category:
        print("Item name and category are required")
        return None

    if category not in VALID_CATEGORIES:
        print(f"Invalid category. Must be: {', '.join(VALID_CATEGORIES)}")
        return None

    if price <= 0:
        print("Price must be greater than 0")
        return None

    if status not in VALID_STATUS:
        print(f"Invalid status. Must be: {', '.join(VALID_STATUS)}")
        return None

    item_id = item_counter
    item_counter += 1

    menu_items[item_id] = {
        "item_id": item_id,
        "item_name": item_name,
        "category": category,
        "price": price,
        "prep_time": prep_time,
        "status": status,
        "description": description,
    }

    save_menu_to_csv()
    print(f"Menu item '{item_name}' added successfully! (ID: {item_id})")
    return item_id


def update_menu_item(item_id, new_details):
    global menu_items

    if item_id not in menu_items:
        print(f"Menu item ID {item_id} not found")
        return False

    item = menu_items[item_id]

    if "item_name" in new_details:
        item["item_name"] = new_details["item_name"]

    if "category" in new_details:
        if new_details["category"] not in VALID_CATEGORIES:
            print(f"Invalid category. Must be: {', '.join(VALID_CATEGORIES)}")
            return False
        item["category"] = new_details["category"]

    if "price" in new_details:
        if new_details["price"] <= 0:
            print("Price must be greater than 0")
            return False
        item["price"] = new_details["price"]

    if "prep_time" in new_details:
        item["prep_time"] = new_details["prep_time"]

    if "status" in new_details:
        if new_details["status"] not in VALID_STATUS:
            print(f"Invalid status. Must be: {', '.join(VALID_STATUS)}")
            return False
        item["status"] = new_details["status"]

    if "description" in new_details:
        item["description"] = new_details["description"]

    save_menu_to_csv()
    print(f"Menu item ID {item_id} updated successfully!")
    return True


def delete_menu_item(item_id):
    global menu_items

    if item_id not in menu_items:
        print(f"❌ Menu item ID {item_id} not found")
        return False

    item_name = menu_items[item_id]["item_name"]
    del menu_items[item_id]

    save_menu_to_csv()
    print(f"Menu item '{item_name}' deleted successfully!")
    return True


def get_menu_item(item_id):
    if item_id not in menu_items:
        print(f"❌ Menu item ID {item_id} not found")
        return None

    return menu_items[item_id]


def get_item_price(item_id):
    if item_id not in menu_items:
        return None
    return menu_items[item_id]["price"]


def get_available_menu():
    available = {}
    for item_id, item in menu_items.items():
        if item["status"] == "Available":
            available[item_id] = item
    return available


def get_menu_by_category(category):
    if category not in VALID_CATEGORIES:
        print(f"❌ Invalid category. Must be: {', '.join(VALID_CATEGORIES)}")
        return {}

    filtered = {}
    for item_id, item in menu_items.items():
        if item["category"] == category:
            filtered[item_id] = item
    return filtered


def search_menu(keyword):
    results = {}
    keyword_lower = keyword.lower()

    for item_id, item in menu_items.items():
        if (
            keyword_lower in item["item_name"].lower()
            or keyword_lower in item["description"].lower()
        ):
            results[item_id] = item

    return results


def set_item_status(item_id, status):
    if item_id not in menu_items:
        print(f"Menu item ID {item_id} not found")
        return False

    if status not in VALID_STATUS:
        print(f"Invalid status. Must be: {', '.join(VALID_STATUS)}")
        return False

    menu_items[item_id]["status"] = status
    save_menu_to_csv()

    print(f"Item '{menu_items[item_id]['item_name']}' is now {status}")
    return True


def display_menu(items_dict=None):
    """Display menu items in a formatted table"""
    if items_dict is None:
        items_dict = menu_items

    print("\n" + "=" * 100)
    print(
        f"{'ID':<5} {'Name':<25} {'Category':<15} {'Price':<10} {'Prep Time':<12} {'Status':<15}"
    )
    print("=" * 100)

    if not items_dict:
        print("No items found.")
    else:
        for item_id, item in items_dict.items():
            status_icon = "🟢" if item["status"] == "Available" else "🔴"
            print(
                f"{item['item_id']:<5} {item['item_name']:<25} {item['category']:<15} "
                f"₱{item['price']:<9.2f} {item['prep_time']} mins{'':<6} {status_icon} {item['status']:<10}"
            )

    print("=" * 100)


def display_menu_details(item_id):
    """Display detailed information about a menu item"""
    if item_id not in menu_items:
        print(f"Menu item ID {item_id} not found")
        return

    item = menu_items[item_id]

    print("\n" + "=" * 60)
    print(f"MENU ITEM DETAILS")
    print("=" * 60)
    print(f"ID: {item['item_id']}")
    print(f"Name: {item['item_name']}")
    print(f"Category: {item['category']}")
    print(f"Price: ₱{item['price']:.2f}")
    print(f"Preparation Time: {item['prep_time']} minutes")
    print(f"Status: {item['status']}")
    print(f"Description: {item['description'] if item['description'] else 'N/A'}")
    print("=" * 60)


def display_categories():
    print("\nMENU BY CATEGORY")

    for category in VALID_CATEGORIES:
        items = get_menu_by_category(category)
        if items:
            print(f"\n{'='*100}")
            print(f"📁 {category.upper()}")
            print(f"{'='*100}")
            display_menu(items)


def interactive_test():
    """Interactive testing menu"""
    load_menu_from_csv()

    while True:
        print("\n=== MENU MANAGEMENT SYSTEM ===")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. View All Menu Items")
        print("5. View Available Items Only")
        print("6. View by Category")
        print("7. Search Menu")
        print("8. Change Item Status")
        print("9. View Item Details")
        print("10. Exit")
        print("\nAuto-save: ON")

        choice = input("\nEnter choice: ")

        if choice == "1":
            print("\n--- Add Menu Item ---")
            item_name = input("Item Name: ")

            print(f"Categories: {', '.join(VALID_CATEGORIES)}")
            category = input("Category: ").title()

            try:
                price = float(input("Price (₱): "))
                prep_time = int(input("Preparation Time (minutes): ") or "10")
            except ValueError:
                print("Invalid number format")
                continue

            description = input("Description (optional): ")

            add_menu_item(item_name, category, price, prep_time, description)

        elif choice == "2":
            display_menu()
            try:
                item_id = int(input("\nItem ID to update: "))
            except ValueError:
                print("Invalid ID")
                continue

            if item_id not in menu_items:
                print(f"Item ID {item_id} not found")
                continue

            print("\n--- Update Menu Item (leave blank to keep current) ---")
            item = menu_items[item_id]

            new_details = {}

            name = input(f"Item Name (current: {item['item_name']}): ")
            if name:
                new_details["item_name"] = name

            print(f"Categories: {', '.join(VALID_CATEGORIES)}")
            category = input(f"Category (current: {item['category']}): ").title()
            if category:
                new_details["category"] = category

            price = input(f"Price (current: ₱{item['price']}): ")
            if price:
                try:
                    new_details["price"] = float(price)
                except ValueError:
                    print("Invalid price")

            prep = input(f"Prep Time (current: {item['prep_time']} mins): ")
            if prep:
                try:
                    new_details["prep_time"] = int(prep)
                except ValueError:
                    print("Invalid prep time")

            desc = input(f"Description (current: {item['description']}): ")
            if desc:
                new_details["description"] = desc

            if new_details:
                update_menu_item(item_id, new_details)
            else:
                print("No changes made")

        elif choice == "3":
            display_menu()
            try:
                item_id = int(input("\nItem ID to delete: "))
                confirm = input(
                    f"Delete '{menu_items.get(item_id, {}).get('item_name', 'Unknown')}'? (yes/no): "
                )
                if confirm.lower() == "yes":
                    delete_menu_item(item_id)
            except ValueError:
                print("Invalid ID")

        elif choice == "4":
            display_menu()

        elif choice == "5":
            available = get_available_menu()
            print(f"\n🟢 AVAILABLE ITEMS ({len(available)})")
            display_menu(available)

        elif choice == "6":
            print(f"\nCategories: {', '.join(VALID_CATEGORIES)}")
            category = input("Select category: ").title()
            items = get_menu_by_category(category)
            display_menu(items)

        elif choice == "7":
            keyword = input("\nSearch keyword: ")
            results = search_menu(keyword)
            print(f"\nSearch Results for '{keyword}' ({len(results)} found)")
            display_menu(results)

        elif choice == "8":
            display_menu()
            try:
                item_id = int(input("\nItem ID: "))
                print(f"Status options: {', '.join(VALID_STATUS)}")
                status = input("New Status: ").title()
                set_item_status(item_id, status)
            except ValueError:
                print("Invalid ID")

        elif choice == "9":
            display_menu()
            try:
                item_id = int(input("\nItem ID: "))
                display_menu_details(item_id)
            except ValueError:
                print("Invalid ID")

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1-10.")


if __name__ == "__main__":
    interactive_test()
