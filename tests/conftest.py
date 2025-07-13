"""
Pytest configuration and shared fixtures for Hawaiian LeniLani Chatbot tests
"""

import pytest
import os
import sys
from unittest.mock import Mock, AsyncMock
from datetime import datetime
import pytz

# Add project directories to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Rasa removed - Claude-only implementation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api_backend')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'claude_integration')))


@pytest.fixture
def hawaii_timezone():
    """Hawaii Standard Time timezone"""
    return pytz.timezone('Pacific/Honolulu')


@pytest.fixture
def mock_datetime_hst(hawaii_timezone):
    """Mock datetime in Hawaii Standard Time"""
    def _mock_datetime(year, month, day, hour, minute=0):
        return datetime(year, month, day, hour, minute, tzinfo=hawaii_timezone)
    return _mock_datetime


@pytest.fixture
def sample_chat_message():
    """Sample chat message for testing"""
    return {
        "message": "Aloha! I need help with my restaurant on Maui",
        "session_id": "test_session_123",
        "metadata": {
            "source": "widget",
            "page": "homepage",
            "timestamp": datetime.now().isoformat()
        }
    }


@pytest.fixture
def sample_business_lead():
    """Sample business lead data"""
    return {
        "session_id": "test_session_123",
        "email": "keoni@mauigrindz.com",
        "name": "Keoni Nakamura",
        "company_name": "Maui Grindz Restaurant",
        "phone": "808-555-1234",
        "island": "maui",
        "business_type": "restaurant",
        "business_size": "10-50",
        "challenges": ["online presence", "customer retention", "local marketing"],
        "timeline": "1-3 months",
        "budget_range": "$5000-$10000",
        "preferred_contact": "email"
    }


# Rasa fixtures removed - Claude-only implementation


@pytest.fixture
def mock_claude_client():
    """Mock Anthropic Claude client"""
    client = Mock()
    
    # Mock message creation
    mock_response = Mock()
    mock_response.content = [
        Mock(text="Aloha! I understand you need help with your business. Let's talk story about how we can support your success while staying true to Hawaiian values.")
    ]
    
    client.messages.create = AsyncMock(return_value=mock_response)
    return client


@pytest.fixture
def mock_database_session():
    """Mock database session"""
    session = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    session.query = Mock()
    session.close = Mock()
    return session


@pytest.fixture
def mock_redis_client():
    """Mock Redis client"""
    redis = Mock()
    redis.get = Mock(return_value=None)
    redis.set = Mock(return_value=True)
    redis.setex = Mock(return_value=True)
    redis.delete = Mock(return_value=1)
    redis.exists = Mock(return_value=False)
    return redis


@pytest.fixture
def island_business_contexts():
    """Island-specific business contexts for testing"""
    return {
        'oahu': {
            'population': 1016508,
            'key_industries': ['tourism', 'military', 'technology', 'healthcare'],
            'business_characteristics': 'urban, diverse, competitive'
        },
        'maui': {
            'population': 164221,
            'key_industries': ['tourism', 'agriculture', 'retail'],
            'business_characteristics': 'tourist-focused, seasonal, luxury'
        },
        'big_island': {
            'population': 200629,
            'key_industries': ['agriculture', 'astronomy', 'tourism'],
            'business_characteristics': 'diverse geography, agricultural, scientific'
        },
        'kauai': {
            'population': 73298,
            'key_industries': ['tourism', 'agriculture', 'film'],
            'business_characteristics': 'eco-focused, limited development, natural'
        },
        'molokai': {
            'population': 7345,
            'key_industries': ['subsistence', 'cultural_tourism'],
            'business_characteristics': 'traditional, small-scale, community-focused'
        },
        'lanai': {
            'population': 3135,
            'key_industries': ['luxury_tourism', 'technology'],
            'business_characteristics': 'exclusive, tech-forward, luxury'
        }
    }


@pytest.fixture
def hawaiian_greetings():
    """Time-based Hawaiian greetings"""
    return {
        'morning': ['Aloha kakahiaka!', 'Good morning!'],
        'midday': ['Aloha awakea!', 'Good day!'],
        'afternoon': ["Aloha 'auinalā!", 'Good afternoon!'],
        'evening': ['Aloha ahiahi!', 'Good evening!'],
        'night': ['Aloha pō!', 'Good night!']
    }


@pytest.fixture
def pidgin_phrases():
    """Common Hawaiian Pidgin phrases for testing"""
    return {
        'greetings': ['howzit', 'eh brah', 'aloha'],
        'affirmatives': ['shoots', 'rajah', 'can'],
        'negatives': ['no can', 'no way', 'cannot'],
        'questions': ['yeah?', 'or what?', 'how you stay?'],
        'expressions': ['da kine', 'stay', 'pau', 'broke da mouth', 'ono']
    }


@pytest.fixture
def business_challenges():
    """Common Hawaiian business challenges"""
    return {
        'tourism': [
            'seasonal fluctuations',
            'online booking systems',
            'competition from mainland chains',
            'finding local workforce',
            'sustainable practices'
        ],
        'restaurant': [
            'high food costs',
            'labor shortage',
            'local vs tourist pricing',
            'online presence',
            'delivery logistics'
        ],
        'agriculture': [
            'export regulations',
            'shipping costs',
            'weather dependency',
            'sustainable farming',
            'market access'
        ],
        'retail': [
            'online competition',
            'inventory shipping',
            'seasonal tourism',
            'local customer base',
            'high rent costs'
        ]
    }


# Environment setup
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Set up test environment variables"""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("TZ", "Pacific/Honolulu")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/15")