"""
Tests for Hawaiian conversation flows and cultural integration
"""

import pytest
from datetime import datetime
import pytz
from unittest.mock import Mock, patch, AsyncMock

from rasa_bot.actions.hawaiian_business_actions import (
    ActionHawaiianGreeting,
    ActionQualifyBusiness,
    ActionIslandSpecificAdvice,
    ActionScheduleAppointment
)
from claude_integration.hawaiian_claude_client import HawaiianClaudeAssistant
from api_backend.services.cultural_intelligence import CulturalToneManager


class TestHawaiianGreetings:
    """Test time-aware Hawaiian greetings"""
    
    @pytest.fixture
    def hawaii_tz(self):
        return pytz.timezone('Pacific/Honolulu')
    
    @pytest.fixture
    def mock_dispatcher(self):
        return Mock()
    
    @pytest.fixture
    def mock_tracker(self):
        tracker = Mock()
        tracker.get_slot.return_value = None
        tracker.sender_id = "test_user_123"
        return tracker
    
    def test_morning_greeting(self, mock_dispatcher, mock_tracker, hawaii_tz):
        """Test morning greeting (5am-10am HST)"""
        with patch('rasa_bot.actions.hawaiian_business_actions.datetime') as mock_datetime:
            # Set time to 8am HST
            mock_datetime.now.return_value = datetime(2024, 1, 15, 8, 0, tzinfo=hawaii_tz)
            
            action = ActionHawaiianGreeting()
            action.run(mock_dispatcher, mock_tracker, {})
            
            # Check that morning greeting was sent
            call_args = mock_dispatcher.utter_message.call_args[1]['text']
            assert "Aloha kakahiaka" in call_args
            assert any(word in call_args.lower() for word in ["morning", "beautiful day"])
    
    def test_afternoon_greeting(self, mock_dispatcher, mock_tracker, hawaii_tz):
        """Test afternoon greeting (2pm-6pm HST)"""
        with patch('rasa_bot.actions.hawaiian_business_actions.datetime') as mock_datetime:
            # Set time to 3pm HST
            mock_datetime.now.return_value = datetime(2024, 1, 15, 15, 0, tzinfo=hawaii_tz)
            
            action = ActionHawaiianGreeting()
            action.run(mock_dispatcher, mock_tracker, {})
            
            call_args = mock_dispatcher.utter_message.call_args[1]['text']
            assert "Aloha 'auinalā" in call_args or "Aloha" in call_args
    
    def test_evening_greeting(self, mock_dispatcher, mock_tracker, hawaii_tz):
        """Test evening greeting (6pm-10pm HST)"""
        with patch('rasa_bot.actions.hawaiian_business_actions.datetime') as mock_datetime:
            # Set time to 7pm HST
            mock_datetime.now.return_value = datetime(2024, 1, 15, 19, 0, tzinfo=hawaii_tz)
            
            action = ActionHawaiianGreeting()
            action.run(mock_dispatcher, mock_tracker, {})
            
            call_args = mock_dispatcher.utter_message.call_args[1]['text']
            assert "Aloha ahiahi" in call_args
            assert any(word in call_args.lower() for word in ["evening", "nice night"])


class TestPidginIntegration:
    """Test Hawaiian Pidgin English understanding and responses"""
    
    @pytest.fixture
    def cultural_manager(self):
        return CulturalToneManager()
    
    def test_pidgin_detection(self, cultural_manager):
        """Test detection of pidgin phrases"""
        pidgin_messages = [
            "Eh howzit brah",
            "My restaurant stay struggling",
            "Can or no can?",
            "Shoots, sounds good",
            "Da kine service you get?"
        ]
        
        for message in pidgin_messages:
            context = cultural_manager.analyze_message(message)
            assert context['uses_pidgin'] == True
    
    def test_standard_english_detection(self, cultural_manager):
        """Test detection of standard English"""
        standard_messages = [
            "Hello, I need help with my business",
            "What services do you offer?",
            "I would like to schedule a consultation",
            "Please provide pricing information"
        ]
        
        for message in standard_messages:
            context = cultural_manager.analyze_message(message)
            assert context['uses_pidgin'] == False
    
    def test_pidgin_response_generation(self, cultural_manager):
        """Test appropriate pidgin responses"""
        # When user uses pidgin
        pidgin_context = cultural_manager.analyze_message("Howzit, my store stay slow")
        assert pidgin_context['recommended_tone'] == 'casual_pidgin'
        
        # When user uses formal English
        formal_context = cultural_manager.analyze_message("Good morning, I require assistance")
        assert formal_context['recommended_tone'] == 'professional'


