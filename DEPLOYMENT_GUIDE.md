# Vertex Training Platform - Complete Deployment Guide

## 🎯 Platform Overview

**Project:** Vertex Sales Training Platform  
**Location:** `/home/ubuntu/vertex_deploy_final`  
**Status:** ✅ Ready for deployment  
**Training Materials:** 18 PDFs included  

---

## 📦 What's Included

### Complete Platform:
- ✅ React frontend (built and optimized)
- ✅ Flask backend with PDF serving
- ✅ SQLite database (user authentication)
- ✅ 18 training materials (all modules)
- ✅ Learning library (videos, podcasts, books)
- ✅ Progress tracking system
- ✅ Activity logging

### Login Credentials:
**Trainer:** seanb@vertexprivatefunding.com / trainer123  
**Sales Team:**
- shawn@vertexprivatefunding.com / sales123
- tamara@vertexprivatefunding.com / sales123
- ronald@vertexprivatefunding.com / sales123

---

## 🚀 Deployment Options

### OPTION 1: Keep Current Temporary Server Running

**Current URL:** https://5000-i7na26kr4aovjdlkpgva9-a50c24c9.manusvm.computer

**Pros:**
- Already working
- No additional setup needed
- Free

**Cons:**
- May go to sleep when inactive
- Requires manual restart
- Not ideal for production

**To keep it running:**
Just use the current URL. I'll keep the server active.

---

### OPTION 2: Deploy to Render.com (Recommended - Free Tier Available)

**Steps:**
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub account (or use "Deploy from Git")
4. Upload this directory or connect a Git repo
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python src/main.py`
   - **Environment:** Python 3
6. Click "Create Web Service"
7. Render will give you a permanent URL like `https://vertex-training.onrender.com`

**Cost:** FREE (with some limitations) or $7/month for always-on

---

### OPTION 3: Deploy to Railway.app (Easy & Fast)

**Steps:**
1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Upload this directory
4. Railway auto-detects Python and deploys
5. Get permanent URL

**Cost:** $5/month (includes $5 free credit)

---

### OPTION 4: Deploy to Your Own Server/VPS

**Requirements:**
- Ubuntu/Linux server
- Python 3.11+
- 1GB RAM minimum

**Steps:**
```bash
# 1. Upload files to your server
scp -r vertex_deploy_final user@yourserver.com:/var/www/

# 2. SSH into server
ssh user@yourserver.com

# 3. Install dependencies
cd /var/www/vertex_deploy_final
pip install -r requirements.txt

# 4. Install production server
pip install gunicorn

# 5. Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app

# 6. Set up as system service (optional but recommended)
sudo nano /etc/systemd/system/vertex-training.service
```

**Service file content:**
```ini
[Unit]
Description=Vertex Training Platform
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/vertex_deploy_final
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable vertex-training
sudo systemctl start vertex-training
```

---

### OPTION 5: Deploy to Vercel/Netlify (Requires Adaptation)

These platforms are optimized for static sites and serverless functions. The current Flask app would need to be converted to serverless functions.

**Not recommended** unless you want to rebuild the backend.

---

## 💡 My Recommendation

**For immediate use:** Continue using the current temporary URL  
**For permanent deployment:** Use Render.com (free tier) or Railway.app ($5/month)

Both Render and Railway are:
- ✅ Easy to set up (5-10 minutes)
- ✅ Provide permanent URLs
- ✅ Auto-restart on crashes
- ✅ Support Python/Flask natively
- ✅ Include free SSL certificates
- ✅ Have free or low-cost tiers

---

## 📋 Files Included

```
vertex_deploy_final/
├── src/
│   ├── main.py (Flask server with PDF fix)
│   ├── static/
│   │   ├── index.html (React app)
│   │   ├── assets/ (JS/CSS)
│   │   └── training-materials/ (18 PDFs)
│   ├── models/ (Database models)
│   └── routes/ (API routes)
├── requirements.txt
├── deploy.sh (Quick start script)
└── DEPLOYMENT_GUIDE.md (this file)
```

---

## 🔧 Quick Start (Local Testing)

```bash
cd /home/ubuntu/vertex_deploy_final
./deploy.sh
```

Then visit: http://localhost:5000

---

## ❓ Need Help?

If you choose Render.com or Railway.app and need help, I can:
1. Create a GitHub repository for you
2. Provide step-by-step screenshots
3. Help configure environment variables
4. Troubleshoot deployment issues

Just let me know which option you'd like to pursue!

