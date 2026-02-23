"""
ONE-TIME MIGRATION SCRIPT
Copies your local SQLite data to Supabase
Run this ONCE from your local PC
"""
import sqlite3
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME     = os.getenv("DB_NAME")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ── Your local SQLite database ───────────────────────────
SQLITE_PATH = Path("restaurant_data.db")

def migrate():
    print("Connecting to Supabase...")
    pg = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    pg_cursor = pg.cursor()
    print("Connected successfully!")

    print("Creating tables in Supabase...")
    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            order_time TIMESTAMP,
            property_name TEXT,
            gross_sales REAL,
            tax REAL,
            tips REAL,
            delivery_charges REAL,
            service_charges REAL,
            additional_charges REAL,
            charges REAL,
            revenue REAL,
            refunds REAL,
            discounts REAL,
            dispatch_type TEXT,
            payment_method TEXT,
            sales_channel_type TEXT,
            sales_channel_name TEXT,
            is_preorder TEXT,
            status TEXT,
            raw_json TEXT
        )
    """)

    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id TEXT,
            order_time TIMESTAMP,
            item_name TEXT,
            category TEXT,
            price REAL,
            quantity INTEGER,
            revenue REAL
        )
    """)
    pg.commit()
    print("Tables created successfully!")

    # ── Read from SQLite ──────────────────────────────────
    print("Reading from local SQLite...")
    sqlite = sqlite3.connect(str(SQLITE_PATH))
    sqlite.row_factory = sqlite3.Row

    orders = sqlite.execute("SELECT * FROM orders").fetchall()
    items  = sqlite.execute("SELECT * FROM order_items").fetchall()
    print(f"Found {len(orders):,} orders and {len(items):,} items in SQLite")

    # ── Insert orders into Supabase ───────────────────────
    print("Migrating orders to Supabase...")
    success = 0
    skipped = 0
    for order in orders:
        try:
            pg_cursor.execute("""
                INSERT INTO orders (
                    order_id, order_time, property_name, gross_sales, tax, tips,
                    delivery_charges, service_charges, additional_charges, charges,
                    revenue, refunds, discounts, dispatch_type, payment_method,
                    sales_channel_type, sales_channel_name, is_preorder, status, raw_json
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (order_id) DO NOTHING
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
                order["status"],
                order["raw_json"]
            ))
            success += 1

            # Show progress every 500 orders
            if success % 500 == 0:
                print(f"  Progress: {success:,} orders migrated...")
                pg.commit()

        except Exception as e:
            print(f"  Skipped order {order['order_id']}: {e}")
            skipped += 1

    pg.commit()
    print(f"Orders done! Migrated: {success:,} | Skipped: {skipped}")

    # ── Insert items into Supabase ────────────────────────
    print("Migrating order items...")
    item_success = 0
    item_skipped = 0
    for item in items:
        try:
            pg_cursor.execute("""
                INSERT INTO order_items (
                    order_id, order_time, item_name, category, price, quantity, revenue
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                item["order_id"],
                item["order_time"],
                item["item_name"],
                item["category"],
                item["price"],
                item["quantity"],
                item["revenue"]
            ))
            item_success += 1

            # Show progress every 1000 items
            if item_success % 1000 == 0:
                print(f"  Progress: {item_success:,} items migrated...")
                pg.commit()

        except Exception as e:
            print(f"  Skipped item: {e}")
            item_skipped += 1

    pg.commit()

    # ── Final verification ────────────────────────────────
    print("\nVerifying migration...")
    pg_cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = pg_cursor.fetchone()[0]

    pg_cursor.execute("SELECT COUNT(*) FROM order_items")
    total_items = pg_cursor.fetchone()[0]

    pg_cursor.execute("SELECT MIN(order_time), MAX(order_time) FROM orders")
    date_range = pg_cursor.fetchone()

    pg_cursor.execute("SELECT SUM(revenue) FROM orders")
    total_revenue = pg_cursor.fetchone()[0] or 0

    sqlite.close()
    pg.close()

    print()
    print("=" * 50)
    print("  MIGRATION COMPLETE!")
    print("=" * 50)
    print(f"  Orders migrated  : {success:,}")
    print(f"  Items migrated   : {item_success:,}")
    print(f"  Total in Supabase: {total_orders:,} orders")
    print(f"  Total items      : {total_items:,}")
    print(f"  Date range       : {date_range[0]} → {date_range[1]}")
    print(f"  Total revenue    : £{total_revenue:,.2f}")
    print("=" * 50)

if __name__ == "__main__":
    migrate()