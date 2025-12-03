import datetime
import string

ADMIN_PLAINTEXT_PW = "AdminPass123!"

database = {
    "admin": {
        "password": "",
        "role": "admin",
        "activated": True,
        "user_details": {
            "name": "mcjabi",
            "birth_date": "1990-01-01",
            "phone": "8-7000",
            "email": "mcjabe@gmail.com",
        },
    }
}
current_user = None
current_display = "main"
is_running = True
ROLES = ("admin", "cashier", "waiter", "customer")


def get_unique_username():
    while True:
        username = input("Enter Username: ")
        if username in database:
            print("Username already taken!")
            continue
        return username


def get_confirmed_password(password, confirm):
    _, is_valid_pw, _ = password_validation(password)
    if not is_valid_pw:
        return False

    if password == confirm:
        return True
    else:
        print("Password doesn't match!")
        return False


def get_validated_field(prompt, validator, error_msg="Validation Error: "):
    while True:
        value = input(prompt)
        is_valid, message = validator(value)
        if is_valid:
            return value
        print(f"{error_msg}{message}")


def check_username_exists(username):
    if username not in database:
        print("Account doesn't exist!")
        return False
    return True


def password_validation(password):
    is_valid = True
    messages = []
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/'\""

    if len(password) < 8:
        messages.append("Password must contain at least 8 characters.")
        is_valid = False
    if not any(char.isupper() for char in password):
        messages.append("Password must contain at least 1 uppercase.")
        is_valid = False
    if not any(char.islower() for char in password):
        messages.append("Password must contain at least 1 lowercase.")
        is_valid = False
    if not any(char.isdigit() for char in password):
        messages.append("Password must contain at least 1 digit.")
        is_valid = False
    if not any(char in special_chars for char in password):
        messages.append("Password must contain at least 1 special character.")
        is_valid = False

    if is_valid:
        strength = "Strong Password!" if len(password) > 8 else "Normal Password."
        return password, True, strength
    else:
        all_messages = messages + ["Weak Password!"]
        return password, False, "\n".join(all_messages)


def is_valid_birth_date(date_string, date_format="%Y-%m-%d"):
    try:
        birth_date = datetime.datetime.strptime(date_string, date_format).date()
    except ValueError:
        return False, "Invalid date format or value (e.g., non-existent date)."

    if birth_date > datetime.date.today():
        return False, "Birth date cannot be in the future."
    return True, "Valid"


def is_valid_contact(phone):
    if len(phone) == 11 and phone.isdigit():
        return True, "Valid"
    return False, "Must be exactly 11 digits and contain only numbers."


def is_valid_email(email):
    if "@" in email and ".com" in email:
        return True, "Valid"
    return False, "Must contain '@' and '.com'"


def display_user_details(username):
    if username not in database:
        print(f"Error: User '{username}' not found.")
        return

    user_data = database[username]
    details = user_data["user_details"]

    print("\n----- User Details -----")
    print(f"Role: {user_data['role'].title()}")
    print(f"Name: {details['name']}")
    print(f"Birth Date: {details.get('birth_date', 'N/A')}")
    print(f"Phone: {details['phone']}")
    print(f"Email: {details['email']}")
    print("------------------------")


def register_account(
    username, password, role, name, birth_date, phone, email, activated=True
):
    database[username] = {
        "password": encrypt_password(password),
        "role": role,
        "activated": activated,
        "user_details": {
            "name": name,
            "birth_date": birth_date,
            "phone": phone,
            "email": email,
        },
    }
    print(f"Account {username} registered successfully!")
    display_user_details(username)


def login(username, password):
    global current_user, current_display
    if not check_username_exists(username):
        return
    if database[username]["password"] != encrypt_password(password):
        return "Incorrect Password!"
    if not database[username]["activated"]:
        return "Account is not activated!"
    current_user = username
    current_display = database[username]["role"]
    display_user_details(current_user)


def logout():
    global current_user, current_display
    current_user = None
    current_display = "main"
    print("Logged out successfully!")


def edit(username, key, value):
    global current_user
    if not check_username_exists(username):
        return

    if key == "username":
        if username in database:
            database[value] = database[username]
            del database[username]
            if current_user == username:
                current_user = value
    elif key == "password":
        database[username][key] = encrypt_password(value)
    elif key == "role" or key == "activated":
        database[username][key] = value
    elif key in database[username]["user_details"]:
        database[username]["user_details"][key] = value

    print(f"{key.title()} updated successfully!")


def account_status(username, activate_status):
    global current_user
    if not check_username_exists(username):
        return
    action = "activated" if activate_status else "deactivated"
    is_currently_active = database[username]["activated"]
    if is_currently_active == activate_status:
        print(f"Account {username} is already {action}.")
    else:
        edit(username, "activated", activate_status)
        if not activate_status:
            if username == current_user:
                print(f"Deactivated user {username} was logged out.")
                logout()


