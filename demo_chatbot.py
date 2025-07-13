#!/usr/bin/env python3
"""
Hawaiian LeniLani Chatbot Demo - Direct Claude Integration
This demo bypasses Rasa for more natural, conversational responses
"""

import os
import sys
import asyncio
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from claude_integration.hawaiian_claude_client import HawaiianClaudeClient
from api_backend.services.cultural_tone_manager import CulturalToneManager


class HawaiianChatbotDemo:
    """Demo chatbot with direct Claude integration for natural conversations"""
    
    def __init__(self):
        # Check for API key
        if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_anthropic_api_key_here":
            print("\n⚠️  Please set your ANTHROPIC_API_KEY in the .env file")
            print("   Edit .env and replace 'your_anthropic_api_key_here' with your actual key")
            sys.exit(1)
            
        self.claude_client = HawaiianClaudeClient()
        self.cultural_tone_manager = CulturalToneManager()
        self.conversation_history = []
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
    def get_greeting(self):
        """Get appropriate Hawaiian greeting based on time"""
        current_time = datetime.now(self.hawaii_tz)
        hour = current_time.hour
        
        if 5 <= hour < 12:
            return "Aloha kakahiaka"
        elif 12 <= hour < 18:
            return "Aloha awakea"
        elif 18 <= hour < 22:
            return "Aloha ahiahi"
        else:
            return "Aloha"
    
    def display_welcome(self):
        """Display welcome message"""
        greeting = self.get_greeting()
        current_time = datetime.now(self.hawaii_tz).strftime("%I:%M %p HST")
        
        print("\n" + "="*60)
        print("🌺 Hawaiian LeniLani AI Consulting Chatbot 🌺")
        print("="*60)
        print(f"\n{greeting}! Welcome to LeniLani Consulting")
        print(f"Current time in Hawaii: {current_time}")
        print("\nI'm here to help your Hawaiian business thrive with AI!")
        print("Type 'exit' or 'quit' to end the conversation")
        print("="*60 + "\n")
    
    def run(self):
        """Run the interactive chatbot"""
        self.display_welcome()
        
        # Initial greeting from bot
        initial_greeting = f"{self.get_greeting()}! I'm your AI consultant from LeniLani. How can I help your business today? Whether you run a restaurant, tourism business, farm, or any other local venture, I'm here to talk story about how AI can help you succeed! 🤙"
        print(f"🤖 Bot: {initial_greeting}\n")
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": initial_greeting
        })
        
        while True:
            try:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n🤖 Bot: Aloha! Thanks for talking story with us. A hui hou! (Until we meet again) 🌺")
                    break
                
                if not user_input:
                    continue
                
                # Generate response using Claude
                print("\n🤖 Bot: ", end="", flush=True)
                
                response = self.claude_client.generate_response(
                    user_message=user_input,
                    conversation_history=self.conversation_history,
                    business_context={
                        "location": "Hawaii",
                        "focus": "Local Hawaiian businesses"
                    },
                    cultural_mode="authentic"
                )
                
                bot_response = response["response"]
                print(bot_response)
                
                # Update conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": bot_response
                })
                
                # Keep only last 10 exchanges
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\n🤖 Bot: Aloha! Mahalo for your time! 🌺")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Let's try again...\n")


if __name__ == "__main__":
    chatbot = HawaiianChatbotDemo()
    chatbot.run()