#!/usr/bin/env python3
"""
Test script for business categories integration
"""
import asyncio
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_backend.services.hawaiian_conversation_router import HawaiianConversationRouter
from api_backend.config.business_categories import HAWAIIAN_BUSINESS_CATEGORIES, CATEGORY_QUICK_SELECT

async def test_category_integration():
    """Test business category integration"""
    print("🌺 Testing Hawaiian Business Categories Integration")
    print("=" * 50)
    
    # Show available categories
    print("\n📊 Available Business Categories:")
    for key, info in HAWAIIAN_BUSINESS_CATEGORIES.items():
        print(f"\n{info['icon']} {info['display_name']}:")
        print(f"   - Project Range: {info['project_range']}")
        print(f"   - Typical ROI: {info['typical_roi']}")
        print(f"   - Success Story: {info['success_story'][:50]}...")
    
    print("\n🔍 Quick Select Options:")
    for option in CATEGORY_QUICK_SELECT:
        print(f"   {option}")
    
    # Test conversation router
    print("\n💬 Testing Conversation Router:")
    router = HawaiianConversationRouter()
    
    # Test messages
    test_messages = [
        ("Aloha! I run a restaurant on Maui", "restaurant_context"),
        ("I have a coffee farm on Big Island", "agriculture_context"),
        ("We operate tours in Oahu", "tourism_context"),
        ("I have a local retail store in Kauai", "retail_context")
    ]
    
    for message, test_name in test_messages:
        print(f"\n🧪 Test: {test_name}")
        print(f"📝 Message: {message}")
        
        try:
            response = await router.route_message(
                user_message=message,
                session_id=f"test_{test_name}"
            )
            
            print(f"✅ Response: {response['response'][:150]}...")
            
            # Check if category was detected
            session = router._get_or_create_session(f"test_{test_name}", None)
            if 'business_category' in session.get('business_context', {}):
                print(f"📊 Detected Category: {session['business_context']['business_category']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n✅ Category integration test complete!")

if __name__ == "__main__":
    asyncio.run(test_category_integration())