"""
Hawaiian Business Models - Data models for Hawaiian business entities
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class Island(str, Enum):
    """Hawaiian islands enum"""
    OAHU = "oahu"
    MAUI = "maui"
    BIG_ISLAND = "big_island"
    KAUAI = "kauai"
    MOLOKAI = "molokai"
    LANAI = "lanai"


class BusinessType(str, Enum):
    """Hawaiian business types"""
    TOURISM = "tourism"
    RESTAURANT = "restaurant"
    AGRICULTURE = "agriculture"
    RETAIL = "retail"
    HOSPITALITY = "hospitality"
    TECHNOLOGY = "technology"
    REAL_ESTATE = "real_estate"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    OTHER = "other"


class ServiceType(str, Enum):
    """LeniLani service types"""
    TOURISM_ANALYTICS = "tourism_analytics"
    RESTAURANT_AI = "restaurant_ai"
    AGRICULTURE_TECH = "agriculture_tech"
    RETAIL_AI = "retail_ai"
    FRACTIONAL_CTO = "fractional_cto"
    CUSTOM_CHATBOT = "custom_chatbot"
    DATA_ANALYTICS = "data_analytics"
    HUBSPOT_INTEGRATION = "hubspot_integration"


class BudgetRange(str, Enum):
    """Budget ranges"""
    UNDER_5K = "under_5k"
    FIVE_TO_10K = "5k_to_10k"
    TEN_TO_20K = "10k_to_20k"
    TWENTY_TO_50K = "20k_to_50k"
    OVER_50K = "over_50k"
    FLEXIBLE = "flexible"


class Timeline(str, Enum):
    """Project timeline urgency"""
    ASAP = "asap"
    WITHIN_MONTH = "within_month"
    WITHIN_QUARTER = "within_quarter"
    WITHIN_6_MONTHS = "within_6_months"
    FLEXIBLE = "flexible"


class BusinessChallenge(BaseModel):
    """Hawaiian business challenge"""
    category: str
    description: str
    impact_level: str = Field(default="medium", pattern="^(low|medium|high)$")
    island_specific: bool = False


class ContactInfo(BaseModel):
    """Contact information"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    preferred_contact_method: Optional[str] = Field(default="email", pattern="^(email|phone|text)$")
    best_time_to_contact: Optional[str] = None


class BusinessInquiry(BaseModel):
    """Hawaiian business inquiry model"""
    business_type: BusinessType
    island: Island
    company_name: Optional[str] = None
    challenges: List[str]
    current_solutions: Optional[List[str]] = []
    budget_range: Optional[BudgetRange] = None
    timeline: Optional[Timeline] = None
    number_of_employees: Optional[str] = None
    annual_revenue: Optional[str] = None
    contact_info: Optional[ContactInfo] = None
    additional_notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ServiceRecommendation(BaseModel):
    """Service recommendation for Hawaiian business"""
    service_type: ServiceType
    service_name: str
    description: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    estimated_roi: str
    implementation_time: str
    price_range: str
    local_examples: List[str] = []
    why_recommended: List[str] = []
    cultural_fit: str


class IslandInsight(BaseModel):
    """Island-specific business insight"""
    island: Island
    market_conditions: Dict[str, str]
    opportunities: List[str]
    challenges: List[str]
    competitive_landscape: str
    seasonal_patterns: Dict[str, str]
    cultural_considerations: List[str]
    success_factors: List[str]


class HawaiianBusinessResponse(BaseModel):
    """Comprehensive response for Hawaiian business inquiry"""
    inquiry_id: str = Field(default_factory=lambda: f"INQ-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    recommendations: List[ServiceRecommendation]
    island_insights: IslandInsight
    estimated_total_investment: str
    implementation_roadmap: List[Dict[str, str]]
    expected_outcomes: List[str]
    local_references: List[Dict[str, str]] = []
    cultural_notes: List[str]
    next_steps: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationState(BaseModel):
    """Track conversation state for Hawaiian business chat"""
    session_id: str
    user_id: Optional[str] = None
    current_intent: Optional[str] = None
    business_context: Optional[BusinessInquiry] = None
    conversation_stage: str = Field(default="greeting", pattern="^(greeting|qualification|recommendation|scheduling|closing)$")
    messages_count: int = 0
    cultural_mode: str = Field(default="authentic", pattern="^(authentic|professional|mixed)$")
    language_preference: str = Field(default="english", pattern="^(english|pidgin|mixed)$")
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}


class HawaiianBusinessMetrics(BaseModel):
    """Metrics for Hawaiian business performance"""
    metric_type: str
    value: float
    unit: str
    period: str
    comparison_to_average: float
    island_benchmark: float
    trend: str = Field(pattern="^(up|down|stable)$")
    insights: List[str]


class LocalPartnership(BaseModel):
    """Local Hawaiian business partnership opportunity"""
    partner_type: str
    partner_name: str
    island: Island
    partnership_benefits: List[str]
    cultural_alignment: str
    contact_method: str
    introduction_available: bool = False