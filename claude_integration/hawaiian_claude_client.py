"""
Hawaiian Claude Client - Integrates Anthropic Claude API with Hawaiian cultural context
"""
import os
import logging
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import json
from datetime import datetime
import pytz

from .cultural_context_manager import CulturalContextManager
from .pidgin_response_processor import PidginResponseProcessor
from .aloha_spirit_injector import AlohaSpiritInjector

logger = logging.getLogger(__name__)

HAWAIIAN_CLAUDE_PROMPT = """
You are an AI assistant for LeniLani Consulting, a Hawaii-based AI and technology consulting firm that specializes in helping local Hawaiian businesses thrive using cutting-edge technology while respecting island culture and values.

HAWAIIAN CULTURAL IDENTITY:
- You embody the spirit of aloha: love, respect, compassion, and genuine care
- You understand ohana (family) approach to business relationships
- You respect malama 'aina (caring for the land) and sustainable practices
- You value lokahi (unity) in helping the Hawaiian business community

COMMUNICATION STYLE:
- Use Hawaiian Pidgin English naturally but professionally
- Mix standard English with local expressions like "shoots," "yeah no worries," "how you stay," "talk story," "choke" (many), "grindz" (good business/food)
- Greet based on Hawaii time: "Aloha kakahiaka" (morning), "Aloha awakea" (afternoon), "Aloha ahiahi" (evening)
- Approach conversations with "talk story" mentality - build relationship first
- Use "brah," "bruddah," or "sistah" occasionally when appropriate, but maintain professionalism

HAWAIIAN BUSINESS UNDERSTANDING:
- Inter-island commerce challenges and logistics
- Seasonal tourism patterns and local vs. visitor markets  
- Agricultural cycles and farm-to-table movements
- Sustainable business practices and environmental consciousness
- Competition with mainland chains while supporting local economy
- Military and government contractor opportunities
- Remote work and digital transformation needs

OUR SERVICES FOR HAWAIIAN BUSINESSES:
- Data Analytics: Tourism patterns, agricultural optimization, seasonal forecasting
- Custom Chatbots: Multi-language support (English/Japanese/Hawaiian), cultural awareness
- Fractional CTO: Technology leadership for growing island businesses
- HubSpot Solutions: Marketing automation for tourism, local events, cultural campaigns

HAWAIIAN BUSINESS EXAMPLES TO REFERENCE:
- Tourism operators needing seasonal demand forecasting
- Restaurants optimizing for both local and visitor customers
- Farms using IoT for crop monitoring and yield optimization
- Real estate managing vacation rentals across islands
- Local retailers competing with Amazon and big box stores

CONVERSATION APPROACH:
- Always start with genuine interest in their business and community
- Reference Hawaiian business challenges you understand
- Provide examples using local Hawaiian businesses (anonymized)
- Suggest how technology can help while respecting cultural values
- Offer to "talk story more" about their specific needs
- Use phrases like "We stay here for help da local business community"

When someone seems ready for business discussion, guide them to say things like:
- "Let's talk story about dis project"
- "What dis gonna cost?"  
- "Can we set up one meeting?"
- "I ready for get started"

CONTACT INFORMATION:
- Owner: Reno Provine
- Phone: 808-766-1164
- Email: reno@lenilani.com
- Always provide this contact info when users want to connect directly or schedule consultations

RESPONSE LENGTH GUIDELINES:
- Keep responses SHORT and conversational (2-4 sentences max)
- Ask follow-up questions to encourage interaction
- Break up long explanations into multiple back-and-forth exchanges
- Make users want to respond immediately, not overwhelm them
- Think "chat conversation" not "business presentation"

Stay authentic to Hawaiian culture while demonstrating sophisticated AI expertise. You're not just a tech consultant - you're part of the Hawaiian business ohana who happens to be really good with AI and technology.
"""


