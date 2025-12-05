"""
🍽 Restaurant Management System - Main Integration
Connects all 6 modules into one complete system
"""

# Import all modules
try:
    import user_management as um
    import menu_management as menu
    import inventory_management as inv
    import ordering_table_management as order
    import billing_and_payment as billing
    import reports_and_analytics as reports
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all module files are in the same directory!")
    exit(1)

from datetime import datetime


def main():
    """Main entry point - Login screen"""

    # Load all data on startup
    print("RESTAURANT MANAGEMENT SYSTEM")
    print("Loading system data...")

    um.load_users_from_csv()
    um.load_activity_log_from_csv()
    menu.load_menu_from_csv()
    inv.load_inventory_from_csv()
    inv.load_usage_log_from_csv()
    order.load_all_data()
    billing.load_transactions_from_csv()

    print("System ready!\n")

    while True:
        print("\n" + "=" * 60)
        print("🍽️ RESTAURANT MANAGEMENT SYSTEM - LOGIN")
        print("=" * 60)
        print("1. Login")
        print("2. Register (Customer)")
        print("3. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            username = input("\nUsername: ")
            password = input("Password: ")

            if um.login(username, password):
                role = um.get_current_user_role()

                # Route to appropriate menu based on role
                if role == "Admin":
                    admin_menu()
                elif role == "Cashier":
                    cashier_menu()
                elif role == "Waiter":
                    waiter_menu()
                elif role == "Customer":
                    customer_menu()
                else:
                    print("Unknown role")

        elif choice == "2":
            register_customer()

        elif choice == "3":
            print("\nThank you for using our system!")
            break

        else:
            print("Invalid choice!")


def register_customer():
    """Quick customer registration"""
    print("\n--- Customer Registration ---")
    username = input("Username: ")
    password = input("Password: ")
    name = input("Full Name: ")
    contact = input("Contact Number: ")

    um.register_user(username, password, "Customer", name, contact)


def admin_menu():
    """Admin has full access to all modules"""

    while um.get_current_user():
        print("\n" + "=" * 60)
        print("ADMIN DASHBOARD")
        print("=" * 60)
        print(f"Logged in as: {um.users[um.get_current_user()]['name']}")
        print("\n1. User Management")
        print("2. Menu Management")
        print("3. Inventory Management")
        print("4. Ordering & Table Management")
        print("5. Billing & Payment")
        print("6. Reports & Analytics")
        print("7. Quick Stats Dashboard")
        print("8. Logout")

        choice = input("\nChoice: ")

        if choice == "1":
            admin_user_management()
        elif choice == "2":
            admin_menu_management()
        elif choice == "3":
            admin_inventory_management()
        elif choice == "4":
            admin_ordering_management()
        elif choice == "5":
            admin_billing_management()
        elif choice == "6":
            admin_reports_analytics()
        elif choice == "7":
            show_quick_dashboard()
        elif choice == "8":
            um.logout()
            break
        else:
            print("Invalid choice!")


def admin_user_management():
    """User management submenu"""
    while True:
        print("\n--- USER MANAGEMENT ---")
        print("1. View All Users")
        print("2. Register New User")
        print("3. Change User Role")
        print("4. Activate/Deactivate User")
        print("5. View Activity Log")
        print("6. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            um.display_all_users()
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            print(f"Roles: {', '.join(um.VALID_ROLES)}")
            role = input("Role: ").title()
            name = input("Full Name: ")
            contact = input("Contact: ")
            um.register_user(username, password, role, name, contact)
        elif choice == "3":
            um.display_all_users()
            username = input("Username to modify: ")
            print(f"Roles: {', '.join(um.VALID_ROLES)}")
            new_role = input("New role: ").title()
            um.change_user_role(username, new_role)
        elif choice == "4":
            um.display_all_users()
            username = input("Username to modify: ")
            status = input("Status (Active/Inactive): ").title()
            um.change_user_status(username, status)
        elif choice == "5":
            limit = int(input("How many recent activities? (default 20): ") or "20")
            um.display_activity_log(limit)
        elif choice == "6":
            break


def admin_menu_management():
    """Menu management submenu"""
    while True:
        print("\n--- MENU MANAGEMENT ---")
        print("1. View All Menu Items")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Change Item Status")
        print("6. View by Category")
        print("7. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            menu.display_menu()
        elif choice == "2":
            item_name = input("Item Name: ")
            print(f"Categories: {', '.join(menu.VALID_CATEGORIES)}")
            category = input("Category: ").title()
            try:
                price = float(input("Price (₱): "))
                prep_time = int(input("Prep Time (minutes): ") or "10")
            except ValueError:
                print("Invalid input")
                continue
            description = input("Description: ")
            menu.add_menu_item(item_name, category, price, prep_time, description)
        elif choice == "3":
            menu.display_menu()
            try:
                item_id = int(input("Item ID to update: "))
                if item_id in menu.menu_items:
                    item = menu.menu_items[item_id]
                    new_details = {}

                    name = input(
                        f"Name (current: {item['item_name']}, blank to skip): "
                    )
                    if name:
                        new_details["item_name"] = name

                    price = input(f"Price (current: {item['price']}, blank to skip): ")
                    if price:
                        new_details["price"] = float(price)

                    if new_details:
                        menu.update_menu_item(item_id, new_details)
                else:
                    print("Item not found")
            except ValueError:
                print("Invalid input")
        elif choice == "4":
            menu.display_menu()
            try:
                item_id = int(input("Item ID to delete: "))
                confirm = input("Confirm deletion? (yes/no): ")
                if confirm.lower() == "yes":
                    menu.delete_menu_item(item_id)
            except ValueError:
                print("Invalid input")
        elif choice == "5":
            menu.display_menu()
            try:
                item_id = int(input("Item ID: "))
                print(f"Status: {', '.join(menu.VALID_STATUS)}")
                status = input("New Status: ").title()
                menu.set_item_status(item_id, status)
            except ValueError:
                print("Invalid input")
        elif choice == "6":
            print(f"Categories: {', '.join(menu.VALID_CATEGORIES)}")
            category = input("Category: ").title()
            items = menu.get_menu_by_category(category)
            menu.display_menu(items)
        elif choice == "7":
            break


def admin_inventory_management():
    """Inventory management submenu"""
    while True:
        print("\n--- INVENTORY MANAGEMENT ---")
        print("1. View All Inventory")
        print("2. Add New Stock Item")
        print("3. Update Stock Quantity")
        print("4. Check Low Stock Alerts")
        print("5. Check Expiring Items")
        print("6. View Usage Log")
        print("7. Generate Inventory Report")
        print("8. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            inv.display_inventory()
        elif choice == "2":
            item_name = input("Item Name: ")
            try:
                quantity = float(input("Quantity: "))
            except ValueError:
                print("Invalid quantity")
                continue
            print(f"Units: {', '.join(inv.UNITS)}")
            unit = input("Unit: ").lower()
            supplier = input("Supplier: ")
            exp_date = input("Expiration Date (YYYY-MM-DD, blank to skip): ")
            try:
                reorder = float(input("Reorder Level (default 10): ") or "10")
            except ValueError:
                reorder = 10
            inv.add_stock(
                item_name, quantity, unit, supplier, exp_date or None, reorder
            )
        elif choice == "3":
            inv.display_inventory()
            item_name = input("Item Name: ")
            try:
                change = float(input("Quantity to add (+) or deduct (-): "))
                reason = input("Reason: ")
                inv.update_stock(item_name, change, reason)
            except ValueError:
                print("Invalid quantity")
        elif choice == "4":
            low_stock = inv.check_reorder_level()
            print(f"\nLOW STOCK ALERTS ({len(low_stock)} items)")
            for item in low_stock.values():
                print(f"  {item['item_name']}: {item['quantity']} {item['unit']}")
        elif choice == "5":
            try:
                days = int(input("Days ahead to check (default 7): ") or "7")
                expiring = inv.check_expiring_soon(days)
                print(f"\nEXPIRING IN {days} DAYS ({len(expiring)} items)")
                for item in expiring.values():
                    print(f"  {item['item_name']}: {item['expiration_date']}")
            except ValueError:
                print("Invalid input")
        elif choice == "6":
            try:
                limit = int(input("Recent entries (default 20): ") or "20")
                inv.display_usage_log(limit)
            except ValueError:
                print("Invalid input")
        elif choice == "7":
            inv.generate_inventory_report()
        elif choice == "8":
            break


def admin_ordering_management():
    """Ordering management submenu"""
    while True:
        print("\n--- ORDERING & TABLE MANAGEMENT ---")
        print("1. View All Tables")
        print("2. View All Orders")
        print("3. Create New Order")
        print("4. Update Order Status")
        print("5. View Order Details")
        print("6. Cancel Order")
        print("7. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            order.display_all_tables()
        elif choice == "2":
            order.display_all_orders()
        elif choice == "3":
            create_order_interactive()
        elif choice == "4":
            order.display_all_orders()
            try:
                order_id = int(input("Order ID: "))
                print(
                    "Status options: Pending, In Progress, Served, Completed, Cancelled"
                )
                status = input("New Status: ").title()
                order.update_order_status(order_id, status)
            except ValueError:
                print("Invalid input")
        elif choice == "5":
            try:
                order_id = int(input("Order ID: "))
                summary = order.get_order_summary(order_id)
                if summary:
                    print(summary)
            except ValueError:
                print("Invalid input")
        elif choice == "6":
            order.display_all_orders()
            try:
                order_id = int(input("Order ID to cancel: "))
                confirm = input("Confirm cancellation? (yes/no): ")
                if confirm.lower() == "yes":
                    order.cancel_order(order_id)
            except ValueError:
                print("Invalid input")
        elif choice == "7":
            break


def admin_billing_management():
    """Billing management submenu"""
    while True:
        print("\n--- BILLING & PAYMENT ---")
        print("1. Process Payment")
        print("2. View Transaction")
        print("3. View All Transactions")
        print("4. View Daily Sales")
        print("5. Generate Receipt")
        print("6. View Discount Codes")
        print("7. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            process_payment_interactive()
        elif choice == "2":
            try:
                trans_id = int(input("Transaction ID: "))
                trans = billing.get_transaction(trans_id)
                if trans:
                    for key, value in trans.items():
                        print(f"{key}: {value}")
            except ValueError:
                print("Invalid input")
        elif choice == "3":
            billing.display_all_transactions()
        elif choice == "4":
            date = input("Date (YYYY-MM-DD, blank for today): ")
            sales = billing.get_daily_sales(date if date else None)
            print(f"\nSALES - {sales['date']}")
            print(f"Total: ₱{sales['total_sales']:,.2f}")
            print(f"Transactions: {sales['transaction_count']}")
        elif choice == "5":
            try:
                trans_id = int(input("Transaction ID: "))
                receipt = billing.generate_receipt(trans_id)
                if receipt:
                    print(receipt)
            except ValueError:
                print("Invalid input")
        elif choice == "6":
            billing.display_discount_codes()
        elif choice == "7":
            break


def admin_reports_analytics():
    """Reports submenu"""
    while True:
        print("\n--- REPORTS & ANALYTICS ---")
        print("1. Sales Report (Custom Range)")
        print("2. Daily Sales")
        print("3. Weekly Sales")
        print("4. Monthly Sales")
        print("5. Best-Selling Items")
        print("6. Inventory Summary")
        print("7. User Activity Summary")
        print("8. Revenue Breakdown")
        print("9. Back")

        choice = input("\nChoice: ")

        if choice == "1":
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            report = reports.generate_sales_report(start, end)
            if report:
                reports.display_sales_report(report)
        elif choice == "2":
            today = datetime.now().strftime("%Y-%m-%d")
            report = reports.generate_sales_report(today, today)
            if report:
                reports.display_sales_report(report)
        elif choice == "3":
            from datetime import timedelta

            today = datetime.now()
            week_ago = (today - timedelta(days=7)).strftime("%Y-%m-%d")
            report = reports.generate_sales_report(week_ago, today.strftime("%Y-%m-%d"))
            if report:
                reports.display_sales_report(report)
        elif choice == "4":
            from datetime import timedelta

            today = datetime.now()
            month_ago = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            report = reports.generate_sales_report(
                month_ago, today.strftime("%Y-%m-%d")
            )
            if report:
                reports.display_sales_report(report)
        elif choice == "5":
            best = reports.get_best_selling_items(limit=10)
            reports.display_best_sellers(best)
        elif choice == "6":
            summary = reports.generate_inventory_summary()
            reports.display_inventory_summary(summary)
        elif choice == "7":
            summary = reports.get_user_activity_summary()
            reports.display_user_activity(summary)
        elif choice == "8":
            breakdown = reports.generate_revenue_breakdown()
            if breakdown:
                print(f"\nREVENUE BREAKDOWN")
                for key, value in breakdown.items():
                    print(f"{key}: ₱{value:,.2f}")
        elif choice == "9":
            break


def show_quick_dashboard():
    """Quick overview dashboard"""
    print("\n" + "=" * 60)
    print("QUICK DASHBOARD")
    print("=" * 60)

    # Today's sales
    today = datetime.now().strftime("%Y-%m-%d")
    sales = billing.get_daily_sales(today)
    print(f"\nToday's Sales: ₱{sales['total_sales']:,.2f}")
    print(f"   Transactions: {sales['transaction_count']}")

    # Low stock alerts
    low_stock = inv.check_reorder_level()
    print(f"\nLow Stock Items: {len(low_stock)}")

    # Available tables
    available_tables = sum(
        1 for t in order.tables.values() if t["status"] == "Available"
    )
    print(f"\n🪑 Available Tables: {available_tables}/{len(order.tables)}")

    # Pending orders
    pending = order.get_all_orders("Pending")
    print(f"\n📋 Pending Orders: {len(pending)}")

    print("=" * 60)


def cashier_menu():
    """Cashier access - billing and viewing orders"""

    while um.get_current_user():
        print("\n" + "=" * 60)
        print("CASHIER DASHBOARD")
        print("=" * 60)
        print(f"Logged in as: {um.users[um.get_current_user()]['name']}")
        print("\n1. View Pending Orders")
        print("2. Process Payment")
        print("3. Generate Receipt")
        print("4. View Today's Sales")
        print("5. View All Transactions")
        print("6. Logout")

        choice = input("\nChoice: ")

        if choice == "1":
            pending = order.get_all_orders("Served")
            print(f"\nSERVED ORDERS (Ready for Payment)")
            for order_id, ord in pending.items():
                print(
                    f"Order #{order_id} | Table: {ord.get('table_number', 'N/A')} | ₱{ord['total_amount']:.2f}"
                )
        elif choice == "2":
            process_payment_interactive()
        elif choice == "3":
            try:
                trans_id = int(input("Transaction ID: "))
                receipt = billing.generate_receipt(trans_id)
                if receipt:
                    print(receipt)
            except ValueError:
                print("Invalid input")
        elif choice == "4":
            today = datetime.now().strftime("%Y-%m-%d")
            sales = billing.get_daily_sales(today)
            print(f"\nTODAY'S SALES")
            print(f"Total: ₱{sales['total_sales']:,.2f}")
            print(f"Transactions: {sales['transaction_count']}")
        elif choice == "5":
            billing.display_all_transactions()
        elif choice == "6":
            um.logout()
            break


def waiter_menu():
    """Waiter access - taking orders"""

    while um.get_current_user():
        print("\n" + "=" * 60)
        print("WAITER DASHBOARD")
        print("=" * 60)
        print(f"Logged in as: {um.users[um.get_current_user()]['name']}")
        print("\n1. View Menu")
        print("2. View Available Tables")
        print("3. Create New Order")
        print("4. View All Orders")
        print("5. Update Order Status")
        print("6. View Order Details")
        print("7. Logout")

        choice = input("\nChoice: ")

        if choice == "1":
            available = menu.get_available_menu()
            menu.display_menu(available)
        elif choice == "2":
            order.display_all_tables()
        elif choice == "3":
            create_order_interactive()
        elif choice == "4":
            order.display_all_orders()
        elif choice == "5":
            order.display_all_orders()
            try:
                order_id = int(input("Order ID: "))
                print("Status: Pending, In Progress, Served")
                status = input("New Status: ").title()
                order.update_order_status(order_id, status)
            except ValueError:
                print("Invalid input")
        elif choice == "6":
            try:
                order_id = int(input("Order ID: "))
                summary = order.get_order_summary(order_id)
                if summary:
                    print(summary)
            except ValueError:
                print("Invalid input")
        elif choice == "7":
            um.logout()
            break


def customer_menu():
    """Customer access - view menu and place orders"""

    while um.get_current_user():
        print("\n" + "=" * 60)
        print("CUSTOMER MENU")
        print("=" * 60)
        print(f"Welcome, {um.users[um.get_current_user()]['name']}!")
        print("\n1. View Menu")
        print("2. Place Order (Takeout/Delivery)")
        print("3. View My Orders")
        print("4. Logout")

        choice = input("\nChoice: ")

        if choice == "1":
            available = menu.get_available_menu()
            menu.display_menu(available)
        elif choice == "2":
            create_order_interactive(customer_mode=True)
        elif choice == "3":
            customer_id = um.get_current_user()
            print(f"\nYOUR ORDERS")
            for order_id, ord in order.orders.items():
                if ord["customer_id"] == customer_id:
                    print(
                        f"Order #{order_id} | {ord['order_type']} | {ord['status']} | ₱{ord['total_amount']:.2f}"
                    )
        elif choice == "4":
            um.logout()
            break


def create_order_interactive(customer_mode=False):
    """Interactive order creation"""

    # Show available menu
    available = menu.get_available_menu()
    menu.display_menu(available)

    # Get customer ID
    if customer_mode:
        customer_id = um.get_current_user()
    else:
        customer_id = input("\nCustomer ID/Name: ")

    # Get order type
    if customer_mode:
        print("\nOrder Type: 1. Takeout  2. Delivery")
        type_choice = input("Choice: ")
        order_type = "Takeout" if type_choice == "1" else "Delivery"
    else:
        print("\nOrder Type: 1. Dine In  2. Takeout  3. Delivery")
        type_choice = input("Choice: ")
        if type_choice == "1":
            order_type = "Dine In"
        elif type_choice == "2":
            order_type = "Takeout"
        else:
            order_type = "Delivery"

    # Select items
    selected_items = []
    print("\nSelect items (enter 0 to finish):")

    while True:
        try:
            item_id = int(input("Item ID: "))
            if item_id == 0:
                break

            if item_id not in available:
                print("Item not available")
                continue

            quantity = int(input("Quantity: "))

            item = available[item_id]
            selected_items.append(
                {
                    "item_id": item_id,
                    "item_name": item["item_name"],
                    "quantity": quantity,
                    "price": item["price"],
                }
            )
            print(f"Added {quantity}x {item['item_name']}")

        except ValueError:
            print("Invalid input")

    if not selected_items:
        print("No items selected")
        return

    # Get table number for dine-in
    table_num = None
    if order_type == "Dine In":
        order.display_all_tables()
        try:
            table_num = int(input("Table number: "))
        except ValueError:
            print("Invalid table number")
            return

    # Create order
    order_id = order.create_order(customer_id, selected_items, order_type, table_num)

    if order_id:
        print(f"\nOrder #{order_id} created successfully!")
        summary = order.get_order_summary(order_id)
        print(summary)


def process_payment_interactive():
    """Interactive payment processing"""

    # Show served orders
    served = order.get_all_orders("Served")
    if not served:
        print("No orders ready for payment")
        return

    print("\n📋 ORDERS READY FOR PAYMENT:")
    for order_id, ord in served.items():
        print(
            f"Order #{order_id} | {ord['order_type']} | Table: {ord.get('table_number', 'N/A')} | ₱{ord['total_amount']:.2f}"
        )

    try:
        order_id = int(input("\nOrder ID to process: "))

        if order_id not in order.orders:
            print("Order not found")
            return

        ord = order.orders[order_id]
        order_items = ord["order_items"]

        # Show bill preview
        discount_code = input("Discount code (leave blank for none): ")
        bill = billing.calculate_total(
            order_items, discount_code if discount_code else None
        )

        print(f"\n--- BILL ---")
        print(f"Subtotal: ₱{bill['subtotal']:.2f}")
        print(f"Service Charge: ₱{bill['service_charge']:.2f}")
        if bill["discount"] > 0:
            print(f"Discount: -₱{bill['discount']:.2f}")
        print(f"Tax: ₱{bill['tax']:.2f}")
        print(f"TOTAL: ₱{bill['total']:.2f}")

        # Payment
        print(f"\nPayment Types: {', '.join(billing.PAYMENT_TYPES)}")
        payment_type = input("Payment Type: ").title()

        if payment_type == "Cash":
            amount_paid = float(input("Amount Paid: "))
        else:
            amount_paid = bill["total"]

        cashier = um.get_current_user()

        trans_id = billing.process_payment(
            order_id,
            order_items,
            payment_type,
            amount_paid,
            discount_code if discount_code else None,
            cashier,
        )

        if trans_id:
            # Update order status to completed
            order.update_order_status(order_id, "Completed")

            # Generate receipt
            print("\nGenerate receipt? (yes/no): ", end="")
            if input().lower() == "yes":
                receipt = billing.generate_receipt(trans_id, order_items)
                print(receipt)

    except ValueError:
        print("Invalid input")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSystem interrupted. Goodbye!")
    except Exception as e:
        print(f"\nSystem error: {e}")
