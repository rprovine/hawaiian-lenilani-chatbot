# Deploy to DigitalOcean App Platform

## Quick Deploy Steps

1. **Create DigitalOcean Account** (if needed)
   - Sign up at https://www.digitalocean.com
   - Get $200 free credit for 60 days

2. **Install doctl CLI** (optional)
   ```bash
   # macOS
   brew install doctl
   
   # Or download from https://docs.digitalocean.com/reference/doctl/how-to/install/
   ```

3. **Deploy via Web Console**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect your GitHub account
   - Select `rprovine/hawaiian-lenilani-chatbot` repository
   - Select `main` branch
   - DigitalOcean will auto-detect the app.yaml file

4. **Configure Environment Variables**
   In the DigitalOcean dashboard, set these encrypted environment variables:
   - `ANTHROPIC_API_KEY`: (get from your .env file)
   - `LEAD_WEBHOOK_URL`: (get from your .env file)

5. **Deploy**
   - Click "Next" through the configuration
   - Choose "Basic" plan ($5/month)
   - Click "Create Resources"

## Deploy via CLI (Alternative)

```bash
# Authenticate
doctl auth init

# Create the app
doctl apps create --spec app.yaml

# List your apps to get the app ID
doctl apps list

# Update environment variables
doctl apps update YOUR_APP_ID --spec app.yaml
```

## Custom Domain Setup

1. In DigitalOcean App Platform:
   - Go to Settings → Domains
   - Add domain: `chatbot.hawaii.lenilani.com`
   - Copy the CNAME record value

2. In your DNS provider:
   - Add CNAME record:
     - Name: `chatbot.hawaii.lenilani.com`
     - Value: `your-app.ondigitalocean.app`

## Monitoring

- View logs: Apps → Your App → Runtime Logs
- View metrics: Apps → Your App → Insights
- Set up alerts: Apps → Your App → Settings → Alerts

## Costs

- Basic plan: $5/month (1 vCPU, 512MB RAM)
- Suitable for the chatbot with moderate traffic
- Auto-scales if needed (additional cost)

## Advantages over Railway/Render

1. **Better Python support** - Automatic detection and configuration
2. **Simpler deployment** - Just connect GitHub and go
3. **Free static site hosting** - Can host frontend too
4. **Built-in monitoring** - Better logs and metrics
5. **Predictable pricing** - Starts at $5/month
6. **Global CDN** - For static assets

## Widget Integration

Once deployed, add this to hawaii.lenilani.com:

```html
<script>
  window.LENILANI_CHATBOT_URL = 'https://your-app.ondigitalocean.app';
</script>
<script src="https://your-app.ondigitalocean.app/widget.js"></script>
```