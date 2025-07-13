# Hawaiian LeniLani Chatbot Setup Guide

## 🌺 Aloha! Welcome to the Hawaiian AI Consulting Chatbot

This guide will help you set up and configure the Hawaiian LeniLani Chatbot, an AI-powered consulting assistant that understands and respects Hawaiian culture, language, and business practices.

## 📋 Prerequisites

Before starting, ensure you have:

1. **System Requirements**
   - Python 3.9 or higher
   - Node.js 18+ and npm
   - Docker and Docker Compose
   - At least 8GB RAM (16GB recommended)
   - 20GB free disk space

2. **API Keys**
   - Anthropic Claude API key
   - HubSpot API key (optional)
   - Google Calendar API credentials (optional)
   - AWS credentials for S3 backups (optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lenilani/hawaiian-chatbot.git
cd hawaiian-chatbot
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp deployment/.env.production .env

# Edit with your API keys
nano .env
```

Required environment variables:
```env
ANTHROPIC_API_KEY=your-claude-api-key
POSTGRES_PASSWORD=secure-password
REDIS_PASSWORD=secure-password
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

### 4. Initialize Rasa

```bash
# Navigate to Rasa directory
cd rasa_bot

# Train the Hawaiian model
rasa train

# Test the model (optional)
rasa shell
```

### 5. Set Up the Database

```bash
# Start PostgreSQL and Redis
docker-compose -f deployment/docker-compose.hawaiian.yml up -d postgres redis

# Wait for services to start
sleep 10

# Initialize database
docker-compose -f deployment/docker-compose.hawaiian.yml exec postgres psql -U lenilani -d hawaiian_lenilani < deployment/init-db.sql
```

### 6. Start Backend Services

```bash
# Start FastAPI backend
cd api_backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Rasa action server
cd rasa_bot
rasa run actions
```

### 7. Build and Start Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🐳 Docker Deployment (Recommended)

For production deployment, use Docker:

```bash
cd deployment
./deploy.sh deploy
```

This will:
- Build all Docker images
- Start all services
- Initialize the database
- Train the Rasa model
- Set up SSL certificates (if configured)

## 🔧 Configuration Details

### Hawaiian Cultural Settings

The chatbot is pre-configured with Hawaiian cultural elements:

1. **Time Zone**: Pacific/Honolulu (HST)
2. **Language**: Hawaiian Pidgin English and standard English
3. **Greetings**: Time-aware Hawaiian greetings
4. **Islands**: Support for all major Hawaiian islands
5. **Business Types**: Tourism, restaurant, agriculture, retail, etc.

### Customizing Cultural Responses

Edit `claude_integration/cultural_prompts.py` to modify:
- Hawaiian values (aloha, ohana, malama aina)
- Pidgin expressions
- Island-specific knowledge
- Business recommendations

### Training Data

Enhance the chatbot's understanding by editing:
- `rasa_bot/data/hawaiian_nlu.yml` - Intent examples
- `rasa_bot/data/hawaiian_stories.yml` - Conversation flows
- `rasa_bot/data/hawaiian_rules.yml` - Business rules

After making changes:
```bash
cd rasa_bot
rasa train
```

## 🧪 Testing

### Test Rasa Components

```bash
# Test NLU
cd rasa_bot
rasa test nlu

# Interactive testing
rasa interactive
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Aloha! I need help with my restaurant", "session_id": "test123"}'
```

### Test Frontend Widget

1. Open http://localhost:3000 in your browser
2. Click the chat widget in the bottom right
3. Try these test phrases:
   - "Aloha"
   - "I have a tourism business on Maui"
   - "Need help with online marketing"
   - "Can schedule one meeting?"

## 🏝️ Island-Specific Configuration

### Supported Islands

The chatbot recognizes and provides specific advice for:
- Oahu - Urban business focus
- Maui - Tourism and hospitality
- Big Island (Hawaii) - Agriculture and astronomy
- Kauai - Eco-tourism and sustainability
- Molokai - Community and tradition
- Lanai - Luxury and exclusivity

### Adding Island-Specific Content

1. Update `rasa_bot/data/hawaiian_nlu.yml` with island examples
2. Add island logic in `actions/hawaiian_business_actions.py`
3. Configure island-specific prompts in `claude_integration/`

## 🔌 Integration Setup

### HubSpot CRM

1. Get your HubSpot API key from: https://app.hubspot.com/settings/
2. Add to `.env`:
   ```env
   HUBSPOT_API_KEY=your-key
   HUBSPOT_PORTAL_ID=your-portal-id
   ```
3. Configure pipeline and owner IDs

### Google Calendar

1. Create OAuth credentials at: https://console.cloud.google.com/
2. Enable Calendar API
3. Add to `.env`:
   ```env
   GOOGLE_CALENDAR_CLIENT_ID=your-client-id
   GOOGLE_CALENDAR_CLIENT_SECRET=your-secret
   ```
4. Run OAuth flow to get refresh token

## 📊 Monitoring

### View Logs

```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f rasa

# Backend logs
tail -f api_backend/logs/app.log
```

### Database Analytics

```bash
# Connect to database
docker exec -it hawaiian_postgres psql -U lenilani -d hawaiian_lenilani

# View daily conversations
SELECT * FROM analytics.daily_conversations ORDER BY date DESC;

# Check island metrics
SELECT * FROM analytics.island_metrics;
```

## 🆘 Troubleshooting

### Common Issues

1. **"Cannot connect to Claude API"**
   - Verify your ANTHROPIC_API_KEY is correct
   - Check internet connectivity
   - Ensure API key has sufficient credits

2. **"Rasa model not found"**
   - Run `rasa train` in the rasa_bot directory
   - Check models directory exists: `ls rasa_bot/models/`

3. **"Database connection failed"**
   - Ensure PostgreSQL is running: `docker ps`
   - Check credentials in .env match docker-compose.yml
   - Verify database initialization completed

4. **"Frontend widget not appearing"**
   - Check browser console for errors
   - Ensure backend is running on correct port
   - Verify CORS settings in backend

### Getting Help

- Documentation: See `docs/` directory
- Issues: https://github.com/lenilani/hawaiian-chatbot/issues
- Community: Join our Slack channel

## 🌴 Next Steps

1. **Customize for Your Business**
   - Add your company information
   - Configure service offerings
   - Set up team calendars

2. **Enhance Cultural Content**
   - Add more pidgin expressions
   - Include local business knowledge
   - Add seasonal greetings

3. **Deploy to Production**
   - Set up SSL certificates
   - Configure domain name
   - Enable backups

## 🤙 Mahalo!

Thank you for setting up the Hawaiian LeniLani Chatbot. We hope it brings the spirit of Aloha to your AI consulting services!

For questions or kokua (help), reach out to: support@lenilani.com

*E komo mai! Welcome to the future of Hawaiian business consulting!*