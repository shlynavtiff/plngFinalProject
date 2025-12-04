import csv
import os
from datetime import datetime

# Global variables
users = {}
current_user = None
user_activity_log = []

VALID_ROLES = ["Admin", "Cashier", "Waiter", "Customer"]


def save_users_to_csv(filename="users.csv"):
    """Save all users to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["username", "password", "role", "name", "contact", "status"]
            )

            for username, user_info in users.items():
                writer.writerow(
                    [
                        username,
                        user_info["password"],
                        user_info["role"],
                        user_info["name"],
                        user_info["contact"],
                        user_info["status"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def load_users_from_csv(filename="users.csv"):
    """Load users from CSV file"""
    global users

    if not os.path.exists(filename):
        print(f"{filename} not found. Creating default admin account.")
        # Create default admin
        users["admin"] = {
            "username": "admin",
            "password": "admin123",
            "role": "Admin",
            "name": "Administrator",
            "contact": "N/A",
            "status": "Active",
        }
        save_users_to_csv()
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            users = {}

            for row in reader:
                users[row["username"]] = {
                    "username": row["username"],
                    "password": row["password"],
                    "role": row["role"],
                    "name": row["name"],
                    "contact": row["contact"],
                    "status": row["status"],
                }

        print(f"Loaded {len(users)} users from {filename}")
        return True
    except Exception as e:
        print(f"Error loading users: {e}")
        return False


def save_activity_log_to_csv(filename="user_activity.csv"):
    """Save user activity log to CSV"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "username", "action"])

            for log in user_activity_log:
                writer.writerow([log["timestamp"], log["username"], log["action"]])
        return True
    except Exception as e:
        print(f"Error saving activity log: {e}")
        return False


def load_activity_log_from_csv(filename="user_activity.csv"):
    """Load activity log from CSV"""
    global user_activity_log

    if not os.path.exists(filename):
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            user_activity_log = []

            for row in reader:
                user_activity_log.append(
                    {
                        "timestamp": row["timestamp"],
                        "username": row["username"],
                        "action": row["action"],
                    }
                )

        return True
    except Exception as e:
        print(f"Error loading activity log: {e}")
        return False


def register_user(username, password, role, name, contact):
    """
    Args:
        username: Unique username
        password: User password
        role: User role (Admin, Cashier, Waiter, Customer)
        name: Full name
        contact: Contact number

    """
    global users

    if not username or not password:
        print("Username and password cannot be empty")
        return False

    if username in users:
        print(f"Username '{username}' already exists")
        return False

    if role not in VALID_ROLES:
        print(f"Invalid role. Must be: {', '.join(VALID_ROLES)}")
        return False

    users[username] = {
        "username": username,
        "password": password,
        "role": role,
        "name": name,
        "contact": contact,
        "status": "Active",
    }

    log_activity(username, f"User registered as {role}")
    save_users_to_csv()
    save_activity_log_to_csv()

    print(f"User '{username}' registered successfully as {role}")
    return True


def login(username, password):
    global current_user

    if username not in users:
        print("Invalid username")
        return False

    user = users[username]

    if user["status"] == "Inactive":
        print("Account is deactivated. Contact admin.")
        return False

    if user["password"] != password:
        print("Invalid password")
        return False

    current_user = username
    log_activity(username, "Logged in")
    save_activity_log_to_csv()

    print(f"Welcome, {user['name']}! ({user['role']})")
    return True


def logout():
    """Logout current user"""
    global current_user

    if current_user is None:
        print("No user is logged in")
        return False

    log_activity(current_user, "Logged out")
    save_activity_log_to_csv()

    print(f"Goodbye, {users[current_user]['name']}!")
    current_user = None
    return True


def get_current_user():
    """Get currently logged in user"""
    return current_user


def get_user_role(username):
    """
    Get role of a user

    Args:
        username: Username to check

    Returns:
        Role string or None if user doesn't exist
    """
    if username not in users:
        return None
    return users[username]["role"]


def get_current_user_role():
    """Get role of currently logged in user"""
    if current_user is None:
        return None
    return users[current_user]["role"]


def update_profile(username, new_data):
    """
    Update user profile

    Args:
        username: Username to update
        new_data: Dictionary with fields to update (name, contact, password)

    Returns:
        True if successful, False if failed
    """
    global users

    if username not in users:
        print(f"User '{username}' not found")
        return False

    # Only current user or admin can update profiles
    if current_user != username and get_current_user_role() != "Admin":
        print("You don't have permission to update this profile")
        return False

    user = users[username]

    if "name" in new_data:
        user["name"] = new_data["name"]
    if "contact" in new_data:
        user["contact"] = new_data["contact"]
    if "password" in new_data:
        user["password"] = new_data["password"]

    log_activity(current_user or "system", f"Updated profile for {username}")
    save_users_to_csv()
    save_activity_log_to_csv()

    print(f"Profile updated for '{username}'")
    return True


def change_user_status(username, status):
    """
    Activate or deactivate user account (Admin only)

    Args:
        username: Username to modify
        status: 'Active' or 'Inactive'

    Returns:
        True if successful, False if failed
    """
    global users

    if get_current_user_role() != "Admin":
        print("Only admins can change user status")
        return False

    if username not in users:
        print(f"User '{username}' not found")
        return False

    if username == current_user:
        print("You cannot deactivate your own account")
        return False

    if status not in ["Active", "Inactive"]:
        print("Status must be 'Active' or 'Inactive'")
        return False

    users[username]["status"] = status

    log_activity(current_user, f"Changed {username} status to {status}")
    save_users_to_csv()
    save_activity_log_to_csv()

    print(f"User '{username}' is now {status}")
    return True


