# 🚀 Quick Deploy Guide - 10 Minutes to Production

## Fastest Path: Railway + Vercel

### 1️⃣ Deploy Backend to Railway (5 min)

1. **Go to Railway**: https://railway.app
2. **Click**: "Start a New Project" → "Deploy from GitHub repo"
3. **Select**: `rprovine/hawaiian-lenilani-chatbot`
4. **Add Environment Variable**:
   ```
   ANTHROPIC_API_KEY = your-anthropic-api-key-here
   ```
5. **Click**: "Deploy Now"
6. **Copy**: Your API URL (like `https://hawaiian-lenilani-api-production.up.railway.app`)

### 2️⃣ Deploy Frontend to Vercel (5 min)

1. **Go to Vercel**: https://vercel.com/rprovines-projects
2. **Click**: "Add New..." → "Project"
3. **Import**: `rprovine/hawaiian-lenilani-chatbot`
4. **Configure**:
   - Root Directory: `frontend`
   - Framework: Create React App
5. **Add Environment Variable**:
   ```
   REACT_APP_API_URL = [Your Railway API URL from step 1]
   ```
6. **Click**: "Deploy"

### ✅ Done! Your app is live!

---

## Alternative: One-Click Deploy Options

### Deploy Backend to Render (Free)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rprovine/hawaiian-lenilani-chatbot)

After clicking:
1. Name your service
2. Add `ANTHROPIC_API_KEY` environment variable
3. Deploy

### Deploy Frontend to Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/rprovine/hawaiian-lenilani-chatbot)

Configure:
- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `frontend/build`

---

## 🎯 Verification Steps

1. **Test Backend**:
   ```bash
   curl https://your-backend-url/health
   ```

2. **Visit Frontend**:
   - Go to your Vercel/Netlify URL
   - Click "Start Talking Story"
   - Chat should work!

---

## 💡 Tips

- Railway gives you $5 free credits monthly
- Render free tier spins down after 15 min inactivity
- Vercel is always free for personal projects
- First deploy takes 5-10 min, updates are faster

Need help? The full deployment guides have more details!