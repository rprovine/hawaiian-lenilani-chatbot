# Hawaiian LeniLani Chatbot Deployment Guide

## 📋 Prerequisites

- GitHub account with the repository
- Node.js 18+ and Python 3.9+ installed
- Claude API key from Anthropic
- Domain name (optional but recommended)

## 🚀 Deployment Options Overview

1. **Vercel + Railway** - Best for production (automatic deployments)
2. **Railway Only** - Simplest all-in-one solution
3. **VPS (DigitalOcean/AWS)** - Most control and customization
4. **Render** - Good free tier option

## 🚀 Deploying to Production

## 🎯 Step-by-Step Deployment from GitHub

### Step 1: Prepare Your GitHub Repository

1. **Fork or Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/hawaiian-lenilani-chatbot.git
   cd hawaiian-lenilani-chatbot
   ```

2. **Create Environment File**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Push to Your GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

### Option 1: Vercel (Frontend) + Railway (Backend)

#### Deploy Frontend to Vercel

1. **Connect GitHub to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select the `hawaiian-lenilani-chatbot` repo

2. **Configure Build Settings**
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   ```

3. **Add Environment Variable**
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   ```
   (You'll update this after deploying backend)

4. **Deploy**
   - Click "Deploy"
   - Note your deployment URL (e.g., `https://your-app.vercel.app`)

#### Deploy Backend to Railway

1. **Connect GitHub to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Service**
   - Railway will auto-detect Python
   - Add these environment variables:
   ```
   ANTHROPIC_API_KEY=your-claude-api-key
   LEAD_WEBHOOK_URL=your-webhook-url
   CORS_ORIGINS=https://your-app.vercel.app
   PORT=8000
   ```

3. **Deploy**
   - Click "Deploy"
   - Generate a domain (e.g., `https://your-backend.railway.app`)

4. **Update Vercel Frontend**
   - Go back to Vercel dashboard
   - Update `REACT_APP_API_URL` with your Railway backend URL
   - Redeploy

### Option 2: Deploy to Railway (All-in-One)

1. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub

2. **Add Two Services**
   
   **Backend Service:**
   - Click "+ New" → "GitHub Repo"
   - Select your repo
   - Add start command: `python run_backend.py`
   - Add all backend environment variables

   **Frontend Service:**
   - Click "+ New" → "GitHub Repo" again
   - Select same repo
   - Set root directory: `frontend`
   - Add build command: `npm run build`
   - Add start command: `serve -s build -l $PORT`
   - Add env var: `REACT_APP_API_URL=https://backend-service.railway.internal`

3. **Generate Domains**
   - Click on each service → Settings → Generate Domain
   - Update CORS_ORIGINS with frontend domain

### Option 3: Deploy to Render (Free Tier)

