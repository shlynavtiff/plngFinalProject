# main.py - Restaurant Management System
# Complete Integration of All Modules

import user_management as um
import menu_management as menu
import inventory_management as inv
import ordering_table_management as order
import billing_payment as billing
import reports_analytics as reports
import os

def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter():
    """Wait for user to press enter"""
    input("\nPress Enter to continue...")

def main_menu():
    """Main entry point - Login first"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("🍽️  RESTAURANT MANAGEMENT SYSTEM")
        print("="*60)
        print("\n1. Login")
        print("2. Exit System")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            clear_screen()
            print("\n" + "="*60)
            print("🔐 LOGIN")
            print("="*60)
            username = input("\nUsername: ").strip()
            password = input("Password: ").strip()
            
            if um.login(username, password):
                print(f"\n✅ Login successful! Welcome {username}")
                press_enter()
                
                # Get role and redirect to appropriate menu
                role = um.get_current_user_role()
                
                if role == 'Admin':
                    admin_menu()
                elif role == 'Cashier':
                    cashier_menu()
                elif role == 'Waiter':
                    waiter_menu()
                elif role == 'Customer':
                    customer_menu()
            else:
                print("\n❌ Invalid credentials!")
                press_enter()
        
        elif choice == '2':
            clear_screen()
            print("\n👋 Thank you for using Restaurant Management System!")
            print("Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice!")
            press_enter()


# ========================== ADMIN MENU ==========================

def admin_menu():
    """Full access to all system features"""
    
    while um.get_current_user():
        clear_screen()
        current_user = um.get_current_user()
        print("\n" + "="*60)
        print(f"👑 ADMIN MENU - Logged in as: {current_user}")
        print("="*60)
        print("\n1. User Management")
        print("2. Menu Management")
        print("3. Inventory Management")
        print("4. Ordering & Table Management")
        print("5. Billing & Payment")
        print("6. Reports & Analytics")
        print("7. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            admin_user_management()
        elif choice == '2':
            admin_menu_management()
        elif choice == '3':
            admin_inventory_management()
        elif choice == '4':
            admin_ordering_management()
        elif choice == '5':
            admin_billing_management()
        elif choice == '6':
            admin_reports_analytics()
        elif choice == '7':
            um.logout()
            print("\n✅ Logged out successfully!")
            press_enter()
            break
        else:
            print("\n❌ Invalid choice!")
            press_enter()


def admin_user_management():
    """Admin - User Management Sub-menu"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("👥 USER MANAGEMENT")
        print("="*60)
        print("\n1. Add New User")
        print("2. View All Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Add New User ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            print("Roles: Admin, Cashier, Waiter, Customer")
            role = input("Role: ").strip()
            
            if um.add_user(username, password, role):
                print(f"\n✅ User '{username}' added successfully!")
            else:
                print("\n❌ Failed to add user!")
            press_enter()
            
        elif choice == '2':
            print("\n--- All Users ---")
            um.view_users()
            press_enter()
            
        elif choice == '3':
            print("\n--- Update User ---")
            user_id = input("User ID to update: ").strip()
            print("Leave blank to keep current value")
            new_username = input("New Username: ").strip() or None
            new_password = input("New Password: ").strip() or None
            new_role = input("New Role: ").strip() or None
            
            if um.update_user(user_id, new_username, new_password, new_role):
                print(f"\n✅ User ID {user_id} updated!")
            else:
                print("\n❌ Failed to update user!")
            press_enter()
            
        elif choice == '4':
            print("\n--- Delete User ---")
            user_id = input("User ID to delete: ").strip()
            confirm = input(f"Delete user ID {user_id}? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                if um.delete_user(user_id):
                    print(f"\n✅ User ID {user_id} deleted!")
                else:
                    print("\n❌ Failed to delete user!")
            press_enter()
            
        elif choice == '5':
            break
        else:
            print("\n❌ Invalid choice!")
            press_enter()


def admin_menu_management():
    """Admin - Menu Management Sub-menu"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("📋 MENU MANAGEMENT")
        print("="*60)
        print("\n1. Add Menu Item")
        print("2. View All Menu Items")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. Toggle Item Availability")
        print("6. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Add Menu Item ---")
            name = input("Item Name: ").strip()
            category = input("Category: ").strip()
            price = float(input("Price: ").strip())
            description = input("Description: ").strip()
            
            if menu.add_menu_item(name, category, price, description):
                print(f"\n✅ '{name}' added to menu!")
            else:
                print("\n❌ Failed to add item!")
            press_enter()
            
        elif choice == '2':
            print("\n--- Menu Items ---")
            menu.view_menu()
            press_enter()
            
        elif choice == '3':
            print("\n--- Update Menu Item ---")
            item_id = input("Item ID to update: ").strip()
            print("Leave blank to keep current value")
            new_name = input("New Name: ").strip() or None
            new_category = input("New Category: ").strip() or None
            new_price = input("New Price: ").strip()
            new_price = float(new_price) if new_price else None
            new_desc = input("New Description: ").strip() or None
            
            if menu.update_menu_item(item_id, new_name, new_category, new_price, new_desc):
                print(f"\n✅ Item ID {item_id} updated!")
            else:
                print("\n❌ Failed to update item!")
            press_enter()
            
        elif choice == '4':
            print("\n--- Delete Menu Item ---")
            item_id = input("Item ID to delete: ").strip()
            confirm = input(f"Delete item ID {item_id}? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                if menu.delete_menu_item(item_id):
                    print(f"\n✅ Item ID {item_id} deleted!")
                else:
                    print("\n❌ Failed to delete item!")
            press_enter()
            
        elif choice == '5':
            print("\n--- Toggle Availability ---")
            item_id = input("Item ID: ").strip()
            available = input("Available? (yes/no): ").strip().lower() == 'yes'
            
            if menu.toggle_availability(item_id, available):
                status = "Available" if available else "Unavailable"
                print(f"\n✅ Item ID {item_id} is now {status}!")
            else:
                print("\n❌ Failed to update availability!")
            press_enter()
            
        elif choice == '6':
            break
        else:
            print("\n❌ Invalid choice!")
            press_enter()


def admin_inventory_management():
    """Admin - Inventory Management Sub-menu"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("📦 INVENTORY MANAGEMENT")
        print("="*60)
        print("\n1. Add Inventory Item")
        print("2. View All Inventory")
        print("3. Update Stock")
        print("4. View Low Stock Items")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Add Inventory Item ---")
            name = input("Item Name: ").strip()
            quantity = float(input("Quantity: ").strip())
            unit = input("Unit (kg, pcs, L, etc.): ").strip()
            reorder_level = float(input("Reorder Level: ").strip())
            
            if inv.add_inventory_item(name, quantity, unit, reorder_level):
                print(f"\n✅ '{name}' added to inventory!")
            else:
                print("\n❌ Failed to add item!")
            press_enter()
            
        elif choice == '2':
            print("\n--- Current Inventory ---")
            inv.view_inventory()
            press_enter()
            
        elif choice == '3':
            print("\n--- Update Stock ---")
            item_name = input("Item Name: ").strip()
            quantity = float(input("Quantity to add: ").strip())
            reason = input("Reason: ").strip()
            
            if inv.add_stock(item_name, quantity, reason):
                print(f"\n✅ Stock updated for '{item_name}'!")
            else:
                print("\n❌ Failed to update stock!")
            press_enter()
            
        elif choice == '4':
            print("\n--- Low Stock Alert ---")
            inv.check_low_stock()
            press_enter()
            
        elif choice == '5':
            break
        else:
            print("\n❌ Invalid choice!")
            press_enter()


def admin_ordering_management():
    """Admin - View and manage orders"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("🍴 ORDER & TABLE MANAGEMENT")
        print("="*60)
        print("\n1. View All Orders")
        print("2. View Order Details")
        print("3. Update Order Status")
        print("4. View Table Status")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- All Orders ---")
            order.view_all_orders()
            press_enter()
            
        elif choice == '2':
            order_id = input("\nOrder ID: ").strip()
            order.view_order_details(order_id)
            press_enter()
            
        elif choice == '3':
            order_id = input("\nOrder ID: ").strip()
            print("Status options: Pending, Preparing, Ready, Completed, Cancelled")
            status = input("New Status: ").strip()
            
            if order.update_order_status(order_id, status):
                print(f"\nOrder {order_id} status updated to '{status}'!")
            else:
                print("\nFailed to update status!")
            press_enter()
            
        elif choice == '4':
            print("\n--- Table Status ---")
            order.view_table_status()
            press_enter()
            
        elif choice == '5':
            break
        else:
            print("\nInvalid choice!")
            press_enter()


def admin_billing_management():
    """Admin - View billing and transactions"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("BILLING & PAYMENT")
        print("="*60)
        print("\n1. View All Transactions")
        print("2. View Transaction Details")
        print("3. Search Transaction")
        print("4. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- All Transactions ---")
            billing.view_all_transactions()
            press_enter()
            
        elif choice == '2':
            trans_id = input("\nTransaction ID: ").strip()
            billing.view_transaction_details(trans_id)
            press_enter()
            
        elif choice == '3':
            search = input("\nSearch (order ID, customer, cashier): ").strip()
            billing.search_transactions(search)
            press_enter()
            
        elif choice == '4':
            break
        else:
            print("\nInvalid choice!")
            press_enter()


def admin_reports_analytics():
    """Admin - Reports and Analytics"""
    
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("REPORTS & ANALYTICS")
        print("="*60)
        print("\n1. Daily Sales Report")
        print("2. Sales by Period")
        print("3. Best Selling Items")
        print("4. Revenue by Category")
        print("5. Inventory Usage Report")
        print("6. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            date = input("\nDate (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date:
                from datetime import date as dt
                date = str(dt.today())
            reports.daily_sales_report(date)
            press_enter()
            
        elif choice == '2':
            start = input("Start Date (YYYY-MM-DD): ").strip()
            end = input("End Date (YYYY-MM-DD): ").strip()
            reports.generate_sales_report(start, end)
            press_enter()
            
        elif choice == '3':
            print("\n--- Best Selling Items ---")
            reports.get_best_selling_items()
            press_enter()
            
        elif choice == '4':
            print("\n--- Revenue by Category ---")
            reports.revenue_by_category()
            press_enter()
            
        elif choice == '5':
            print("\n--- Inventory Usage ---")
            reports.inventory_usage_report()
            press_enter()
            
        elif choice == '6':
            break
        else:
            print("\nInvalid choice!")
            press_enter()

def cashier_menu():
    """Cashier access - Billing and order viewing"""
    
    while um.get_current_user():
        clear_screen()
        current_user = um.get_current_user()
        print("\n" + "="*60)
        print(f"💵 CASHIER MENU - Logged in as: {current_user}")
        print("="*60)
        print("\n1. View Orders (Pending Payment)")
        print("2. Process Payment")
        print("3. View Transactions")
        print("4. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Orders Ready for Payment ---")
            order.view_pending_orders()
            press_enter()
            
        elif choice == '2':
            cashier_process_payment()
            
        elif choice == '3':
            print("\n--- Recent Transactions ---")
            billing.view_all_transactions()
            press_enter()
            
        elif choice == '4':
            um.logout()
            print("\nLogged out successfully!")
            press_enter()
            break
        else:
            print("\nInvalid choice!")
            press_enter()


def cashier_process_payment():
    """Cashier - Process payment for an order"""
    
    clear_screen()
    print("\n" + "="*60)
    print("PROCESS PAYMENT")
    print("="*60)
    
    order_id = input("\nOrder ID: ").strip()
    
    # Get order details
    order_details = order.get_order_by_id(order_id)
    
    if not order_details:
        print("\nOrder not found!")
        press_enter()
        return
    
    # Display order summary
    print(f"\n--- Order #{order_id} Summary ---")
    order.view_order_details(order_id)
    
    # Get order items and total
    order_items = order.get_order_items(order_id)
    total = sum(item['price'] * item['quantity'] for item in order_items)
    
    print(f"\nTotal Amount: ₱{total:.2f}")
    
    print("\nPayment Methods: Cash, Card, E-Wallet, GCash")
    payment_type = input("Payment Method: ").strip()
    amount_paid = float(input("Amount Paid: ").strip())
    
    if amount_paid < total:
        print(f"\nInsufficient payment! Need ₱{total - amount_paid:.2f} more.")
        press_enter()
        return
    
    # Process payment
    cashier = um.get_current_user()
    trans_id = billing.process_payment(order_id, order_items, payment_type, amount_paid, cashier)
    
    if trans_id:
        print(f"\nPayment processed successfully!")
        print(f"Transaction ID: {trans_id}")
        
        if amount_paid > total:
            change = amount_paid - total
            print(f"Change: ₱{change:.2f}")
        
        # Generate and display receipt
        print("\n" + "="*60)
        receipt = billing.generate_receipt(trans_id, order_items)
        print(receipt)
        
        # Update order status to Completed
        order.update_order_status(order_id, 'Completed')
    else:
        print("\nPayment processing failed!")
    
    press_enter()


def waiter_menu():
    """Waiter access - Order taking and management"""
    
    while um.get_current_user():
        clear_screen()
        current_user = um.get_current_user()
        print("\n" + "="*60)
        print(f"WAITER MENU - Logged in as: {current_user}")
        print("="*60)
        print("\n1. View Menu")
        print("2. Create New Order")
        print("3. View My Orders")
        print("4. Update Order Status")
        print("5. View Table Status")
        print("6. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Available Menu ---")
            menu.get_available_menu()
            press_enter()
            
        elif choice == '2':
            waiter_create_order()
            
        elif choice == '3':
            waiter = um.get_current_user()
            print(f"\n--- Orders by {waiter} ---")
            order.view_orders_by_waiter(waiter)
            press_enter()
            
        elif choice == '4':
            order_id = input("\nOrder ID: ").strip()
            print("Status: Pending, Preparing, Ready, Completed, Cancelled")
            status = input("New Status: ").strip()
            
            if order.update_order_status(order_id, status):
                print(f"\nOrder {order_id} updated to '{status}'!")
            else:
                print("\nFailed to update!")
            press_enter()
            
        elif choice == '5':
            print("\n--- Table Status ---")
            order.view_table_status()
            press_enter()
            
        elif choice == '6':
            um.logout()
            print("\nLogged out successfully!")
            press_enter()
            break
        else:
            print("\nInvalid choice!")
            press_enter()


def waiter_create_order():
    """Waiter - Create new order"""
    
    clear_screen()
    print("\n" + "="*60)
    print("📝 CREATE NEW ORDER")
    print("="*60)
    
    # Customer info
    customer_name = input("\nCustomer Name: ").strip()
    
    # Order type
    print("\nOrder Type: Dine In, Takeout, Delivery")
    order_type = input("Order Type: ").strip()
    
    table_num = None
    if order_type.lower() == 'dine in':
        table_num = input("Table Number: ").strip()
    
    # Show available menu
    print("\n--- Available Menu ---")
    available_items = menu.get_available_menu()
    
    # Collect order items
    order_items = []
    
    while True:
        print("\n" + "-"*60)
        item_id = input("Item ID (or 'done' to finish): ").strip()
        
        if item_id.lower() == 'done':
            break
        
        # Get item details from menu
        item = menu.get_menu_item_by_id(item_id)
        
        if not item:
            print("❌ Item not found!")
            continue
        
        quantity = int(input(f"Quantity for {item['name']}: ").strip())
        
        order_items.append({
            'item_id': item_id,
            'item_name': item['name'],
            'quantity': quantity,
            'price': item['price']
        })
        
        print(f"✅ Added {quantity}x {item['name']}")
    
    if not order_items:
        print("\n❌ No items added!")
        press_enter()
        return
    
    # Display order summary
    print("\n" + "="*60)
    print("ORDER SUMMARY")
    print("="*60)
    total = 0
    for item in order_items:
        subtotal = item['price'] * item['quantity']
        total += subtotal
        print(f"{item['item_name']} x{item['quantity']} - ₱{subtotal:.2f}")
    print(f"\n💰 Total: ₱{total:.2f}")
    
    confirm = input("\nConfirm order? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        # Create order
        waiter = um.get_current_user()
        order_id = order.create_order(customer_name, order_items, order_type, waiter, table_num)
        
        if order_id:
            print(f"\nOrder #{order_id} created successfully!")
            
            # Optional: Deduct inventory for ingredients
            # This would require mapping menu items to ingredients
            # inv.deduct_stock(...) for each ingredient
        else:
            print("\nFailed to create order!")
    else:
        print("\nOrder cancelled!")
    
    press_enter()

def customer_menu():
    """Customer access - View menu and place orders"""
    
    while um.get_current_user():
        clear_screen()
        current_user = um.get_current_user()
        print("\n" + "="*60)
        print(f"👤 CUSTOMER MENU - Logged in as: {current_user}")
        print("="*60)
        print("\n1. View Menu")
        print("2. Place Order")
        print("3. View My Orders")
        print("4. Logout")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
            print("\n--- Menu ---")
            menu.view_menu_by_category()
            press_enter()
            
        elif choice == '2':
            customer_place_order()
            
        elif choice == '3':
            customer = um.get_current_user()
            print(f"\n--- Your Orders ---")
            order.view_orders_by_customer(customer)
            press_enter()
            
        elif choice == '4':
            um.logout()
            print("\nLogged out successfully!")
            press_enter()
            break
        else:
            print("\nInvalid choice!")
            press_enter()


def customer_place_order():
    """Customer - Place order (similar to waiter but self-service)"""
    
    clear_screen()
    print("\n" + "="*60)
    print("🛒 PLACE ORDER")
    print("="*60)
    
    customer_name = um.get_current_user()
    
    print("\nOrder Type: Takeout, Delivery")
    order_type = input("Order Type: ").strip()
    
    # Show menu
    print("\n--- Available Menu ---")
    menu.get_available_menu()
    
    # Collect items
    order_items = []
    
    while True:
        print("\n" + "-"*60)
        item_id = input("Item ID (or 'done'): ").strip()
        
        if item_id.lower() == 'done':
            break
        
        item = menu.get_menu_item_by_id(item_id)
        
        if not item:
            print("Item not found!")
            continue
        
        quantity = int(input(f"Quantity: ").strip())
        
        order_items.append({
            'item_id': item_id,
            'item_name': item['name'],
            'quantity': quantity,
            'price': item['price']
        })
        
        print(f"Added {quantity}x {item['name']}")
    
    if not order_items:
        print("\n❌ No items!")
        press_enter()
        return
    
    # Summary
    print("\n" + "="*60)
    print("ORDER SUMMARY")
    print("="*60)
    total = 0
    for item in order_items:
        subtotal = item['price'] * item['quantity']
        total += subtotal
        print(f"{item['item_name']} x{item['quantity']} - ₱{subtotal:.2f}")
    print(f"\n💰 Total: ₱{total:.2f}")
    
    confirm = input("\nConfirm? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        order_id = order.create_order(customer_name, order_items, order_type)
        
        if order_id:
            print(f"\nOrder #{order_id} placed!")
            print("Please proceed to cashier for payment.")
        else:
            print("\nFailed!")
    else:
        print("\nCancelled!")
    
    press_enter()


if __name__ == "__main__":
    main_menu()