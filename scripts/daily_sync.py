"""
DAILY AUTO-SYNC SCRIPT
========================
Runs every night via Windows Task Scheduler.
Fetches all new orders from Flipdish API since the last sync
and saves them permanently to the local SQLite database.
Logs every run with timestamp so you can verify it worked.
"""
import sqlite3
import toml
import sys
import logging
from pathlib import Path
from datetime import datetime

# ── Paths ────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH      = PROJECT_ROOT / "restaurant_data.db"
LOG_PATH     = PROJECT_ROOT / "logs" / "daily_sync.log"
SECRETS_PATH = PROJECT_ROOT / ".streamlit" / "secrets.toml"

# ── Logging (writes to file + console) ───────────────────
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Add project to path for imports ──────────────────────
sys.path.insert(0, str(PROJECT_ROOT))
from utils.flipdish_api import FlipDishAPI


def run_daily_sync():
    log.info("=" * 50)
    log.info("DAILY SYNC STARTED")
    log.info("=" * 50)

    # 1. Load credentials
    try:
        secrets = toml.load(str(SECRETS_PATH))
        token   = secrets["flipdish"]["bearer_token"]
        app_id  = secrets["flipdish"]["app_id"]
        log.info(f"Credentials loaded. App ID: {app_id}")
    except Exception as e:
        log.error(f"Failed to load secrets.toml: {e}")
        return

    # 2. Connect to DB
    try:
        conn   = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        log.info(f"Connected to database: {DB_PATH.name}")
    except Exception as e:
        log.error(f"Failed to connect to database: {e}")
        return

    # 3. Fetch from Flipdish API (paginate through all available pages)
    api = FlipDishAPI(token, app_id)
    new_orders = 0
    page = 1

    try:
        while True:
            orders, total = api.fetch_orders_page(page=page, limit=100)
            if not orders:
                log.info("No more orders returned from API.")
                break

            log.info(f"Page {page}: received {len(orders)} orders from API (total in window: {total})")

            for order in orders:
                order_id = str(order.get("OrderId", "")).strip()
                if not order_id:
                    continue

                # Skip if already in database (safe deduplication)
                cursor.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
                if cursor.fetchone():
                    continue  # Already exists — skip

                # Dispatch type mapping
                dispatch_map = {"Pickup": "Collection", "DineIn": "Dine In", "TableService": "Dine In"}
                raw_dispatch = order.get("DeliveryType", "Unknown")

                cursor.execute("""
                    INSERT INTO orders (
                        order_id, order_time, property_name, gross_sales, tax, tips,
                        delivery_charges, service_charges, additional_charges, charges,
                        revenue, refunds, discounts, dispatch_type, payment_method,
                        sales_channel_type, sales_channel_name, is_preorder, status, raw_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    order.get("PlacedTime"),
                    order.get("Store", {}).get("Name", "Chocoberry Cardiff"),
                    float(order.get("OrderItemsAmount", 0) or 0),
                    float(order.get("TotalTax", 0) or 0),
                    float(order.get("TipAmount", 0) or 0),
                    float(order.get("DeliveryAmount", 0) or 0),
                    float(order.get("ServiceChargeAmount", 0) or 0),
                    float(order.get("ProcessingFee", 0) or 0),
                    0.0,
                    float(order.get("Amount", 0) or 0),
                    float(order.get("RefundedAmount", 0) or 0),
                    float((order.get("Voucher") or {}).get("Amount", 0) or 0),
                    dispatch_map.get(raw_dispatch, raw_dispatch),
                    order.get("PaymentAccountType", "Unknown"),
                    order.get("AppType", "Unknown"),
                    (order.get("Channel") or {}).get("Source", "Unknown"),
                    "Yes" if order.get("IsPreOrder") else "No",
                    order.get("OrderState", "Unknown"),
                    str(order)
                ))

                # Insert order items
                for item in order.get("OrderItems", []):
                    cursor.execute("""
                        INSERT INTO order_items (order_id, order_time, item_name, category, price, quantity, revenue)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        order_id,
                        order.get("PlacedTime"),
                        item.get("Name", "Unknown"),
                        item.get("MenuSectionName", "Unknown"),
                        float(item.get("Price", 0) or 0),
                        1,
                        float(item.get("PriceIncludingOptionSetItems", 0) or item.get("Price", 0) or 0),
                    ))

                new_orders += 1

            if len(orders) < 100:
                break  # Last page
            page += 1

        conn.commit()

    except Exception as e:
        log.error(f"Sync error: {e}")
        conn.rollback()
    finally:
        # Final DB stats for this run
        total_in_db = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        latest      = conn.execute("SELECT MAX(order_time) FROM orders").fetchone()[0]
        conn.close()

    log.info(f"New orders added this run : {new_orders}")
    log.info(f"Total orders in database  : {total_in_db:,}")
    log.info(f"Latest order in database  : {latest}")
    log.info("DAILY SYNC COMPLETE")
    log.info("=" * 50)


if __name__ == "__main__":
    run_daily_sync()
