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

logger = logging.getLogger(__name__)


class HawaiianConversationRouter:
    """Routes conversations to Claude AI for cultural and business responses"""
    
    def __init__(self):
        # Session storage (in production, use Redis)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
        logger.info("Hawaiian Conversation Router initialized")
    
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
            
            # Add greeting status to context
            business_context['has_greeted'] = session.get('has_greeted', False)
            business_context['message_count'] = len(conversation_history) // 2  # Rough count of exchanges
            
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