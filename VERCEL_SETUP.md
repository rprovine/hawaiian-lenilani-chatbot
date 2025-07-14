# Vercel Deployment Setup for Hawaiian LeniLani Chatbot

## Prerequisites
- Vercel account (you have one at https://vercel.com/rprovines-projects)
- GitHub repository connected to Vercel

## Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/rprovines-projects
   - Click "Add New..." → "Project"

2. **Import GitHub Repository**
   - Select "Import Git Repository"
   - Choose `rprovine/hawaiian-lenilani-chatbot`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend` (⚠️ Important!)
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Environment Variables**
   Add these in the Vercel dashboard:
   ```
   REACT_APP_API_URL=https://your-backend-url.com
   REACT_APP_WEBSOCKET_URL=wss://your-backend-url.com
   ```
   
   For local testing, use:
   ```
   REACT_APP_API_URL=http://localhost:8000
   REACT_APP_WEBSOCKET_URL=ws://localhost:8000
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

## Option 2: Deploy via GitHub Actions

1. **Get Vercel Tokens**
   - Install Vercel CLI: `npm i -g vercel`
   - Run: `vercel login`
   - Run: `vercel link` (in the frontend directory)
   - This creates `.vercel/project.json` with your IDs

2. **Add GitHub Secrets**
   Go to your GitHub repo → Settings → Secrets → Actions:
   
   - `VERCEL_TOKEN`: Get from https://vercel.com/account/tokens
   - `VERCEL_ORG_ID`: Found in `.vercel/project.json`
   - `VERCEL_PROJECT_ID`: Found in `.vercel/project.json`

3. **Push to GitHub**
   The workflow will automatically deploy on push to main branch

## Option 3: Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel --prod
```

## Custom Domain Setup

1. In Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain (e.g., `chat.lenilani.com`)
3. Follow DNS configuration instructions

## Environment Variables for Production

Make sure to set these in Vercel dashboard:

```env
# Required
REACT_APP_API_URL=https://your-api-domain.com

# Optional
REACT_APP_WEBSOCKET_URL=wss://your-api-domain.com
REACT_APP_GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-X
```

## Notes

- The frontend is a static React app that can be hosted on Vercel's edge network
- The backend API needs to be hosted separately (Railway, Heroku, AWS, etc.)
- Make sure CORS is configured on your backend to allow requests from your Vercel domain
- The chat widget functionality requires the backend API to be running

## Troubleshooting

1. **Build Fails**: 
   - Check that root directory is set to `frontend`
   - Ensure all dependencies are in package.json

2. **API Connection Issues**:
   - Verify CORS settings on backend
   - Check environment variables are set correctly

3. **404 Errors**:
   - Make sure `vercel.json` includes the rewrite rules for React Router