def encrypt_password(password):
    CIPHER = (
        list(string.ascii_lowercase)
        + list(string.ascii_uppercase)
        + list(string.punctuation)
        + list(string.digits)
        + [" "]
    )
    KEY = 5
    L = len(CIPHER)
    cipher_text = ""
    for char in password:
        try:
            index = CIPHER.index(char)
        except ValueError:
            cipher_text += char
            continue
        new_index = (index - KEY) % L
        cipher_text += CIPHER[new_index]
    return cipher_text


def decrypt_password(password):
    CIPHER = (
        list(string.ascii_lowercase)
        + list(string.ascii_uppercase)
        + list(string.punctuation)
        + list(string.digits)
        + [" "]
    )
    KEY = 5
    L = len(CIPHER)
    plain_text = ""
    for char in password:
        try:
            index = CIPHER.index(char)
        except ValueError:
            plain_text += char
            continue
        new_index = (index + KEY) % L
        plain_text += CIPHER[new_index]
    return plain_text


def remove_account(username):
    if check_username_exists(username):
        if current_user == username:
            logout()
        del database[username]
        print(f"Account {username} removed!")


def display(screen_name):
    print(f"\n===== {screen_name.replace('_', ' ').title()} =====")

    if screen_name == "main":
        print("1. Login \n2. Register \n3. Exit")
    elif screen_name == "admin":
        print(
            "1. User Management \n2. Menu Management \n3. Inventory Management \n4. Reports and Analytics \n5. Logout"
        )
    elif screen_name == "user_management":
        print(
            "1. Add User \n2. Edit User \n3. Remove User \n4. Display Database \n5. Back"
        )
    elif screen_name == "edit":
        print(
            "1. Change Username \n2. Change Password \n3. Change User Type \n4. Activate User \n5. Deactivate User\n6. Back"
        )
    elif screen_name == "customer":
        print("1. View Menu \n2. Order \n3. Logout")
    elif screen_name == "cashier":
        print("1. Process Billing \n2. View Transactions \n3. Logout")
    elif screen_name == "waiter":
        print(
            "1. Place Order \n2. Assign Table \n3. Update Order Status \n4. Track Order Status \n5. View Order Summary\n6. Logout"
        )
    elif screen_name == "database":
        print("--- All Registered Users ---")
        for username in database.keys():
            display_user_details(username)
        print("----------------------------")
    elif screen_name in [
        "menu_management",
        "inventory_management",
        "reports_analytics",
    ]:
        pass


