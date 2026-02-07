# 🚀 How to Run Your Dashboard

## Quick Start

1. **Open PowerShell** (or Terminal)

2. **Navigate to your project folder:**
   ```powershell
   cd C:\Users\GEO\Desktop\Dashboard
   ```

3. **Run the dashboard:**
   ```powershell
   py -m streamlit run dashboards\restaurant_dashboard.py
   ```

4. **The dashboard will open automatically in your browser!**
   - If it doesn't open automatically, go to: http://localhost:8501

---

## What You'll See

Your dashboard includes:

### ✅ **Requirement 1: Sales Dashboards**
- Daily sales trends
- Weekly analysis
- Monthly overview
- Interactive charts with date range filters

### ✅ **Requirement 2: Delivery vs Dine-In Analysis**
- Sales breakdown by dispatch type (Collection, Delivery, Dine In, Take Away)
- Pie charts and bar graphs
- Average order values per type

### ✅ **Requirement 3: Sales Channel Analysis**
- Performance by channel (POS, Uber Eats, Deliveroo, Just Eat)
- Market share visualizations
- Order count and revenue comparison

### ✅ **Requirement 4 & 5: Demand Forecasting & Peak Hours**
- Hourly sales patterns
- Peak hour identification
- Day-of-week analysis
- Busiest times highlighted

---

## Dashboard Features

- 🎛️ **Filters**: Date range, dispatch type, sales channel
- 📊 **Interactive Charts**: Hover for details, zoom, pan
- 📈 **Live KPIs**: Total revenue, average order, order count
- 📱 **Responsive**: Works on any screen size

---

## Stopping the Dashboard

Press `Ctrl + C` in PowerShell to stop the server

---

## Troubleshooting

**If you see an error:**
1. Make sure you're in the correct folder
2. Check that CSV files are in: `data/raw/chocoberry_cardiff/`
3. Try: `py -m streamlit run dashboards\restaurant_dashboard.py`

**If browser doesn't open:**
- Manually open: http://localhost:8501
- Or: http://127.0.0.1:8501

---

**Ready to see your dashboard? Run the command now!** 🎉
