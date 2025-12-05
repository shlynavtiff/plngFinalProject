import csv
import os
from datetime import datetime

transactions = {}
transaction_counter = 1000
discount_codes = {
    "WELCOME10": 0.10,
    "STUDENT15": 0.15,
    "VIP20": 0.20,
    "SENIOR": 0.20,
}

PAYMENT_TYPES = ["Cash", "Card", "E-Wallet"]
SERVICE_CHARGE_RATE = 0.10  # 10% service charge
TAX_RATE = 0.12  # 12% VAT


def save_transactions_to_csv(filename="transactions.csv"):
    """Save all transactions to CSV file"""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "transaction_id",
                    "order_id",
                    "subtotal",
                    "service_charge",
                    "tax",
                    "discount",
                    "total",
                    "payment_type",
                    "amount_paid",
                    "change",
                    "timestamp",
                    "cashier",
                ]
            )

            for trans_id, trans in transactions.items():
                writer.writerow(
                    [
                        trans["transaction_id"],
                        trans["order_id"],
                        trans["subtotal"],
                        trans["service_charge"],
                        trans["tax"],
                        trans["discount"],
                        trans["total"],
                        trans["payment_type"],
                        trans["amount_paid"],
                        trans["change"],
                        trans["timestamp"],
                        trans["cashier"],
                    ]
                )
        return True
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False


def load_transactions_from_csv(filename="transactions.csv"):
    """Load transactions from CSV file"""
    global transactions, transaction_counter

    if not os.path.exists(filename):
        print(f"{filename} not found. Starting fresh.")
        return False

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            transactions = {}
            max_trans_id = 1000

            for row in reader:
                trans_id = int(row["transaction_id"])
                max_trans_id = max(max_trans_id, trans_id)

                transactions[trans_id] = {
                    "transaction_id": trans_id,
                    "order_id": int(row["order_id"]),
                    "subtotal": float(row["subtotal"]),
                    "service_charge": float(row["service_charge"]),
                    "tax": float(row["tax"]),
                    "discount": float(row["discount"]),
                    "total": float(row["total"]),
                    "payment_type": row["payment_type"],
                    "amount_paid": float(row["amount_paid"]),
                    "change": float(row["change"]),
                    "timestamp": row["timestamp"],
                    "cashier": row["cashier"],
                }

            transaction_counter = max_trans_id + 1

        print(f"Loaded {len(transactions)} transactions from {filename}")
        return True
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return False


def calculate_subtotal(order_items):
    """
    Calculate subtotal from order items

    Args:
        order_items: List of items with price and quantity
        Example: [{'item_name': 'Burger', 'price': 150, 'quantity': 2}]

    Returns:
        Subtotal amount
    """
    subtotal = 0
    for item in order_items:
        subtotal += item["price"] * item["quantity"]
    return subtotal


def calculate_total(
    order_items, discount_code=None, apply_service_charge=True, apply_tax=True
):
    """
    Calculate total bill with all charges

    Args:
        order_items: List of order items
        discount_code: Optional discount code
        apply_service_charge: Whether to apply service charge
        apply_tax: Whether to apply tax

    """
    subtotal = calculate_subtotal(order_items)

    service_charge = subtotal * SERVICE_CHARGE_RATE if apply_service_charge else 0

    subtotal_with_service = subtotal + service_charge

    discount_amount = 0
    discount_rate = 0
    if discount_code and discount_code.upper() in discount_codes:
        discount_rate = discount_codes[discount_code.upper()]
        discount_amount = subtotal_with_service * discount_rate

    after_discount = subtotal_with_service - discount_amount

    tax = after_discount * TAX_RATE if apply_tax else 0

    total = after_discount + tax

    return {
        "subtotal": round(subtotal, 2),
        "service_charge": round(service_charge, 2),
        "discount": round(discount_amount, 2),
        "discount_code": discount_code.upper() if discount_code else None,
        "tax": round(tax, 2),
        "total": round(total, 2),
    }


def apply_discount(total, discount_code):
    """
    Apply discount to total

    Args:
        total: Total amount before discount
        discount_code: Discount code

    Returns:
        Discounted amount or original if invalid code
    """
    if discount_code.upper() in discount_codes:
        discount_rate = discount_codes[discount_code.upper()]
        discount_amount = total * discount_rate
        return round(total - discount_amount, 2)
    else:
        print(f"Invalid discount code: {discount_code}")
        return total


