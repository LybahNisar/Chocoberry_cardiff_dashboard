"""
PUSH SQLITE DATA TO SUPABASE
Reads from local restaurant_data.db
Pushes everything to Supabase cleanly
"""
import sqlite3
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME     = os.getenv("DB_NAME")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SQLITE_PATH = Path("restaurant_data.db")

def push():
    print("=" * 55)
    print("  PUSH SQLITE → SUPABASE")
    print("=" * 55)

    # Connect to both databases
    print("\nConnecting to SQLite...")
    sqlite = sqlite3.connect(str(SQLITE_PATH))
    sqlite.row_factory = sqlite3.Row

    print("Connecting to Supabase...")
    pg = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = pg.cursor()
    print("Both connected successfully!")

    # Read all orders from SQLite
    print("\nReading orders from SQLite...")
    orders = sqlite.execute("SELECT * FROM orders").fetchall()
    items  = sqlite.execute("SELECT * FROM order_items").fetchall()
    print(f"Found {len(orders):,} orders")
    print(f"Found {len(items):,} items")

    # Clear Supabase first
    print("\nClearing existing Supabase data...")
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    pg.commit()
    print("Cleared successfully!")

    # Push orders
    print("\nPushing orders to Supabase...")
    success = 0
    skipped = 0
    for order in orders:
        try:
            cursor.execute("""
                INSERT INTO orders (
                    order_id, order_time, property_name,
                    gross_sales, tax, tips, delivery_charges,
                    service_charges, additional_charges, charges,
                    revenue, refunds, discounts, dispatch_type,
                    payment_method, sales_channel_type,
                    sales_channel_name, is_preorder, status, raw_json
                ) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                ) ON CONFLICT (order_id) DO NOTHING
            """, (
                order["order_id"],
                order["order_time"],
                order["property_name"],
                order["gross_sales"],
                order["tax"],
                order["tips"],
                order["delivery_charges"],
                order["service_charges"],
                order["additional_charges"],
                order["charges"],
                order["revenue"],
                order["refunds"],
                order["discounts"],
                order["dispatch_type"],
                order["payment_method"],
                order["sales_channel_type"],
                order["sales_channel_name"],
                order["is_preorder"],
                order["status"]   if "status"   in order.keys() else None,
                order["raw_json"] if "raw_json" in order.keys() else None,
            ))
            success += 1
            if success % 500 == 0:
                pg.commit()
                print(f"  Progress: {success:,} orders pushed...")
        except Exception as e:
            print(f"  Skipped order {order['order_id']}: {e}")
            skipped += 1

    pg.commit()
    print(f"Orders done! Success: {success:,} | Skipped: {skipped}")

    # Push items
    print("\nPushing order items to Supabase...")
    item_success = 0
    for item in items:
        try:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, order_time, item_name,
                    category, price, quantity, revenue
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                item["order_id"],
                item["order_time"],
                item["item_name"],
                item["category"],
                item["price"],
                item["quantity"],
                item["revenue"],
            ))
            item_success += 1
            if item_success % 1000 == 0:
                pg.commit()
                print(f"  Progress: {item_success:,} items pushed...")
        except Exception as e:
            print(f"  Skipped item: {e}")

    pg.commit()

    # Final verification
    print("\nVerifying Supabase data...")
    cursor.execute("SELECT COUNT(*) FROM orders")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(revenue) FROM orders")
    revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT MIN(order_time), MAX(order_time) FROM orders")
    dates = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM orders WHERE order_time::date = '2026-01-04'")
    j4 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE order_time::date = '2026-02-23'")
    f23 = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_items")
    total_items = cursor.fetchone()[0]

    sqlite.close()
    pg.close()

    print()
    print("=" * 55)
    print("  SUPABASE PUSH COMPLETE!")
    print("=" * 55)
    print(f"  Orders pushed    : {success:,}")
    print(f"  Items pushed     : {item_success:,}")
    print(f"  Total in Supabase: {total:,} orders")
    print(f"  Total items      : {total_items:,}")
    print(f"  Total revenue    : £{revenue:,.2f}")
    print(f"  Date start       : {dates[0]}")
    print(f"  Date end         : {dates[1]}")
    print(f"  Jan 4 orders     : {j4}  {'✅ PASS' if j4 > 0 else '❌ FAIL'}")
    print(f"  Feb 23 orders    : {f23} {'✅ PASS' if f23 > 0 else '❌ FAIL'}")
    print("=" * 55)

if __name__ == "__main__":
    push()