# 🎨 Visual Deployment Guide

## Deploy to Railway in 5 Steps

### Step 1: Click Deploy Button
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/hawaiian-lenilani-chatbot)

### Step 2: Configure Variables
```
ANTHROPIC_API_KEY = sk-ant-api03-xxxxx
LEAD_WEBHOOK_URL = https://webhook.site/xxxxx
PORT = 8000
```

### Step 3: Deploy
Click "Deploy" and wait ~3 minutes

### Step 4: Get Your URL
Railway gives you: `https://your-app.railway.app`

### Step 5: Test
Visit your URL and chat with Leni Begonia!

---

## 🎯 Deploy Checklist

```markdown
Before Deploy:
☐ Have Claude API key ready
☐ Have GitHub account
☐ Have webhook URL (optional)

During Deploy:
☐ Connect GitHub
☐ Add environment variables
☐ Click deploy
☐ Generate domain

After Deploy:
☐ Test chatbot
☐ Test lead capture
☐ Add to website
```

---

## 📱 Add to Your Website

```html
<!-- Copy this code -->
<script src="https://your-app.railway.app/widget.js"></script>
```

---

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| "Site can't be reached" | Wait 3 minutes for deploy |
| "Chatbot not responding" | Check API key in variables |
| "CORS error" | Update CORS_ORIGINS variable |
| "Module not found" | Check logs, restart service |

---

## 📞 Get Help

### Live Support
- **Call/Text**: 808-766-1164
- **Email**: reno@lenilani.com

### Resources
- [Railway Docs](https://docs.railway.app)
- [Claude API Docs](https://docs.anthropic.com)
- [GitHub Issues](https://github.com/YOUR_USERNAME/hawaiian-lenilani-chatbot/issues)