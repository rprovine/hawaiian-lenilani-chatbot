# Backend Deployment Guide for Hawaiian LeniLani Chatbot

This guide covers multiple deployment options for the backend API.

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway provides simple deployment with automatic SSL and easy environment management.

1. **Sign up/Login**: https://railway.app

2. **Deploy from GitHub**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and link project
   railway login
   railway link
   
   # Deploy
   railway up
   ```

3. **Set Environment Variables** in Railway Dashboard:
   ```env
   ANTHROPIC_API_KEY=your-api-key-here
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Get your URL**: Railway provides a URL like `hawaiian-lenilani-api.railway.app`

### Option 2: Render.com (Free Tier Available)

1. **Sign up**: https://render.com

2. **New Web Service**:
   - Connect GitHub repo
   - Choose "Web Service"
   - Runtime: Python 3
   - Build Command: `pip install -r requirements-minimal.txt && pip install email-validator gunicorn`
   - Start Command: `gunicorn api_backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Environment Variables**:
   - Add `ANTHROPIC_API_KEY`
   - Add `PYTHONPATH=/opt/render/project/src`

### Option 3: Fly.io (Global Edge Deployment)

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy**:
   ```bash
   fly auth login
   fly launch  # Follow prompts, app config is in fly.toml
   
   # Set secrets
   fly secrets set ANTHROPIC_API_KEY=your-api-key-here
   
   # Deploy
   fly deploy
   ```

### Option 4: Heroku

1. **Create `Procfile`**:
   ```
   web: gunicorn api_backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```

2. **Deploy**:
   ```bash
   heroku create hawaiian-lenilani-api
   heroku config:set ANTHROPIC_API_KEY=your-api-key-here
   git push heroku main
   ```

### Option 5: Google Cloud Run (Serverless)

1. **Build and Push**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/hawaiian-lenilani-api
   ```

2. **Deploy**:
   ```bash
   gcloud run deploy hawaiian-lenilani-api \
     --image gcr.io/YOUR_PROJECT/hawaiian-lenilani-api \
     --platform managed \
     --region us-west1 \
     --allow-unauthenticated
   ```

## 🔧 Environment Variables (All Platforms)

Required:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

Recommended:
```env
# CORS (your frontend domains)
CORS_ORIGINS=https://your-app.vercel.app,https://yourdomain.com

# Python
PYTHONPATH=/app  # or /opt/render/project/src for Render

# Optional
LOG_LEVEL=INFO
APP_ENV=production
```

## 🔒 Post-Deployment Setup

1. **Update Frontend Environment**:
   - In Vercel, update `REACT_APP_API_URL` to your backend URL
   - Example: `https://hawaiian-lenilani-api.railway.app`

2. **Test the Connection**:
   ```bash
   curl https://your-backend-url/health
   ```

3. **Monitor Logs**:
   - Railway: `railway logs`
   - Fly.io: `fly logs`
   - Render: Dashboard → Logs

## 📊 Recommended Services by Use Case

- **Hobby/Demo**: Render.com (free tier)
- **Production**: Railway or Fly.io
- **Enterprise**: Google Cloud Run or AWS
- **Maximum Simplicity**: Railway

## 🆘 Troubleshooting

### CORS Issues
Add your frontend URL to `CORS_ORIGINS` environment variable

### Import Errors
Ensure `PYTHONPATH` is set correctly:
- Docker/Railway: `/app`
- Render: `/opt/render/project/src`

### Memory Issues
Free tiers have limited memory. If you get memory errors:
- Reduce worker count in gunicorn
- Use `-w 2` instead of `-w 4`

### Cold Starts
Free tiers may have cold starts. Consider:
- Keeping at least 1 instance running
- Using a health check monitor to keep warm

## 🌺 Next Steps

1. Choose a platform based on your needs
2. Deploy the backend
3. Update frontend with backend URL
4. Test the full application

Need help? Contact reno@lenilani.com