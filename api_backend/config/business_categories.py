"""
Hawaiian Business Categories Configuration
Launch strategy focused on high-impact categories
"""

HAWAIIAN_BUSINESS_CATEGORIES = {
    "tourism_hospitality": {
        "display_name": "Tourism & Hospitality",
        "icon": "🏨",
        "description": "Hotels, tours, activities, vacation rentals",
        "subcategories": [
            "Hotels & Resorts",
            "Activity/Tour Operators",
            "Vacation Rental Managers",
            "Transportation Services"
        ],
        "ai_solutions": [
            "Seasonal booking optimization",
            "Multi-language customer service", 
            "Weather-based recommendations",
            "Dynamic pricing strategies"
        ],
        "pain_points": [
            "Seasonal fluctuations",
            "Language barriers (Japanese/Korean)",
            "Mainland competition",
            "Weather dependency"
        ],
        "typical_roi": "25-40% booking improvement",
        "project_range": "$8,000-$20,000",
        "success_story": "One Maui activity operator increased bookings 35% with our seasonal prediction AI",
        "hook": "Optimize for both kamaaina and malihini with AI that understands Hawaii tourism patterns"
    },
    "restaurants_food": {
        "display_name": "Restaurants & Food Service",
        "icon": "🍽️",
        "description": "Local restaurants, food trucks, catering",
        "subcategories": [
            "Local Hawaiian Restaurants",
            "Food Trucks",
            "Catering Services",
            "Farm-to-Table Operations"
        ],
        "ai_solutions": [
            "Local vs. tourist optimization",
            "Inventory management", 
            "Multi-language ordering",
            "Cultural menu recommendations"
        ],
        "pain_points": [
            "Food waste",
            "Local vs tourist preferences",
            "Supply chain challenges",
            "Competition with chains"
        ],
        "typical_roi": "30% waste reduction, 20% order increase",
        "project_range": "$5,000-$12,000",
        "success_story": "Local restaurant reduced food waste 30% and increased local customer orders 25%",
        "hook": "Serve your community better while competing with mainland chains"
    },
    "agriculture_farming": {
        "display_name": "Agriculture & Farming",
        "icon": "🌱",
        "description": "Coffee farms, traditional crops, sustainable farming",
        "subcategories": [
            "Coffee Farms",
            "Traditional Hawaiian Crops",
            "Macadamia Nut Operations",
            "Sustainable/Organic Farms"
        ],
        "ai_solutions": [
            "Crop yield prediction",
            "Irrigation optimization",
            "Market timing analysis",
            "Sustainable practice tracking"
        ],
        "pain_points": [
            "Weather unpredictability",
            "Market timing",
            "Resource optimization",
            "Sustainable practices"
        ],
        "typical_roi": "15-25% yield improvement",
        "project_range": "$6,000-$15,000",
        "success_story": "Big Island coffee farm improved yield 20% while reducing water usage 35%",
        "hook": "Malama 'aina with smart farming technology that respects traditional practices"
    },
    "local_retail": {
        "display_name": "Local Retail & Hawaiian Products",
        "icon": "🏪",
        "description": "Hawaiian products, local markets, specialty stores",
        "subcategories": [
            "Hawaiian Product Stores",
            "Local Markets/Co-ops",
            "Surf/Ocean Sports Retailers",
            "Community Gift Shops"
        ],
        "ai_solutions": [
            "Customer segmentation",
            "Inventory optimization",
            "Cultural storytelling",
            "Loyalty programs"
        ],
        "pain_points": [
            "Amazon competition",
            "Inventory management",
            "Customer loyalty",
            "Cultural authenticity"
        ],
        "typical_roi": "20% local customer retention increase",
        "project_range": "$2,000-$8,000",
        "success_story": "Hawaiian product store increased local customer retention 40% with cultural AI recommendations",
        "hook": "Beat Amazon with AI that understands local customers and Hawaiian culture"
    }
}

# Phase 2 Categories (for future expansion)
PHASE_2_CATEGORIES = {
    "real_estate": {
        "display_name": "Real Estate & Property Management",
        "icon": "🏠",
        "timeline": "3-6 months"
    },
    "healthcare_wellness": {
        "display_name": "Healthcare & Wellness",
        "icon": "🏥",
        "timeline": "3-6 months"
    },
    "professional_services": {
        "display_name": "Professional Services",
        "icon": "💼",
        "timeline": "3-6 months"
    }
}

# Quick category selection for chatbot
CATEGORY_QUICK_SELECT = [
    "🏨 Tourism & Hospitality",
    "🍽️ Restaurants & Food Service",
    "🌱 Agriculture & Farming",
    "🏪 Local Retail & Products",
    "🏢 Other Business Type"
]

# Island-specific category strengths
ISLAND_CATEGORY_FOCUS = {
    "oahu": ["tourism_hospitality", "restaurants_food", "local_retail"],
    "maui": ["tourism_hospitality", "agriculture_farming", "restaurants_food"],
    "big_island": ["agriculture_farming", "tourism_hospitality", "local_retail"],
    "kauai": ["tourism_hospitality", "agriculture_farming", "local_retail"],
    "molokai": ["agriculture_farming", "local_retail"],
    "lanai": ["tourism_hospitality", "agriculture_farming"]
}