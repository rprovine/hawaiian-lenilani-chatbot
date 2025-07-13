"""
Cultural Context Models - Data models for Hawaiian cultural elements
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, time
from pydantic import BaseModel, Field
from enum import Enum


class HawaiianValue(str, Enum):
    """Core Hawaiian values"""
    ALOHA = "aloha"  # Love, affection, compassion
    OHANA = "ohana"  # Family
    MALAMA_AINA = "malama_aina"  # Care for the land
    LOKAHI = "lokahi"  # Unity, harmony
    KULEANA = "kuleana"  # Responsibility
    PONO = "pono"  # Righteousness, balance
    IMUA = "imua"  # Move forward with strength
    HAAHAA = "haahaa"  # Humility
    MAHALO = "mahalo"  # Gratitude
    MANA = "mana"  # Spiritual power


class CommunicationStyle(str, Enum):
    """Hawaiian communication styles"""
    FORMAL_PROFESSIONAL = "formal_professional"
    CASUAL_PROFESSIONAL = "casual_professional"
    LOCAL_AUTHENTIC = "local_authentic"
    PIDGIN_HEAVY = "pidgin_heavy"
    MIXED_STYLE = "mixed_style"


class TimeOfDay(str, Enum):
    """Hawaiian time periods"""
    KAKAHIAKA = "kakahiaka"  # Morning (sunrise to 10am)
    AWAKEA = "awakea"  # Late morning to afternoon (10am to 2pm)
    AUINA_LA = "auina_la"  # Late afternoon (2pm to sunset)
    AHIAHI = "ahiahi"  # Evening (sunset to 10pm)
    PO = "po"  # Night (10pm to sunrise)


class CulturalGreeting(BaseModel):
    """Hawaiian cultural greeting"""
    time_of_day: TimeOfDay
    hawaiian_greeting: str
    english_greeting: str
    pidgin_greeting: str
    emoji: str
    cultural_note: str


class PidginPhrase(BaseModel):
    """Hawaiian Pidgin phrase with translation"""
    pidgin: str
    standard_english: str
    context: str
    usage_notes: Optional[str] = None
    formality_level: int = Field(ge=1, le=5)  # 1=very casual, 5=professional


class CulturalContext(BaseModel):
    """Complete cultural context for interaction"""
    primary_value: HawaiianValue
    supporting_values: List[HawaiianValue] = []
    communication_style: CommunicationStyle
    time_context: TimeOfDay
    greeting: CulturalGreeting
    suggested_phrases: List[PidginPhrase] = []
    cultural_insights: List[str] = []
    business_etiquette: List[str] = []


class IslandCulture(BaseModel):
    """Island-specific cultural characteristics"""
    island_name: str
    nickname: str
    cultural_identity: str
    local_values: List[str]
    communication_patterns: List[str]
    business_customs: List[str]
    important_traditions: List[str]
    local_phrases: List[PidginPhrase]
    dos_and_donts: Dict[str, List[str]]


class CulturalEvent(BaseModel):
    """Hawaiian cultural events that impact business"""
    event_name: str
    date: Optional[datetime] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    business_impact: str
    cultural_significance: str
    appropriate_greetings: List[str]
    business_considerations: List[str]


class HawaiianWisdom(BaseModel):
    """Hawaiian proverbs and wisdom"""
    hawaiian_text: str
    english_translation: str
    literal_meaning: str
    cultural_meaning: str
    business_application: str
    appropriate_contexts: List[str]


class CulturalTone(BaseModel):
    """Tone settings for culturally appropriate communication"""
    warmth_level: int = Field(ge=1, le=10, default=8)
    formality_level: int = Field(ge=1, le=10, default=5)
    pidgin_intensity: int = Field(ge=0, le=10, default=5)
    cultural_references: int = Field(ge=0, le=10, default=7)
    emoji_usage: int = Field(ge=0, le=10, default=6)
    relationship_focus: int = Field(ge=1, le=10, default=9)
    
    def to_style_config(self) -> Dict[str, Any]:
        """Convert tone settings to style configuration"""
        return {
            "warm_greeting": self.warmth_level >= 7,
            "use_pidgin": self.pidgin_intensity >= 3,
            "heavy_pidgin": self.pidgin_intensity >= 7,
            "add_emojis": self.emoji_usage >= 5,
            "cultural_depth": self.cultural_references >= 5,
            "talk_story_mode": self.relationship_focus >= 8,
            "professional_balance": self.formality_level >= 5
        }


class CulturalBusinessProtocol(BaseModel):
    """Hawaiian business cultural protocols"""
    protocol_name: str
    description: str
    when_applicable: List[str]
    key_elements: List[str]
    common_mistakes: List[str]
    proper_approach: str
    cultural_significance: str
    business_benefits: str


class LocalBusinessEtiquette(BaseModel):
    """Local Hawaiian business etiquette guidelines"""
    situation: str
    mainland_approach: str
    hawaiian_approach: str
    key_differences: List[str]
    cultural_reasoning: str
    expected_outcomes: str
    tips_for_success: List[str]