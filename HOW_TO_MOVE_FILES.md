# How to Move Your CSV Files to the Dashboard Project

## Quick Instructions

**Move your 12 CSV files from Downloads to:**
```
C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\
```

---

## Method 1: Drag and Drop (Easiest - 30 seconds)

1. Open **two File Explorer windows** side by side:
   - Window 1: Navigate to your **Downloads** folder
   - Window 2: Navigate to `C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\`

2. In Downloads, find the folder with your CSV files (probably named `dashboard-sales_summary_report...`)

3. **Select all 12 CSV files:**
   - Click the first file
   - Hold `Ctrl + A` to select all

4. **Drag and drop** from Downloads → Dashboard folder

✅ Done!

---

## Method 2: Cut and Paste

1. **Navigate to your CSV files** in Downloads folder

2. **Select all 12 CSV files:**
   - Press `Ctrl + A`

3. **Cut the files:**
   - Press `Ctrl + X` (or right-click → Cut)

4. **Navigate to destination folder:**
   - Copy this path: `C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\`
   - Paste it in File Explorer address bar
   - Press Enter

5. **Paste the files:**
   - Press `Ctrl + V` (or right-click → Paste)

✅ Done!

---

## Method 3: Using PowerShell (If you know exact location)

If your CSV files are in a folder called `dashboard-sales_summary_report_-_summary` in Downloads:

```powershell
Move-Item -Path "C:\Users\GEO\Downloads\dashboard-sales_summary_report_-_summary\*.csv" -Destination "C:\Users\GEO\Desktop\Dashboard\data\raw\chocoberry_cardiff\" -Force
```

---

## Files to Move (12 total):

1. ✅ sales_data.csv (177 KB - most important)
2. ✅ sales_overview.csv
3. ✅ gross_sales_by_dispatch_type.csv
4. ✅ gross_sales_by_hour_of_day.csv
5. ✅ gross_sales_by_payment_method.csv
6. ✅ gross_sales_by_sales_channel.csv
7. ✅ gross_sales_per_day.csv
8. ✅ gross_sales_per_day_of_week.csv
9. ✅ revenue_after_refunds.csv
10. ✅ revenue_summary.csv
11. ✅ charges_summary.csv
12. ✅ total_charges.csv

---

## After Moving Files

Once files are moved, you're ready to choose your dashboard tool and start building!

**Next step:** Choose dashboard tool (Python, Power BI, Google Data Studio, or Excel)
