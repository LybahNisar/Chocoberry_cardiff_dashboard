"""
MASTER MERGE & IMPORT — FINAL FEB 23 VERSION
"""
import pandas as pd
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

RAW = Path("data/raw/chocoberry_cardiff")
DB  = Path("restaurant_data.db")

print("=" * 55)
print("  MASTER MERGE & IMPORT — FEB 23 UPDATE")
print("=" * 55)

# ── STEP 1: Load CSVs ──────────────────────────────────────
print("\n[1/6] Loading CSV files...")
files = ["sales_data.csv", "sales_data_21feb.csv", "sales_data_23feb.csv"]
dfs = []

for f in files:
    path = RAW / f
    if path.exists():
        df = pd.read_csv(path, dtype=str)
        df.columns = df.columns.str.strip()
        df["Order time"] = pd.to_datetime(df["Order time"], errors="coerce")
        print(f"  {f:<20} : {len(df):,} rows  [{df['Order time'].min().date()} -> {df['Order time'].max().date()}]")
        dfs.append(df)
    else:
        print(f"  {f:<20} : MISSING")

# ── STEP 2: Combine and Deduplicate ───────────────────────
print("\n[2/6] Merging and deduplicating by Order ID...")
combined = pd.concat(dfs, ignore_index=True)
print(f"  Combined total rows   : {len(combined):,}")

# Remove corrupted NaN ID rows
combined = combined.dropna(subset=["Order ID"])
combined["Order ID"] = combined["Order ID"].astype(str).str.strip()

# Deduplicate - keep the first occurrence after sorting by date (or just keep unique)
combined = combined.drop_duplicates(subset=["Order ID"], keep="first")
combined = combined.sort_values("Order time")
print(f"  Total unique orders   : {len(combined):,}")

# ── STEP 3: Verify date coverage ─────────────────────────
print("\n[3/6] Verifying date coverage...")
jan4  = combined[combined["Order time"].dt.date == pd.Timestamp("2026-01-04").date()]
feb21 = combined[combined["Order time"].dt.date == pd.Timestamp("2026-02-21").date()]
feb23 = combined[combined["Order time"].dt.date == pd.Timestamp("2026-02-23").date()]

print(f"  Earliest : {combined['Order time'].min()}")
print(f"  Latest   : {combined['Order time'].max()}")
print(f"  Jan 4    : {len(jan4)} orders   {'PASS' if len(jan4) > 0 else 'FAIL - ABORTING'}")
print(f"  Feb 21   : {len(feb21)} orders  {'PASS' if len(feb21) > 0 else 'MISSING'}")
print(f"  Feb 23   : {len(feb23)} orders  {'PASS' if len(feb23) > 0 else 'MISSING'}")

if len(jan4) == 0:
    print("\n  CRITICAL ERROR: Jan 4 data not present! Aborting to protect database.")
    exit(1)

# ── STEP 4: Backup DB and reimport ───────────────────────
print("\n[4/6] Backing up database and reimporting...")
backup = DB.parent / f"restaurant_data_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
if DB.exists():
    shutil.copy2(DB, backup)
    print(f"  Backup: {backup.name}")

conn = sqlite3.connect(str(DB))
conn.execute("DELETE FROM orders")
conn.commit()

# Clean numeric columns
numeric_cols = [
    "Gross sales", "Tax on gross sales", "Tips", "Delivery charges",
    "Service charges", "Additional charges", "Charges", "Revenue", "Refunds", "Discounts"
]
for col in numeric_cols:
    if col in combined.columns:
        combined[col] = combined[col].astype(str).str.replace(",", "", regex=False)
        combined[col] = pd.to_numeric(combined[col], errors="coerce").fillna(0.0)

# DB column mapping
col_map = {
    "Order ID":             "order_id",
    "Order time":           "order_time",
    "Property name":        "property_name",
    "Gross sales":          "gross_sales",
    "Tax on gross sales":   "tax",
    "Tips":                 "tips",
    "Delivery charges":     "delivery_charges",
    "Service charges":      "service_charges",
    "Additional charges":   "additional_charges",
    "Charges":              "charges",
    "Revenue":              "revenue",
    "Refunds":              "refunds",
    "Discounts":            "discounts",
    "Dispatch type":        "dispatch_type",
    "Payment method":       "payment_method",
    "Sales channel type":   "sales_channel_type",
    "Sales channel name":   "sales_channel_name",
    "Is preorder":          "is_preorder",
}

valid_cols = {k: v for k, v in col_map.items() if k in combined.columns}
df_import = combined[list(valid_cols.keys())].rename(columns=valid_cols)
df_import.to_sql("orders", conn, if_exists="append", index=False)
conn.commit()

# ── STEP 5: Final DB Audit ───────────────────────────────
print("\n[5/6] Final database audit...")
total   = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
revenue = conn.execute("SELECT SUM(revenue) FROM orders").fetchone()[0] or 0
avg     = conn.execute("SELECT AVG(gross_sales) FROM orders").fetchone()[0] or 0
tax     = conn.execute("SELECT SUM(tax) FROM orders").fetchone()[0] or 0
deliv   = conn.execute("SELECT SUM(delivery_charges) FROM orders").fetchone()[0] or 0
first   = conn.execute("SELECT MIN(order_time) FROM orders").fetchone()[0]
last    = conn.execute("SELECT MAX(order_time) FROM orders").fetchone()[0]
j4cnt   = conn.execute("SELECT COUNT(*) FROM orders WHERE order_time LIKE '2026-01-04%'").fetchone()[0]
f21cnt  = conn.execute("SELECT COUNT(*) FROM orders WHERE order_time LIKE '2026-02-21%'").fetchone()[0]
f23cnt  = conn.execute("SELECT COUNT(*) FROM orders WHERE order_time LIKE '2026-02-23%'").fetchone()[0]
conn.close()

print()
print("  " + "=" * 45)
print("  DASHBOARD KPI — GROUND TRUTH")
print("  " + "=" * 45)
print(f"  Total Orders          : {total:,}")
print(f"  Total Revenue   (GBP) : {revenue:,.2f}")
print(f"  Average Order   (GBP) : {avg:.2f}")
print(f"  Total Tax       (GBP) : {tax:,.2f}")
print(f"  Total Delivery  (GBP) : {deliv:,.2f}")
print(f"  Date Start            : {first}")
print(f"  Date End              : {last}")
print(f"  Jan 4 Orders          : {j4cnt} ({'PASS' if j4cnt > 0 else 'FAIL'})")
print(f"  Feb 21 Orders         : {f21cnt} ({'PASS' if f21cnt > 0 else 'FAIL'})")
print(f"  Feb 23 Orders         : {f23cnt} ({'PASS' if f23cnt > 0 else 'FAIL'})")
print()
overall = "PASS" if (j4cnt > 0 and f23cnt > 0 and total > 8000) else "NEEDS REVIEW"
print(f"  OVERALL RESULT        : {overall}")
print("  " + "=" * 45)
