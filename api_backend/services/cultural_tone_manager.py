"""
Cultural Tone Manager - Manages Hawaiian cultural tone and context
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import random
import pytz

from ..models.cultural_context import (
    CulturalContext, CommunicationStyle, HawaiianValue,
    TimeOfDay, CulturalGreeting, PidginPhrase, CulturalTone
)

logger = logging.getLogger(__name__)


class CulturalToneManager:
    """Manages cultural tone and context for Hawaiian business conversations"""
    
    def __init__(self):
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
        # Cultural greetings by time
        self.greetings = {
            TimeOfDay.KAKAHIAKA: CulturalGreeting(
                time_of_day=TimeOfDay.KAKAHIAKA,
                hawaiian_greeting="Aloha kakahiaka",
                english_greeting="Good morning",
                pidgin_greeting="Howzit! Early yeah?",
                emoji="🌅",
                cultural_note="Morning is sacred time in Hawaiian culture"
            ),
            TimeOfDay.AWAKEA: CulturalGreeting(
                time_of_day=TimeOfDay.AWAKEA,
                hawaiian_greeting="Aloha awakea",
                english_greeting="Good afternoon",
                pidgin_greeting="Howzit! Hot one today!",
                emoji="☀️",
                cultural_note="Midday is time for productivity and connection"
            ),
            TimeOfDay.AHIAHI: CulturalGreeting(
                time_of_day=TimeOfDay.AHIAHI,
                hawaiian_greeting="Aloha ahiahi",
                english_greeting="Good evening",
                pidgin_greeting="Howzit! Pau hana time?",
                emoji="🌙",
                cultural_note="Evening is time for family and reflection"
            )
        }
        
        # Business-appropriate pidgin phrases
        self.business_pidgin = [
            PidginPhrase(
                pidgin="We go talk story",
                standard_english="Let's discuss this",
                context="business_meeting",
                formality_level=3
            ),
            PidginPhrase(
                pidgin="Can? Shoots!",
                standard_english="Is that possible? Great!",
                context="agreement",
                formality_level=2
            ),
            PidginPhrase(
                pidgin="No worries, we figure it out",
                standard_english="Don't worry, we'll find a solution",
                context="problem_solving",
                formality_level=3
            ),
            PidginPhrase(
                pidgin="Da kine technology",
                standard_english="This type of technology",
                context="explanation",
                formality_level=2
            )
        ]
        
        logger.info("Cultural Tone Manager initialized")
    
    def get_current_time_of_day(self) -> TimeOfDay:
        """Get current Hawaiian time of day"""
        hawaii_time = datetime.now(self.hawaii_tz)
        hour = hawaii_time.hour
        
        if 5 <= hour < 10:
            return TimeOfDay.KAKAHIAKA
        elif 10 <= hour < 14:
            return TimeOfDay.AWAKEA
        elif 14 <= hour < 18:
            return TimeOfDay.AUINA_LA
        elif 18 <= hour < 22:
            return TimeOfDay.AHIAHI
        else:
            return TimeOfDay.PO
    
    def get_cultural_context(
        self,
        business_type: Optional[str] = None,
        island: Optional[str] = None,
        communication_preference: str = "mixed"
    ) -> CulturalContext:
        """Build complete cultural context"""
        
        time_of_day = self.get_current_time_of_day()
        
        # Select primary value based on context
        if business_type == "agriculture":
            primary_value = HawaiianValue.MALAMA_AINA
        elif business_type == "tourism":
            primary_value = HawaiianValue.ALOHA
        else:
            primary_value = HawaiianValue.OHANA
        
        # Build supporting values
        supporting_values = [
            HawaiianValue.LOKAHI,
            HawaiianValue.KULEANA
        ]
        
        # Determine communication style
        if communication_preference == "professional":
            comm_style = CommunicationStyle.FORMAL_PROFESSIONAL
        elif communication_preference == "local":
            comm_style = CommunicationStyle.LOCAL_AUTHENTIC
        else:
            comm_style = CommunicationStyle.MIXED_STYLE
        
        # Get appropriate greeting
        greeting = self.greetings.get(
            time_of_day,
            self.greetings[TimeOfDay.AWAKEA]
        )
        
        # Build cultural insights
        insights = self._get_cultural_insights(business_type, island)
        
        # Build business etiquette
        etiquette = self._get_business_etiquette(business_type)
        
        return CulturalContext(
            primary_value=primary_value,
            supporting_values=supporting_values,
            communication_style=comm_style,
            time_context=time_of_day,
            greeting=greeting,
            suggested_phrases=random.sample(self.business_pidgin, min(3, len(self.business_pidgin))),
            cultural_insights=insights,
            business_etiquette=etiquette
        )
    
    def enhance_response(
        self,
        response: str,
        cultural_context: CulturalContext,
        tone_settings: Optional[CulturalTone] = None
    ) -> str:
        """Enhance response with cultural elements"""
        
        if not tone_settings:
            tone_settings = CulturalTone()
        
        style_config = tone_settings.to_style_config()
        
        # Add greeting if not present
        if style_config["warm_greeting"] and not self._has_greeting(response):
            greeting = cultural_context.greeting
            if style_config["use_pidgin"]:
                response = f"{greeting.pidgin_greeting} {response}"
            else:
                response = f"{greeting.hawaiian_greeting}! {response}"
        
        # Add cultural value reference
        if style_config["cultural_depth"]:
            value_phrase = self._get_value_phrase(cultural_context.primary_value)
            if random.random() < 0.3:
                response += f" {value_phrase}"
        
        # Add emoji if appropriate
        if style_config["add_emojis"]:
            response = self._add_contextual_emoji(response, cultural_context)
        
        return response
    
    def _has_greeting(self, text: str) -> bool:
        """Check if text has greeting"""
        greetings = ["aloha", "howzit", "hello", "hi", "good morning", "good afternoon", "good evening"]
        return any(g in text.lower() for g in greetings)
    
    def _get_value_phrase(self, value: HawaiianValue) -> str:
        """Get phrase for Hawaiian value"""
        phrases = {
            HawaiianValue.ALOHA: "With aloha always.",
            HawaiianValue.OHANA: "Your business is our ohana.",
            HawaiianValue.MALAMA_AINA: "Caring for our islands together.",
            HawaiianValue.LOKAHI: "Working in harmony.",
            HawaiianValue.KULEANA: "We take our responsibility seriously.",
            HawaiianValue.PONO: "Doing what's right for Hawaii."
        }
        return phrases.get(value, "Mahalo!")
    
    def _add_contextual_emoji(
        self,
        text: str,
        context: CulturalContext
    ) -> str:
        """Add contextually appropriate emoji"""
        # Don't add if already has emoji
        if any(char in text for char in "🌺🌴🤙🌊🏝️🌈"):
            return text
        
        # Add based on context
        if "mahalo" in text.lower():
            text += " 🙏"
        elif "aloha" in text.lower():
            text += " 🌺"
        elif any(word in text.lower() for word in ["beach", "ocean", "surf"]):
            text += " 🌊"
        elif context.primary_value == HawaiianValue.MALAMA_AINA:
            text += " 🌱"
        elif random.random() < 0.3:
            text += " 🤙"
        
        return text
    
    def _get_cultural_insights(
        self,
        business_type: Optional[str],
        island: Optional[str]
    ) -> List[str]:
        """Get relevant cultural insights"""
        insights = []
        
        if business_type == "tourism":
            insights.extend([
                "Visitors appreciate authentic cultural experiences",
                "Respect for local customs attracts repeat visitors",
                "Japanese visitors value exceptional service and attention to detail"
            ])
        elif business_type == "restaurant":
            insights.extend([
                "Local customers value 'ohana-style portions and service",
                "Farm-to-table resonates with malama 'aina values",
                "Multi-generational dining is common in Hawaii"
            ])
        elif business_type == "agriculture":
            insights.extend([
                "Traditional Hawaiian farming practices inspire modern sustainability",
                "Community-supported agriculture thrives in island culture",
                "Respect for the 'aina is fundamental to success"
            ])
        
        if island == "maui":
            insights.append("Maui's 'no ka oi' (the best) spirit drives excellence")
        elif island == "big_island":
            insights.append("Big Island's diverse microclimates offer unique opportunities")
        elif island == "kauai":
            insights.append("Kauai's garden isle identity emphasizes natural beauty")
        
        return insights[:3]
    
    def _get_business_etiquette(
        self,
        business_type: Optional[str]
    ) -> List[str]:
        """Get business etiquette tips"""
        general_etiquette = [
            "Build relationships before discussing business",
            "Show respect for local culture and traditions",
            "Be patient - island time values relationships over rushing",
            "Include family in business discussions when appropriate"
        ]
        
        if business_type == "tourism":
            general_etiquette.append("Educate visitors about cultural sensitivity")
        elif business_type == "restaurant":
            general_etiquette.append("Accommodate multi-generational dining preferences")
        
        return general_etiquette[:4]
    
    def get_business_cultural_notes(
        self,
        business_type: str,
        island: str
    ) -> List[str]:
        """Get specific cultural notes for business type and island"""
        notes = []
        
        # Business-specific notes
        business_notes = {
            "tourism": [
                "Emphasize authentic cultural experiences over commercialization",
                "Train staff in basic Hawaiian language and customs",
                "Partner with local cultural practitioners"
            ],
            "restaurant": [
                "Source ingredients locally to support island farmers",
                "Offer 'ohana-style (family) portions",
                "Create gathering spaces for talk story"
            ],
            "agriculture": [
                "Practice sustainable farming that honors the 'aina",
                "Share harvest with community (Hawaiian tradition)",
                "Educate visitors about Hawaiian agriculture"
            ],
            "retail": [
                "Feature local artisans and products prominently",
                "Support other local businesses through partnerships",
                "Create community gathering opportunities"
            ]
        }
        
        # Island-specific notes
        island_notes = {
            "oahu": [
                "Balance serving locals and tourists in urban areas",
                "Navigate high competition with aloha spirit",
                "Leverage diverse cultural communities"
            ],
            "maui": [
                "Cater to luxury market while maintaining local values",
                "Respect water conservation efforts",
                "Connect with upcountry and coastal communities"
            ],
            "big_island": [
                "Work with diverse microclimates and communities",
                "Respect volcanic and cultural sacred sites",
                "Bridge Hilo and Kona side differences"
            ],
            "kauai": [
                "Maintain small-town feel in business approach",
                "Prioritize environmental protection",
                "Build strong community relationships"
            ]
        }
        
        # Combine notes
        if business_type in business_notes:
            notes.extend(business_notes[business_type])
        
        if island in island_notes:
            notes.extend(island_notes[island])
        
        # Add general cultural notes
        notes.extend([
            "Success in Hawaii requires genuine community integration",
            "Relationships and trust are valued over quick transactions",
            "Contributing to community wellbeing ensures business longevity"
        ])
        
        return notes[:5]  # Return top 5 most relevant notes