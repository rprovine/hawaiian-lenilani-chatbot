"""
Island Business Intelligence - Hawaiian island-specific business insights
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

from ..models.hawaiian_business import (
    Island, BusinessType, ServiceType, BusinessInquiry,
    ServiceRecommendation, IslandInsight, BusinessChallenge
)

logger = logging.getLogger(__name__)


class IslandBusinessIntelligence:
    """Provides island-specific business intelligence for Hawaiian businesses"""
    
    def __init__(self):
        # Island-specific market data
        self.island_data = {
            Island.OAHU: {
                "population": 1016508,
                "visitor_count_annual": 5000000,
                "key_industries": ["Tourism", "Military", "Healthcare", "Technology", "Real Estate"],
                "business_density": "high",
                "competition_level": "very_high",
                "avg_commercial_rent": "$35-50/sqft",
                "tourism_seasons": {
                    "peak": ["June-August", "December-January"],
                    "shoulder": ["April-May", "September-November"],
                    "low": ["February-March"]
                },
                "unique_challenges": [
                    "High cost of living and doing business",
                    "Traffic congestion affecting logistics",
                    "Intense competition from mainland chains",
                    "Limited affordable commercial space"
                ],
                "opportunities": [
                    "Large local population for year-round business",
                    "Military contracts and federal opportunities",
                    "Tech hub development in Kakaako",
                    "International business gateway"
                ]
            },
            Island.MAUI: {
                "population": 167417,
                "visitor_count_annual": 3000000,
                "key_industries": ["Tourism", "Agriculture", "Real Estate", "Renewable Energy"],
                "business_density": "medium",
                "competition_level": "high",
                "avg_commercial_rent": "$25-40/sqft",
                "tourism_seasons": {
                    "peak": ["December-April", "June-August"],
                    "shoulder": ["May", "September-November"],
                    "low": ["October-November"]
                },
                "unique_challenges": [
                    "Seasonal tourism fluctuations",
                    "Water usage restrictions",
                    "Limited local workforce",
                    "High dependency on tourism"
                ],
                "opportunities": [
                    "Luxury tourism market",
                    "Agritourism potential",
                    "Renewable energy initiatives",
                    "Wedding and events industry"
                ]
            },
            Island.BIG_ISLAND: {
                "population": 200000,
                "visitor_count_annual": 1800000,
                "key_industries": ["Agriculture", "Tourism", "Astronomy", "Energy"],
                "business_density": "low",
                "competition_level": "medium",
                "avg_commercial_rent": "$15-25/sqft",
                "tourism_seasons": {
                    "peak": ["December-March", "July-August"],
                    "shoulder": ["April-June", "September-November"],
                    "low": ["May", "September"]
                },
                "unique_challenges": [
                    "Geographic size and logistics",
                    "Limited infrastructure in some areas",
                    "Natural disaster risks (volcanic, earthquake)",
                    "Split market between Hilo and Kona"
                ],
                "opportunities": [
                    "Agricultural innovation and exports",
                    "Astronomy and research facilities",
                    "Geothermal and renewable energy",
                    "Eco-tourism and adventure tourism"
                ]
            },
            Island.KAUAI: {
                "population": 73298,
                "visitor_count_annual": 1300000,
                "key_industries": ["Tourism", "Agriculture", "Film Production"],
                "business_density": "low",
                "competition_level": "low",
                "avg_commercial_rent": "$20-30/sqft",
                "tourism_seasons": {
                    "peak": ["December-March", "June-August"],
                    "shoulder": ["April-May", "September-November"],
                    "low": ["October-November"]
                },
                "unique_challenges": [
                    "Small market size",
                    "Limited development due to regulations",
                    "Transportation and shipping costs",
                    "Workforce availability"
                ],
                "opportunities": [
                    "Eco-tourism leadership",
                    "Film and media production",
                    "Sustainable agriculture",
                    "Wellness and retreat market"
                ]
            }
        }
        
        # Business type insights
        self.business_insights = {
            BusinessType.TOURISM: {
                "market_trends": [
                    "Shift towards experiential and cultural tourism",
                    "Growing demand for sustainable tourism",
                    "Increase in remote work + vacation travelers",
                    "Multi-generational travel trending up"
                ],
                "technology_needs": [
                    "Online booking optimization",
                    "Multi-language support systems",
                    "Dynamic pricing algorithms",
                    "Customer experience analytics"
                ],
                "success_factors": [
                    "Authentic cultural experiences",
                    "Strong online presence and reviews",
                    "Sustainable practices certification",
                    "Local community integration"
                ]
            },
            BusinessType.RESTAURANT: {
                "market_trends": [
                    "Farm-to-table movement strong in Hawaii",
                    "Fusion cuisine popularity",
                    "Ghost kitchens and delivery growth",
                    "Health-conscious options demand"
                ],
                "technology_needs": [
                    "POS systems with local tax handling",
                    "Inventory management for imports",
                    "Online ordering platforms",
                    "Customer loyalty programs"
                ],
                "success_factors": [
                    "Local ingredient sourcing",
                    "Multi-generational appeal",
                    "Efficient operations for high rent",
                    "Strong local following"
                ]
            },
            BusinessType.AGRICULTURE: {
                "market_trends": [
                    "Increased demand for local produce",
                    "Agritourism opportunities growing",
                    "Export market development",
                    "Sustainable farming practices valued"
                ],
                "technology_needs": [
                    "Precision agriculture tools",
                    "Supply chain management",
                    "Direct-to-consumer platforms",
                    "Weather and climate monitoring"
                ],
                "success_factors": [
                    "Water conservation practices",
                    "Diversified crop portfolio",
                    "Value-added products",
                    "Community supported agriculture"
                ]
            }
        }
        
        logger.info("Island Business Intelligence initialized")
    
    def get_island_insights(
        self,
        island: str,
        business_type: Optional[str] = None
    ) -> IslandInsight:
        """Get comprehensive insights for specific island"""
        
        island_enum = Island(island.lower())
        island_info = self.island_data.get(island_enum, {})
        
        if not island_info:
            raise ValueError(f"No data available for island: {island}")
        
        # Build market conditions
        market_conditions = {
            "population": f"{island_info['population']:,} residents",
            "annual_visitors": f"{island_info['visitor_count_annual']:,} visitors",
            "competition": island_info['competition_level'],
            "commercial_rent": island_info['avg_commercial_rent'],
            "business_density": island_info['business_density']
        }
        
        # Get seasonal patterns
        seasonal_patterns = island_info['tourism_seasons']
        
        # Cultural considerations
        cultural_considerations = [
            "Build genuine relationships with local community",
            "Respect Hawaiian cultural sites and practices",
            "Support other local businesses",
            "Participate in community events and giving"
        ]
        
        # Add island-specific cultural notes
        if island_enum == Island.OAHU:
            cultural_considerations.append("Balance urban efficiency with aloha spirit")
        elif island_enum == Island.MAUI:
            cultural_considerations.append("Embrace 'Maui no ka oi' excellence standard")
        elif island_enum == Island.BIG_ISLAND:
            cultural_considerations.append("Respect Pele and volcanic cultural significance")
        elif island_enum == Island.KAUAI:
            cultural_considerations.append("Maintain harmony with Garden Isle nature")
        
        return IslandInsight(
            island=island_enum,
            market_conditions=market_conditions,
            opportunities=island_info['opportunities'],
            challenges=island_info['unique_challenges'],
            competitive_landscape=f"{island_info['competition_level']} competition",
            seasonal_patterns=seasonal_patterns,
            cultural_considerations=cultural_considerations,
            success_factors=self._get_island_success_factors(island_enum, business_type)
        )
    
    def generate_recommendations(
        self,
        inquiry: BusinessInquiry,
        island_insights: IslandInsight
    ) -> List[ServiceRecommendation]:
        """Generate service recommendations based on business inquiry"""
        
        recommendations = []
        
        # Map business type to relevant services
        service_mapping = {
            BusinessType.TOURISM: [
                ServiceType.TOURISM_ANALYTICS,
                ServiceType.CUSTOM_CHATBOT,
                ServiceType.HUBSPOT_INTEGRATION
            ],
            BusinessType.RESTAURANT: [
                ServiceType.RESTAURANT_AI,
                ServiceType.DATA_ANALYTICS,
                ServiceType.CUSTOM_CHATBOT
            ],
            BusinessType.AGRICULTURE: [
                ServiceType.AGRICULTURE_TECH,
                ServiceType.DATA_ANALYTICS,
                ServiceType.FRACTIONAL_CTO
            ],
            BusinessType.RETAIL: [
                ServiceType.RETAIL_AI,
                ServiceType.DATA_ANALYTICS,
                ServiceType.HUBSPOT_INTEGRATION
            ]
        }
        
        # Get relevant services
        relevant_services = service_mapping.get(
            inquiry.business_type,
            [ServiceType.DATA_ANALYTICS, ServiceType.FRACTIONAL_CTO]
        )
        
        # Generate recommendations for each service
        for service_type in relevant_services:
            recommendation = self._create_service_recommendation(
                service_type,
                inquiry,
                island_insights
            )
            recommendations.append(recommendation)
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _create_service_recommendation(
        self,
        service_type: ServiceType,
        inquiry: BusinessInquiry,
        island_insights: IslandInsight
    ) -> ServiceRecommendation:
        """Create detailed service recommendation"""
        
        # Service details
        service_details = {
            ServiceType.TOURISM_ANALYTICS: {
                "name": "Tourism Analytics & Optimization",
                "description": "AI-powered analytics for Hawaiian tourism businesses",
                "roi": "25-40% booking increase",
                "time": "3-8 weeks",
                "price": "$8,000-$25,000"
            },
            ServiceType.RESTAURANT_AI: {
                "name": "Restaurant AI System",
                "description": "Smart restaurant management for local and tourist markets",
                "roi": "30% waste reduction, 20% order increase",
                "time": "2-6 weeks",
                "price": "$5,000-$15,000"
            },
            ServiceType.AGRICULTURE_TECH: {
                "name": "Agricultural Technology Solutions",
                "description": "IoT and AI for sustainable Hawaiian agriculture",
                "roi": "15-25% yield improvement",
                "time": "4-12 weeks",
                "price": "$10,000-$30,000"
            },
            ServiceType.RETAIL_AI: {
                "name": "Retail AI Competition Edge",
                "description": "Compete with mainland chains using local advantages",
                "roi": "20% customer retention increase",
                "time": "2-6 weeks",
                "price": "$3,000-$12,000"
            },
            ServiceType.FRACTIONAL_CTO: {
                "name": "Fractional CTO Services",
                "description": "Part-time technology leadership for Hawaiian businesses",
                "roi": "50% technology cost optimization",
                "time": "Ongoing",
                "price": "$175-$350/hour"
            },
            ServiceType.CUSTOM_CHATBOT: {
                "name": "Custom Hawaiian Chatbot",
                "description": "Multi-language chatbot with cultural awareness",
                "roi": "60% customer service efficiency",
                "time": "4-8 weeks",
                "price": "$5,000-$20,000"
            },
            ServiceType.DATA_ANALYTICS: {
                "name": "Hawaiian Business Data Analytics",
                "description": "Data-driven insights for island businesses",
                "roi": "30% better decision making",
                "time": "2-6 weeks",
                "price": "$3,000-$15,000"
            },
            ServiceType.HUBSPOT_INTEGRATION: {
                "name": "HubSpot CRM Integration",
                "description": "Marketing automation for Hawaiian businesses",
                "roi": "40% marketing efficiency",
                "time": "2-4 weeks",
                "price": "$2,000-$8,000"
            }
        }
        
        details = service_details[service_type]
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(
            service_type,
            inquiry,
            island_insights
        )
        
        # Get local examples
        local_examples = self._get_local_examples(
            service_type,
            inquiry.island,
            inquiry.business_type
        )
        
        # Why recommended
        why_recommended = self._get_recommendation_reasons(
            service_type,
            inquiry,
            island_insights
        )
        
        # Cultural fit
        cultural_fit = self._assess_cultural_fit(
            service_type,
            inquiry.business_type
        )
        
        return ServiceRecommendation(
            service_type=service_type,
            service_name=details["name"],
            description=details["description"],
            relevance_score=relevance_score,
            estimated_roi=details["roi"],
            implementation_time=details["time"],
            price_range=details["price"],
            local_examples=local_examples,
            why_recommended=why_recommended,
            cultural_fit=cultural_fit
        )
    
    def _calculate_relevance_score(
        self,
        service_type: ServiceType,
        inquiry: BusinessInquiry,
        island_insights: IslandInsight
    ) -> float:
        """Calculate relevance score for service recommendation"""
        
        score = 0.5  # Base score
        
        # Boost for matching challenges
        challenge_keywords = {
            ServiceType.TOURISM_ANALYTICS: ["seasonal", "visitor", "booking", "competition"],
            ServiceType.RESTAURANT_AI: ["inventory", "waste", "customer", "efficiency"],
            ServiceType.AGRICULTURE_TECH: ["yield", "sustainable", "monitor", "climate"],
            ServiceType.RETAIL_AI: ["competition", "mainland", "customer", "inventory"],
            ServiceType.FRACTIONAL_CTO: ["technology", "leadership", "strategy", "growth"]
        }
        
        service_keywords = challenge_keywords.get(service_type, [])
        for challenge in inquiry.challenges:
            if any(keyword in challenge.lower() for keyword in service_keywords):
                score += 0.1
        
        # Boost for island fit
        if inquiry.island == Island.OAHU and service_type in [
            ServiceType.FRACTIONAL_CTO,
            ServiceType.RETAIL_AI
        ]:
            score += 0.1
        elif inquiry.island == Island.MAUI and service_type == ServiceType.TOURISM_ANALYTICS:
            score += 0.15
        elif inquiry.island == Island.BIG_ISLAND and service_type == ServiceType.AGRICULTURE_TECH:
            score += 0.15
        
        # Budget considerations
        if inquiry.budget_range:
            # Add budget matching logic
            score += 0.05
        
        # Timeline urgency
        if inquiry.timeline == "asap":
            score += 0.05
        
        return min(score, 1.0)
    
    def _get_local_examples(
        self,
        service_type: ServiceType,
        island: Island,
        business_type: BusinessType
    ) -> List[str]:
        """Get local business examples (anonymized)"""
        
        examples = {
            ServiceType.TOURISM_ANALYTICS: [
                f"Maui adventure tour operator increased bookings 35% in shoulder season",
                f"Oahu cultural tour company optimized Japanese market messaging",
                f"Big Island helicopter tours reduced no-shows by 40%"
            ],
            ServiceType.RESTAURANT_AI: [
                f"Kauai farm-to-table restaurant reduced waste by 30%",
                f"Oahu poke shop chain optimized inventory across 5 locations",
                f"Maui beachfront restaurant improved table turnover 25%"
            ],
            ServiceType.AGRICULTURE_TECH: [
                f"Kona coffee farm increased yield 20% with precision irrigation",
                f"Maui tropical fruit farm reduced water usage 35%",
                f"Oahu vertical farm optimized growing cycles"
            ]
        }
        
        return examples.get(service_type, ["Multiple Hawaiian businesses seeing success"])[:2]
    
    def _get_recommendation_reasons(
        self,
        service_type: ServiceType,
        inquiry: BusinessInquiry,
        island_insights: IslandInsight
    ) -> List[str]:
        """Get specific reasons for recommendation"""
        
        reasons = []
        
        # Challenge-based reasons
        for challenge in inquiry.challenges[:2]:
            if "competition" in challenge.lower():
                reasons.append(f"Addresses your challenge: {challenge}")
            elif "seasonal" in challenge.lower():
                reasons.append("Helps manage seasonal fluctuations")
        
        # Island-specific reasons
        if inquiry.island == Island.OAHU:
            reasons.append("Perfect for Oahu's competitive market")
        elif inquiry.island == Island.MAUI:
            reasons.append("Ideal for Maui's tourism-dependent economy")
        
        # Service-specific benefits
        service_benefits = {
            ServiceType.TOURISM_ANALYTICS: "Understand visitor patterns unique to Hawaii",
            ServiceType.RESTAURANT_AI: "Optimize for local and tourist preferences",
            ServiceType.AGRICULTURE_TECH: "Support sustainable island agriculture",
            ServiceType.FRACTIONAL_CTO: "Get Silicon Valley expertise with local understanding"
        }
        
        if service_type in service_benefits:
            reasons.append(service_benefits[service_type])
        
        return reasons[:3]
    
    def _assess_cultural_fit(
        self,
        service_type: ServiceType,
        business_type: BusinessType
    ) -> str:
        """Assess cultural fit of service"""
        
        cultural_assessments = {
            ServiceType.TOURISM_ANALYTICS: "Helps preserve authentic experiences while optimizing business",
            ServiceType.RESTAURANT_AI: "Maintains 'ohana hospitality while improving efficiency",
            ServiceType.AGRICULTURE_TECH: "Supports malama 'aina through sustainable technology",
            ServiceType.RETAIL_AI: "Strengthens local business against mainland competition",
            ServiceType.FRACTIONAL_CTO: "Brings global expertise with local cultural sensitivity"
        }
        
        return cultural_assessments.get(
            service_type,
            "Aligns with Hawaiian values of innovation and tradition"
        )
    
    def _get_island_success_factors(
        self,
        island: Island,
        business_type: Optional[str]
    ) -> List[str]:
        """Get success factors for island and business type"""
        
        general_factors = [
            "Strong community relationships and local partnerships",
            "Authentic integration of Hawaiian culture",
            "Sustainable business practices",
            "Excellent customer service with aloha spirit"
        ]
        
        # Island-specific factors
        if island == Island.OAHU:
            general_factors.extend([
                "Efficient operations to handle high volume",
                "Strong online presence for visibility"
            ])
        elif island == Island.MAUI:
            general_factors.extend([
                "Luxury service standards",
                "Environmental consciousness"
            ])
        elif island == Island.BIG_ISLAND:
            general_factors.extend([
                "Adaptability to diverse markets",
                "Innovation in traditional industries"
            ])
        elif island == Island.KAUAI:
            general_factors.extend([
                "Eco-friendly practices",
                "Small business agility"
            ])
        
        return general_factors[:5]
    
    def get_top_opportunities(self, island: str) -> List[str]:
        """Get top business opportunities for island"""
        island_enum = Island(island.lower())
        island_info = self.island_data.get(island_enum, {})
        return island_info.get("opportunities", [])[:3]
    
    def get_success_stories(self, island: str) -> List[Dict[str, str]]:
        """Get success stories for island (anonymized)"""
        
        # This would connect to a database of real stories
        # For now, return sample stories
        stories = [
            {
                "business_type": "Tourism",
                "challenge": "Seasonal booking fluctuations",
                "solution": "AI-powered dynamic pricing and marketing",
                "result": "35% increase in shoulder season bookings",
                "testimonial": "The insights helped us understand our Japanese visitors better!"
            },
            {
                "business_type": "Restaurant",
                "challenge": "High food waste and inventory costs",
                "solution": "Smart inventory management system",
                "result": "30% reduction in waste, 20% cost savings",
                "testimonial": "Now we can focus on cooking great food, not worrying about waste!"
            }
        ]
        
        return stories