def user_choice(screen_name):
    global is_running, current_display
    while True:
        choice = input("Enter Choice: ")

        match screen_name:
            case "main":
                match choice:
                    case "1":
                        print("\n===== Login ====")
                        login(input("Username: "), input("Password: "))
                        break
                    case "2":
                        print("\n===== Register ====")
                        username = get_unique_username()

                        new_password = None
                        while new_password is None:
                            password_attempt = input("Enter Password: ")
                            _, is_valid, msg = password_validation(password_attempt)
                            if not is_valid:
                                print(msg)
                                continue

                            confirmed_password_attempt = None
                            for attempt_count in range(3):
                                confirm_attempt = input("Confirm Password: ")
                                if get_confirmed_password(
                                    password_attempt, confirm_attempt
                                ):
                                    confirmed_password_attempt = password_attempt
                                    break
                                else:
                                    print(
                                        f"You have {2 - attempt_count} attempts left for confirmation!"
                                    )

                            if confirmed_password_attempt:
                                new_password = confirmed_password_attempt
                                print(msg)
                            else:
                                print(
                                    "Password confirmation failed. Please re-enter your password."
                                )

                        name = input("Enter Name: ").title()
                        birth_date = get_validated_field(
                            "Enter Birth Date (YYYY-MM-DD): ", is_valid_birth_date
                        )
                        phone = get_validated_field("Enter Phone: ", is_valid_contact)
                        email = get_validated_field("Enter Email: ", is_valid_email)
                        register_account(
                            username,
                            new_password,
                            "customer",
                            name,
                            birth_date,
                            phone,
                            email,
                        )
                        break
                    case "3":
                        is_running = False
                        print("Exiting application...")
                        break
                    case _:
                        print("Invalid choice. Please enter '1', '2', or '3'.")
                        continue

            case "admin":
                match choice:
                    case "1":
                        current_display = "user_management"
                        break
                    case "2":
                        current_display = "menu_management"
                        break
                    case "3":
                        current_display = "inventory_management"
                        break
                    case "4":
                        current_display = "reports_analytics"
                        break
                    case "5":
                        logout()
                        break
                    case _:
                        print("Invalid choice. Please enter 1-5.")
                        continue

            case "user_management":
                match choice:
                    case "1":
                        print("\n===== Register New User ====")
                        username = get_unique_username()

                        new_password = None
                        while new_password is None:
                            password_attempt = input("Enter Password: ")
                            _, is_valid, msg = password_validation(password_attempt)
                            if not is_valid:
                                print(msg)
                                continue

                            confirmed_password_attempt = None
                            for attempt_count in range(3):
                                confirm_attempt = input("Confirm Password: ")
                                if get_confirmed_password(
                                    password_attempt, confirm_attempt
                                ):
                                    confirmed_password_attempt = password_attempt
                                    break
                                else:
                                    print(
                                        f"You have {2 - attempt_count} attempts left for confirmation!"
                                    )

                            if confirmed_password_attempt:
                                new_password = confirmed_password_attempt
                                print(msg)
                            else:
                                print(
                                    "Password confirmation failed. Please re-enter your password."
                                )

                        role = get_validated_field(
                            f"Enter Type of User ({', '.join(ROLES)}): ",
                            lambda r: (
                                r.lower() in ROLES,
                                f"Invalid User Type! Must be one of: {ROLES}",
                            ),
                        )
                        name = input("Enter Name: ").title()
                        birth_date = get_validated_field(
                            "Enter Birth Date (YYYY-MM-DD): ", is_valid_birth_date
                        )
                        phone = get_validated_field("Enter Phone: ", is_valid_contact)
                        email = get_validated_field("Enter Email: ", is_valid_email)
                        register_account(
                            username, new_password, role, name, birth_date, phone, email
                        )
                        break
                    case "2":
                        current_display = "edit"
                        break
                    case "3":
                        print("\n===== Remove Account ====")
                        remove_account(input("Enter Username: "))
                        break
                    case "4":
                        display("database")
                        continue
                    case "5":
                        current_display = "admin"
                        break
                    case _:
                        print("Invalid choice. Please enter 1-5.")
                        continue

            case "edit":
                match choice:
                    case "1":
                        username = input("Username to change: ")
                        if not check_username_exists(username):
                            continue
                        new_username = get_unique_username()
                        edit(username, "username", new_username)
                        break
                    case "2":
                        username = input("Username to change password: ")
                        if not check_username_exists(username):
                            continue
                        while True:
                            current_pw_attempt = input("Enter CURRENT Password: ")
                            if database[username]["password"] == encrypt_password(
                                current_pw_attempt
                            ):
                                break
                            else:
                                print("Invalid password")
                                continue
                        new_password = None
                        while new_password is None:
                            password_attempt = input("Enter NEW Password: ")
                            _, is_valid, msg = password_validation(password_attempt)
                            if not is_valid:
                                print(msg)
                                continue
                            confirmed_password_attempt = None
                            for attempt_count in range(3):
                                confirm_attempt = input("Confirm NEW Password: ")
                                if get_confirmed_password(
                                    password_attempt, confirm_attempt
                                ):
                                    confirmed_password_attempt = password_attempt
                                    break
                                else:
                                    print(
                                        f"You have {2 - attempt_count} attempts left for confirmation!"
                                    )
                            if confirmed_password_attempt:
                                new_password = confirmed_password_attempt
                                print(msg)
                            else:
                                print(
                                    "New password confirmation failed. Returning to edit menu."
                                )
                                break
                        if new_password:
                            edit(username, "password", new_password)
                        break
                    case "3":
                        username = input("Username to change role: ")
                        if not check_username_exists(username):
                            continue
                        role = get_validated_field(
                            f"New Role ({', '.join(ROLES)}): ",
                            lambda r: (r.lower() in ROLES, "Invalid Role!"),
                        )
                        edit(username, "role", role.lower())
                        break
                    case "4":
                        print("\n===== Activate Account ====")
                        username = input("Username to activate: ")
                        account_status(username, True)
                        break
                    case "5":
                        print("\n===== Deactivate Account ====")
                        username = input("Username to deactivate: ")
                        account_status(username, False)
                        break
                    case "6":
                        current_display = "admin"
                        break
                    case _:
                        print("Invalid choice. Please enter 1-6.")
                        continue

            case "menu_management":
                pass

            case "inventory_management":
                pass

            case "reports_analytics":
                pass

            case "customer":
                match choice:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":
                        logout()
                        break
                    case _:
                        print("Invalid choice")

            case "cashier":
                match choice:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":
                        logout()
                        break
                    case _:
                        print("Invalid choice")

            case "waiter":
                match choice:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":
                        pass
                    case "4":
                        pass
                    case "5":
                        pass
                    case "6":
                        logout()
                        break
                    case _:
                        print("Invalid choice")

            case _:
                logout()
                break


def screen(screen_name):
    display(screen_name)
    user_choice(screen_name)


if database["admin"]["password"] == "":
    database["admin"]["password"] = encrypt_password(ADMIN_PLAINTEXT_PW)

while is_running:
    screen(current_display)
