# Setting Up hawaii.lenilani.com

## Overview
You have two main options for setting up hawaii.lenilani.com:

1. **Option A**: Point directly to your Render backend (Simplest)
2. **Option B**: Create a dedicated landing page (More flexible)

---

## Option A: Direct Backend Pointing (Simplest - 5 minutes)

### Step 1: Add Custom Domain to Render
1. Go to your Render dashboard
2. Navigate to your service: `hawaiian-lenilani-chatbot`
3. Click on "Settings" → "Custom Domains"
4. Add: `hawaii.lenilani.com`
5. Render will provide DNS instructions

### Step 2: Configure DNS
Add these records in your domain registrar:

```
Type: CNAME
Name: hawaii
Value: hawaiian-lenilani-chatbot.onrender.com
TTL: 300
```

### Step 3: Update CORS
In Render environment variables, add:
```
CORS_ORIGINS=https://hawaii.lenilani.com,https://lenilani.com
```

### Step 4: Create Landing Page
Add this to your backend at `api_backend/main.py`:

```python
@app.get("/", response_class=HTMLResponse)
async def serve_landing():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hawaiian AI Business Assistant</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                font-family: -apple-system, sans-serif;
                background: linear-gradient(135deg, #0081a7 0%, #00afb9 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 20px;
            }
            .container {
                max-width: 600px;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 30px;
                opacity: 0.9;
            }
            .cta {
                background: white;
                color: #0081a7;
                padding: 15px 30px;
                border-radius: 30px;
                text-decoration: none;
                display: inline-block;
                font-weight: bold;
                transition: transform 0.3s;
            }
            .cta:hover {
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌺 Aloha!</h1>
            <h2>Hawaiian AI Business Assistant</h2>
            <p>Empowering Hawaiian businesses with AI technology while preserving the spirit of aloha.</p>
            <a href="https://lenilani.com" class="cta">Visit LeniLani Consulting</a>
            <p style="margin-top: 40px; font-size: 0.9em;">
                Try our chatbot - look for the 🌺 in the bottom right!
            </p>
        </div>
        
        <!-- Chatbot Widget -->
        <script>
            window.LENILANI_CHATBOT_URL = window.location.origin;
        </script>
        <script src="/widget.js"></script>
    </body>
    </html>
    """
```

---

## Option B: Dedicated Landing Page (More Control)

### Step 1: Create a GitHub Pages Site
1. Create new repository: `hawaii-lenilani-landing`
2. Enable GitHub Pages in repository settings
3. Add custom domain: `hawaii.lenilani.com`

### Step 2: Create Landing Page
Create `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hawaiian AI Business Assistant - LeniLani Consulting</title>
    <meta name="description" content="AI-powered business consulting for Hawaiian companies. Combining cutting-edge technology with the spirit of aloha.">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #0081a7 0%, #00afb9 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        
        .hero-content {
            max-width: 800px;
        }
        
        .hero h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            font-weight: 700;
        }
        
        .hero .tagline {
            font-size: 1.5em;
            margin-bottom: 30px;
            opacity: 0.95;
        }
        
        .hero .description {
            font-size: 1.1em;
            margin-bottom: 40px;
            opacity: 0.9;
        }
        
        .cta-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .cta {
            display: inline-block;
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .cta-primary {
            background: white;
            color: #0081a7;
        }
        
        .cta-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .cta-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        
        .cta-secondary:hover {
            background: white;
            color: #0081a7;
        }
        
        /* Features Section */
        .features {
            padding: 80px 20px;
            background: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .features h2 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 50px;
            color: #0081a7;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }
        
        .feature {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .feature-icon {
            font-size: 3em;
            margin-bottom: 20px;
        }
        
        .feature h3 {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #0081a7;
        }
        
        .chat-prompt {
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 15px 25px;
            border-radius: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5em;
            }
            .hero .tagline {
                font-size: 1.2em;
            }
            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>🌺 Hawaiian AI Business Assistant</h1>
            <p class="tagline">Where Technology Meets Aloha Spirit</p>
            <p class="description">
                Empowering Hawaiian businesses with cutting-edge AI technology 
                while preserving our island values and culture.
            </p>
            <div class="cta-buttons">
                <a href="https://lenilani.com" class="cta cta-primary">Visit LeniLani Consulting</a>
                <a href="#features" class="cta cta-secondary">Learn More</a>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features" id="features">
        <div class="container">
            <h2>How We Help Hawaiian Businesses</h2>
            <div class="feature-grid">
                <div class="feature">
                    <div class="feature-icon">🤖</div>
                    <h3>AI Integration</h3>
                    <p>Seamlessly integrate AI tools into your business operations while maintaining the personal touch that makes Hawaii special.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <h3>Data Analytics</h3>
                    <p>Understand your customers better with insights tailored to Hawaii's unique market dynamics and seasonal patterns.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🌴</div>
                    <h3>Local Expertise</h3>
                    <p>We understand island business challenges - from shipping logistics to tourist seasons to supporting our local community.</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Chat Prompt -->
    <div class="chat-prompt">
        👋 Click the flower to chat! →
    </div>
    
    <!-- Chatbot Widget -->
    <script>
        window.LENILANI_CHATBOT_URL = 'https://hawaiian-lenilani-chatbot.onrender.com';
    </script>
    <script src="https://hawaiian-lenilani-chatbot.onrender.com/widget.js"></script>
</body>
</html>
```

### Step 3: Configure DNS
Add CNAME record:
```
Type: CNAME
Name: hawaii
Value: [your-github-username].github.io
TTL: 300
```

---

## Quick Decision Guide

### Use Option A (Direct Backend) if:
- You want the simplest setup (5 minutes)
- You don't need a complex landing page
- You're okay with a basic page

### Use Option B (GitHub Pages) if:
- You want a rich landing page
- You need more design control
- You want to A/B test different designs
- You want separate hosting for the page

---

## Testing Your Setup

1. **DNS Propagation**: Use https://dnschecker.org to verify DNS
2. **SSL Certificate**: Render/GitHub Pages provides free SSL
3. **Widget Loading**: Check browser console for errors
4. **Mobile Testing**: Ensure responsive on all devices

## Next Steps

After setup:
1. Test the chatbot thoroughly
2. Add analytics (Google Analytics, etc.)
3. Set up monitoring
4. Create marketing materials pointing to hawaii.lenilani.com

---

Need help? Contact support@render.com or create an issue on GitHub!