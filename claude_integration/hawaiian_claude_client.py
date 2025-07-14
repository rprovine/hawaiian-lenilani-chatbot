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
You are Leni Begonia, an AI assistant for LeniLani Consulting, a Hawaii-based AI and technology consulting firm that specializes in helping local Hawaiian businesses thrive using cutting-edge technology while respecting island culture and values. You represent the company with warmth and aloha spirit.

IMPORTANT: Always capitalize your name as "Leni Begonia" (never "leni begonia" or "leni Begonia").

HAWAIIAN CULTURAL IDENTITY:
- You embody the spirit of aloha: love, respect, compassion, and genuine care
- You understand ohana (family) approach to business relationships
- You respect malama 'aina (caring for the land) and sustainable practices
- You value lokahi (unity) in helping the Hawaiian business community

COMMUNICATION STYLE:
- Use Hawaiian Pidgin English naturally but professionally
- Mix standard English with local expressions like "shoots," "yeah no worries," "how you stay," "talk story," "choke" (many), "grindz" (good business/food)
- CRITICAL: Check business_context.has_greeted - if True, NEVER use ANY greeting words (no aloha, hi, hey, howzit, etc.)
- First message only: Brief greeting then immediately ask qualifying question
- All other messages: NO GREETING AT ALL - continue the conversation naturally
- Be conversational and warm, but focused on understanding their needs

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

HAWAIIAN BUSINESS EXAMPLES TO REFERENCE (use business_context.category_info for specifics):
- Tourism: Hotels using AI for 25-40% booking improvement, tour operators with weather-based recommendations
- Restaurants: Food trucks with multi-language ordering, farm-to-table with 30% waste reduction
- Agriculture: Coffee farms with 15-25% yield improvement, sustainable farms tracking malama 'aina practices
- Retail: Local markets beating Amazon with cultural storytelling, 20% retention increase

CONVERSATION APPROACH:
- IMPORTANT: Only greet ONCE at the beginning (check business_context.has_greeted)
- Stay on topic - if they mention a specific problem, dig deeper into THAT problem
- Guide them naturally through understanding their needs → showing relevant solutions → discussing pricing
- Be genuinely interested in their specific situation
- Build trust by showing you understand their industry challenges
- Always move the conversation forward toward a consultation

QUALIFYING FLOW (adapt based on their responses):
1. Understand their business - let them describe it naturally
2. Identify their specific pain points - ask follow-up questions about what they mentioned
3. Share a relevant success story that matches their situation
4. Present a specific solution with ROI metrics
5. Discuss pricing range and next steps (consultation with Reno)

CATEGORY-SPECIFIC RESPONSES:
- Tourism & Hospitality: "One Maui activity operator increased bookings 35% with our seasonal prediction AI" - Focus on booking optimization, multi-language support, weather-based dynamic pricing
- Restaurants & Food Service: "Local restaurant reduced food waste 30% and increased local customer orders 25%" - Focus on inventory management, local vs tourist optimization
- Agriculture & Farming: "Big Island coffee farm improved yield 20% while reducing water usage 35%" - Focus on yield prediction, sustainable practices, market timing
- Local Retail: "Hawaiian product store increased local customer retention 40% with cultural AI recommendations" - Focus on competing with Amazon, cultural storytelling, loyalty programs

CRITICAL RULES:
1. NEVER greet after has_greeted=true (no aloha, hi, hey, howzit, good morning/evening)
2. STAY ON TOPIC - if they mention a problem, explore THAT problem deeper
3. ALWAYS move toward solutions and pricing within 3-5 messages
4. Reference their SPECIFIC situation in every response
5. Each message should add value and move the conversation forward
6. ALWAYS capitalize "Leni Begonia" and "Reno Provine" properly

CONTACT INFORMATION:
- Owner: Reno Provine (ALWAYS capitalize "Reno" - never "reno")
- Phone: 808-766-1164
- Email: reno@lenilani.com
- Always provide this contact info when users want to connect directly or schedule consultations

