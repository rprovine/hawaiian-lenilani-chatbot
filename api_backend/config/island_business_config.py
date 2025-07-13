"""
Island Business Configuration - Business-specific configuration for Hawaiian islands
"""

ISLAND_BUSINESS_CONFIG = {
    "services": {
        "tourism_analytics": {
            "name": "Tourism Analytics & Optimization",
            "description": "AI-powered analytics specifically designed for Hawaiian tourism businesses",
            "features": [
                "Seasonal visitor pattern analysis",
                "Multi-market segmentation (Japan, US Mainland, Europe)",
                "Weather impact correlation",
                "Competitive pricing intelligence",
                "Cultural event calendar integration"
            ],
            "deliverables": [
                "Custom analytics dashboard",
                "Weekly performance reports",
                "Predictive booking models",
                "Marketing optimization recommendations",
                "ROI tracking system"
            ],
            "pricing": {
                "starter": "$8,000 - $12,000",
                "professional": "$12,000 - $20,000",
                "enterprise": "$20,000 - $40,000"
            },
            "timeline": "3-8 weeks",
            "ideal_clients": [
                "Tour operators",
                "Activity providers",
                "Hotels and resorts",
                "Vacation rentals",
                "Transportation services"
            ]
        },
        "restaurant_ai": {
            "name": "Restaurant AI System",
            "description": "Smart restaurant management for Hawaiian food service businesses",
            "features": [
                "Local vs tourist preference tracking",
                "Multi-language ordering support",
                "Inventory optimization for island supply chains",
                "Plate waste reduction analytics",
                "Peak time staffing recommendations"
            ],
            "deliverables": [
                "POS integration",
                "Inventory management system",
                "Customer preference profiles",
                "Waste tracking dashboard",
                "Staff scheduling optimizer"
            ],
            "pricing": {
                "food_truck": "$5,000 - $8,000",
                "single_location": "$8,000 - $15,000",
                "multi_location": "$15,000 - $30,000"
            },
            "timeline": "2-6 weeks",
            "ideal_clients": [
                "Local restaurants",
                "Food trucks",
                "Resort restaurants",
                "Catering services",
                "Plate lunch shops"
            ]
        },
        "agriculture_tech": {
            "name": "Agricultural Technology Solutions",
            "description": "IoT and AI solutions for sustainable Hawaiian agriculture",
            "features": [
                "Microclimate monitoring",
                "Water usage optimization",
                "Crop yield prediction",
                "Pest and disease early warning",
                "Market demand forecasting"
            ],
            "deliverables": [
                "IoT sensor network",
                "Mobile monitoring app",
                "Automated irrigation controls",
                "Harvest optimization calendar",
                "Market price integration"
            ],
            "pricing": {
                "small_farm": "$10,000 - $20,000",
                "medium_operation": "$20,000 - $40,000",
                "large_estate": "$40,000+"
            },
            "timeline": "4-12 weeks",
            "ideal_clients": [
                "Coffee farms",
                "Tropical fruit growers",
                "Macadamia nut farms",
                "Taro farmers",
                "Organic producers"
            ]
        },
        "retail_ai": {
            "name": "Local Retail AI Solutions",
            "description": "Help local retailers compete with mainland chains",
            "features": [
                "Customer segmentation (local vs visitor)",
                "Inventory optimization",
                "Local product storytelling",
                "Community engagement tools",
                "Price competitiveness analysis"
            ],
            "deliverables": [
                "Customer analytics platform",
                "Inventory management system",
                "Marketing automation",
                "Loyalty program",
                "Performance dashboards"
            ],
            "pricing": {
                "single_store": "$3,000 - $8,000",
                "small_chain": "$8,000 - $15,000",
                "regional": "$15,000+"
            },
            "timeline": "2-6 weeks",
            "ideal_clients": [
                "Local boutiques",
                "Hawaiian product stores",
                "Surf shops",
                "Art galleries",
                "Farmers markets"
            ]
        },
        "fractional_cto": {
            "name": "Fractional CTO Services",
            "description": "Part-time technology leadership with Hawaiian market expertise",
            "features": [
                "Technology strategy development",
                "Vendor management",
                "Digital transformation planning",
                "Team building and training",
                "Island-specific solutions"
            ],
            "deliverables": [
                "Technology roadmap",
                "System architecture",
                "Vendor negotiations",
                "Team development plan",
                "Monthly progress reports"
            ],
            "pricing": {
                "advisory": "$2,000 - $4,000/month",
                "hands_on": "$4,000 - $8,000/month",
                "intensive": "$8,000+/month"
            },
            "timeline": "Ongoing",
            "ideal_clients": [
                "Growing startups",
                "Established businesses modernizing",
                "Companies expanding to Hawaii",
                "Digital transformation projects"
            ]
        }
    },
    
    "islands": {
        "oahu": {
            "business_environment": {
                "strengths": [
                    "Largest population and customer base",
                    "Most developed infrastructure",
                    "International business connections",
                    "Diverse economy"
                ],
                "challenges": [
                    "Highest competition",
                    "Expensive real estate",
                    "Traffic and logistics",
                    "Parking limitations"
                ],
                "opportunities": [
                    "Government contracts",
                    "Tech sector growth",
                    "International tourism",
                    "Military market"
                ]
            },
            "key_business_areas": {
                "honolulu": "Urban center, government, finance",
                "waikiki": "Tourism central",
                "kakaako": "Tech and innovation hub",
                "pearl_city": "Military-adjacent businesses",
                "north_shore": "Surf culture and eco-tourism",
                "kailua": "Upscale residential and boutique"
            },
            "market_insights": {
                "tourism_ratio": "60% mainland, 30% Japan, 10% other",
                "peak_seasons": "Summer and December-January",
                "local_preferences": "Efficiency with aloha",
                "price_sensitivity": "Medium-high due to competition"
            }
        },
        "maui": {
            "business_environment": {
                "strengths": [
                    "High-end tourism market",
                    "Strong wedding/event industry",
                    "Agricultural diversity",
                    "Luxury brand presence"
                ],
                "challenges": [
                    "Seasonal fluctuations",
                    "Limited workforce",
                    "High cost of living",
                    "Water restrictions"
                ],
                "opportunities": [
                    "Eco-luxury tourism",
                    "Agritourism",
                    "Renewable energy",
                    "Wellness retreats"
                ]
            },
            "key_business_areas": {
                "lahaina": "Historic town, tourist hub",
                "kihei": "Affordable tourism, local community",
                "wailea": "Luxury resorts and high-end retail",
                "paia": "Bohemian, windsurfing culture",
                "upcountry": "Agriculture, artisanal products",
                "hana": "Remote, exclusive tourism"
            },
            "market_insights": {
                "tourism_ratio": "70% mainland, 20% international, 10% local",
                "peak_seasons": "Winter (whale season) and summer",
                "local_preferences": "Quality over quantity",
                "price_sensitivity": "Low for luxury, high for local"
            }
        },
        "big_island": {
            "business_environment": {
                "strengths": [
                    "Diverse agriculture",
                    "Lower costs than other islands",
                    "Space for expansion",
                    "Unique volcanic tourism"
                ],
                "challenges": [
                    "Large geographic area",
                    "Split markets (Hilo/Kona)",
                    "Infrastructure limitations",
                    "Natural disaster risks"
                ],
                "opportunities": [
                    "Agricultural exports",
                    "Astronomy tourism",
                    "Renewable energy",
                    "Adventure tourism"
                ]
            },
            "key_business_areas": {
                "kailua_kona": "Tourism, coffee country",
                "hilo": "Local community, university town",
                "waimea": "Ranching, cooler climate",
                "volcano": "National park tourism",
                "pahoa": "Alternative lifestyle, lower costs",
                "waikoloa": "Resort area"
            },
            "market_insights": {
                "tourism_ratio": "80% mainland, 15% international, 5% local",
                "peak_seasons": "Winter and coffee harvest season",
                "local_preferences": "Self-sufficiency valued",
                "price_sensitivity": "High for locals, varies for tourists"
            }
        },
        "kauai": {
            "business_environment": {
                "strengths": [
                    "Pristine natural beauty",
                    "Strong environmental ethics",
                    "Tight-knit community",
                    "Film industry presence"
                ],
                "challenges": [
                    "Small market size",
                    "Limited development allowed",
                    "Single-road infrastructure",
                    "Weather impacts"
                ],
                "opportunities": [
                    "Eco-tourism leadership",
                    "Sustainable agriculture",
                    "Wellness tourism",
                    "Artisanal products"
                ]
            },
            "key_business_areas": {
                "lihue": "Commercial center, airport",
                "kapaa": "Local community, small business",
                "princeville": "Luxury resort area",
                "poipu": "Tourist beaches and resorts",
                "hanalei": "Boutique tourism, surfing",
                "waimea": "Historic town, local focus"
            },
            "market_insights": {
                "tourism_ratio": "85% mainland, 10% international, 5% local",
                "peak_seasons": "Summer and winter holidays",
                "local_preferences": "Environmental consciousness crucial",
                "price_sensitivity": "Medium, quality important"
            }
        }
    },
    
    "industry_insights": {
        "tourism": {
            "trends": [
                "Experiential over passive tourism",
                "Sustainability requirements increasing",
                "Multi-generational travel growth",
                "Workations and extended stays"
            ],
            "technology_adoption": "Medium-high",
            "key_metrics": [
                "Occupancy rates",
                "RevPAR (Revenue per available room)",
                "Guest satisfaction scores",
                "Repeat visitor percentage"
            ]
        },
        "hospitality": {
            "trends": [
                "Contactless service options",
                "Local experience packages",
                "Dietary restriction awareness",
                "Cultural authenticity demand"
            ],
            "technology_adoption": "Medium",
            "key_metrics": [
                "Table turnover",
                "Average check size",
                "Food cost percentage",
                "Labor efficiency"
            ]
        },
        "agriculture": {
            "trends": [
                "Organic certification value",
                "Direct-to-consumer sales",
                "Agritourism integration",
                "Climate change adaptation"
            ],
            "technology_adoption": "Low-medium",
            "key_metrics": [
                "Yield per acre",
                "Water usage efficiency",
                "Market price tracking",
                "Export percentages"
            ]
        },
        "retail": {
            "trends": [
                "Local maker movements",
                "Instagram-worthy experiences",
                "Community event hosting",
                "Subscription services"
            ],
            "technology_adoption": "Low-medium",
            "key_metrics": [
                "Sales per square foot",
                "Customer acquisition cost",
                "Inventory turnover",
                "Local vs tourist sales ratio"
            ]
        }
    }
}