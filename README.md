# Hawaiian LeniLani AI Consulting Chatbot

## 🌺 Aloha! Welcome to the Hawaiian AI Consulting Chatbot

This is a production-ready AI chatbot specifically designed for hawaii.lenilani.com that serves Hawaiian businesses with authentic cultural integration. This chatbot combines cutting-edge AI technology with genuine understanding of Hawaiian business culture, values, and practices.

### 🎯 Mission
To establish LeniLani as the premier AI consultant for Hawaiian businesses by demonstrating both technical excellence and authentic cultural understanding - helping local businesses thrive while respecting island culture and values.

## 🏝️ Key Features

- **Authentic Hawaiian Communication**: Natural use of Hawaiian Pidgin English and cultural greetings
- **Island Business Intelligence**: Understanding of inter-island commerce, tourism patterns, and local challenges
- **Cultural Values Integration**: Embodies aloha, ohana, malama 'aina, and lokahi in all interactions
- **Hybrid AI System**: Rasa for structured workflows + Claude API for cultural conversations
- **Hawaiian Business Services**: Tailored solutions for tourism, agriculture, retail, and restaurants

## 🛠️ Technology Stack

- **AI Engines**: Rasa 3.x + Anthropic Claude API
- **Backend**: FastAPI with Hawaiian business logic
- **Frontend**: React.js with Hawaiian-themed design
- **Databases**: PostgreSQL + Redis
- **Integrations**: HubSpot CRM, Google Calendar (Hawaii timezone)
- **Deployment**: Docker + Production-ready configuration

## 🚀 Quick Start

### 🌟 Deploy in 10 Minutes!

See our deployment guides:
- **[RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)** - Easiest option, deploy in 10 minutes
- **[GITHUB_DEPLOYMENT.md](./GITHUB_DEPLOYMENT.md)** - Complete GitHub to production guide
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - All deployment options detailed

### Prerequisites
- Python 3.9+
- Node.js 18+
- Claude API key from Anthropic

### Local Development

```bash
# Clone the repository
git clone https://github.com/lenilani/hawaiian-chatbot.git
cd hawaiian-lenilani-chatbot

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Running the Application

```bash
# Start all services with Docker Compose
docker-compose -f deployment/docker-compose.hawaiian.yml up

# Or run services individually:

# 1. Start Rasa
cd rasa_bot
rasa run --enable-api --cors "*"

# 2. Start Rasa actions server
rasa run actions

# 3. Start FastAPI backend
cd ../api_backend
uvicorn main:app --reload --port 8000

# 4. Start frontend
cd ../frontend
npm start
```

## 🌴 Hawaiian Business Services

1. **Tourism Analytics** - Seasonal patterns, Japanese vs mainland visitors
2. **Restaurant AI** - Local vs tourist optimization, multi-language ordering
3. **Agricultural Tech** - IoT for coffee farms, sustainable farming
4. **Local Retail AI** - Compete with mainland chains using local advantages
5. **Fractional CTO** - Tech leadership understanding island constraints

## 🤝 Cultural Guidelines

This chatbot embodies Hawaiian values:
- **Aloha**: Love, respect, and genuine care in all interactions
- **Ohana**: Family-oriented business relationships
- **Malama 'Aina**: Environmental responsibility
- **Lokahi**: Unity and collaboration
- **Talk Story**: Building relationships before business

## 📚 Documentation

- [Hawaiian Setup Guide](docs/HAWAIIAN_SETUP.md)
- [Cultural Guidelines](docs/CULTURAL_GUIDELINES.md)
- [Island Business Guide](docs/ISLAND_BUSINESS_GUIDE.md)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run Hawaiian conversation tests
pytest tests/test_hawaiian_conversations.py

# Run cultural integration tests
pytest tests/test_cultural_integration.py
```

## 🌊 Deployment

Production deployment to hawaii.lenilani.com:

```bash
# Build and deploy
./deploy.sh production
```

## 🌺 Contributing

We welcome contributions that enhance our service to Hawaiian businesses! Please ensure all contributions:
- Respect Hawaiian culture and values
- Use authentic language (not stereotypical)
- Consider island-specific business needs
- Follow our coding standards

## 📞 Contact

LeniLani Consulting - AI Solutions for Hawaiian Businesses
- Website: [hawaii.lenilani.com](https://hawaii.lenilani.com)
- Email: aloha@lenilani.com

---

*E komo mai (Welcome) to the future of Hawaiian business AI - where technology meets aloha!* 🌺