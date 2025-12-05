import csv
import os
from datetime import datetime, timedelta

inventory = {}
inventory_counter = 1
usage_log = []

UNITS = ["kg", "g", "L", "ml", "pcs", "packs"]


def save_inventory_to_csv(filename="inventory.csv"):
    """Save all inventory items to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "item_id",
                    "item_name",
                    "quantity",
                    "unit",
                    "supplier",
                    "expiration_date",
                    "reorder_level",
                    "last_updated",
                ]
            )

            for item_id, item in inventory.items():
                writer.writerow(
                    [
                        item["item_id"],
                        item["item_name"],
                        item["quantity"],
                        item["unit"],
                        item["supplier"],
                        item["expiration_date"],
                        item["reorder_level"],
                        item["last_updated"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False


def load_inventory_from_csv(filename="inventory.csv"):
    """Load inventory items from CSV file"""
    global inventory, inventory_counter

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting with empty inventory.")
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            inventory = {}
            max_item_id = 0

            for row in reader:
                item_id = int(row["item_id"])
                max_item_id = max(max_item_id, item_id)

                inventory[item_id] = {
                    "item_id": item_id,
                    "item_name": row["item_name"],
                    "quantity": float(row["quantity"]),
                    "unit": row["unit"],
                    "supplier": row["supplier"],
                    "expiration_date": row["expiration_date"],
                    "reorder_level": float(row["reorder_level"]),
                    "last_updated": row["last_updated"],
                }

            inventory_counter = max_item_id + 1

        print(f"Loaded {len(inventory)} inventory items from {filename}")
        return True
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return False


def save_usage_log_to_csv(filename="inventory_usage.csv"):
    """Save inventory usage log to CSV"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["timestamp", "item_name", "quantity_used", "reason", "remaining"]
            )

            for log in usage_log:
                writer.writerow(
                    [
                        log["timestamp"],
                        log["item_name"],
                        log["quantity_used"],
                        log["reason"],
                        log["remaining"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving usage log: {e}")
        return False


def load_usage_log_from_csv(filename="inventory_usage.csv"):
    """Load usage log from CSV"""
    global usage_log

    if not os.path.exists(filename):
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            usage_log = []

            for row in reader:
                usage_log.append(
                    {
                        "timestamp": row["timestamp"],
                        "item_name": row["item_name"],
                        "quantity_used": float(row["quantity_used"]),
                        "reason": row["reason"],
                        "remaining": float(row["remaining"]),
                    }
                )

        return True
    except Exception as e:
        print(f"Error loading usage log: {e}")
        return False


def add_stock(
    item_name, quantity, unit, supplier, expiration_date=None, reorder_level=10
):
    """
    Add a new inventory item

    Args:
        item_name: Name of the ingredient/item
        quantity: Initial quantity
        unit: Unit of measurement (kg, g, L, ml, pcs, packs)
        supplier: Supplier name
        expiration_date: Expiration date (YYYY-MM-DD) or None
        reorder_level: Minimum quantity before alert

    """
    global inventory, inventory_counter

    if not item_name:
        print("Item name is required")
        return None

    if unit not in UNITS:
        print(f"Invalid unit. Must be: {', '.join(UNITS)}")
        return None

    if quantity < 0:
        print("Quantity cannot be negative")
        return None

    for item_id, item in inventory.items():
        if item["item_name"].lower() == item_name.lower():
            print(f"Item '{item_name}' already exists. Use update_stock() instead.")
            return None

    item_id = inventory_counter
    inventory_counter += 1

    inventory[item_id] = {
        "item_id": item_id,
        "item_name": item_name,
        "quantity": quantity,
        "unit": unit,
        "supplier": supplier,
        "expiration_date": expiration_date or "N/A",
        "reorder_level": reorder_level,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    save_inventory_to_csv()
    print(f"Inventory item '{item_name}' added successfully! (ID: {item_id})")
    return item_id


def update_stock(item_name, quantity_change, reason="Manual adjustment"):
    """
    Update stock quantity (add or deduct)

    Args:
        item_name: Name of the item
        quantity_change: Amount to add (positive) or deduct (negative)
        reason: Reason for the change

    """
    global inventory

    # Find item by name
    item_id = None
    for id, item in inventory.items():
        if item["item_name"].lower() == item_name.lower():
            item_id = id
            break

    if item_id is None:
        print(f"Item '{item_name}' not found in inventory")
        return False

    item = inventory[item_id]
    new_quantity = item["quantity"] + quantity_change

    if new_quantity < 0:
        print(
            f"Cannot deduct {abs(quantity_change)} {item['unit']}. Only {item['quantity']} {item['unit']} available."
        )
        return False

    item["quantity"] = new_quantity
    item["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_usage(item_name, abs(quantity_change), reason, new_quantity)

    save_inventory_to_csv()
    save_usage_log_to_csv()

    action = "Added" if quantity_change > 0 else "Deducted"
    print(
        f"{action} {abs(quantity_change)} {item['unit']} of '{item_name}'. New quantity: {new_quantity} {item['unit']}"
    )

    if new_quantity <= item["reorder_level"]:
        print(f"LOW STOCK ALERT: '{item_name}' is at or below reorder level!")

    return True


def deduct_stock(item_name, quantity_used, reason="Order processed"):
    """
    Deduct stock (wrapper for update_stock with negative value)

    Args:
        item_name: Name of the item
        quantity_used: Amount to deduct
        reason: Reason for deduction

    """
    return update_stock(item_name, -quantity_used, reason)


def add_to_stock(item_name, quantity_added, reason="Stock replenishment"):
    """
    Add to existing stock (wrapper for update_stock with positive value)

    Args:
        item_name: Name of the item
        quantity_added: Amount to add
        reason: Reason for addition

    """
    return update_stock(item_name, quantity_added, reason)


def check_reorder_level():
    """
    Check all items and return those at or below reorder level

    """
    low_stock = {}

    for item_id, item in inventory.items():
        if item["quantity"] <= item["reorder_level"]:
            low_stock[item_id] = item

    return low_stock


def get_stock_quantity(item_name):
    """
    Get current quantity of an item

    Args:
        item_name: Name of the item

    """
    for item in inventory.values():
        if item["item_name"].lower() == item_name.lower():
            return item["quantity"]
    return None


def set_reorder_level(item_name, new_level):
    """
    Set reorder level for an item

    Args:
        item_name: Name of the item
        new_level: New reorder level

    """
    for item in inventory.values():
        if item["item_name"].lower() == item_name.lower():
            item["reorder_level"] = new_level
            save_inventory_to_csv()
            print(f"Reorder level for '{item_name}' set to {new_level} {item['unit']}")
            return True

    print(f"Item '{item_name}' not found")
    return False


def check_expiring_soon(days=7):
    expiring = {}
    today = datetime.now()
    check_date = today + timedelta(days=days)

    for item_id, item in inventory.items():
        if item["expiration_date"] != "N/A":
            try:
                exp_date = datetime.strptime(item["expiration_date"], "%Y-%m-%d")
                if today <= exp_date <= check_date:
                    expiring[item_id] = item
            except ValueError:
                pass

    return expiring


def log_usage(item_name, quantity_used, reason, remaining):
    global usage_log

    usage_log.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "item_name": item_name,
            "quantity_used": quantity_used,
            "reason": reason,
            "remaining": remaining,
        }
    )


def generate_inventory_report():
    """Generate and display inventory report"""
    print("\n" + "=" * 100)
    print("📊 INVENTORY REPORT")
    print("=" * 100)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Items: {len(inventory)}")

    low_stock = check_reorder_level()
    print(f"\nLow Stock Items: {len(low_stock)}")
    if low_stock:
        for item in low_stock.values():
            print(
                f"  - {item['item_name']}: {item['quantity']} {item['unit']} (Reorder at: {item['reorder_level']})"
            )

    expiring = check_expiring_soon(7)
    print(f"\nItems Expiring in 7 Days: {len(expiring)}")
    if expiring:
        for item in expiring.values():
            print(f"  - {item['item_name']}: Expires {item['expiration_date']}")

    # Total inventory value (if you want to add prices later)
    print("\n" + "=" * 100)


def display_inventory():
    """Display all inventory items"""
    print("\n" + "=" * 110)
    print(
        f"{'ID':<5} {'Item Name':<25} {'Quantity':<12} {'Unit':<8} {'Supplier':<20} {'Reorder Level':<15}"
    )
    print("=" * 110)

    if not inventory:
        print("No inventory items found.")
    else:
        for item in inventory.values():
            status_icon = "⚠️" if item["quantity"] <= item["reorder_level"] else "✅"
            print(
                f"{item['item_id']:<5} {item['item_name']:<25} "
                f"{status_icon} {item['quantity']:<9.2f} {item['unit']:<8} "
                f"{item['supplier']:<20} {item['reorder_level']:<15.2f}"
            )

    print("=" * 110)


def display_usage_log(limit=20):
    """Display recent usage log"""
    print(f"\nRECENT INVENTORY USAGE (Last {limit})")
    print("=" * 100)
    print(
        f"{'Timestamp':<20} {'Item':<25} {'Used':<12} {'Remaining':<12} {'Reason':<30}"
    )
    print("=" * 100)

    if not usage_log:
        print("No usage logged yet.")
    else:
        for log in usage_log[-limit:]:
            print(
                f"{log['timestamp']:<20} {log['item_name']:<25} "
                f"{log['quantity_used']:<12.2f} {log['remaining']:<12.2f} {log['reason']:<30}"
            )

    print("=" * 100)


def interactive_test():
    """Interactive testing menu"""
    load_inventory_from_csv()
    load_usage_log_from_csv()

    while True:
        print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
        print("1. Add New Stock Item")
        print("2. Update Stock Quantity")
        print("3. View All Inventory")
        print("4. Check Low Stock Alerts")
        print("5. Check Expiring Items")
        print("6. Set Reorder Level")
        print("7. View Usage Log")
        print("8. Generate Inventory Report")
        print("9. Exit")
        print("\nAuto-save: ON")

        choice = input("\nEnter choice: ")

        if choice == "1":
            print("\n--- Add New Stock Item ---")
            item_name = input("Item Name: ")

            try:
                quantity = float(input("Initial Quantity: "))
            except ValueError:
                print("Invalid quantity")
                continue

            print(f"Units: {', '.join(UNITS)}")
            unit = input("Unit: ").lower()

            supplier = input("Supplier Name: ")

            exp_date = input("Expiration Date (YYYY-MM-DD) or leave blank: ")
            if not exp_date:
                exp_date = None

            try:
                reorder = float(input("Reorder Level (default 10): ") or "10")
            except ValueError:
                reorder = 10

            add_stock(item_name, quantity, unit, supplier, exp_date, reorder)

        elif choice == "2":
            display_inventory()
            item_name = input("\nItem Name: ")

            try:
                change = float(input("Quantity to add (+) or deduct (-): "))
            except ValueError:
                print("Invalid quantity")
                continue

            reason = input("Reason: ")
            update_stock(item_name, change, reason)

        elif choice == "3":
            display_inventory()

        elif choice == "4":
            low_stock = check_reorder_level()
            print(f"\nLOW STOCK ALERTS ({len(low_stock)} items)")
            print("=" * 80)

            if not low_stock:
                print("All items are sufficiently stocked!")
            else:
                for item in low_stock.values():
                    print(
                        f"{item['item_name']}: {item['quantity']} {item['unit']} "
                        f"(Reorder at: {item['reorder_level']} {item['unit']})"
                    )
            print("=" * 80)

        elif choice == "5":
            try:
                days = int(
                    input("Check items expiring in how many days? (default 7): ") or "7"
                )
            except ValueError:
                days = 7

            expiring = check_expiring_soon(days)
            print(f"\nITEMS EXPIRING IN {days} DAYS ({len(expiring)} items)")
            print("=" * 80)

            if not expiring:
                print(f"No items expiring in the next {days} days!")
            else:
                for item in expiring.values():
                    print(f"{item['item_name']}: Expires on {item['expiration_date']}")
            print("=" * 80)

        elif choice == "6":
            display_inventory()
            item_name = input("\nItem Name: ")

            try:
                new_level = float(input("New Reorder Level: "))
                set_reorder_level(item_name, new_level)
            except ValueError:
                print("Invalid number")

        elif choice == "7":
            try:
                limit = int(
                    input("How many recent entries to show? (default 20): ") or "20"
                )
                display_usage_log(limit)
            except ValueError:
                print("Invalid number")

        elif choice == "8":
            generate_inventory_report()

        elif choice == "9":
            print("wasd")
            break

        else:
            print("Invalid choice! Please select 1-9.")


if __name__ == "__main__":
    interactive_test()