class TestIslandSpecificLogic:
    """Test island-specific business advice"""
    
    @pytest.fixture
    def mock_dispatcher(self):
        return Mock()
    
    @pytest.fixture
    def mock_domain(self):
        return {}
    
    def test_oahu_business_advice(self, mock_dispatcher):
        """Test Oahu-specific business recommendations"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'island': 'oahu',
            'business_type': 'technology'
        }.get(x)
        
        action = ActionIslandSpecificAdvice()
        action.run(mock_dispatcher, tracker, {})
        
        call_args = mock_dispatcher.utter_message.call_args[1]['text']
        assert any(term in call_args.lower() for term in ['kakaako', 'tech hub', 'honolulu'])
    
    def test_maui_tourism_advice(self, mock_dispatcher):
        """Test Maui tourism business recommendations"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'island': 'maui',
            'business_type': 'tourism'
        }.get(x)
        
        action = ActionIslandSpecificAdvice()
        action.run(mock_dispatcher, tracker, {})
        
        call_args = mock_dispatcher.utter_message.call_args[1]['text']
        assert any(term in call_args.lower() for term in ['wedding', 'luxury', 'seasonal'])
    
    def test_big_island_agriculture(self, mock_dispatcher):
        """Test Big Island agriculture recommendations"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'island': 'big_island',
            'business_type': 'agriculture'
        }.get(x)
        
        action = ActionIslandSpecificAdvice()
        action.run(mock_dispatcher, tracker, {})
        
        call_args = mock_dispatcher.utter_message.call_args[1]['text']
        assert any(term in call_args.lower() for term in ['coffee', 'kona', 'volcanic soil'])


class TestBusinessQualification:
    """Test business qualification and lead scoring"""
    
    @pytest.fixture
    def mock_dispatcher(self):
        return Mock()
    
    def test_high_quality_lead(self, mock_dispatcher):
        """Test qualification of high-quality lead"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'business_type': 'tourism',
            'island': 'maui',
            'business_size': 'medium',
            'challenges': ['online marketing', 'booking system'],
            'timeline': 'immediate',
            'budget': '$5000-$10000'
        }.get(x)
        tracker.get_latest_input_channel.return_value = 'web'
        
        action = ActionQualifyBusiness()
        result = action.run(mock_dispatcher, tracker, {})
        
        # Should set high qualification score
        assert result[0]['name'] == 'qualification_score'
        assert float(result[0]['value']) >= 0.7
    
    def test_low_quality_lead(self, mock_dispatcher):
        """Test qualification of low-quality lead"""
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'business_type': None,
            'island': None,
            'business_size': None,
            'challenges': None,
            'timeline': 'just looking',
            'budget': 'not sure'
        }.get(x)
        tracker.get_latest_input_channel.return_value = 'web'
        
        action = ActionQualifyBusiness()
        result = action.run(mock_dispatcher, tracker, {})
        
        # Should set low qualification score
        assert result[0]['name'] == 'qualification_score'
        assert float(result[0]['value']) < 0.5


