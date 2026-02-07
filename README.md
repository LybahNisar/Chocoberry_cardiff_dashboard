# Restaurant Analytics Dashboard Project

**Client:** Afrikana / Chocoberry Restaurant Group  
**Data Source:** Flipdish POS System  
**Time Period:** Last 180 Days (Aug 2025 - Feb 2026)  
**Analyst:** [Your Name]  
**Project Start:** February 4, 2026

---

## Project Objective

Build automated analytics dashboards to provide actionable insights across 6 key business areas:

1. ✅ **Automated Sales Dashboards** - Daily, weekly, monthly performance tracking
2. ✅ **Branch Performance Analysis** - Identify underperforming locations
3. ✅ **Channel Analysis** - Delivery vs Dine-in (Talabat, UberEats, in-store)
4. ⚠️ **Menu Profitability** - High-margin vs low-margin items (data pending)
5. ✅ **Demand Forecasting** - Optimize staff scheduling
6. ✅ **Peak Time Prediction** - Predict busy days and hours

---

## Current Status

**Phase:** Data Collection & Project Setup  
**Progress:** 20% Complete  
**Branches Covered:** 1 of N (Chocoberry Cardiff only)

### Data Collected
- ✅ Sales Summary Report (180 days) - Chocoberry Cardiff
- ✅ All 12 CSV exports (sales, channels, hourly patterns, etc.)
- ❌ Menu Items Report (Flipdish system error - alternative approach needed)
- ❌ Other branch data (access pending)
- ❌ Menu cost data (client to provide)

---

## Folder Structure

```
Dashboard/
├── README.md                          # This file - project overview
├── data/                              # All data files
│   ├── raw/                          # Original CSV exports from Flipdish
│   │   ├── chocoberry_cardiff/       # By branch - CSV files go directly here
│   │   │   ├── sales_data.csv
│   │   │   ├── sales_overview.csv
│   │   │   ├── gross_sales_by_dispatch_type.csv
│   │   │   │   └── ... (other CSVs)
│   │   ├── afrikana/                 # Other branches (when available)
│   │   └── other_locations/
│   ├── processed/                    # Cleaned and combined data
│   │   ├── all_branches_combined.csv
│   │   ├── hourly_patterns.csv
│   │   └── channel_analysis.csv
│   └── external/                     # Data from client
│       ├── menu_costs.xlsx
│       └── commission_rates.xlsx
├── notebooks/                         # Analysis notebooks (if using Python)
│   ├── 01_data_exploration.ipynb
│   ├── 02_sales_analysis.ipynb
│   ├── 03_forecasting_model.ipynb
│   └── 04_dashboard_prototypes.ipynb
├── dashboards/                        # Dashboard files
│   ├── sales_dashboard.pbix          # Power BI files
│   ├── branch_performance.pbix
│   ├── demand_forecasting.pbix
│   └── screenshots/                  # Dashboard screenshots for documentation
├── scripts/                           # Automation scripts (if using Python)
│   ├── data_processing.py
│   ├── load_data.py
│   ├── forecasting_model.py
│   └── utils.py
├── docs/                              # Documentation
│   ├── data_dictionary.md            # Explain each CSV file and column
│   ├── insights_summary.md           # Key findings and recommendations
│   ├── user_guide.md                 # How to use the dashboards
│   └── technical_notes.md            # Implementation details
├── reports/                           # Output reports
│   ├── weekly_summary.pdf
│   └── presentation.pptx
└── requirements.txt                   # Python dependencies (if applicable)
```

---

## Technology Stack

**Chosen Tool:** [To be decided - Power BI / Python / Google Data Studio]

**Why:**
- [Justification for chosen tool]

**Alternatives Considered:**
- Option A: Power BI - Professional, licensed
- Option B: Python (Streamlit) - Custom, free, flexible
- Option C: Google Data Studio - Free, cloud-based

---

## Data Sources

### Available from Flipdish
- Sales transactions (order-level detail)
- Revenue breakdowns (gross sales, tax, tips, charges)
- Channel data (delivery partners, POS)
- Dispatch types (delivery, dine-in, collection)
- Temporal patterns (hourly, daily, weekly)

### Needed from Client
- Menu item costs (for profitability calculation)
- Delivery commission rates (Deliveroo, Uber Eats, etc.)
- Staff wage data (optional - for ROI calculation)
- Access credentials for all branches

---

## Known Limitations

1. **Menu Items Report Unavailable**
   - Flipdish export fails with "Bad Request" error
   - Alternative: Request data from client or use order-level approximation

2. **Single Branch Data**
   - Currently have Chocoberry Cardiff only
   - Need access to all locations for branch comparison

3. **Cost Data Missing**
   - Cannot calculate profit margins without ingredient costs
   - Can only show revenue and bestsellers

---

## Next Steps

1. ✅ Create folder structure
2. ⬜ Move downloaded CSV files to proper location
3. ⬜ Choose dashboard tool
4. ⬜ Request missing data from client
5. ⬜ Begin data analysis and dashboard development

---

## Contact & Support

**Analyst:** [Your contact info]  
**Client Contact:** [Client contact]  
**Project Timeline:** 3-4 weeks to first deliverable
