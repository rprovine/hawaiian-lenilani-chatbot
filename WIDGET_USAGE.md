# Using the Hawaiian LeniLani Chatbot Widget

## Quick Start (Local Development)

1. **Start the backend server:**
   ```bash
   python run_backend.py
   ```

2. **Open the demo page:**
   - Open `widget-standalone.html` in your browser
   - Or visit any local HTML file and add the widget code

## Adding the Widget to Any Website

### Option 1: Local Development
```html
<script>
  window.LENILANI_CHATBOT_URL = 'http://localhost:8000';
</script>
<script src="http://localhost:8000/widget.js"></script>
```

### Option 2: Production (after deployment)
```html
<script>
  window.LENILANI_CHATBOT_URL = 'https://your-api-url.com';
</script>
<script src="https://your-api-url.com/widget.js"></script>
```

## How It Works

1. The widget creates a chat bubble in the bottom-right corner
2. Clicking the bubble opens the chat window
3. Users can chat with Leni Begonia directly
4. All conversations are handled by your backend API
5. Lead capture happens automatically when qualified

## Customization

You can customize the widget by modifying `public/widget.js`:
- Colors and styling
- Position and size
- Messages and text
- Animation effects

## Testing

1. Start your backend: `python run_backend.py`
2. Open `widget-standalone.html` in your browser
3. Click the chat bubble to start chatting

## Adding to hawaii.lenilani.com

Once you have a deployed backend URL, add this before the closing `</body>` tag:

```html
<script>
  window.LENILANI_CHATBOT_URL = 'https://chatbot.hawaii.lenilani.com';
</script>
<script src="https://chatbot.hawaii.lenilani.com/widget.js"></script>
```

No frontend deployment needed - the widget loads directly from your API!