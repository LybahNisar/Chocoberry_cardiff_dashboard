# 🔒 How to Set Your Dashboard Password

## ✅ Password Protection is Now Installed!

Your dashboard now requires a password to access. Here's how to set YOUR password:

---

## 📝 **STEP 1: Set Your Password**

1. **Open this file:**
   ```
   C:\Users\GEO\Desktop\Dashboard\.streamlit\secrets.toml
   ```

2. **Replace `YOUR_PASSWORD_HERE` with your actual password:**
   ```toml
   # Dashboard Password
   password = "MySecurePassword2026"
   ```

3. **Save the file**

**Tips for choosing a password:**
- ✅ Use at least 12 characters
- ✅ Mix letters, numbers, and symbols
- ✅ Don't use common words
- ❌ Don't use: "password123", "admin", "12345"

**Example good passwords:**
- `Choco#Berry@2026!`
- `Restaurant$Analytics#2024`
- `Cardiff*Sales!Secure`

---

## 🧪 **STEP 2: Test It**

1. **Stop your current dashboard** (if running)
   - Press `Ctrl + C` in the terminal

2. **Restart the dashboard:**
   ```bash
   py -m streamlit run dashboards\restaurant_dashboard.py
   ```

3. **You should see a login screen!** 🔒

4. **Enter your password** to access the dashboard

---

## ☁️ **STEP 3: For Cloud Deployment**

When you deploy to Streamlit Cloud later, you'll need to add the SAME password there:

1. Go to Streamlit Cloud → Your App → Settings → Secrets
2. Add:
   ```toml
   password = "YOUR_SAME_PASSWORD_HERE"
   ```

**Important:** Use the EXACT SAME password in both places!

---

## ✅ **What You Have Now:**

- ✅ Password-protected dashboard
- ✅ Login screen on startup
- ✅ Secure access only for people with password
- ✅ Works both locally AND when deployed to cloud

---

## 🔄 **How to Change Password Later:**

1. Edit `.streamlit\secrets.toml`
2. Change the password
3. Save and restart dashboard
4. If deployed, update password in Streamlit Cloud secrets too

---

## 🐛 **Troubleshooting:**

**Problem: "Missing secrets file"**
- Solution: Make sure `.streamlit\secrets.toml` exists
- Check you spelled `secrets.toml` correctly

**Problem: Password not working**
- Solution: Check there are no extra spaces in the password
- Make sure the file is saved

**Problem: Still no password screen**
- Solution: Restart the dashboard completely
- Check the code was added to `restaurant_dashboard.py`

---

**Your dashboard is now secure!** 🎉

Next step: Follow the deployment guide to put it online!
