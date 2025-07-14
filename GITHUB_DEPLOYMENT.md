# 🚀 GitHub to Production - Quick Deployment Guide

Deploy your Hawaiian LeniLani Chatbot in 15 minutes!

## 🎯 Fastest Option: Railway (Recommended)

Railway offers the simplest deployment with automatic GitHub integration.

### 1. Prepare Your Repository

```bash
# If you haven't already, push your code to GitHub
git add .
git commit -m "🌺 Ready for deployment"
git push origin main
```

### 2. Deploy to Railway

1. **Go to [railway.app](https://railway.app)**
2. **Click "Start a New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your `hawaiian-lenilani-chatbot` repository**

### 3. Configure Environment Variables

Click on your deployment and add these variables:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
LEAD_WEBHOOK_URL=https://webhook.site/your-url

# Email (optional)
LEAD_EMAIL=reno@lenilani.com

# Important for Railway
PORT=8000
```

### 4. Generate Public URL

1. Click "Settings" tab
2. Under "Domains", click "Generate Domain"
3. Your app is now live! 🎉

### 5. Test Your Deployment

Visit your Railway URL and test the chatbot!

---

## 💡 Alternative: Vercel + Render (Free Tier)

### Frontend (Vercel)

1. **Go to [vercel.com](https://vercel.com/new)**
2. **Import your GitHub repo**
3. **Configure:**
   - Root Directory: `frontend`
   - Framework: Create React App
   - Environment: `REACT_APP_API_URL=https://your-backend.onrender.com`

### Backend (Render)

1. **Go to [render.com](https://render.com)**
2. **New → Web Service**
3. **Connect GitHub repo**
4. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_backend.py`
   - Add all environment variables

---

## 📱 Add to Your Website

Once deployed, add this to your website:

```html
<!-- LeniLani AI Chatbot -->
<script src="https://your-app.railway.app/widget.js"></script>
```

---

## 🔧 Environment Variables Reference

```env
# Claude API (Required)
ANTHROPIC_API_KEY=your-key-here

# Lead Capture (Required)
LEAD_WEBHOOK_URL=https://webhook.site/xxxxx

# Contact Info
LEAD_EMAIL=reno@lenilani.com

# Frontend URL (for CORS)
CORS_ORIGINS=https://your-frontend-url.com
```

---

## 🆘 Quick Troubleshooting

### "Site can't be reached"
- Wait 2-3 minutes for deployment to complete
- Check Railway logs for errors
- Verify environment variables are set

### "Chatbot not responding"
- Check ANTHROPIC_API_KEY is correct
- Look for 401/429 errors in logs
- Verify CORS_ORIGINS includes your domain

### "Leads not capturing"
- Verify LEAD_WEBHOOK_URL is set
- Test webhook manually
- Check logs/leads/ directory

---

## 📞 Need Help?

- **Email**: reno@lenilani.com
- **Phone**: 808-766-1164
- **GitHub Issues**: [Create an issue](https://github.com/YOUR_USERNAME/hawaiian-lenilani-chatbot/issues)

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Claude API key ready
- [ ] Webhook URL configured
- [ ] Deployed to Railway/Vercel/Render
- [ ] Environment variables set
- [ ] Tested chatbot functionality
- [ ] Added widget to website
- [ ] Verified lead capture works

🌺 **Congratulations!** Your Hawaiian AI chatbot is live!