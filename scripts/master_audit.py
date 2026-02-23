"""
MASTER FORENSIC AUDIT SCRIPT (ASCII SAFE)
Professional Debugger - Feb 21, 2026
"""
import sqlite3
import sys
import toml
import pandas as pd
from pathlib import Path
from datetime import datetime, date

# Force ASCII output to avoid Windows terminal encoding errors
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.flipdish_api import FlipDishAPI

SEP = "=" * 55

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

def run_audit():
    conn = sqlite3.connect('restaurant_data.db')

    section("1. DATABASE COVERAGE (Jan 4 - Feb 21)")
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    df['order_time'] = pd.to_datetime(df['order_time'], errors='coerce')
    df = df.dropna(subset=['order_time'])

    print(f"  Total orders in DB        : {len(df):,}")
    print(f"  Earliest order            : {df['order_time'].min()}")
    print(f"  Latest order              : {df['order_time'].max()}")

    jan4  = df[df['order_time'].dt.date == date(2026, 1, 4)]
    feb21 = df[df['order_time'].dt.date == date(2026, 2, 21)]
    print(f"  Jan 4 orders              : {len(jan4)}")
    print(f"  Feb 21 orders (today)     : {len(feb21)}")

    section("2. KPI ACCURACY (All Time)")
    total_revenue   = df['revenue'].sum()
    total_orders    = len(df)
    avg_order       = df['gross_sales'].mean()
    total_tax       = df['tax'].sum()
    total_delivery  = df['delivery_charges'].sum()

    print(f"  Total Revenue (GBP)       : {total_revenue:,.2f}")
    print(f"  Total Orders              : {total_orders:,}")
    print(f"  Average Order Value (GBP) : {avg_order:.2f}")
    print(f"  Total Tax (GBP)           : {total_tax:,.2f}")
    print(f"  Total Delivery (GBP)      : {total_delivery:,.2f}")

    section("3. DAILY GAP CHECK (Feb 13 - Feb 21)")
    check_dates = pd.date_range('2026-02-13', '2026-02-21').date
    for d in check_dates:
        count = len(df[df['order_time'].dt.date == d])
        status = "OK" if count > 50 else ("LOW" if count > 0 else "MISSING")
        print(f"  {d}  |  {count:>4} orders  |  {status}")

    section("4. LIVE API FETCH TEST")
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        token  = secrets["flipdish"]["bearer_token"]
        app_id = secrets["flipdish"]["app_id"]

        api = FlipDishAPI(token, app_id)
        page = 1
        all_live = []

        # Paginate through ALL available API orders
        while True:
            orders, total = api.fetch_orders_page(page=page, limit=100)
            if not orders:
                break
            all_live.extend(orders)
            print(f"  Fetched page {page}: {len(orders)} orders (total so far: {len(all_live)}/{total})")
            if len(orders) < 100:
                break
            page += 1

        print(f"\n  Total live orders in API window : {len(all_live)}")

        if all_live:
            times = sorted([o.get('PlacedTime','') for o in all_live if o.get('PlacedTime')])
            print(f"  API window START  : {times[0]}")
            print(f"  API window END    : {times[-1]}")

            api_df = pd.DataFrame({'time': pd.to_datetime(times)})
            api_by_day = api_df.groupby(api_df['time'].dt.date).size()
            print(f"\n  API Orders by Day:")
            for d, cnt in api_by_day.items():
                print(f"    {d}  |  {cnt} orders")

            db_ids  = set(df['order_id'].astype(str))
            api_ids = set(str(o.get('OrderId')) for o in all_live)
            missing = api_ids - db_ids
            print(f"\n  API orders NOT yet in DB: {len(missing)}")
            if missing:
                print("  ACTION REQUIRED: Click 'Sync New Orders' in the dashboard sidebar!")

    except Exception as e:
        print(f"  API Error: {e}")

    section("5. VERDICT")
    print(f"  Jan 4 data present       : {'PASS' if len(jan4) > 0 else 'FAIL'}")
    print(f"  Feb 21 data present      : {'PASS' if len(feb21) > 0 else 'SYNC NEEDED'}")
    print(f"  Orders realistic (>5000) : {'PASS' if total_orders > 5000 else 'FAIL'} ({total_orders:,})")
    print(f"  Revenue realistic(>50k)  : {'PASS' if total_revenue > 50000 else 'FAIL'} (GBP {total_revenue:,.0f})")
    print()

    conn.close()

if __name__ == "__main__":
    run_audit()
