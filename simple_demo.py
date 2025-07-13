#!/usr/bin/env python3
"""
Simple Hawaiian LeniLani Chatbot Demo - Direct Claude Integration
"""

import os
from datetime import datetime
import pytz
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HAWAIIAN_PROMPT = """You are an AI assistant for LeniLani Consulting, a Hawaii-based AI consulting firm helping local Hawaiian businesses.

Key traits:
- Embody aloha spirit: warm, respectful, genuinely caring
- Mix professional English with natural Hawaiian Pidgin when appropriate
- Understand Hawaiian business challenges: high costs, seasonal tourism, logistics
- Focus on practical AI solutions for restaurants, tourism, farms, retail

Communication style:
- Start with relationship building ("talk story")
- Use local expressions naturally: "shoots", "yeah", "stay", "da kine"
- Reference local context: islands, weather, tourist seasons
- Be conversational and helpful, not robotic or menu-driven

When discussing business:
- Ask about specific challenges they face
- Share relevant examples from other Hawaiian businesses
- Suggest practical AI solutions that respect local values
- Focus on ROI and practical implementation

Never give menu-style responses or lists of options unless specifically asked."""

class SimpleChatbot:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your_anthropic_api_key_here":
            print("\n⚠️  Please set your ANTHROPIC_API_KEY in the .env file")
            exit(1)
            
        self.client = Anthropic(api_key=api_key)
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        self.messages = []
        
    def get_greeting(self):
        hour = datetime.now(self.hawaii_tz).hour
        if 5 <= hour < 12:
            return "Aloha kakahiaka"
        elif 12 <= hour < 18:
            return "Aloha awakea"
        else:
            return "Aloha ahiahi"
    
    def chat(self, user_input):
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            system=HAWAIIAN_PROMPT,
            messages=self.messages
        )
        
        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        # Keep only last 10 messages
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]
            
        return assistant_message
    
    def run(self):
        current_time = datetime.now(self.hawaii_tz).strftime("%I:%M %p HST")
        
        print("\n" + "="*60)
        print("🌺 Hawaiian LeniLani AI Consulting Chatbot 🌺")
        print("="*60)
        print(f"\n{self.get_greeting()}! Welcome to LeniLani Consulting")
        print(f"Current time in Hawaii: {current_time}")
        print("\nType 'exit' to end the conversation")
        print("="*60 + "\n")
        
        # Initial greeting
        initial = f"{self.get_greeting()}! I'm here to help your Hawaiian business thrive with AI. What kind of business do you run? I'd love to talk story about how we can help! 🤙"
        print(f"🤖 Bot: {initial}\n")
        self.messages.append({"role": "assistant", "content": initial})
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\n🤖 Bot: Aloha! Mahalo for talking story. A hui hou! 🌺")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 Bot: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n\n🤖 Bot: Aloha! Mahalo! 🌺")
                break
            except EOFError:
                print("\n\n🤖 Bot: Aloha! Input was interrupted. Mahalo! 🌺")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please check your API key and try again.\n")

if __name__ == "__main__":
    bot = SimpleChatbot()
    bot.run()