def process_payment(
    order_id,
    order_items,
    payment_type,
    amount_paid,
    discount_code=None,
    cashier="System",
):
    """
    Process payment and create transaction record

    Args:
        order_id: ID of the order being paid
        order_items: List of order items
        payment_type: Payment method (Cash, Card, E-Wallet)
        amount_paid: Amount customer paid (for cash)
        discount_code: Optional discount code
        cashier: Username of cashier processing payment

    Returns:
        transaction_id if successful, None if failed
    """
    global transactions, transaction_counter

    if payment_type not in PAYMENT_TYPES:
        print(f"Invalid payment type. Must be: {', '.join(PAYMENT_TYPES)}")
        return None

    bill = calculate_total(order_items, discount_code)

    if payment_type == "Cash" and amount_paid < bill["total"]:
        print(
            f"Insufficient payment. Total: ₱{bill['total']:.2f}, Paid: ₱{amount_paid:.2f}"
        )
        return None

    change = 0
    if payment_type == "Cash":
        change = round(amount_paid - bill["total"], 2)
    else:
        amount_paid = bill["total"]  # For card/e-wallet, amount paid = total

    transaction_id = transaction_counter
    transaction_counter += 1

    transactions[transaction_id] = {
        "transaction_id": transaction_id,
        "order_id": order_id,
        "subtotal": bill["subtotal"],
        "service_charge": bill["service_charge"],
        "tax": bill["tax"],
        "discount": bill["discount"],
        "total": bill["total"],
        "payment_type": payment_type,
        "amount_paid": amount_paid,
        "change": change,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cashier": cashier,
    }

    save_transactions_to_csv()

    print(f"Payment processed successfully! Transaction ID: {transaction_id}")
    if payment_type == "Cash" and change > 0:
        print(f"Change: ₱{change:.2f}")

    return transaction_id


def generate_receipt(transaction_id, order_items=None):
    """
    Generate receipt for a transaction

    Args:
        transaction_id: ID of the transaction
        order_items: List of order items (optional, for detailed receipt)

    """
    if transaction_id not in transactions:
        print(f"Transaction ID {transaction_id} not found")
        return None

    trans = transactions[transaction_id]

    receipt = f"""
{'='*60}
           RESTAURANT MANAGEMENT SYSTEM
                    OFFICIAL RECEIPT
{'='*60}
Transaction ID: {trans['transaction_id']}
Order ID: {trans['order_id']}
Date: {trans['timestamp']}
Cashier: {trans['cashier']}
{'='*60}
"""

    # Add order items if provided
    if order_items:
        receipt += "\nITEMS ORDERED:\n"
        receipt += f"{'Item':<30} {'Qty':<5} {'Price':<12} {'Total':<12}\n"
        receipt += "-" * 60 + "\n"

        for item in order_items:
            item_total = item["price"] * item["quantity"]
            receipt += f"{item['item_name']:<30} {item['quantity']:<5} ₱{item['price']:<11.2f} ₱{item_total:<11.2f}\n"

        receipt += "-" * 60 + "\n"

    receipt += f"""
Subtotal:               ₱{trans['subtotal']:>10.2f}
Service Charge (10%):   ₱{trans['service_charge']:>10.2f}
"""

    if trans["discount"] > 0:
        receipt += f"Discount:              -₱{trans['discount']:>10.2f}\n"

    receipt += f"""Tax (12%):              ₱{trans['tax']:>10.2f}
{'='*60}
TOTAL:                  ₱{trans['total']:>10.2f}
{'='*60}
Payment Type: {trans['payment_type']}
Amount Paid:            ₱{trans['amount_paid']:>10.2f}
"""

    if trans["change"] > 0:
        receipt += f"Change:                 ₱{trans['change']:>10.2f}\n"

    receipt += f"""{'='*60}
        Thank you for dining with us!
           Please come again! 😊
{'='*60}
"""

    return receipt


def get_transaction(transaction_id):
    """
    Get transaction details

    Args:
        transaction_id: ID of the transaction
    """
    if transaction_id not in transactions:
        print(f"Transaction ID {transaction_id} not found")
        return None

    return transactions[transaction_id]