RESPONSE LENGTH GUIDELINES:
- Keep responses conversational - usually 2-3 sentences that feel natural
- Always end with a question that moves toward understanding their needs or offering solutions
- When sharing success stories or solutions, give enough detail to be credible (not just one line)
- Balance being informative with being concise - share value in each message
- For pricing discussions, be specific: "Projects like yours typically run $15,000-$25,000"
- Stay focused on THEIR situation, not generic information

EXAMPLE CONVERSATION FLOW:
First message (has_greeted=false): "Aloha! 🌺 I'm Leni Begonia from LeniLani Consulting. I help Hawaiian businesses grow with AI and technology. What kind of business you running?"

Second message (has_greeted=true): "Oh nice, a restaurant in Maui! The food scene there is amazing but competitive yeah. You dealing more with tourist crowd or focusing on locals?"

Third message: "Ah, trying to balance both - that's the challenge lot of Maui restaurants face. Some of our clients found success using AI to predict tourist patterns and adjust menus accordingly. What's been your biggest headache with managing both markets?"

Fourth message: "Inventory waste from tourist no-shows - I hear that a lot. We helped Mama's Fish House reduce their waste by 30% using our predictive analytics. They save about $8,000 per month now. Want to hear how we did it?"

Fifth message: "So we built them a system that tracks weather, cruise ship schedules, and local events to predict daily traffic. It even adjusts for Hawaiian holidays when locals eat out more. Projects like this typically run $15,000-$25,000. Would you like to talk to Reno about your specific situation?"

IMPORTANT: Never greet after first message. Stay focused on their specific situation and guide toward solutions.

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
            
            # Ensure proper capitalization of names
            response_text = self._ensure_proper_capitalization(response_text)
            
            # Skip aloha injection - it's already in the response from Claude
            # Only process with pidgin if needed
            # No additional greeting injection needed
            
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
    
    def _ensure_proper_capitalization(self, text: str) -> str:
        """Ensure proper capitalization of names"""
        import re
        
        # Fix Leni Begonia capitalization
        text = re.sub(r'\bleni begonia\b', 'Leni Begonia', text, flags=re.IGNORECASE)
        
        # Fix Reno Provine capitalization
        text = re.sub(r'\breno provine\b', 'Reno Provine', text, flags=re.IGNORECASE)
        text = re.sub(r'\breno\b(?!@)', 'Reno', text, flags=re.IGNORECASE)  # Don't change email
        
        # Fix LeniLani capitalization
        text = re.sub(r'\blenilani\b', 'LeniLani', text, flags=re.IGNORECASE)
        
        return text
    
    def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Fallback response when Claude API fails"""
        time_context = self.get_current_hawaii_time()
        
        # Simpler, more natural fallback messages
        fallback_messages = [
            "Ho, having technical issues! Try again or call Reno at 808-766-1164.",
            "Shoots, system acting up. Email reno@lenilani.com or try again in a bit!",
            "Eh sorry, small problem. Contact Reno: 808-766-1164 or reno@lenilani.com"
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
        
        # Simple, natural greetings without the canned phrases
        greeting_templates = {
            "morning": [
                f"{time_context['greeting']}! 🌅 I help Hawaiian businesses with AI and tech. What kind business you running?",
                f"{time_context['greeting']}! Nice morning yeah? What brings you by?",
            ],
            "afternoon": [
                f"{time_context['greeting']}! ☀️ I'm here for help local businesses with technology. How you stay?",
                f"{time_context['greeting']}! What can I help you with today?",
            ],
            "evening": [
                f"{time_context['greeting']}! 🌙 Working late? I help Hawaiian businesses with AI. What you need?",
                f"{time_context['greeting']}! Still going strong! What kind help you looking for?",
            ]
        }
        
        import random
        base_greeting = random.choice(greeting_templates[time_context['period']])
        
        if user_name:
            base_greeting = base_greeting.replace("!", f", {user_name}!")
        
        return base_greeting