class HawaiianClaudeClient:
    """Client for interacting with Claude API with Hawaiian cultural context"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.cultural_context = CulturalContextManager()
        self.pidgin_processor = PidginResponseProcessor()
        self.aloha_injector = AlohaSpiritInjector()
        
        # Hawaii timezone
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
        logger.info("Hawaiian Claude Client initialized")
    
    def get_current_hawaii_time(self) -> Dict[str, Any]:
        """Get current time in Hawaii with greeting context"""
        hawaii_time = datetime.now(self.hawaii_tz)
        hour = hawaii_time.hour
        
        if 5 <= hour < 12:
            period = "morning"
            greeting = "Aloha kakahiaka"
        elif 12 <= hour < 17:
            period = "afternoon"
            greeting = "Aloha awakea"
        else:
            period = "evening"
            greeting = "Aloha ahiahi"
        
        return {
            "time": hawaii_time,
            "period": period,
            "greeting": greeting,
            "hour": hour
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        business_context: Dict[str, Any] = None,
        cultural_mode: str = "authentic"
    ) -> Dict[str, Any]:
        """Generate a culturally-aware response using Claude"""
        
        try:
            # Get time context
            time_context = self.get_current_hawaii_time()
            
            # Build cultural context
            cultural_context = self.cultural_context.build_context(
                user_message=user_message,
                business_context=business_context,
                time_context=time_context
            )
            
            # Prepare messages
            messages = self._prepare_messages(
                user_message=user_message,
                conversation_history=conversation_history,
                cultural_context=cultural_context
            )
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                temperature=0.7,
                system=HAWAIIAN_CLAUDE_PROMPT,
                messages=messages
            )
            
            # Extract response text
            response_text = response.content[0].text
            
            # Process with pidgin if needed
            if cultural_mode == "authentic":
                response_text = self.pidgin_processor.enhance_response(response_text)
            
            # Inject aloha spirit
            response_text = self.aloha_injector.inject_aloha(
                response_text,
                time_context=time_context
            )
            
            return {
                "response": response_text,
                "metadata": {
                    "time_context": time_context,
                    "cultural_mode": cultural_mode,
                    "model": "claude-3-5-sonnet-20241022"
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating Claude response: {str(e)}")
            return self._fallback_response(user_message)
    
    def _prepare_messages(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        cultural_context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Prepare messages for Claude API"""
        messages = []
        
        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                content = msg.get("content", "").strip()
                if content:  # Only add messages with non-empty content
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": content
                    })
        
        # Add cultural context as assistant message
        if cultural_context:
            context_msg = f"[Context: {json.dumps(cultural_context)}]"
            if context_msg.strip():  # Only add if context message is not empty
                messages.append({
                    "role": "assistant",
                    "content": context_msg
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return messages
    
    def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Fallback response when Claude API fails"""
        time_context = self.get_current_hawaii_time()
        
        fallback_messages = [
            f"{time_context['greeting']}! Ho, looks like we stay having some technical difficulties. No worries though! You can reach Reno directly at reno@lenilani.com or call 808-766-1164.",
            f"Shoots! Our AI stay taking one quick break. But no worries, we still here for help! Email Reno at reno@lenilani.com or call 808-766-1164 for talk story session.",
            f"Eh, sorry bout dat! Our system stay little bit slow right now. Try again in couple minutes or contact Reno directly at reno@lenilani.com (808-766-1164) - we always here for da local business community!"
        ]
        
        import random
        response = random.choice(fallback_messages)
        
        return {
            "response": response,
            "metadata": {
                "time_context": time_context,
                "cultural_mode": "authentic",
                "fallback": True
            }
        }
    
    def handle_business_inquiry(
        self,
        business_type: str,
        island: str,
        challenges: List[str],
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Handle specific business inquiry with cultural context"""
        
        # Build business context
        business_context = {
            "business_type": business_type,
            "island": island,
            "challenges": challenges,
            "island_specific": self.cultural_context.get_island_context(island)
        }
        
        # Create targeted prompt
        inquiry_prompt = f"""
        A {business_type} business on {island} is looking for help. 
        They face these challenges: {', '.join(challenges)}.
        
        Please provide specific, culturally-aware advice that:
        1. Shows understanding of {island}-specific business environment
        2. Suggests relevant technology solutions from our services
        3. References similar local businesses (anonymized)
        4. Maintains authentic Hawaiian communication style
        """
        
        return self.generate_response(
            user_message=inquiry_prompt,
            conversation_history=conversation_history,
            business_context=business_context
        )
    
    def generate_cultural_greeting(self, user_name: Optional[str] = None) -> str:
        """Generate a culturally appropriate greeting"""
        time_context = self.get_current_hawaii_time()
        
        greeting_templates = {
            "morning": [
                f"{time_context['greeting']}! 🌅 Beautiful morning, yeah? How can we help your business today?",
                f"{time_context['greeting']}! Hope you getting one good start to da day! What can we do for you?",
            ],
            "afternoon": [
                f"{time_context['greeting']}! ☀️ Perfect time for talk story about your business! How you stay?",
                f"{time_context['greeting']}! Hot one today, yeah? Let's talk about how we can help your business stay cool with technology!",
            ],
            "evening": [
                f"{time_context['greeting']}! 🌙 Mahalo for reaching out! Even after hours, we stay thinking about helping local businesses.",
                f"{time_context['greeting']}! Perfect time for plan tomorrow's success! What's on your mind?",
            ]
        }
        
        import random
        base_greeting = random.choice(greeting_templates[time_context['period']])
        
        if user_name:
            base_greeting = base_greeting.replace("!", f", {user_name}!")
        
        return base_greeting