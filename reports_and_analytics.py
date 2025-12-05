import csv
import os
from datetime import datetime, timedelta
from collections import Counter

report_cache = {}

def generate_sales_report(start_date, end_date, transactions_file='transactions.csv'):
    """
    Generate sales report for a date range
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        transactions_file: Path to transactions CSV
    
    Returns:
        Dictionary with sales summary
    """
    if not os.path.exists(transactions_file):
        print(f"{transactions_file} not found")
        return None
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD")
        return None
    
    total_sales = 0
    total_transactions = 0
    payment_breakdown = {'Cash': 0, 'Card': 0, 'E-Wallet': 0}
    daily_sales = {}
    total_discount = 0
    total_tax = 0
    total_service_charge = 0
    
    try:
        with open(transactions_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                trans_date = datetime.strptime(row['timestamp'].split(' ')[0], '%Y-%m-%d')
                
                if start <= trans_date <= end:
                    amount = float(row['total'])
                    total_sales += amount
                    total_transactions += 1
                    
                    payment_type = row['payment_type']
                    payment_breakdown[payment_type] = payment_breakdown.get(payment_type, 0) + amount
                    
                    date_str = trans_date.strftime('%Y-%m-%d')
                    daily_sales[date_str] = daily_sales.get(date_str, 0) + amount
                    
                    total_discount += float(row['discount'])
                    total_tax += float(row['tax'])
                    total_service_charge += float(row['service_charge'])
        
        report = {
            'start_date': start_date,
            'end_date': end_date,
            'total_sales': round(total_sales, 2),
            'total_transactions': total_transactions,
            'average_transaction': round(total_sales / total_transactions, 2) if total_transactions > 0 else 0,
            'payment_breakdown': payment_breakdown,
            'daily_sales': daily_sales,
            'total_discount': round(total_discount, 2),
            'total_tax': round(total_tax, 2),
            'total_service_charge': round(total_service_charge, 2)
        }
        
        return report
    
    except Exception as e:
        print(f"❌ Error generating sales report: {e}")
        return None


def get_best_selling_items(orders_file='orders.csv', order_items_file='order_items.csv', limit=10):
    """
    Get best-selling menu items
    
    Args:
        orders_file: Path to orders CSV
        order_items_file: Path to order items CSV
        limit: Number of top items to return
    
    Returns:
        List of tuples (item_name, quantity_sold)
    """
    if not os.path.exists(order_items_file):
        print(f"{order_items_file} not found")
        return []
    
    item_sales = Counter()
    
    try:
        with open(order_items_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                item_name = row['item_name']
                quantity = int(row['quantity'])
                item_sales[item_name] += quantity
        
        # Get top items
        best_sellers = item_sales.most_common(limit)
        return best_sellers
    
    except Exception as e:
        print(f"Error getting best-selling items: {e}")
        return []


def get_least_ordered_items(orders_file='orders.csv', order_items_file='order_items.csv', 
                            menu_file='menu_items.csv', limit=10):
    """
    Get least-ordered menu items
    
    Args:
        orders_file: Path to orders CSV
        order_items_file: Path to order items CSV
        menu_file: Path to menu items CSV
        limit: Number of items to return
    
    """
    if not os.path.exists(order_items_file) or not os.path.exists(menu_file):
        print(f"Required files not found")
        return []
    
    item_sales = Counter()
    all_menu_items = set()
    
    try:
        # Get all menu items
        with open(menu_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                all_menu_items.add(row['item_name'])
        
        # Count sales
        with open(order_items_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item_name = row['item_name']
                quantity = int(row['quantity'])
                item_sales[item_name] += quantity
        
        # Find items with 0 or low sales
        for item in all_menu_items:
            if item not in item_sales:
                item_sales[item] = 0
        
        # Get least ordered
        least_ordered = item_sales.most_common()[:-limit-1:-1]
        return least_ordered
    
    except Exception as e:
        print(f"Error getting least-ordered items: {e}")
        return []


def generate_inventory_summary(inventory_file='inventory.csv'):
    """
    Generate inventory summary report
    
    Args:
        inventory_file: Path to inventory CSV
    
    Returns:
        Dictionary with inventory summary
    """
    if not os.path.exists(inventory_file):
        print(f"{inventory_file} not found")
        return None
    
    total_items = 0
    low_stock_items = []
    out_of_stock_items = []
    
    try:
        with open(inventory_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                total_items += 1
                quantity = float(row['quantity'])
                reorder_level = float(row['reorder_level'])
                item_name = row['item_name']
                
                if quantity == 0:
                    out_of_stock_items.append(item_name)
                elif quantity <= reorder_level:
                    low_stock_items.append({
                        'item_name': item_name,
                        'quantity': quantity,
                        'unit': row['unit'],
                        'reorder_level': reorder_level
                    })
        
        summary = {
            'total_items': total_items,
            'low_stock_count': len(low_stock_items),
            'out_of_stock_count': len(out_of_stock_items),
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items
        }
        
        return summary
    
    except Exception as e:
        print(f"Error generating inventory summary: {e}")
        return None


def get_user_activity_summary(activity_file='user_activity.csv'):
    """
    Get user activity summary
    
    Args:
        activity_file: Path to user activity CSV
    
    Returns:
        Dictionary with activity summary
    """
    if not os.path.exists(activity_file):
        print(f"{activity_file} not found")
        return None
    
    user_actions = Counter()
    total_activities = 0
    recent_activities = []
    
    try:
        with open(activity_file, 'r') as file:
            reader = csv.DictReader(file)
            
            activities = list(reader)
            total_activities = len(activities)
            
            for row in activities:
                username = row['username']
                user_actions[username] += 1
            
            recent_activities = activities[-20:]
        
        summary = {
            'total_activities': total_activities,
            'active_users': len(user_actions),
            'user_actions': dict(user_actions.most_common()),
            'recent_activities': recent_activities
        }
        
        return summary
    
    except Exception as e:
        print(f"Error getting user activity: {e}")
        return None


def get_table_utilization(orders_file='orders.csv'):
    """
    Get table utilization statistics
    
    Args:
        orders_file: Path to orders CSV
    """
    if not os.path.exists(orders_file):
        print(f"{orders_file} not found")
        return None
    
    table_usage = Counter()
    total_dine_in = 0
    
    try:
        with open(orders_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                if row['order_type'] == 'Dine In' and row['table_number']:
                    table_num = row['table_number']
                    table_usage[table_num] += 1
                    total_dine_in += 1
        
        stats = {
            'total_dine_in_orders': total_dine_in,
            'tables_used': len(table_usage),
            'most_used_tables': table_usage.most_common(5),
            'table_usage': dict(table_usage)
        }
        
        return stats
    
    except Exception as e:
        print(f"Error getting table utilization: {e}")
        return None

def generate_revenue_breakdown(transactions_file='transactions.csv'):
    """
    Generate revenue breakdown by components
    
    Args:
        transactions_file: Path to transactions CSV
    
    """
    if not os.path.exists(transactions_file):
        print(f"{transactions_file} not found")
        return None
    
    total_subtotal = 0
    total_service = 0
    total_tax = 0
    total_discount = 0
    
    try:
        with open(transactions_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                total_subtotal += float(row['subtotal'])
                total_service += float(row['service_charge'])
                total_tax += float(row['tax'])
                total_discount += float(row['discount'])
        
        breakdown = {
            'subtotal': round(total_subtotal, 2),
            'service_charges': round(total_service, 2),
            'tax_collected': round(total_tax, 2),
            'discounts_given': round(total_discount, 2),
            'net_revenue': round(total_subtotal + total_service + total_tax - total_discount, 2)
        }
        
        return breakdown
    
    except Exception as e:
        print(f"Error generating revenue breakdown: {e}")
        return None


def export_report_to_csv(report_data, filename, headers):
    """
    Args:
        report_data: List of dictionaries or list of lists
        filename: Output filename
        headers: List of column headers
    """
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            
            for row in report_data:
                if isinstance(row, dict):
                    writer.writerow([row.get(h, '') for h in headers])
                else:
                    writer.writerow(row)
        
        print(f"Report exported to {filename}")
        return True
    
    except Exception as e:
        print(f"Error exporting report: {e}")
        return False

def display_sales_report(report):
    """Display formatted sales report"""
    if not report:
        return
    
    print("\n" + "="*80)
    print("SALES REPORT")
    print("="*80)
    print(f"Period: {report['start_date']} to {report['end_date']}")
    print(f"\nTotal Sales: ₱{report['total_sales']:,.2f}")
    print(f"Total Transactions: {report['total_transactions']}")
    print(f"Average Transaction: ₱{report['average_transaction']:,.2f}")
    
    print(f"\nRevenue Breakdown:")
    print(f"  Service Charges: ₱{report['total_service_charge']:,.2f}")
    print(f"  Tax Collected: ₱{report['total_tax']:,.2f}")
    print(f"  Discounts Given: ₱{report['total_discount']:,.2f}")
    
    print(f"\nPayment Method Breakdown:")
    for method, amount in report['payment_breakdown'].items():
        percentage = (amount / report['total_sales'] * 100) if report['total_sales'] > 0 else 0
        print(f"  {method}: ₱{amount:,.2f} ({percentage:.1f}%)")
    
    print("\nDaily Sales:")
    for date, amount in sorted(report['daily_sales'].items()):
        print(f"  {date}: ₱{amount:,.2f}")
    
    print("="*80)


def display_best_sellers(best_sellers):
    """Display best-selling items"""
    print("\n" + "="*60)
    print("BEST-SELLING ITEMS")
    print("="*60)
    print(f"{'Rank':<6} {'Item Name':<35} {'Quantity Sold':<15}")
    print("="*60)
    
    if not best_sellers:
        print("No data available")
    else:
        for i, (item, qty) in enumerate(best_sellers, 1):
            print(f"{i:<6} {item:<35} {qty:<15}")
    
    print("="*60)


def display_inventory_summary(summary):
    """Display inventory summary"""
    if not summary:
        return
    
    print("\n" + "="*80)
    print("INVENTORY SUMMARY")
    print("="*80)
    print(f"Total Items: {summary['total_items']}")
    print(f"Low Stock Items: {summary['low_stock_count']}")
    print(f"Out of Stock Items: {summary['out_of_stock_count']}")
    
    if summary['out_of_stock_items']:
        print("\n❌ OUT OF STOCK:")
        for item in summary['out_of_stock_items']:
            print(f"  - {item}")
    
    if summary['low_stock_items']:
        print("\nLOW STOCK ALERTS:")
        for item in summary['low_stock_items']:
            print(f"  - {item['item_name']}: {item['quantity']} {item['unit']} "
                  f"(Reorder at: {item['reorder_level']} {item['unit']})")
    
    print("="*80)


def display_user_activity(summary):
    """Display user activity summary"""
    if not summary:
        return
    
    print("\n" + "="*80)
    print("USER ACTIVITY SUMMARY")
    print("="*80)
    print(f"Total Activities Logged: {summary['total_activities']}")
    print(f"Active Users: {summary['active_users']}")
    
    print("\nTop Active Users:")
    for i, (user, count) in enumerate(list(summary['user_actions'].items())[:10], 1):
        print(f"  {i}. {user}: {count} actions")
    
    print("\nRecent Activities:")
    for activity in summary['recent_activities'][-10:]:
        print(f"  [{activity['timestamp']}] {activity['username']}: {activity['action']}")
    
    print("="*80)

def interactive_test():
    """Interactive testing menu"""
    
    while True:
        print("\n=== REPORTS & ANALYTICS SYSTEM ===")
        print("1. Sales Report (Date Range)")
        print("2. Best-Selling Items")
        print("3. Least-Ordered Items")
        print("4. Inventory Summary")
        print("5. User Activity Summary")
        print("6. Table Utilization")
        print("7. Revenue Breakdown")
        print("8. Daily Sales (Quick)")
        print("9. Weekly Sales (Quick)")
        print("10. Monthly Sales (Quick)")
        print("11. Exit")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
            report = generate_sales_report(start_date, end_date)
            if report:
                display_sales_report(report)
        
        elif choice == '2':
            try:
                limit = int(input("Top N items (default 10): ") or "10")
                best_sellers = get_best_selling_items(limit=limit)
                display_best_sellers(best_sellers)
            except ValueError:
                print("Invalid number")
        
        elif choice == '3':
            try:
                limit = int(input("Bottom N items (default 10): ") or "10")
                least_ordered = get_least_ordered_items(limit=limit)
                print("\n" + "="*60)
                print("LEAST-ORDERED ITEMS")
                print("="*60)
                for i, (item, qty) in enumerate(least_ordered, 1):
                    print(f"{i}. {item}: {qty} sold")
                print("="*60)
            except ValueError:
                print("Invalid number")
        
        elif choice == '4':
            summary = generate_inventory_summary()
            display_inventory_summary(summary)
        
        elif choice == '5':
            summary = get_user_activity_summary()
            display_user_activity(summary)
        
        elif choice == '6':
            stats = get_table_utilization()
            if stats:
                print("\n" + "="*60)
                print("🪑 TABLE UTILIZATION")
                print("="*60)
                print(f"Total Dine-in Orders: {stats['total_dine_in_orders']}")
                print(f"Tables Used: {stats['tables_used']}")
                print("\nMost Used Tables:")
                for table, count in stats['most_used_tables']:
                    print(f"  Table {table}: {count} times")
                print("="*60)
        
        elif choice == '7':
            breakdown = generate_revenue_breakdown()
            if breakdown:
                print("\n" + "="*60)
                print("REVENUE BREAKDOWN")
                print("="*60)
                print(f"Subtotal: ₱{breakdown['subtotal']:,.2f}")
                print(f"Service Charges: ₱{breakdown['service_charges']:,.2f}")
                print(f"Tax Collected: ₱{breakdown['tax_collected']:,.2f}")
                print(f"Discounts Given: -₱{breakdown['discounts_given']:,.2f}")
                print("-" * 60)
                print(f"Net Revenue: ₱{breakdown['net_revenue']:,.2f}")
                print("="*60)
        
        elif choice == '8':
            today = datetime.now().strftime('%Y-%m-%d')
            report = generate_sales_report(today, today)
            if report:
                display_sales_report(report)
        
        elif choice == '9':
            today = datetime.now()
            week_ago = (today - timedelta(days=7)).strftime('%Y-%m-%d')
            today_str = today.strftime('%Y-%m-%d')
            report = generate_sales_report(week_ago, today_str)
            if report:
                display_sales_report(report)
        
        elif choice == '10':
            today = datetime.now()
            month_ago = (today - timedelta(days=30)).strftime('%Y-%m-%d')
            today_str = today.strftime('%Y-%m-%d')
            report = generate_sales_report(month_ago, today_str)
            if report:
                display_sales_report(report)
        
        elif choice == '11':
            print("Goodbye!")
            break
        
        else:
            print("Invalid broddie")


if __name__ == "__main__":
    interactive_test()