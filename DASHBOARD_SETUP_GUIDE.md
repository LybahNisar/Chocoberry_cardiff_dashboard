# 🚀 Restaurant Dashboard Setup Guide

## Step 1: Install Python (5 minutes)

### Option A: Microsoft Store (Easiest)
1. Press `Windows + S` to open search
2. Type: **Microsoft Store**
3. Open Microsoft Store
4. Search for: **Python 3.12**
5. Click **Get** or **Install**
6. Wait for installation to complete

### Option B: Direct Download
1. Go to: https://www.python.org/downloads/
2. Click **Download Python 3.12.x**
3. Run the installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click **Install Now**

---

## Step 2: Verify Python Installation

Open **PowerShell** (not Command Prompt):
1. Press `Windows + X`
2. Click **Windows PowerShell** or **Terminal**

Run this command:
```powershell
python --version
```

You should see: `Python 3.12.x` or similar

---

## Step 3: Install Required Libraries

Copy and paste these commands **ONE BY ONE** into PowerShell:

```powershell
pip install streamlit
```

```powershell
pip install pandas
```

```powershell
pip install plotly
```

```powershell
pip install openpyxl
```

Each installation takes 10-30 seconds. You'll see progress bars.

---

## Step 4: Run the Dashboard

Once I create the dashboard code, you'll run:

```powershell
cd C:\Users\GEO\Desktop\Dashboard
streamlit run dashboards\restaurant_dashboard.py
```

The dashboard will open automatically in your browser!

---

## Troubleshooting

### If "python" command not found:
Try: `python3 --version` or `py --version`

### If "pip" command not found:
Try: `python -m pip install streamlit`

### If permission errors:
Run PowerShell as Administrator

---

**Ready? Start with Step 1!** ✅
