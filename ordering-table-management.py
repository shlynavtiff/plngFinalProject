from datetime import datetime
import csv
import os

orders = {}
tables = {}
order_counter = 1000

SAMPLE_MENU = [
    {"item_id": 1, "item_name": "Burger", "quantity": 1, "price": 150},
    {"item_id": 2, "item_name": "Fries", "quantity": 1, "price": 80},
    {"item_id": 3, "item_name": "Coke", "quantity": 1, "price": 50},
    {"item_id": 4, "item_name": "Pizza", "quantity": 1, "price": 300},
    {"item_id": 5, "item_name": "Spaghetti", "quantity": 1, "price": 200},
    {"item_id": 6, "item_name": "Iced Tea", "quantity": 1, "price": 40},
]


def save_tables_to_csv(filename="tables.csv"):
    """Save all tables to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["table_number", "status", "order_id", "capacity"])

            for table_num, table_info in tables.items():
                writer.writerow(
                    [
                        table_num,
                        table_info["status"],
                        table_info["order_id"] if table_info["order_id"] else "",
                        table_info["capacity"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving tables: {e}")
        return False


def load_tables_from_csv(filename="tables.csv"):
    """Load tables from CSV file"""
    global tables

    if not os.path.exists(filename):
        print(f"{filename} not found. Initializing default tables.")
        initialize_tables()
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            tables = {}

            for row in reader:
                table_num = int(row["table_number"])
                tables[table_num] = {
                    "status": row["status"],
                    "order_id": int(row["order_id"]) if row["order_id"] else None,
                    "capacity": int(row["capacity"]),
                }

        print(f"Loaded {len(tables)} tables from {filename}")
        return True
    except Exception as e:
        print(f"Error loading tables: {e}")
        return False


def save_orders_to_csv(filename="orders.csv"):
    """Save all orders to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "order_id",
                    "customer_id",
                    "order_type",
                    "table_number",
                    "status",
                    "order_time",
                    "total_amount",
                ]
            )

            for order_id, order in orders.items():
                writer.writerow(
                    [
                        order["order_id"],
                        order["customer_id"],
                        order["order_type"],
                        order["table_number"] if order["table_number"] else "",
                        order["status"],
                        order["order_time"],
                        order["total_amount"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving orders: {e}")
        return False


def load_orders_from_csv(filename="orders.csv"):
    """Load orders from CSV file"""
    global orders, order_counter

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting fresh.")
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            orders = {}
            max_order_id = 1000

            for row in reader:
                order_id = int(row["order_id"])
                max_order_id = max(max_order_id, order_id)

                orders[order_id] = {
                    "order_id": order_id,
                    "customer_id": row["customer_id"],
                    "order_type": row["order_type"],
                    "table_number": (
                        int(row["table_number"]) if row["table_number"] else None
                    ),
                    "status": row["status"],
                    "order_time": row["order_time"],
                    "total_amount": float(row["total_amount"]),
                    "order_items": [],  # Items loaded separately
                }

            order_counter = max_order_id + 1

        print(f"Loaded {len(orders)} orders from {filename}")
        return True
    except Exception as e:
        print(f"Error loading orders: {e}")
        return False


def save_order_items_to_csv(filename="order_items.csv"):
    """Save all order items to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["order_id", "item_id", "item_name", "quantity", "price"])

            for order_id, order in orders.items():
                for item in order["order_items"]:
                    writer.writerow(
                        [
                            order_id,
                            item["item_id"],
                            item["item_name"],
                            item["quantity"],
                            item["price"],
                        ]
                    )
        return True
    except Exception as e:
        print(f"Error saving order items: {e}")
        return False


def load_order_items_from_csv(filename="order_items.csv"):
    """Load order items from CSV file"""
    global orders

    if not os.path.exists(filename):
        print(f"{filename} not found.")
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                order_id = int(row["order_id"])

                if order_id in orders:
                    orders[order_id]["order_items"].append(
                        {
                            "item_id": int(row["item_id"]),
                            "item_name": row["item_name"],
                            "quantity": int(row["quantity"]),
                            "price": float(row["price"]),
                        }
                    )

        print(f"Order items loaded from {filename}")
        return True
    except Exception as e:
        print(f"Error loading order items: {e}")
        return False


def save_all_data():
    """Save all data (tables, orders, and order items) to CSV files"""
    save_tables_to_csv()
    save_orders_to_csv()
    save_order_items_to_csv()


def load_all_data():
    """Load all data (tables, orders, and order items) from CSV files"""
    print("\nLoading data from CSV files...")
    load_tables_from_csv()
    load_orders_from_csv()
    load_order_items_from_csv()
    print("Data loaded!\n")


# ==================== ORIGINAL FUNCTIONS ====================


def initialize_tables(num_tables=10):
    global tables
    for i in range(1, num_tables + 1):
        tables[i] = {"status": "Available", "order_id": None, "capacity": 4}
    print(f"Initialized {num_tables} tables")


def create_order(customer_id, order_items, order_type, table_number=None):
    global orders, order_counter

    if order_type not in ["Dine In", "Takeout", "Delivery"]:
        print(f"Invalid order type. Must be Dine In, Takeout, or Delivery")
        return None

    if order_type == "Dine In":
        if table_number is None:
            print("Table number is required for dine-in orders")
            return None
        if table_number not in tables:
            print(f"Table {table_number} does not exist")
            return None
        if tables[table_number]["status"] == "Occupied":
            print(f"Table {table_number} is already occupied")
            return None

    if not order_items or len(order_items) == 0:
        print("Order must have at least one item")
        return None

    order_id = order_counter
    order_counter += 1

    total_amount = 0
    for item in order_items:
        total_amount += item["price"] * item["quantity"]

    orders[order_id] = {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_items": order_items,
        "order_type": order_type,
        "table_number": table_number,
        "status": "Pending",
        "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount": total_amount,
    }

    if order_type == "Dine In" and table_number:
        assign_table(table_number, order_id)

    print(f"Order {order_id} created successfully!")
    save_all_data()  # AUTO-SAVE
    return order_id


def update_order(order_id, new_items):
    global orders

    if order_id not in orders:
        print(f"Order {order_id} not found")
        return False

    order = orders[order_id]

    if order["status"] in ["Served", "Completed", "Cancelled"]:
        print(f"Cannot update order with status: {order['status']}")
        return False

    order["order_items"] = new_items
    total_amount = 0
    for item in new_items:
        total_amount += item["price"] * item["quantity"]
    order["total_amount"] = total_amount

    print(f"Order {order_id} updated successfully!")
    save_all_data()
    return True


def cancel_order(order_id):
    global orders, tables

    if order_id not in orders:
        print(f"Order {order_id} not found")
        return False

    order = orders[order_id]

    if order["status"] in ["Served", "Completed"]:
        print(f"Cannot cancel order with status: {order['status']}")
        return False

    order["status"] = "Cancelled"

    if order["table_number"]:
        tables[order["table_number"]]["status"] = "Available"
        tables[order["table_number"]]["order_id"] = None

    print(f"Order {order_id} cancelled successfully!")
    save_all_data()  # AUTO-SAVE
    return True


def assign_table(table_number, order_id):
    global tables, orders

    if table_number not in tables:
        print(f"Table {table_number} does not exist")
        return False

    if tables[table_number]["status"] == "Occupied":
        print(f"Table {table_number} is already occupied")
        return False

    if order_id not in orders:
        print(f"Order {order_id} not found")
        return False

    tables[table_number]["status"] = "Occupied"
    tables[table_number]["order_id"] = order_id
    orders[order_id]["table_number"] = table_number

    print(f"Table {table_number} assigned to order {order_id}")
    return True


def get_order_status(order_id):
    if order_id not in orders:
        print(f"Order {order_id} not found")
        return None
    return orders[order_id]


def update_order_status(order_id, new_status):
    global orders, tables

    valid_statuses = ["Pending", "In Progress", "Served", "Completed", "Cancelled"]

    if new_status not in valid_statuses:
        print(f"Invalid status. Must be: {', '.join(valid_statuses)}")
        return False

    if order_id not in orders:
        print(f"Order {order_id} not found")
        return False

    orders[order_id]["status"] = new_status

    if new_status == "Completed":
        table_number = orders[order_id]["table_number"]
        if table_number:
            tables[table_number]["status"] = "Available"
            tables[table_number]["order_id"] = None

    print(f"Order {order_id} status updated to '{new_status}'")
    save_all_data()
    return True


def get_table_status(table_number):
    if table_number not in tables:
        print(f"Table {table_number} does not exist")
        return None
    return tables[table_number]


def get_all_tables():
    return tables


def get_order_summary(order_id):
    if order_id not in orders:
        print(f"Order {order_id} not found")
        return None

    order = orders[order_id]

    summary = f"""
═══════════════════════════════════
ORDER SUMMARY
═══════════════════════════════════
Order ID: {order['order_id']}
Customer ID: {order['customer_id']}
Order Type: {order['order_type']}
Table Number: {order['table_number'] if order['table_number'] else 'N/A'}
Status: {order['status']}
Order Time: {order['order_time']}

ITEMS:
"""

    for item in order["order_items"]:
        summary += f"\n   • {item['item_name']} x{item['quantity']} - ₱{item['price'] * item['quantity']:.2f}"

    summary += f"\n\n   Total Amount: ₱{order['total_amount']:.2f}"
    summary += "\n═══════════════════════════════════"

    return summary


def get_all_orders(filter_status=None):
    if filter_status:
        filtered = {}
        for order_id, order in orders.items():
            if order["status"] == filter_status:
                filtered[order_id] = order
        return filtered
    return orders


def display_all_tables():
    print("\nTABLE STATUS")
    print("=" * 50)
    for table_num, table_info in tables.items():
        status_icon = "🔴" if table_info["status"] == "Occupied" else "🟢"
        order_info = (
            f" (Order #{table_info['order_id']})" if table_info["order_id"] else ""
        )
        print(f"{status_icon} Table {table_num}: {table_info['status']}{order_info}")
    print("=" * 50)


def display_all_orders():
    print("\nALL ORDERS")
    print("=" * 50)
    if not orders:
        print("No orders yet.")
    else:
        for order_id, order in orders.items():
            print(
                f"Order #{order_id} | {order['order_type']} | Status: {order['status']} | ₱{order['total_amount']:.2f}"
            )
    print("=" * 50)


def interactive_test():
    load_all_data()

    if not tables:
        initialize_tables(5)

    while True:
        print("\n=== RESTAURANT MANAGEMENT ===")
        print("1. Create Order")
        print("2. View Order")
        print("3. View All Tables")
        print("4. Update Order Status")
        print("5. Reload Data from CSV")
        print("6. Exit")
        print("\nAuto-save: ON (saves after every action)")

        choice = input("\nEnter choice: ")

        if choice == "1":
            try:
                customer_id = input("Customer ID: ")
                order_type = input("Order Type (Dine In/Takeout/Delivery): ").title()

                print("\nMENU:")
                for item in SAMPLE_MENU:
                    print(f"{item['item_id']}. {item['item_name']} - ₱{item['price']}")

                selected_items = []

                while True:
                    try:
                        item_id = int(input("\nEnter item ID (0 to finish): "))
                        if item_id == 0:
                            break

                        quantity = int(input("Quantity: "))

                        found = False
                        for menu_item in SAMPLE_MENU:
                            if menu_item["item_id"] == item_id:
                                selected_items.append(
                                    {
                                        "item_id": menu_item["item_id"],
                                        "item_name": menu_item["item_name"],
                                        "quantity": quantity,
                                        "price": menu_item["price"],
                                    }
                                )
                                found = True
                                break

                        if not found:
                            print(f"Item ID {item_id} not found in menu!")

                    except ValueError:
                        print("Please enter a valid number!")

                table_num = None
                if order_type == "Dine In":
                    try:
                        table_num = int(input("Table number: "))
                    except ValueError:
                        print("Invalid table number! Order cancelled.")
                        continue

                order_id = create_order(
                    customer_id, selected_items, order_type, table_num
                )

                if order_id:
                    print(f"\n✅ Order created! ID: {order_id}")

            except Exception as e:
                print(f"Error creating order: {e}")

        elif choice == "2":
            try:
                order_id = int(input("Order ID: "))
                summary = get_order_summary(order_id)
                if summary:
                    print(summary)
            except ValueError:
                print("Please enter a valid order ID number!")

        elif choice == "3":
            display_all_tables()

        elif choice == "4":
            try:
                order_id = int(input("Order ID: "))
                status = input(
                    "New Status (Pending/In Progress/Served/Completed/Cancelled): "
                ).title()
                update_order_status(order_id, status)
            except ValueError:
                print("Please enter a valid order ID number!")
            except Exception as e:
                print(f"Error updating order: {e}")

        elif choice == "5":
            load_all_data()

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1-6.")


if __name__ == "__main__":
    interactive_test()
