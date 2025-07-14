# 🚂 Railway Deployment - 10 Minute Setup

Deploy your Hawaiian LeniLani Chatbot to Railway in just 10 minutes!

## 📺 Video Tutorial
[Coming soon - contact reno@lenilani.com for walkthrough]

## 🚀 Quick Start

### 1. Sign Up for Railway
- Go to [railway.app](https://railway.app)
- Sign in with GitHub (recommended)

### 2. Create New Project

![Railway New Project](https://railway.app/button.svg)

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`hawaiian-lenilani-chatbot`** repository
4. Railway will automatically detect it's a Python app

### 3. Configure Environment Variables

Click on your service, then go to **Variables** tab and add:

```env
# REQUIRED - Copy these exactly
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx  # Your Claude API key
LEAD_WEBHOOK_URL=https://webhook.site/xxxxx  # Your webhook URL
PORT=8000

# OPTIONAL - But recommended
LEAD_EMAIL=reno@lenilani.com
CORS_ORIGINS=*  # Change to your domain later
```

### 4. Update Start Command

1. Go to **Settings** tab
2. Under **Deploy**, find **Start Command**
3. Change it to:
   ```
   python run_backend.py
   ```

### 5. Generate Public URL

1. In **Settings** tab
2. Under **Networking**
3. Click **Generate Domain**
4. You'll get something like: `your-app-production.up.railway.app`

### 6. Deploy Frontend (Same Project)

1. Click **+ New** → **GitHub Repo**
2. Select same repository
3. In **Settings**:
   - Set **Root Directory**: `frontend`
   - Set **Build Command**: `npm install && npm run build`
   - Set **Start Command**: `npx serve -s build -l $PORT`
4. In **Variables** add:
   ```
   REACT_APP_API_URL=https://your-backend-service.railway.internal:8000
   ```
5. Generate another domain for frontend

## 🎯 Complete Setup in Railway

Your project should have:
- ✅ Backend service (Python)
- ✅ Frontend service (Node.js)
- ✅ Both with public domains
- ✅ Environment variables configured

## 🧪 Test Your Deployment

1. **Visit your frontend URL**
   ```
   https://your-frontend.railway.app
   ```

2. **Test the chatbot**
   - Click the chat widget
   - Say "Hello"
   - Provide test email/phone
   - Check webhook.site for lead

## 🔧 Common Issues & Fixes

### "Application failed to respond"
```bash
# Make sure PORT is set to 8000 in variables
# Check logs for errors
```

### "CORS error in browser"
```bash
# Update CORS_ORIGINS to include your frontend URL:
CORS_ORIGINS=https://your-frontend.railway.app
```

### "Module not found error"
```bash
# Make sure requirements.txt is in root directory
# Railway should auto-detect Python and install deps
```

### "Frontend shows blank page"
```bash
# Update REACT_APP_API_URL to your backend URL
# Must start with https://
```

## 💰 Costs

- **Hobby Plan**: $5/month (includes $5 of usage)
- **Typical usage**: $10-20/month
- **Free trial**: $5 credit on signup

## 🚀 Advanced Configuration

### Custom Domain
1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records as shown

### Auto-Deploy from GitHub
1. Already enabled by default!
2. Every push to main = automatic deploy

### Monitoring
1. Check **Metrics** tab for usage
2. Set up alerts in Settings

### Database (Optional)
1. Click **+ New** → **Database** → **PostgreSQL**
2. Railway handles connection automatically

## 📱 Add to Your Website

Once deployed, add this code to hawaii.lenilani.com:

```html
<!-- Start of LeniLani Chatbot -->
<script>
  window.LeniLaniConfig = {
    apiUrl: 'https://your-backend.railway.app'
  };
</script>
<script src="https://your-frontend.railway.app/widget.js"></script>
<!-- End of LeniLani Chatbot -->
```

## ✅ Final Checklist

- [ ] Both services deployed
- [ ] Environment variables set
- [ ] Public URLs generated
- [ ] Chatbot responding
- [ ] Lead capture working
- [ ] Added to website

## 🎉 Success!

Your chatbot is now live on Railway! 

**Next steps:**
1. Share your Railway URLs
2. Test lead capture thoroughly
3. Add custom domain (optional)
4. Monitor usage and costs

## 📞 Need Help?

- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **Email**: reno@lenilani.com
- **Phone**: 808-766-1164

---

💡 **Pro Tip**: Star your Railway project to find it easily later!