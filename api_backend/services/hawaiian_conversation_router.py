"""
Hawaiian Conversation Router - Routes conversations to Claude AI
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

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
            # Import Claude client (avoid circular import)
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            from claude_integration.hawaiian_claude_client import HawaiianClaudeClient
            
            claude_client = HawaiianClaudeClient()
            
            # Build conversation history
            conversation_history = session.get("conversation_history", [])
            
            # Add metadata as business context
            business_context = {}
            if metadata:
                business_context.update(metadata)
            
            # Generate Claude response
            claude_response = await asyncio.to_thread(
                claude_client.generate_response,
                user_message=message,
                conversation_history=conversation_history,
                business_context=business_context,
                cultural_mode="authentic"
            )
            
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
                "conversation_stage": "greeting"
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