1. **Deploy Backend**
   - Go to [render.com](https://render.com)
   - New → Web Service → Connect GitHub
   - Configure:
     ```
     Name: lenilani-chatbot-api
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: python run_backend.py
     ```
   - Add environment variables
   - Deploy (note the URL)

2. **Deploy Frontend**
   - New → Static Site → Connect GitHub
   - Configure:
     ```
     Name: lenilani-chatbot
     Root Directory: frontend
     Build Command: npm run build
     Publish Directory: frontend/build
     ```
   - Add env var: `REACT_APP_API_URL=your-backend-url`
   - Deploy

### Option 4: Deploy Everything to a VPS (DigitalOcean, AWS, etc.)

1. **Set up your server**:
   ```bash
   ssh root@your-server-ip
   
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install Docker Compose
   curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose
   ```

2. **Clone and configure**:
   ```bash
   git clone https://github.com/your-repo/hawaiian-lenilani-chatbot.git
   cd hawaiian-lenilani-chatbot
   
   # Copy and update .env
   cp .env.example .env
   nano .env  # Add your API keys
   ```

3. **Run with Docker Compose**:
   ```bash
   cd deployment
   docker-compose -f docker-compose.hawaiian.yml up -d
   ```

## 🌐 Widget Installation on hawaii.lenilani.com

### Method 1: Simple Script Tag (Easiest)

Add this to your website's HTML, just before the closing `</body>` tag:

```html
<!-- Hawaiian LeniLani AI Chatbot -->
<script>
  (function() {
    var script = document.createElement('script');
    script.src = 'https://chat.lenilani.com/widget.js';
    script.async = true;
    document.body.appendChild(script);
  })();
</script>
```

### Method 2: Custom Configuration

```html
<!-- Hawaiian LeniLani AI Chatbot with Configuration -->
<script>
  window.LeniLaniConfig = {
    position: 'bottom-right', // or 'bottom-left'
    primaryColor: '#F4A261',  // Hawaiian sunset orange
    greeting: 'Aloha! Need help with your business?',
    owner: {
      name: 'Reno Provine',
      email: 'reno@lenilani.com',
      phone: '808-766-1164'
    }
  };
</script>
<script src="https://chat.lenilani.com/widget.js" async></script>
```

### Method 3: WordPress Plugin

If hawaii.lenilani.com uses WordPress:

1. Add to `functions.php`:
```php
function add_lenilani_chatbot() {
    if (!is_admin()) {
        wp_enqueue_script(
            'lenilani-chatbot', 
            'https://chat.lenilani.com/widget.js', 
            array(), 
            '1.0.0', 
            true
        );
    }
}
add_action('wp_enqueue_scripts', 'add_lenilani_chatbot');
```

2. Or use a plugin like "Header Footer Code Manager" to add the script.

## 🔧 Production Configuration

### 1. Update CORS in Backend

Edit `/api_backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hawaii.lenilani.com",
        "https://lenilani.com",
        "https://chat.lenilani.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Environment Variables for Production

Create `.env.production`:
```env
# API URLs
REACT_APP_API_URL=https://api.lenilani.com
REACT_APP_WEBSOCKET_URL=wss://api.lenilani.com

# Claude API
ANTHROPIC_API_KEY=your_production_key

# Database (use managed database)
DATABASE_URL=postgresql://user:pass@db.lenilani.com:5432/hawaiian_lenilani

# Security
SECRET_KEY=generate-a-secure-random-key
ALLOWED_HOSTS=api.lenilani.com,chat.lenilani.com

# HubSpot
HUBSPOT_API_KEY=your_hubspot_key
```

### 3. SSL Configuration

For `chat.lenilani.com`, you'll need SSL. If using Nginx:

```nginx
server {
    listen 80;
    server_name chat.lenilani.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name chat.lenilani.com;
    
    ssl_certificate /etc/letsencrypt/live/chat.lenilani.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chat.lenilani.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
```

## 🎯 Quick Deployment Checklist

- [ ] Set up subdomain: `chat.lenilani.com`
- [ ] Configure DNS to point to your server
- [ ] Install SSL certificate (Let's Encrypt)
- [ ] Update environment variables
- [ ] Configure CORS for hawaii.lenilani.com
- [ ] Deploy backend and frontend
- [ ] Test widget on staging site
- [ ] Add widget script to hawaii.lenilani.com
- [ ] Monitor logs and performance

## 📱 Mobile Optimization

The widget automatically adapts for mobile devices:
- Full screen on mobile
- Touch-friendly interface
- Responsive design
- Fast loading

## 🔒 Security Considerations

1. **API Rate Limiting**: Implement rate limiting to prevent abuse
2. **Input Validation**: All user inputs are sanitized
3. **HTTPS Only**: Ensure all communications are encrypted
4. **CORS**: Only allow your domains
5. **Environment Variables**: Never commit sensitive keys

## 📊 Analytics Integration

Add Google Analytics to track widget usage:

```javascript
// In widget-embed.js
gtag('event', 'chatbot_opened', {
  'event_category': 'engagement',
  'event_label': 'Hawaiian LeniLani Chatbot'
});
```

## 🆘 Troubleshooting

1. **Widget not appearing**: Check browser console for errors
2. **CORS errors**: Verify allowed origins in backend
3. **Connection issues**: Check API URL configuration
4. **SSL warnings**: Ensure valid certificates

## 📞 Support

For deployment assistance:
- Email: reno@lenilani.com
- Phone: 808-766-1164