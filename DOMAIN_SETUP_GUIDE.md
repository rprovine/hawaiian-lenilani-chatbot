# 🌐 Domain Setup Guide - chatbot.hawaii.lenilani.com

## Part 1: Point chatbot.hawaii.lenilani.com to Railway

### Step 1: Get Your Railway URL
After deploying to Railway, you'll have a URL like:
- `your-app-name.railway.app`

### Step 2: Add Custom Domain in Railway

1. **In Railway Dashboard:**
   - Click on your deployed service
   - Go to **Settings** → **Domains**
   - Click **+ Custom Domain**
   - Enter: `chatbot.hawaii.lenilani.com`
   - Railway will show you DNS settings

2. **Railway will provide:**
   ```
   Type: CNAME
   Name: chatbot.hawaii
   Value: your-app-name.railway.app
   ```

### Step 3: Update DNS Settings

Go to your DNS provider (where hawaii.lenilani.com is registered):

**If using Cloudflare:**
1. Log into Cloudflare
2. Select your domain
3. Go to DNS
4. Add record:
   ```
   Type: CNAME
   Name: chatbot.hawaii
   Target: your-app-name.railway.app
   Proxy: ON (orange cloud)
   ```

**If using GoDaddy:**
1. Log into GoDaddy
2. Go to DNS Management
3. Add record:
   ```
   Type: CNAME
   Host: chatbot.hawaii
   Points to: your-app-name.railway.app
   TTL: 600
   ```

**If using Namecheap:**
1. Go to Advanced DNS
2. Add new record:
   ```
   Type: CNAME Record
   Host: chatbot.hawaii
   Value: your-app-name.railway.app
   TTL: Automatic
   ```

### Step 4: Wait for DNS Propagation
- Usually takes 5-30 minutes
- Check status at: https://dnschecker.org

### Step 5: Enable HTTPS in Railway
- Railway automatically provisions SSL
- No additional configuration needed

---

## Part 2: Add Chatbot Widget to hawaii.lenilani.com

### Option 1: Simple Widget Embed

Add this code to **every page** where you want the chatbot (before `</body>` tag):

```html
<!-- Hawaiian LeniLani AI Chatbot -->
<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'https://chatbot.hawaii.lenilani.com/widget.js';
    script.async = true;
    script.onload = function() {
      console.log('LeniLani Chatbot loaded successfully');
    };
    document.body.appendChild(script);
  })();
</script>
<!-- End Chatbot -->
```

### Option 2: With Configuration

```html
<!-- Hawaiian LeniLani AI Chatbot with Settings -->
<script>
  window.LeniLaniConfig = {
    apiUrl: 'https://chatbot.hawaii.lenilani.com',
    position: 'bottom-right',
    primaryColor: '#F4A261',
    greeting: 'Aloha! How can I help your business today?',
    companyInfo: {
      name: 'LeniLani Consulting',
      owner: 'Reno Provine',
      email: 'reno@lenilani.com',
      phone: '808-766-1164'
    }
  };
</script>
<script src="https://chatbot.hawaii.lenilani.com/widget.js" async></script>
```

### Option 3: WordPress Installation

**Method A - Using Header/Footer Plugin:**
1. Install "Insert Headers and Footers" plugin
2. Go to Settings → Insert Headers and Footers
3. Paste the widget code in "Scripts in Footer"
4. Save

**Method B - Edit theme:**
1. Go to Appearance → Theme Editor
2. Edit `footer.php`
3. Add widget code before `</body>`
4. Save

**Method C - Create custom plugin:**
Create `lenilani-chatbot.php`:
```php
<?php
/**
 * Plugin Name: LeniLani AI Chatbot
 * Description: Adds AI chatbot to your Hawaiian business website
 * Version: 1.0
 */

function add_lenilani_chatbot() {
    ?>
    <script>
      window.LeniLaniConfig = {
        apiUrl: 'https://chatbot.hawaii.lenilani.com'
      };
    </script>
    <script src="https://chatbot.hawaii.lenilani.com/widget.js" async></script>
    <?php
}
add_action('wp_footer', 'add_lenilani_chatbot');
```

### Option 4: Google Tag Manager

1. Create new tag in GTM
2. Tag Type: Custom HTML
3. Paste widget code
4. Trigger: All Pages
5. Publish

---

## 🧪 Testing Your Setup

### Test 1: Domain Access
```bash
# Check if domain resolves
curl https://chatbot.hawaii.lenilani.com/health

# Should return:
{"status":"healthy","message":"Aloha!"}
```

### Test 2: Widget Loading
1. Visit hawaii.lenilani.com
2. Open browser console (F12)
3. Should see: "LeniLani Chatbot loaded successfully"
4. Chat bubble should appear bottom-right

### Test 3: Cross-Origin Requests
Make sure Railway environment has:
```
CORS_ORIGINS=https://hawaii.lenilani.com,https://www.hawaii.lenilani.com
```

---

## 🔧 Troubleshooting

### "Site can't be reached"
- Check DNS propagation: https://dnschecker.org
- Verify CNAME record is correct
- Wait 30 minutes for DNS

### "CORS error" in console
- Add your domain to CORS_ORIGINS in Railway
- Include both www and non-www versions

### "Widget not showing"
- Check browser console for errors
- Verify script tag is before </body>
- Clear browser cache

### "Mixed content" warning
- Ensure both sites use HTTPS
- Update widget URL to use https://

---

## 📱 Mobile Optimization

The widget automatically:
- Detects mobile devices
- Switches to full-screen mode
- Provides touch-friendly interface

---

## 🎨 Customization

### Change Widget Position
```javascript
window.LeniLaniConfig = {
  position: 'bottom-left' // or 'bottom-right'
};
```

### Custom Colors
```javascript
window.LeniLaniConfig = {
  primaryColor: '#F4A261',     // Sunset orange
  backgroundColor: '#264653',  // Ocean blue
  textColor: '#FFFFFF'        // White text
};
```

### Custom Welcome Message
```javascript
window.LeniLaniConfig = {
  greeting: 'Aloha! Need help growing your Hawaiian business?',
  placeholder: 'Type your message here...'
};
```

---

## 🚀 Quick Implementation Checklist

- [ ] Deploy to Railway
- [ ] Get Railway URL
- [ ] Add CNAME record for chatbot.hawaii
- [ ] Wait for DNS propagation
- [ ] Update CORS_ORIGINS in Railway
- [ ] Add widget code to hawaii.lenilani.com
- [ ] Test on desktop and mobile
- [ ] Verify lead capture works

---

## 📞 Need Help?

**For technical support:**
- Email: reno@lenilani.com
- Phone: 808-766-1164

**For DNS help:**
- Check your domain registrar's support
- Railway Discord: discord.gg/railway