def get_daily_sales(date=None):
    """
    Get total sales for a specific date

    Args:
        date: Date string (YYYY-MM-DD), defaults to today

    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    daily_total = 0
    transaction_count = 0
    payment_breakdown = {"Cash": 0, "Card": 0, "E-Wallet": 0}

    for trans in transactions.values():
        trans_date = trans["timestamp"].split(" ")[0]
        if trans_date == date:
            daily_total += trans["total"]
            transaction_count += 1
            payment_breakdown[trans["payment_type"]] += trans["total"]

    return {
        "date": date,
        "total_sales": round(daily_total, 2),
        "transaction_count": transaction_count,
        "payment_breakdown": payment_breakdown,
    }


def display_all_transactions():
    """Display all transactions"""
    print("\n" + "=" * 100)
    print(
        f"{'Trans ID':<10} {'Order ID':<10} {'Total':<12} {'Payment':<12} {'Cashier':<15} {'Timestamp':<20}"
    )
    print("=" * 100)

    if not transactions:
        print("No transactions found.")
    else:
        for trans in transactions.values():
            print(
                f"{trans['transaction_id']:<10} {trans['order_id']:<10} "
                f"₱{trans['total']:<11.2f} {trans['payment_type']:<12} "
                f"{trans['cashier']:<15} {trans['timestamp']:<20}"
            )

    print("=" * 100)


def add_discount_code(code, rate):
    """
    Add a new discount code

    Args:
        code: Discount code name
        rate: Discount rate (0.10 = 10%)

    """
    global discount_codes

    if rate < 0 or rate > 1:
        print("Discount rate must be between 0 and 1")
        return False

    discount_codes[code.upper()] = rate
    print(f"Discount code '{code.upper()}' added ({rate*100}% off)")
    return True


def display_discount_codes():
    """Display all available discount codes"""
    print("\nAVAILABLE DISCOUNT CODES")
    print("=" * 50)
    print(f"{'Code':<20} {'Discount':<15}")
    print("=" * 50)

    for code, rate in discount_codes.items():
        print(f"{code:<20} {rate*100:.0f}%")

    print("=" * 50)


def interactive_test():
    """Interactive testing menu"""
    load_transactions_from_csv()

    while True:
        print("\n=== BILLING & PAYMENT SYSTEM ===")
        print("1. Process Payment")
        print("2. View Transaction")
        print("3. Generate Receipt")
        print("4. View All Transactions")
        print("5. View Daily Sales")
        print("6. View Discount Codes")
        print("7. Add Discount Code")
        print("8. Exit")
        print("\nAuto-save: ON")

        choice = input("\nEnter choice: ")

        if choice == "1":
            print("\n--- Process Payment ---")

            try:
                order_id = int(input("Order ID: "))
            except ValueError:
                print("Invalid order ID")
                continue

            # Simulate order items (in real integration, get from ordering module)
            print("\nEnter order items (type 'done' when finished):")
            order_items = []
            while True:
                item_name = input("  Item name (or 'done'): ")
                if item_name.lower() == "done":
                    break

                try:
                    price = float(input("  Price: "))
                    quantity = int(input("  Quantity: "))
                    order_items.append(
                        {"item_name": item_name, "price": price, "quantity": quantity}
                    )
                except ValueError:
                    print(" Invalid input")

            if not order_items:
                print("No items entered")
                continue

            # Show bill preview
            discount_input = input("\nDiscount code (leave blank for none): ")
            bill = calculate_total(
                order_items, discount_input if discount_input else None
            )

            print(f"\n--- BILL PREVIEW ---")
            print(f"Subtotal: ₱{bill['subtotal']:.2f}")
            print(f"Service Charge: ₱{bill['service_charge']:.2f}")
            if bill["discount"] > 0:
                print(f"Discount: -₱{bill['discount']:.2f}")
            print(f"Tax: ₱{bill['tax']:.2f}")
            print(f"TOTAL: ₱{bill['total']:.2f}")

            print(f"\nPayment types: {', '.join(PAYMENT_TYPES)}")
            payment_type = input("Payment type: ").title()

            if payment_type == "Cash":
                try:
                    amount_paid = float(input(f"Amount paid: "))
                except ValueError:
                    print("Invalid amount")
                    continue
            else:
                amount_paid = bill["total"]

            cashier = input("Cashier username: ")

            trans_id = process_payment(
                order_id,
                order_items,
                payment_type,
                amount_paid,
                discount_input if discount_input else None,
                cashier,
            )

            if trans_id:
                print("\nGenerate receipt? (yes/no): ", end="")
                if input().lower() == "yes":
                    receipt = generate_receipt(trans_id, order_items)
                    print(receipt)

        elif choice == "2":
            try:
                trans_id = int(input("Transaction ID: "))
                trans = get_transaction(trans_id)
                if trans:
                    print("\n--- TRANSACTION DETAILS ---")
                    for key, value in trans.items():
                        print(f"{key}: {value}")
            except ValueError:
                print("Invalid transaction ID")

        elif choice == "3":
            try:
                trans_id = int(input("Transaction ID: "))
                receipt = generate_receipt(trans_id)
                if receipt:
                    print(receipt)
            except ValueError:
                print("Invalid transaction ID")

        elif choice == "4":
            display_all_transactions()

        elif choice == "5":
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            sales = get_daily_sales(date if date else None)

            print(f"\nDAILY SALES REPORT - {sales['date']}")
            print("=" * 60)
            print(f"Total Sales: ₱{sales['total_sales']:.2f}")
            print(f"Total Transactions: {sales['transaction_count']}")
            print("\nPayment Breakdown:")
            for payment_type, amount in sales["payment_breakdown"].items():
                print(f"  {payment_type}: ₱{amount:.2f}")
            print("=" * 60)

        elif choice == "6":
            display_discount_codes()

        elif choice == "7":
            code = input("Discount code name: ")
            try:
                rate = float(input("Discount rate (e.g., 0.15 for 15%): "))
                add_discount_code(code, rate)
            except ValueError:
                print("Invalid rate")

        elif choice == "8":
            print("aaaaaaaaaaaaa")
            break

        else:
            print("Invalid choice! Please select 1-8.")


if __name__ == "__main__":
    interactive_test()
