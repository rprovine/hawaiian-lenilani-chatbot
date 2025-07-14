# Deploy to Render in 5 Minutes

## Step 1: Push to GitHub
```bash
git add -A
git commit -m "Ready for Render deployment"
git push origin main
```

## Step 2: Deploy on Render

1. Go to https://render.com and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select `rprovine/hawaiian-lenilani-chatbot`
5. Configure:
   - **Name**: `hawaiian-chatbot-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_backend.py`

## Step 3: Add Environment Variables

Click "Environment" and add:

1. **ANTHROPIC_API_KEY**
   - Get from your .env file
   - Starts with `sk-ant-api03-`

2. **LEAD_WEBHOOK_URL**
   - Get from your .env file
   - Or use webhook.site for testing

## Step 4: Deploy
Click **"Create Web Service"** and wait 2-3 minutes

## Step 5: Add to Your Website

Once deployed, you'll get a URL like: `https://hawaiian-chatbot-api.onrender.com`

Add to hawaii.lenilani.com:
```html
<!-- Add before </body> tag -->
<script>
  window.LENILANI_CHATBOT_URL = 'https://hawaiian-chatbot-api.onrender.com';
</script>
<script src="https://hawaiian-chatbot-api.onrender.com/widget.js"></script>
```

## That's it! 🎉

Your chatbot is now live. The free tier includes:
- 750 hours/month (enough for full month)
- Automatic HTTPS
- Auto-deploy when you push to GitHub

## Troubleshooting

If deployment fails:
1. Check the logs in Render dashboard
2. Make sure all files are pushed to GitHub
3. Environment variables are set correctly

## Custom Domain (Optional)

To use `chatbot.hawaii.lenilani.com`:
1. In Render: Settings → Custom Domains
2. Add `chatbot.hawaii.lenilani.com`
3. Add CNAME record in your DNS:
   - Name: `chatbot`
   - Value: `hawaiian-chatbot-api.onrender.com`