def change_user_role(username, new_role):
    """
    Change user role (Admin only)

    Args:
        username: Username to modify
        new_role: New role

    Returns:
        True if successful, False if failed
    """
    global users

    if get_current_user_role() != "Admin":
        print("Only admins can change user roles")
        return False

    if username not in users:
        print(f"User '{username}' not found")
        return False

    if new_role not in VALID_ROLES:
        print(f"Invalid role. Must be: {', '.join(VALID_ROLES)}")
        return False

    old_role = users[username]["role"]
    users[username]["role"] = new_role

    log_activity(current_user, f"Changed {username} role from {old_role} to {new_role}")
    save_users_to_csv()
    save_activity_log_to_csv()

    print(f"User '{username}' role changed from {old_role} to {new_role}")
    return True


def log_activity(username, action):
    """Log user activity"""
    global user_activity_log

    user_activity_log.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "action": action,
        }
    )


def display_all_users():
    """Display all users"""
    print("\n👥 ALL USERS")
    print("=" * 80)
    print(f"{'Username':<15} {'Name':<20} {'Role':<12} {'Contact':<15} {'Status':<10}")
    print("=" * 80)

    if not users:
        print("No users found.")
    else:
        for username, user in users.items():
            print(
                f"{username:<15} {user['name']:<20} {user['role']:<12} {user['contact']:<15} {user['status']:<10}"
            )

    print("=" * 80)


def display_activity_log(limit=10):
    """Display recent user activity"""
    print(f"\n📋 RECENT ACTIVITY (Last {limit})")
    print("=" * 80)
    print(f"{'Timestamp':<20} {'Username':<15} {'Action':<45}")
    print("=" * 80)

    if not user_activity_log:
        print("No activity logged yet.")
    else:
        for log in user_activity_log[-limit:]:
            print(f"{log['timestamp']:<20} {log['username']:<15} {log['action']:<45}")

    print("=" * 80)


def check_permission(required_role):
    """
    Check if current user has required role

    Args:
        required_role: Role required for action

    Returns:
        True if user has permission, False otherwise
    """
    if current_user is None:
        print("You must be logged in")
        return False

    user_role = get_current_user_role()

    if user_role != required_role and user_role != "Admin":
        print(f"This action requires {required_role} role")
        return False

    return True


def interactive_test():
    """Interactive testing menu"""
    load_users_from_csv()
    load_activity_log_from_csv()

    while True:
        print("\n=== USER MANAGEMENT SYSTEM ===")
        if current_user:
            print(
                f"Logged in as: {users[current_user]['name']} ({users[current_user]['role']})"
            )
        else:
            print("Not logged in")

        print("\n1. Login")
        print("2. Register New User")
        print("3. Logout")
        print("4. View All Users")
        print("5. Update My Profile")
        print("6. Change User Status (Admin)")
        print("7. Change User Role (Admin)")
        print("8. View Activity Log")
        print("9. Exit")
        print("\nAuto-save: ON")

        choice = input("\nEnter choice: ")

        if choice == "1":
            if current_user:
                print("You are already logged in")
                continue

            username = input("Username: ")
            password = input("Password: ")
            login(username, password)

        elif choice == "2":
            print("\n--- Register New User ---")
            username = input("Username: ")
            password = input("Password: ")

            print(f"\nRoles: {', '.join(VALID_ROLES)}")
            role = input("Role: ").title()

            name = input("Full Name: ")
            contact = input("Contact Number: ")

            register_user(username, password, role, name, contact)

        elif choice == "3":
            logout()

        elif choice == "4":
            display_all_users()

        elif choice == "5":
            if not current_user:
                print("Please login first")
                continue

            print("\n--- Update Profile ---")
            print("Leave blank to keep current value")

            new_data = {}
            name = input(f"New Name (current: {users[current_user]['name']}): ")
            if name:
                new_data["name"] = name

            contact = input(
                f"New Contact (current: {users[current_user]['contact']}): "
            )
            if contact:
                new_data["contact"] = contact

            password = input("New Password (leave blank to keep): ")
            if password:
                new_data["password"] = password

            if new_data:
                update_profile(current_user, new_data)
            else:
                print("⚠️ No changes made")

        elif choice == "6":
            if not current_user:
                print("Please login first")
                continue

            if get_current_user_role() != "Admin":
                print("Only admins can change user status")
                continue

            display_all_users()
            username = input("\nUsername to modify: ")
            status = input("New status (Active/Inactive): ").title()

            change_user_status(username, status)

        elif choice == "7":
            if not current_user:
                print("Please login first")
                continue

            if get_current_user_role() != "Admin":
                print("Only admins can change user roles")
                continue

            display_all_users()
            username = input("\nUsername to modify: ")
            print(f"Roles: {', '.join(VALID_ROLES)}")
            new_role = input("New role: ").title()

            change_user_role(username, new_role)

        elif choice == "8":
            try:
                limit = int(
                    input("How many recent activities to show? (default 10): ") or "10"
                )
                display_activity_log(limit)
            except ValueError:
                print("Invalid number")

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please select 1-9.")


if __name__ == "__main__":
    interactive_test()
