"""
Cultural Context Manager - Manages Hawaiian cultural context for conversations
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CulturalContextManager:
    """Manages Hawaiian cultural context for AI conversations"""
    
    def __init__(self):
        self.hawaiian_values = {
            "aloha": {
                "meaning": "Love, affection, compassion, mercy, sympathy, kindness",
                "business_application": "Build genuine relationships before transactions"
            },
            "ohana": {
                "meaning": "Family, including extended family and close friends",
                "business_application": "Treat business partners as family, support community"
            },
            "malama_aina": {
                "meaning": "To care for and honor the land",
                "business_application": "Sustainable practices, environmental responsibility"
            },
            "lokahi": {
                "meaning": "Unity, harmony, working together",
                "business_application": "Collaborative solutions, community partnerships"
            },
            "kuleana": {
                "meaning": "Responsibility, privilege, area of responsibility",
                "business_application": "Take ownership, be accountable to community"
            },
            "pono": {
                "meaning": "Righteousness, balance, harmony",
                "business_application": "Ethical business practices, doing what's right"
            }
        }
        
        self.island_contexts = {
            "oahu": {
                "nickname": "The Gathering Place",
                "business_characteristics": [
                    "Urban center with diverse economy",
                    "Heavy tourism and military presence",
                    "Tech hub of Hawaii",
                    "High cost of living and rent"
                ],
                "key_industries": ["Tourism", "Military", "Technology", "Healthcare", "Real Estate"],
                "challenges": ["Traffic congestion", "High competition", "Expensive real estate"],
                "opportunities": ["Government contracts", "Tech innovation", "International business"]
            },
            "maui": {
                "nickname": "The Valley Isle",
                "business_characteristics": [
                    "High-end tourism destination",
                    "Strong agricultural heritage",
                    "Seasonal visitor patterns",
                    "Growing tech scene"
                ],
                "key_industries": ["Tourism", "Agriculture", "Real Estate", "Renewable Energy"],
                "challenges": ["Seasonal fluctuations", "Water scarcity", "Housing costs"],
                "opportunities": ["Eco-tourism", "Agri-tech", "Luxury market"]
            },
            "big island": {
                "nickname": "The Orchid Isle",
                "business_characteristics": [
                    "Diverse climates and agriculture",
                    "Active volcanoes attract tourists",
                    "Growing astronomy industry",
                    "Lower cost of living"
                ],
                "key_industries": ["Agriculture", "Tourism", "Astronomy", "Energy"],
                "challenges": ["Geographic isolation", "Limited infrastructure", "Natural disasters"],
                "opportunities": ["Renewable energy", "Specialty agriculture", "Research"]
            },
            "kauai": {
                "nickname": "The Garden Isle",
                "business_characteristics": [
                    "Small, tight-knit community",
                    "Pristine natural environment",
                    "Limited development",
                    "Strong environmental focus"
                ],
                "key_industries": ["Tourism", "Agriculture", "Film Production"],
                "challenges": ["Limited resources", "Environmental restrictions", "Small market"],
                "opportunities": ["Eco-tourism", "Sustainable agriculture", "Wellness tourism"]
            }
        }
        
        self.business_cultural_phrases = {
            "relationship_building": [
                "Let's talk story first",
                "We like get to know you",
                "Ohana style business",
                "Building bridges, not just deals"
            ],
            "commitment": [
                "We stay with you long term",
                "Your success is our kuleana",
                "Partners for da long haul",
                "We no leave you hanging"
            ],
            "problem_solving": [
                "We figure it out together",
                "No worry, we find one way",
                "Plenty solutions if we work together",
                "Every challenge get one opportunity"
            ],
            "sustainability": [
                "Malama da 'aina while we grow",
                "Sustainable success for generations",
                "Taking care of tomorrow today",
                "Good for business, good for da islands"
            ]
        }
        
        logger.info("Cultural Context Manager initialized")
    
    def build_context(
        self,
        user_message: str,
        business_context: Optional[Dict[str, Any]] = None,
        time_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build comprehensive cultural context for the conversation"""
        
        context = {
            "values_applied": [],
            "cultural_elements": [],
            "communication_style": "warm_professional"
        }
        
        # Apply relevant Hawaiian values based on message content
        if any(word in user_message.lower() for word in ["help", "support", "need"]):
            context["values_applied"].append(self.hawaiian_values["aloha"])
            context["values_applied"].append(self.hawaiian_values["kuleana"])
        
        if any(word in user_message.lower() for word in ["community", "local", "together"]):
            context["values_applied"].append(self.hawaiian_values["ohana"])
            context["values_applied"].append(self.hawaiian_values["lokahi"])
        
        if any(word in user_message.lower() for word in ["sustainable", "environment", "green"]):
            context["values_applied"].append(self.hawaiian_values["malama_aina"])
        
        # Add business context if provided
        if business_context:
            if "island" in business_context:
                island = business_context["island"].lower()
                if island in self.island_contexts:
                    context["island_context"] = self.island_contexts[island]
            
            if "business_type" in business_context:
                context["business_type"] = business_context["business_type"]
        
        # Add time-based context
        if time_context:
            context["time_greeting"] = time_context.get("greeting", "Aloha")
            context["time_period"] = time_context.get("period", "day")
        
        # Select appropriate cultural phrases
        context["suggested_phrases"] = self._select_cultural_phrases(user_message)
        
        return context
    
    def _select_cultural_phrases(self, user_message: str) -> List[str]:
        """Select appropriate cultural phrases based on conversation context"""
        selected_phrases = []
        
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["meet", "know", "introduce"]):
            selected_phrases.extend(self.business_cultural_phrases["relationship_building"])
        
        if any(word in message_lower for word in ["help", "solve", "fix", "challenge"]):
            selected_phrases.extend(self.business_cultural_phrases["problem_solving"])
        
        if any(word in message_lower for word in ["long term", "future", "grow"]):
            selected_phrases.extend(self.business_cultural_phrases["commitment"])
        
        if any(word in message_lower for word in ["sustainable", "environment", "green"]):
            selected_phrases.extend(self.business_cultural_phrases["sustainability"])
        
        return selected_phrases[:3]  # Return top 3 most relevant phrases
    
    def get_island_context(self, island: str) -> Dict[str, Any]:
        """Get specific context for an island"""
        island_lower = island.lower()
        return self.island_contexts.get(island_lower, {})
    
    def get_cultural_value(self, value_name: str) -> Dict[str, str]:
        """Get specific Hawaiian cultural value details"""
        return self.hawaiian_values.get(value_name, {})
    
    def enhance_message_with_culture(self, message: str, context: Dict[str, Any]) -> str:
        """Enhance a message with cultural elements"""
        enhanced_message = message
        
        # Add cultural greeting if appropriate
        if context.get("time_greeting") and not any(
            greeting in message for greeting in ["Aloha", "aloha", "Howzit", "howzit"]
        ):
            enhanced_message = f"{context['time_greeting']}! {enhanced_message}"
        
        # Add cultural closing if discussing next steps
        if any(word in message.lower() for word in ["next step", "move forward", "proceed"]):
            if not any(closing in message for closing in ["mahalo", "Mahalo", "a hui hou"]):
                enhanced_message += " Mahalo for your time!"
        
        return enhanced_message
    
    def get_business_greeting(self, business_type: str, island: str) -> str:
        """Get a culturally appropriate business greeting"""
        island_context = self.get_island_context(island)
        
        greetings = {
            "tourism": f"Aloha! Always exciting to work with tourism businesses on {island}!",
            "restaurant": f"Aloha! Food brings ohana together - love working with restaurants!",
            "agriculture": f"Aloha! Malama 'aina - honored to support our farmers!",
            "retail": f"Aloha! Local retail is the heartbeat of our communities!",
            "technology": f"Aloha! Tech innovation in paradise - let's make it happen!",
            "default": f"Aloha! Excited to learn about your {island} business!"
        }
        
        return greetings.get(business_type.lower(), greetings["default"])