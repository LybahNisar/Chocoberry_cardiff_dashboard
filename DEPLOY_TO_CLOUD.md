# Deploy Dashboard to Streamlit Cloud (FREE)

## What You'll Get
- Live URL: `https://your-dashboard.streamlit.app`
- Client can access 24/7 from UK
- No installation needed for client
- FREE hosting

---

## Step 1: Create GitHub Account (5 mins)

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Create account (free)

---

## Step 2: Upload Your Dashboard to GitHub (10 mins)

### Option A: Use GitHub Desktop (Easiest)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in
3. Click "Create New Repository"
   - Name: `chocoberry-dashboard`
   - Local Path: `C:\Users\GEO\Desktop\Dashboard`
4. Click "Create Repository"
5. Click "Publish repository"
6. Uncheck "Keep this code private" (if you want it free)
7. Click "Publish repository"

### Option B: Use GitHub Web (No software needed)

1. Go to [github.com](https://github.com)
2. Click "New" repository
3. Name: `chocoberry-dashboard`
4. Click "Create repository"
5. Click "uploading an existing file"
6. Drag and drop your entire Dashboard folder
7. Click "Commit changes"

---

## Step 3: Deploy to Streamlit Cloud (5 mins)

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "Sign in with GitHub"
3. Authorize Streamlit
4. Click "New app"
5. Fill in:
   - **Repository**: `chocoberry-dashboard`
   - **Branch**: `main`
   - **Main file path**: `dashboards/restaurant_dashboard.py`
6. Click "Deploy!"
7. Wait 2-3 minutes for deployment

---

## Step 4: Share with Client

Your dashboard will be live at:
```
https://[your-username]-chocoberry-dashboard.streamlit.app
```

Send this URL to your client in UK - they can view it immediately!

---

## Important Notes

### ⚠️ Data Privacy
Your CSV files will be PUBLIC on GitHub. If client data is sensitive:
- Make repository private (requires GitHub Pro $4/month)
- Or use dummy/anonymized data for demo

### ✅ Updates
When you update code:
1. Make changes locally
2. Push to GitHub (using GitHub Desktop or web)
3. Streamlit auto-redeploys in 1-2 mins

---

## Troubleshooting

**Error: "Module not found"**
→ Check `requirements.txt` is in root folder

**Dashboard doesn't load**
→ Check main file path is `dashboards/restaurant_dashboard.py`

**Need help?**
→ Streamlit has free support: [discuss.streamlit.io](https://discuss.streamlit.io)

---

## Alternative: Private Hosting

If you need private hosting:
1. **Streamlit Cloud for Teams** ($250/year)
2. **Heroku** (free tier available)
3. **Render** (free tier available)

---

**Total time: 20 minutes**  
**Cost: FREE**  
**Client access: Immediate via URL**
