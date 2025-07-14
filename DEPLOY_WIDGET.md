# Deploy Hawaiian LeniLani Chatbot Widget

## Complete Widget Features
- 🌺 Full Hawaiian theme with ocean gradient colors
- 🏝️ Leni Begonia branding with logo
- 📱 Responsive design for mobile and desktop
- 💬 Welcome screen with quick action menu
- 🎨 Beautiful animations and transitions
- ⚡ Auto-capture leads when qualified
- 🔔 Notification dot for first-time visitors

## Quick Deployment (No Backend Deployment Needed!)

### Option 1: Using Your Local Backend
1. Start your backend locally:
   ```bash
   python run_backend.py
   ```

2. Add to any website:
   ```html
   <!-- Add before closing </body> tag -->
   <script>
     window.LENILANI_CHATBOT_URL = 'http://localhost:8000';
   </script>
   <script src="http://localhost:8000/widget.js"></script>
   ```

### Option 2: Using ngrok (Recommended for Testing)
1. Install ngrok:
   ```bash
   brew install ngrok  # macOS
   ```

2. Start your backend:
   ```bash
   python run_backend.py
   ```

3. Create public tunnel:
   ```bash
   ngrok http 8000
   ```

4. Use the ngrok URL in your website:
   ```html
   <script>
     window.LENILANI_CHATBOT_URL = 'https://YOUR-ID.ngrok.io';
   </script>
   <script src="https://YOUR-ID.ngrok.io/widget.js"></script>
   ```

### Option 3: Deploy Backend Once, Use Anywhere

#### Simple Deployment with Render.com (Free)
1. Push to GitHub
2. Go to https://render.com
3. New > Web Service > Connect GitHub repo
4. Settings:
   - Name: `hawaiian-chatbot-api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_backend.py`
5. Add Environment Variables:
   - `ANTHROPIC_API_KEY`: (your key)
   - `LEAD_WEBHOOK_URL`: (your webhook)

#### Add to hawaii.lenilani.com
Once deployed, add this code to your website:
```html
<!-- Add before closing </body> tag -->
<script>
  window.LENILANI_CHATBOT_URL = 'https://hawaiian-chatbot-api.onrender.com';
</script>
<script src="https://hawaiian-chatbot-api.onrender.com/widget.js"></script>
```

## Testing the Widget

Open `test-widget.html` in your browser or create a test page:

```html
<!DOCTYPE html>
<html>
<head>
    <title>LeniLani Chatbot Test</title>
</head>
<body>
    <h1>Your Website Content Here</h1>
    
    <!-- Hawaiian Chatbot Widget -->
    <script>
      window.LENILANI_CHATBOT_URL = 'http://localhost:8000';
    </script>
    <script src="http://localhost:8000/widget.js"></script>
</body>
</html>
```

## Widget Features

1. **Chat Bubble**: Ocean gradient button in bottom-right corner
2. **Welcome Screen**: 
   - Leni Begonia introduction
   - Quick action buttons (Services, Consultation, Pricing, Chat)
3. **Chat Interface**:
   - Real-time messaging with Leni Begonia
   - Hawaiian-themed design
   - Quick reply suggestions
   - Typing indicators
4. **Lead Capture**: Automatically captures qualified leads via webhook

## Customization

To customize colors or styling, edit `public/hawaiian-widget.js`:
- `hawaiianColors` object for color scheme
- `styles` string for CSS customization
- `chatHTML` for layout changes

## No Frontend Deployment Needed!

The widget is completely self-contained. Just deploy your backend API once, and the widget can be added to any website with just 2 lines of code!