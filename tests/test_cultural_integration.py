"""
Tests for Hawaiian cultural integration and authenticity
"""

import pytest
from unittest.mock import Mock, patch
import json

from api_backend.services.cultural_intelligence import CulturalToneManager
from claude_integration.cultural_prompts import (
    HAWAIIAN_VALUES,
    PIDGIN_PHRASES,
    ISLAND_BUSINESS_CONTEXT,
    get_cultural_prompt
)


class TestCulturalAuthenticity:
    """Test Hawaiian cultural elements are properly integrated"""
    
    def test_hawaiian_values_present(self):
        """Test all core Hawaiian values are defined"""
        required_values = ['aloha', 'ohana', 'malama_aina', 'kokua', 'pono', 'lokahi']
        
        for value in required_values:
            assert value in HAWAIIAN_VALUES
            assert 'description' in HAWAIIAN_VALUES[value]
            assert 'business_application' in HAWAIIAN_VALUES[value]
    
    def test_pidgin_phrases_authentic(self):
        """Test pidgin phrases are authentic and appropriate"""
        # Check common pidgin phrases exist
        expected_phrases = [
            'howzit', 'shoots', 'rajah', 'da kine', 'pau', 
            'grindz', 'ono', 'talk story', 'no worry'
        ]
        
        pidgin_list = [phrase.lower() for phrase in PIDGIN_PHRASES]
        for phrase in expected_phrases:
            assert any(phrase in p for p in pidgin_list)
    
    def test_no_offensive_content(self):
        """Test no offensive or inappropriate cultural content"""
        # List of terms that should not appear
        inappropriate_terms = [
            'hula girl', 'grass skirt', 'tiki', 'hawaiian time',
            'lazy', 'primitive', 'savage'
        ]
        
        all_content = str(HAWAIIAN_VALUES) + str(PIDGIN_PHRASES) + str(ISLAND_BUSINESS_CONTEXT)
        
        for term in inappropriate_terms:
            assert term.lower() not in all_content.lower()


class TestIslandKnowledge:
    """Test island-specific business knowledge"""
    
    def test_all_islands_covered(self):
        """Test all six main Hawaiian islands are included"""
        expected_islands = ['oahu', 'maui', 'big_island', 'kauai', 'molokai', 'lanai']
        
        for island in expected_islands:
            assert island in ISLAND_BUSINESS_CONTEXT
            assert 'characteristics' in ISLAND_BUSINESS_CONTEXT[island]
            assert 'key_industries' in ISLAND_BUSINESS_CONTEXT[island]
            assert 'business_tips' in ISLAND_BUSINESS_CONTEXT[island]
    
    def test_island_characteristics_accurate(self):
        """Test island characteristics are accurate"""
        # Oahu should mention urban/city
        assert any(term in ISLAND_BUSINESS_CONTEXT['oahu']['characteristics'].lower() 
                  for term in ['urban', 'city', 'honolulu'])
        
        # Maui should mention tourism
        assert 'tourism' in ISLAND_BUSINESS_CONTEXT['maui']['characteristics'].lower()
        
        # Big Island should mention size/diverse
        assert any(term in ISLAND_BUSINESS_CONTEXT['big_island']['characteristics'].lower()
                  for term in ['largest', 'diverse', 'volcano'])
        
        # Kauai should mention garden/nature
        assert any(term in ISLAND_BUSINESS_CONTEXT['kauai']['characteristics'].lower()
                  for term in ['garden', 'natural', 'pristine'])


class TestCulturalToneManager:
    """Test the cultural tone management system"""
    
    @pytest.fixture
    def tone_manager(self):
        return CulturalToneManager()
    
    def test_pidgin_detection_accuracy(self, tone_manager):
        """Test accurate detection of pidgin vs standard English"""
        pidgin_examples = [
            ("Eh brah, howzit?", True),
            ("My store stay busy today", True),
            ("Can can or no can?", True),
            ("Good morning, how are you?", False),
            ("I would like to schedule a meeting", False),
            ("Da kine service real good", True)
        ]
        
        for text, expected_pidgin in pidgin_examples:
            result = tone_manager.analyze_message(text)
            assert result['uses_pidgin'] == expected_pidgin
    
    def test_cultural_keywords_detection(self, tone_manager):
        """Test detection of cultural keywords"""
        messages_with_culture = [
            "Need help with my ohana business",
            "Want to malama our aina",
            "Looking for pono business practices",
            "How to show aloha to customers"
        ]
        
        for message in messages_with_culture:
            result = tone_manager.analyze_message(message)
            assert len(result['cultural_elements']) > 0
    
    def test_formality_detection(self, tone_manager):
        """Test detection of conversation formality"""
        formal_messages = [
            "Good afternoon, I would like to inquire about your services",
            "Please provide information regarding consulting fees",
            "I am interested in scheduling a professional consultation"
        ]
        
        casual_messages = [
            "hey whats up",
            "need some help with my biz",
            "yo can you kokua?"
        ]
        
        for message in formal_messages:
            result = tone_manager.analyze_message(message)
            assert result['formality'] == 'formal'
        
        for message in casual_messages:
            result = tone_manager.analyze_message(message)
            assert result['formality'] == 'casual'


