# Hawaiian LeniLani Chatbot - Widget Integration Guide

## Quick Start (2 minutes)

To add the Hawaiian AI Chatbot to your website, add these two lines of code just before the closing `</body>` tag:

```html
<script>
    window.LENILANI_CHATBOT_URL = 'https://hawaiian-lenilani-chatbot.onrender.com';
</script>
<script src="https://cdn.jsdelivr.net/gh/rprovine/hawaiian-lenilani-chatbot@main/public/hawaiian-widget.js"></script>
```

That's it! The chatbot will appear as a flower icon (🌺) in the bottom right corner of your website.

## Integration Options

### Option 1: CDN Integration (Recommended)
Use the JSDelivr CDN for automatic updates and fast loading:

```html
<script>
    window.LENILANI_CHATBOT_URL = 'https://YOUR-BACKEND-URL.onrender.com';
</script>
<script src="https://cdn.jsdelivr.net/gh/rprovine/hawaiian-lenilani-chatbot@main/public/hawaiian-widget.js"></script>
```

### Option 2: Self-Hosted
Download the widget file and host it on your server:

1. Download: [hawaiian-widget.js](https://raw.githubusercontent.com/rprovine/hawaiian-lenilani-chatbot/main/public/hawaiian-widget.js)
2. Upload to your website
3. Add to your HTML:

```html
<script>
    window.LENILANI_CHATBOT_URL = 'https://YOUR-BACKEND-URL.onrender.com';
</script>
<script src="/path/to/hawaiian-widget.js"></script>
```

### Option 3: WordPress Integration
Add to your theme's footer.php or use a plugin like "Insert Headers and Footers":

```html
<script>
    window.LENILANI_CHATBOT_URL = 'https://YOUR-BACKEND-URL.onrender.com';
</script>
<script src="https://cdn.jsdelivr.net/gh/rprovine/hawaiian-lenilani-chatbot@main/public/hawaiian-widget.js"></script>
```

## Features

- **🌺 Hawaiian-themed design** with ocean colors and aloha spirit
- **💬 Natural conversation** powered by Claude AI
- **📱 Mobile responsive** - works on all devices
- **🚀 Fast loading** - doesn't slow down your website
- **🎨 Automatic styling** - looks great on any website

## Customization

### Change Backend URL
Replace the URL with your own deployed backend:

```javascript
window.LENILANI_CHATBOT_URL = 'https://your-custom-backend.com';
```

### Position Adjustment
The widget appears in the bottom right by default. To change position, add CSS:

```css
.lenilani-chat-widget {
    bottom: 20px !important;
    right: 20px !important;
    /* Or for bottom left: */
    /* left: 20px !important; */
    /* right: auto !important; */
}
```

## Testing

1. Open your website with the widget code added
2. Look for the 🌺 flower icon in the bottom right
3. Click to open the chat
4. Type "Aloha" to start a conversation

## Troubleshooting

### Widget doesn't appear
- Check browser console for errors (F12)
- Verify the backend URL is correct
- Ensure scripts are placed before `</body>`

### Chat not responding
- Verify backend is running: `https://YOUR-BACKEND-URL/health`
- Check if ANTHROPIC_API_KEY is set in Render environment

### CORS errors
- Backend should allow all origins by default
- Contact support if issues persist

## Support

- **Email**: reno@lenilani.com
- **Phone**: (808) 766-1164
- **GitHub**: [Report issues](https://github.com/rprovine/hawaiian-lenilani-chatbot/issues)

## Examples

- [Basic Integration](production-widget-example.html)
- [Test Page](simple-widget-test.html)
- [Debug Page](debug-widget-test.html)

---

Made with 🌺 Aloha in Hawaii