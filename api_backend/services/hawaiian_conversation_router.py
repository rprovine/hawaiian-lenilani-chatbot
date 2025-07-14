"""
Hawaiian Conversation Router - Routes conversations to Claude AI
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import sys
import re

logger = logging.getLogger(__name__)


class HawaiianConversationRouter:
    """Routes conversations to Claude AI for cultural and business responses"""
    
    def __init__(self):
        # Session storage (in production, use Redis)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        # Initialize lead capture service
        self.lead_capture = None
        self._init_lead_capture()
        
        logger.info("Hawaiian Conversation Router initialized")
    
    def _init_lead_capture(self):
        """Initialize lead capture service"""
        try:
            from .lead_capture_service import LeadCaptureService
            self.lead_capture = LeadCaptureService()
        except Exception as e:
            logger.warning(f"Lead capture service not available: {str(e)}")
    
    async def route_message(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route message to Claude AI for cultural and business responses
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Get or create session
            session = self._get_or_create_session(session_id, user_id)
            
            # Route all messages to Claude
            return await self._route_to_claude(
                user_message,
                session,
                metadata
            )
                
        except Exception as e:
            logger.error(f"Error routing message: {str(e)}")
            return self._fallback_response(user_message)
    
    
    async def _route_to_claude(
        self,
        message: str,
        session: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Route to Claude for cultural and business responses"""
        try:
            # Import Claude client and business categories (avoid circular import)
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            from claude_integration.hawaiian_claude_client import HawaiianClaudeClient
            from api_backend.config.business_categories import HAWAIIAN_BUSINESS_CATEGORIES, CATEGORY_QUICK_SELECT, ISLAND_CATEGORY_FOCUS
            
            claude_client = HawaiianClaudeClient()
            
            # Build conversation history
            conversation_history = session.get("conversation_history", [])
            
            # Add metadata as business context
            business_context = {}
            if metadata:
                business_context.update(metadata)
            
            # Add greeting status and conversation tracking to context
            business_context['has_greeted'] = session.get('has_greeted', False)
            business_context['message_count'] = len(conversation_history) // 2  # Rough count of exchanges
            business_context['conversation_history'] = conversation_history[-6:]  # Last 3 exchanges for context
            
            # Add business categories context
            business_context['categories'] = HAWAIIAN_BUSINESS_CATEGORIES
            business_context['quick_select'] = CATEGORY_QUICK_SELECT
            
            # Extract business context from message
            extracted_context = self._extract_business_context(message, business_context)
            business_context.update(extracted_context)
            
            # Add island-specific category focus if island is known
            if business_context.get('island'):
                island_key = business_context['island'].lower().replace(' ', '_')
                business_context['island_focus'] = ISLAND_CATEGORY_FOCUS.get(island_key, [])
            
            # Generate Claude response
            claude_response = await asyncio.to_thread(
                claude_client.generate_response,
                user_message=message,
                conversation_history=conversation_history,
                business_context=business_context,
                cultural_mode="authentic"
            )
            
            # Mark that we've greeted if this is first message
            if not session.get('has_greeted'):
                session['has_greeted'] = True
            
            # Update conversation history
            conversation_history.append({
                "role": "user",
                "content": message
            })
            conversation_history.append({
                "role": "assistant",
                "content": claude_response["response"]
            })
            
            # Keep only last 20 messages
            session["conversation_history"] = conversation_history[-20:]
            
            # Check if lead information is available and capture it
            lead_info = self._extract_lead_info(message, conversation_history, session)
            logger.info(f"Lead extraction result: {lead_info}")
            if lead_info and self.lead_capture:
                logger.info(f"Capturing lead with info: {lead_info}")
                asyncio.create_task(self._capture_lead(lead_info, session))
            
            return {
                "response": claude_response["response"],
                "metadata": claude_response.get("metadata", {}),
                "source": "claude"
            }
            
        except Exception as e:
            logger.error(f"Error routing to Claude: {str(e)}")
            return self._fallback_response(message)
    
    def _get_or_create_session(
        self,
        session_id: Optional[str],
        user_id: Optional[str]
    ) -> Dict[str, Any]:
        """Get or create user session"""
        if not session_id:
            session_id = f"session_{datetime.now().timestamp()}"
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": datetime.now(),
                "conversation_history": [],
                "business_context": {},
                "conversation_stage": "greeting",
                "has_greeted": False
            }
        
        return self.sessions[session_id]
    
    def _fallback_response(self, message: str) -> Dict[str, Any]:
        """Fallback response when routing fails"""
        return {
            "response": (
                "Ho brah, sorry! Having some technical difficulties right now. "
                "But no worries! You can reach Reno directly at reno@lenilani.com or "
                "call 808-766-1164. We stay here for help you!"
            ),
            "source": "fallback",
            "error": True
        }
    
    def _extract_business_context(self, message: str, existing_context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business context from message"""
        context = {}
        message_lower = message.lower()
        
        # Extract island mentions
        islands = ["oahu", "maui", "big island", "hawaii island", "kauai", "molokai", "lanai"]
        for island in islands:
            if island in message_lower:
                context["island"] = island.title()
                break
        
        # Import categories if not already imported
        try:
            from api_backend.config.business_categories import HAWAIIAN_BUSINESS_CATEGORIES
        except:
            return context
            
        # Extract business category mentions
        for category_key, category_info in HAWAIIAN_BUSINESS_CATEGORIES.items():
            # Check main category keywords
            if any(keyword in message_lower for keyword in category_info['display_name'].lower().split()):
                context['business_category'] = category_key
                context['category_info'] = category_info
                break
            
            # Check subcategories
            for subcategory in category_info['subcategories']:
                if subcategory.lower() in message_lower:
                    context['business_category'] = category_key
                    context['category_info'] = category_info
                    context['subcategory'] = subcategory
                    break
                    
        # Extract specific business type within categories
        business_types = [
            "restaurant", "food truck", "cafe", "coffee shop",
            "hotel", "resort", "vacation rental", "tour",
            "farm", "agriculture", "produce", "coffee farm",
            "retail", "store", "shop", "boutique",
            "real estate", "property", "development",
            "healthcare", "medical", "wellness", "clinic",
            "technology", "software", "it services",
            "construction", "contractor", "building",
            "professional services", "consulting", "legal", "accounting"
        ]
        
        for btype in business_types:
            if btype in message_lower:
                context["business_type"] = btype
                # Map to category if not already set
                if 'business_category' not in context:
                    if btype in ["restaurant", "food truck", "cafe", "coffee shop"]:
                        context['business_category'] = 'restaurants_food'
                        context['category_info'] = HAWAIIAN_BUSINESS_CATEGORIES.get('restaurants_food', {})
                    elif btype in ["hotel", "resort", "vacation rental", "tour"]:
                        context['business_category'] = 'tourism_hospitality'
                        context['category_info'] = HAWAIIAN_BUSINESS_CATEGORIES.get('tourism_hospitality', {})
                    elif btype in ["farm", "agriculture", "produce", "coffee farm"]:
                        context['business_category'] = 'agriculture_farming'
                        context['category_info'] = HAWAIIAN_BUSINESS_CATEGORIES.get('agriculture_farming', {})
                    elif btype in ["retail", "store", "shop", "boutique"]:
                        context['business_category'] = 'local_retail'
                        context['category_info'] = HAWAIIAN_BUSINESS_CATEGORIES.get('local_retail', {})
                break
                
        # Extract challenges
        challenge_keywords = [
            "struggle", "problem", "issue", "challenge", "difficult",
            "help with", "need", "looking for", "want to", "trying to"
        ]
        
        for keyword in challenge_keywords:
            if keyword in message_lower:
                context["has_challenge"] = True
                break
                
        return context
    
    def _extract_lead_info(self, message: str, conversation_history: List[Dict], session: Dict) -> Optional[Dict]:
        """Extract lead information from conversation"""
        # Look for email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        
        # Look for phone
        phone_pattern = r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\(\d{3}\)\s*\d{3}[-.\s]?\d{4})'
        phone_match = re.search(phone_pattern, message)
        
        # Check if we have enough info to create a lead
        if email_match or phone_match or len(conversation_history) > 6:
            lead_info = {
                "email": email_match.group() if email_match else None,
                "phone": phone_match.group() if phone_match else None,
                "business_type": session.get("business_context", {}).get("business_type"),
                "location": session.get("business_context", {}).get("island"),
                "main_challenge": session.get("business_context", {}).get("challenge"),
                "message_count": len(conversation_history) // 2
            }
            
            # Extract name if mentioned
            name_patterns = [
                r"(?:my name is|i'm|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
                r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+here"
            ]
            for pattern in name_patterns:
                name_match = re.search(pattern, message, re.IGNORECASE)
                if name_match:
                    lead_info["name"] = name_match.group(1)
                    break
            
            return lead_info
        
        return None
    
    async def _capture_lead(self, lead_info: Dict, session: Dict):
        """Capture and send lead information"""
        try:
            logger.info(f"Starting lead capture for: {lead_info}")
            # Generate conversation summary
            conversation_summary = self._generate_conversation_summary(session)
            
            # Calculate qualification score
            qualification_score = self._calculate_qualification_score(lead_info, session)
            logger.info(f"Lead qualification score: {qualification_score}")
            
            # Capture the lead
            result = await self.lead_capture.capture_lead(
                lead_data=lead_info,
                conversation_summary=conversation_summary,
                qualification_score=qualification_score
            )
            
            if result["success"]:
                logger.info(f"Lead captured successfully: {result['lead_id']}")
            else:
                logger.error(f"Failed to capture lead: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Error in lead capture: {str(e)}")
    
    def _generate_conversation_summary(self, session: Dict) -> str:
        """Generate a summary of the conversation"""
        conversation_history = session.get("conversation_history", [])
        business_context = session.get("business_context", {})
        
        summary_parts = []
        
        # Business type and location
        if business_context.get("business_type"):
            summary_parts.append(f"Business: {business_context['business_type']}")
        if business_context.get("island"):
            summary_parts.append(f"Location: {business_context['island']}")
        
        # Main topics discussed
        if business_context.get("challenge"):
            summary_parts.append(f"Main challenge: {business_context['challenge']}")
        
        # Conversation flow
        if conversation_history:
            summary_parts.append(f"Messages exchanged: {len(conversation_history) // 2}")
            
            # Get last few user messages
            user_messages = [msg["content"] for msg in conversation_history if msg["role"] == "user"][-3:]
            if user_messages:
                summary_parts.append(f"Recent topics: {', '.join(msg[:50] + '...' if len(msg) > 50 else msg for msg in user_messages)}")
        
        return " | ".join(summary_parts)
    
    def _calculate_qualification_score(self, lead_info: Dict, session: Dict) -> int:
        """Calculate lead qualification score (0-100)"""
        score = 0
        
        # Contact info provided (30 points)
        if lead_info.get("email"):
            score += 20
        if lead_info.get("phone"):
            score += 10
        
        # Business details (30 points)
        if lead_info.get("business_type"):
            score += 10
        if lead_info.get("location"):
            score += 10
        if lead_info.get("main_challenge"):
            score += 10
        
        # Engagement level (40 points)
        message_count = lead_info.get("message_count", 0)
        if message_count >= 5:
            score += 40
        elif message_count >= 3:
            score += 25
        elif message_count >= 2:
            score += 15
        
        return min(score, 100)
    
    def get_suggestions(self, user_message: str) -> List[str]:
        """Get contextual suggestions for user"""
        # Basic contextual suggestions
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "aloha", "howzit"]):
            return [
                "Tell me about your services",
                "I need help with my business",
                "What's the pricing?",
                "Show me examples"
            ]
        elif any(word in message_lower for word in ["tourism", "hotel", "visitor"]):
            return [
                "Tourism analytics",
                "Booking optimization",
                "Seasonal forecasting",
                "Get a quote"
            ]
        elif any(word in message_lower for word in ["restaurant", "food", "dining"]):
            return [
                "Restaurant AI solutions",
                "Inventory optimization",
                "Customer analytics",
                "Schedule consultation"
            ]
        else:
            return [
                "Learn more",
                "See pricing",
                "Talk to someone",
                "View examples"
            ]