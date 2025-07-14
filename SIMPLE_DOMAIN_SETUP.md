# 🌐 Simple Domain Setup - 3 Steps

## What You Need to Do:

### 1️⃣ After Railway Deployment

Once your app is deployed to Railway, you'll get a URL like:
```
https://hawaiian-chatbot-production.up.railway.app
```

### 2️⃣ Add This to Your DNS

Go to your domain provider (GoDaddy, Namecheap, Cloudflare, etc.) and add:

```
Type: CNAME
Name: chatbot.hawaii
Points to: hawaiian-chatbot-production.up.railway.app
```

**Example for different providers:**

**Cloudflare:**
- Type: CNAME
- Name: chatbot.hawaii
- Target: your-app.railway.app
- Proxy status: Proxied (orange cloud)

**GoDaddy:**
- Type: CNAME
- Host: chatbot.hawaii
- Points to: your-app.railway.app
- TTL: 600 seconds

### 3️⃣ Add Widget to hawaii.lenilani.com

Add this code to your website (in the HTML, before `</body>`):

```html
<!-- LeniLani Chatbot -->
<script>
  window.LeniLaniConfig = {
    apiUrl: 'https://chatbot.hawaii.lenilani.com'
  };
</script>
<script src="https://chatbot.hawaii.lenilani.com/widget.js"></script>
```

## That's It! 🎉

Your chatbot will be:
- **Available at:** chatbot.hawaii.lenilani.com
- **Embedded on:** hawaii.lenilani.com

## Quick Test:

1. **Test the subdomain:**
   ```
   https://chatbot.hawaii.lenilani.com
   ```

2. **Test the widget:**
   - Visit hawaii.lenilani.com
   - Look for chat bubble in bottom-right
   - Click to open chat

## If Something's Not Working:

**"Site can't be reached"**
- Wait 30 minutes for DNS to update
- Check CNAME record is correct

**"Chat bubble not showing"**
- Make sure widget code is added
- Check browser console (F12) for errors
- Try clearing cache

**Need help?**
- Email: reno@lenilani.com
- Phone: 808-766-1164