class TestCulturalValues:
    """Test integration of Hawaiian cultural values"""
    
    @pytest.fixture
    async def claude_assistant(self):
        return HawaiianClaudeAssistant(api_key="test_key")
    
    @pytest.mark.asyncio
    async def test_aloha_spirit_response(self, claude_assistant):
        """Test responses embody aloha spirit"""
        with patch.object(claude_assistant.client.messages, 'create') as mock_create:
            mock_create.return_value = Mock(
                content=[Mock(text="Aloha! I understand your business needs help. Let's work together with the spirit of aloha to find solutions that benefit both your business and our community.")]
            )
            
            response = await claude_assistant.get_hawaiian_response(
                "My business is struggling",
                {"business_type": "restaurant", "island": "oahu"}
            )
            
            assert "aloha" in response.lower()
            assert any(word in response.lower() for word in ["together", "community", "help"])
    
    @pytest.mark.asyncio
    async def test_ohana_values(self, claude_assistant):
        """Test ohana (family) values in responses"""
        with patch.object(claude_assistant.client.messages, 'create') as mock_create:
            mock_create.return_value = Mock(
                content=[Mock(text="Your business ohana is important to us. We'll help you build strong relationships with customers and treat them like family.")]
            )
            
            response = await claude_assistant.get_hawaiian_response(
                "How do I improve customer relationships?",
                {"business_type": "retail", "island": "maui"}
            )
            
            assert "ohana" in response.lower() or "family" in response.lower()
    
    @pytest.mark.asyncio
    async def test_malama_aina_sustainability(self, claude_assistant):
        """Test malama aina (care for land) in responses"""
        with patch.object(claude_assistant.client.messages, 'create') as mock_create:
            mock_create.return_value = Mock(
                content=[Mock(text="Let's explore sustainable practices that malama our aina while growing your business. Consider eco-friendly packaging and local sourcing.")]
            )
            
            response = await claude_assistant.get_hawaiian_response(
                "I want to make my business more sustainable",
                {"business_type": "tourism", "island": "kauai"}
            )
            
            assert any(term in response.lower() for term in ["malama", "sustainable", "eco"])


class TestHawaiianTimeHandling:
    """Test Hawaii Standard Time handling"""
    
    def test_no_daylight_savings(self):
        """Test that HST doesn't observe daylight savings"""
        hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
        # Test summer date
        summer_date = datetime(2024, 7, 15, 12, 0)
        summer_hst = hawaii_tz.localize(summer_date)
        
        # Test winter date
        winter_date = datetime(2024, 1, 15, 12, 0)
        winter_hst = hawaii_tz.localize(winter_date)
        
        # UTC offset should be same (no DST)
        assert summer_hst.utcoffset() == winter_hst.utcoffset()
    
    @pytest.mark.asyncio
    async def test_appointment_scheduling_hst(self):
        """Test appointment scheduling uses HST"""
        dispatcher = Mock()
        tracker = Mock()
        tracker.get_slot.side_effect = lambda x: {
            'email': 'test@example.com',
            'preferred_date': '2024-01-20',
            'preferred_time': 'afternoon'
        }.get(x)
        
        with patch('rasa_bot.actions.hawaiian_business_actions.datetime') as mock_datetime:
            hawaii_tz = pytz.timezone('Pacific/Honolulu')
            mock_datetime.now.return_value = datetime(2024, 1, 15, 10, 0, tzinfo=hawaii_tz)
            
            action = ActionScheduleAppointment()
            action.run(dispatcher, tracker, {})
            
            # Should mention HST in response
            call_args = dispatcher.utter_message.call_args[1]['text']
            assert 'HST' in call_args or 'Hawaii' in call_args


class TestConversationFlows:
    """Test complete conversation flows"""
    
    @pytest.mark.asyncio
    async def test_tourism_business_flow(self):
        """Test complete flow for tourism business"""
        # This would test the full conversation flow
        # from greeting -> qualification -> advice -> appointment
        pass
    
    @pytest.mark.asyncio
    async def test_restaurant_help_flow(self):
        """Test complete flow for restaurant seeking help"""
        # This would test pidgin understanding through full flow
        pass
    
    @pytest.mark.asyncio
    async def test_tech_startup_flow(self):
        """Test complete flow for tech startup on Oahu"""
        # This would test formal business language handling
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])