class TestCulturalPromptGeneration:
    """Test cultural prompt generation for Claude"""
    
    def test_morning_prompt_includes_greeting(self):
        """Test morning context includes appropriate greeting"""
        context = {
            'time_of_day': 'morning',
            'island': 'maui',
            'uses_pidgin': False
        }
        
        prompt = get_cultural_prompt(context)
        assert 'kakahiaka' in prompt or 'morning' in prompt.lower()
    
    def test_pidgin_context_prompt(self):
        """Test pidgin context generates appropriate prompt"""
        context = {
            'uses_pidgin': True,
            'island': 'oahu',
            'business_type': 'restaurant'
        }
        
        prompt = get_cultural_prompt(context)
        assert any(term in prompt.lower() for term in ['pidgin', 'local', 'casual'])
    
    def test_island_specific_prompt(self):
        """Test island-specific context in prompts"""
        islands = ['oahu', 'maui', 'big_island', 'kauai', 'molokai', 'lanai']
        
        for island in islands:
            context = {'island': island}
            prompt = get_cultural_prompt(context)
            assert island in prompt.lower()


class TestBusinessTypeUnderstanding:
    """Test understanding of Hawaiian business types"""
    
    def test_tourism_business_keywords(self):
        """Test recognition of tourism-related businesses"""
        tourism_keywords = [
            'hotel', 'resort', 'tour', 'activities', 'luau',
            'snorkel', 'dive', 'surf', 'vacation rental'
        ]
        
        manager = CulturalToneManager()
        for keyword in tourism_keywords:
            result = manager.analyze_message(f"I have a {keyword} business")
            assert result['business_context']['type'] == 'tourism'
    
    def test_restaurant_business_keywords(self):
        """Test recognition of restaurant businesses"""
        restaurant_keywords = [
            'restaurant', 'cafe', 'food truck', 'catering',
            'plate lunch', 'poke', 'shave ice'
        ]
        
        manager = CulturalToneManager()
        for keyword in restaurant_keywords:
            result = manager.analyze_message(f"I run a {keyword}")
            assert result['business_context']['type'] == 'restaurant'
    
    def test_agriculture_business_keywords(self):
        """Test recognition of agriculture businesses"""
        agriculture_keywords = [
            'farm', 'ranch', 'taro', 'coffee', 'macadamia',
            'tropical fruit', 'organic', 'aquaculture'
        ]
        
        manager = CulturalToneManager()
        for keyword in agriculture_keywords:
            result = manager.analyze_message(f"We have a {keyword} operation")
            assert result['business_context']['type'] == 'agriculture'


class TestTimeZoneHandling:
    """Test proper Hawaii Standard Time handling"""
    
    def test_hst_no_daylight_savings(self):
        """Test HST doesn't change for daylight savings"""
        import pytz
        from datetime import datetime
        
        hst = pytz.timezone('Pacific/Honolulu')
        
        # Summer date
        summer = hst.localize(datetime(2024, 7, 1, 12, 0))
        # Winter date  
        winter = hst.localize(datetime(2024, 1, 1, 12, 0))
        
        # Offset should be same (no DST in Hawaii)
        assert summer.utcoffset() == winter.utcoffset()
        assert str(summer.utcoffset()) == '-10:00:00'
    
    def test_time_based_greetings(self):
        """Test appropriate greetings for different times"""
        manager = CulturalToneManager()
        
        # Mock different times
        times = [
            (6, 'morning'),
            (11, 'day'),
            (15, 'afternoon'),
            (19, 'evening'),
            (23, 'night')
        ]
        
        for hour, expected_period in times:
            with patch('api_backend.services.cultural_intelligence.datetime') as mock_dt:
                mock_dt.now.return_value.hour = hour
                context = manager.get_cultural_context()
                assert expected_period in context['time_of_day']


class TestCulturalSensitivity:
    """Test cultural sensitivity in responses"""
    
    def test_sacred_sites_respect(self):
        """Test respectful handling of sacred sites"""
        sacred_sites = [
            'mauna kea', 'diamond head', 'leahi', 'iolani palace',
            'haleakala', 'waimea canyon'
        ]
        
        manager = CulturalToneManager()
        for site in sacred_sites:
            result = manager.analyze_message(f"I want to build near {site}")
            assert result.get('requires_cultural_sensitivity', False) == True
    
    def test_cultural_appropriation_detection(self):
        """Test detection of potential cultural appropriation"""
        sensitive_phrases = [
            "tiki bar theme",
            "hula girl decorations",
            "fake hawaiian ceremony",
            "tropical paradise theme"
        ]
        
        manager = CulturalToneManager()
        for phrase in sensitive_phrases:
            result = manager.analyze_message(f"I want to create a {phrase}")
            assert result.get('cultural_warning', False) == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])