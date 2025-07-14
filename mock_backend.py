#!/usr/bin/env python3
"""Mock backend for testing without valid API key"""
import os
import sys
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create a simple mock app
app = FastAPI(title="Mock Hawaiian LeniLani Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    hawaii_tz = pytz.timezone('Pacific/Honolulu')
    current_time = datetime.now(hawaii_tz)
    return {
        "status": "healthy",
        "message": "Mock API is running! 🌺",
        "hawaii_time": current_time.strftime("%Y-%m-%d %I:%M %p HST"),
        "greeting": "Aloha!"
    }

@app.post("/chat")
async def chat(data: dict):
    """Mock chat endpoint with Hawaiian responses"""
    message = data.get("message", "").lower()
    
    # Mock responses based on keywords
    if "hello" in message or "aloha" in message or "hi" in message:
        response = "Aloha! 🌺 Welcome to LeniLani Consulting! I'm your AI assistant for Hawaiian businesses. How can I help you today? We offer services like tourism analytics, restaurant AI solutions, and technology consulting specifically for island businesses."
    elif "service" in message or "help" in message or "what do you do" in message:
        response = "Shoots! We help Hawaiian businesses with:\n\n🌴 Tourism Analytics - Understand visitor patterns\n🍽️ Restaurant AI - Optimize for locals and tourists\n🏝️ Island Tech Solutions - Inter-island commerce\n💻 Fractional CTO Services - Tech leadership\n\nWhat kind of business you stay running?"
    elif "price" in message or "cost" in message or "how much" in message:
        response = "Eh, we get different packages for different businesses, yeah? Most start around $500/month for basic analytics. But no worries, we can talk story first, see what you really need. Want to schedule one free consultation with Reno? Can call 808-766-1164 or email reno@lenilani.com."
    elif "restaurant" in message:
        response = "Oh, you get one restaurant? Nice! We help plenty restaurants on all da islands. Can help with:\n- Menu optimization for tourist vs local taste\n- Inventory management with island supply chains\n- Multi-language ordering systems\n- Seasonal demand forecasting\n\nWhat island your restaurant stay on?"
    else:
        response = "Mahalo for your message! I stay here for help Hawaiian businesses with AI and technology. Can you tell me more about your business and what kind help you looking for? Or if you like talk to someone directly, can contact Reno at 808-766-1164."
    
    return {
        "response": response,
        "metadata": {
            "timestamp": datetime.now(pytz.timezone('Pacific/Honolulu')).isoformat(),
            "mock": True
        },
        "suggestions": [
            "Tell me about your services",
            "I have a restaurant on Maui",
            "What's the pricing?",
            "Schedule consultation"
        ]
    }

@app.get("/services")
async def services():
    return {
        "services": {
            "tourism_analytics": {
                "name": "Tourism Analytics & Forecasting",
                "description": "Understand visitor patterns and optimize for seasonal demand"
            },
            "restaurant_ai": {
                "name": "Restaurant AI Solutions",
                "description": "Smart systems for island restaurants"
            },
            "fractional_cto": {
                "name": "Fractional CTO Services",
                "description": "Tech leadership for growing businesses"
            }
        },
        "islands_served": ["Oahu", "Maui", "Big Island", "Kauai", "Molokai", "Lanai"]
    }

if __name__ == "__main__":
    print("🌺 Starting MOCK Hawaiian LeniLani Chatbot API...")
    print("⚠️  This is a mock server for testing without API key")
    print("🌴 API will be available at: http://localhost:8000")
    print("🤙 Press Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)