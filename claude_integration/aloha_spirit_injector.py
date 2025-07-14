"""
Aloha Spirit Injector - Adds authentic Hawaiian warmth and values to responses
"""
import logging
import random
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class AlohaSpiritInjector:
    """Injects aloha spirit and Hawaiian values into AI responses"""
    
    def __init__(self):
        # Aloha expressions by context
        self.aloha_expressions = {
            "greeting": {
                "morning": [
                    "E komo mai! 🌺",
                    "Aloha kakahiaka! 🌅",
                    "Morning! ☀️"
                ],
                "afternoon": [
                    "Aloha awakea! ☀️",
                    "Afternoon! 🌴",
                    "Aloha! 💪"
                ],
                "evening": [
                    "Aloha ahiahi! 🌙",
                    "Evening! Still going? 🌟",
                    "Aloha! Working late? 🌅"
                ]
            },
            "encouragement": [
                "You got dis, brah! 💪",
                "Together we going make it happen! 🤝",
                "No worry, every challenge get one solution! 🌈",
                "Stay strong! Success stay coming! 🌺",
                "We believe in you and your business! 🎯"
            ],
            "appreciation": [
                "Mahalo nui loa for your trust! 🙏",
                "We appreciate you choosing local! 🌺",
                "Thank you for being part of our ohana! 🤙",
                "Your support means everything! 🌴",
                "Grateful for da opportunity to help! 🙌"
            ],
            "closing": [
                "A hui hou! Until we meet again! 🤙",
                "Malama pono! Take care! 🌺",
                "Looking forward to our journey together! 🌊",
                "E komo mai - you always welcome here! 🏝️",
                "Mahalo and aloha! 🌈"
            ]
        }
        
        # Value-based enhancements
        self.value_expressions = {
            "aloha": [
                "With aloha in everything we do",
                "Bringing genuine care to your business",
                "Love and respect guide our work",
                "Aloha is our foundation"
            ],
            "ohana": [
                "Your success is our family's success",
                "We treat your business like ohana",
                "Growing together as one ohana",
                "No one gets left behind in our business ohana"
            ],
            "malama_aina": [
                "Caring for our islands while we grow",
                "Sustainable success for future generations",
                "Technology that respects our 'aina",
                "Growing responsibly with the land"
            ],
            "lokahi": [
                "Working in harmony for success",
                "Unity makes us stronger",
                "Together we achieve more",
                "Collaborative success for all"
            ],
            "kuleana": [
                "Your success is our responsibility",
                "We take our kuleana seriously",
                "Committed to doing our part",
                "Honored to share this responsibility"
            ]
        }
        
        # Contextual warmth additions
        self.warmth_additions = {
            "business_inquiry": [
                "We're excited to learn more about your vision!",
                "Your business sounds amazing!",
                "Love hearing about local businesses thriving!",
                "This is exactly the kind of business Hawaii needs!"
            ],
            "problem_solving": [
                "Every challenge is a chance to grow stronger!",
                "We've helped many businesses overcome similar challenges!",
                "No problem too big when we work together!",
                "Let's turn this challenge into opportunity!"
            ],
            "next_steps": [
                "Looking forward to this journey together!",
                "Excited for what we can accomplish!",
                "This is just the beginning of something great!",
                "Can't wait to see your business flourish!"
            ],
            "gratitude": [
                "Mahalo for trusting us with your business!",
                "Grateful for the opportunity to serve!",
                "Thank you for choosing local expertise!",
                "Honored to be part of your success story!"
            ]
        }
        
        # Hawaiian wisdom and proverbs
        self.hawaiian_wisdom = [
            "'A'ohe hana nui ke alu 'ia - No task is too big when done together",
            "E ola mau ka 'ōlelo Hawai'i - Let Hawaiian language and culture live on",
            "Ua mau ke ea o ka 'āina i ka pono - The life of the land is perpetuated in righteousness",
            "He ali'i ka 'āina; he kauwā ke kanaka - The land is chief; man is its servant",
            "I ka 'ōlelo no ke ola, i ka 'ōlelo nō ka make - In language there is life, in language there is death"
        ]
        
        logger.info("Aloha Spirit Injector initialized")
    
    def inject_aloha(
        self,
        response: str,
        time_context: Optional[Dict[str, Any]] = None,
        conversation_stage: str = "general",
        business_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Inject aloha spirit into response
        
        Args:
            response: Original response text
            time_context: Time of day context
            conversation_stage: Stage of conversation (greeting, inquiry, closing, etc.)
            business_context: Business-specific context
        
        Returns:
            Response enhanced with aloha spirit
        """
        
        # Determine if we should add greeting (if not already present)
        if conversation_stage == "greeting" or (
            time_context and not self._has_greeting(response)
        ):
            response = self._add_greeting(response, time_context)
        
        # Add value expression if appropriate
        if random.random() < 0.3:
            response = self._add_value_expression(response, business_context)
        
        # Add contextual warmth
        if random.random() < 0.4:
            response = self._add_warmth(response, conversation_stage)
        
        # Add wisdom occasionally for depth
        if random.random() < 0.1 and conversation_stage in ["closing", "encouragement"]:
            response = self._add_wisdom(response)
        
        # Ensure proper closing
        if conversation_stage == "closing":
            response = self._ensure_warm_closing(response)
        
        return response
    
    def _has_greeting(self, text: str) -> bool:
        """Check if text already has a greeting"""
        greetings = ["aloha", "howzit", "e komo mai", "good morning", "good afternoon", "good evening"]
        return any(greeting in text.lower() for greeting in greetings)
    
    def _add_greeting(self, response: str, time_context: Optional[Dict[str, Any]]) -> str:
        """Add appropriate greeting based on time"""
        if not time_context:
            greeting = "Aloha! 🌺 "
        else:
            period = time_context.get("period", "afternoon")
            greeting = random.choice(self.aloha_expressions["greeting"][period]) + " "
        
        return greeting + response
    
    def _add_value_expression(self, response: str, business_context: Optional[Dict[str, Any]]) -> str:
        """Add Hawaiian value expression"""
        # Select appropriate value based on context
        if business_context:
            if any(word in str(business_context).lower() for word in ["sustainable", "environment", "green"]):
                value = "malama_aina"
            elif any(word in str(business_context).lower() for word in ["community", "together", "local"]):
                value = "ohana"
            elif any(word in str(business_context).lower() for word in ["unity", "partnership", "collaborate"]):
                value = "lokahi"
            else:
                value = "aloha"
        else:
            value = random.choice(list(self.value_expressions.keys()))
        
        expression = random.choice(self.value_expressions[value])
        
        # Add expression as a new sentence
        if not response.endswith("."):
            response += "."
        response += f" {expression}."
        
        return response
    
    def _add_warmth(self, response: str, conversation_stage: str) -> str:
        """Add contextual warmth based on conversation stage"""
        warmth_categories = {
            "greeting": "business_inquiry",
            "inquiry": "business_inquiry",
            "problem": "problem_solving",
            "solution": "problem_solving",
            "next": "next_steps",
            "closing": "gratitude",
            "general": random.choice(["business_inquiry", "next_steps"])
        }
        
        category = warmth_categories.get(conversation_stage, "business_inquiry")
        warmth = random.choice(self.warmth_additions[category])
        
        # Add warmth appropriately
        if "?" in response:
            # Add before the question
            parts = response.split("?", 1)
            response = parts[0] + "? " + warmth + parts[1] if len(parts) > 1 else parts[0] + "? " + warmth
        else:
            # Add at the end
            if not response.endswith("."):
                response += "."
            response += " " + warmth
        
        return response
    
    def _add_wisdom(self, response: str) -> str:
        """Add Hawaiian wisdom or proverb"""
        wisdom = random.choice(self.hawaiian_wisdom)
        
        # Add as a closing thought
        if not response.endswith("."):
            response += "."
        response += f"\n\nRemember: {wisdom}"
        
        return response
    
    def _ensure_warm_closing(self, response: str) -> str:
        """Ensure response has a warm closing"""
        # Check if already has a closing
        closing_words = ["mahalo", "aloha", "a hui hou", "malama pono"]
        if any(word in response.lower() for word in closing_words):
            return response
        
        # Add closing
        closing = random.choice(self.aloha_expressions["closing"])
        if not response.endswith("."):
            response += "."
        response += " " + closing
        
        return response
    
    def add_encouragement(self, response: str) -> str:
        """Add encouragement to response"""
        encouragement = random.choice(self.aloha_expressions["encouragement"])
        
        if not response.endswith("."):
            response += "."
        response += " " + encouragement
        
        return response
    
    def add_appreciation(self, response: str) -> str:
        """Add appreciation to response"""
        appreciation = random.choice(self.aloha_expressions["appreciation"])
        
        # Add at beginning or end based on context
        if random.random() < 0.5:
            response = appreciation + " " + response
        else:
            if not response.endswith("."):
                response += "."
            response += " " + appreciation
        
        return response