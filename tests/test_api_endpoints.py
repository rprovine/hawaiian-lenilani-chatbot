"""
Tests for FastAPI endpoints and API functionality
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import json
from datetime import datetime

from api_backend.main import app
from api_backend.models import ChatMessage, ChatResponse, BusinessLead


class TestAPIEndpoints:
    """Test FastAPI endpoints"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def valid_chat_message(self):
        return {
            "message": "Aloha! I need help with my restaurant",
            "session_id": "test_session_123",
            "metadata": {
                "source": "widget",
                "page": "homepage"
            }
        }
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "aloha" in data["message"].lower()
        assert "timestamp" in data
    
    def test_chat_endpoint_success(self, client, valid_chat_message):
        """Test successful chat interaction"""
        with patch('api_backend.main.conversation_router.route_message') as mock_route:
            mock_route.return_value = {
                "response": "Aloha! I'd love to help with your restaurant. What kind of food do you serve?",
                "intent": "business_help",
                "confidence": 0.95,
                "quick_replies": ["Local cuisine", "Seafood", "International", "Food truck"]
            }
            
            response = client.post("/chat", json=valid_chat_message)
            assert response.status_code == 200
            
            data = response.json()
            assert "response" in data
            assert "intent" in data
            assert len(data["quick_replies"]) > 0
    
    def test_chat_endpoint_validation(self, client):
        """Test chat endpoint input validation"""
        # Missing required fields
        invalid_message = {"message": "Hello"}
        response = client.post("/chat", json=invalid_message)
        assert response.status_code == 422
        
        # Empty message
        empty_message = {"message": "", "session_id": "test123"}
        response = client.post("/chat", json=empty_message)
        assert response.status_code == 422
    
    def test_qualify_lead_endpoint(self, client):
        """Test lead qualification endpoint"""
        lead_data = {
            "session_id": "test_session_123",
            "email": "test@hawaiibusiness.com",
            "business_type": "restaurant",
            "island": "maui",
            "challenges": ["online presence", "customer retention"],
            "timeline": "1-3 months",
            "budget_range": "$5000-$10000"
        }
        
        with patch('api_backend.main.lead_service.create_lead') as mock_create:
            mock_create.return_value = Mock(
                id="lead_123",
                qualification_score=0.85,
                qualification_status="qualified"
            )
            
            response = client.post("/qualify-lead", json=lead_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["qualified"] == True
            assert data["score"] >= 0.8
    
    def test_island_insights_endpoint(self, client):
        """Test island-specific insights endpoint"""
        params = {
            "island": "big_island",
            "business_type": "agriculture"
        }
        
        response = client.get("/insights/island", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "insights" in data
        assert "opportunities" in data["insights"]
        assert "challenges" in data["insights"]
        assert any("coffee" in opp.lower() for opp in data["insights"]["opportunities"])
    
    def test_analytics_endpoint(self, client):
        """Test analytics endpoint"""
        params = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        }
        
        with patch('api_backend.main.analytics_service.get_analytics') as mock_analytics:
            mock_analytics.return_value = {
                "total_conversations": 150,
                "qualified_leads": 45,
                "conversion_rate": 0.30,
                "island_breakdown": {
                    "oahu": 60,
                    "maui": 40,
                    "big_island": 30,
                    "kauai": 20
                }
            }
            
            response = client.get("/analytics", params=params)
            assert response.status_code == 200
            
            data = response.json()
            assert "total_conversations" in data
            assert "island_breakdown" in data


class TestWebSocketEndpoint:
    """Test WebSocket chat functionality"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_websocket_connection(self, client):
        """Test WebSocket connection establishment"""
        with client.websocket_connect("/ws?session_id=test123") as websocket:
            # Send initial message
            websocket.send_json({
                "message": "Howzit!",
                "type": "chat"
            })
            
            # Receive response
            response = websocket.receive_json()
            assert "response" in response
            assert "timestamp" in response
    
    def test_websocket_pidgin_conversation(self, client):
        """Test WebSocket handles pidgin conversation"""
        with patch('api_backend.main.conversation_router.route_message') as mock_route:
            mock_route.return_value = {
                "response": "Howzit brah! How I can help your business stay successful?",
                "intent": "greet",
                "confidence": 0.95
            }
            
            with client.websocket_connect("/ws?session_id=test123") as websocket:
                websocket.send_json({
                    "message": "Eh howzit, my store stay slow",
                    "type": "chat"
                })
                
                response = websocket.receive_json()
                assert "howzit" in response["response"].lower()


class TestBusinessEndpoints:
    """Test business-specific endpoints"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_schedule_appointment_endpoint(self, client):
        """Test appointment scheduling endpoint"""
        appointment_data = {
            "lead_id": "lead_123",
            "preferred_date": "2024-02-15",
            "preferred_time": "afternoon",
            "meeting_type": "consultation",
            "timezone": "Pacific/Honolulu"
        }
        
        with patch('api_backend.main.calendar_service.schedule_appointment') as mock_schedule:
            mock_schedule.return_value = {
                "appointment_id": "apt_123",
                "confirmed_time": "2024-02-15T14:00:00-10:00",
                "meeting_link": "https://meet.google.com/abc-defg-hij"
            }
            
            response = client.post("/schedule-appointment", json=appointment_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "appointment_id" in data
            assert "-10:00" in data["confirmed_time"]  # HST timezone
    
    def test_get_recommendations_endpoint(self, client):
        """Test service recommendations endpoint"""
        params = {
            "business_type": "tourism",
            "island": "maui",
            "budget": "medium"
        }
        
        response = client.get("/recommendations", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
        
        # Check recommendations are relevant
        for rec in data["recommendations"]:
            assert "service" in rec
            assert "reason" in rec
            assert "estimated_value" in rec


class TestCulturalEndpoints:
    """Test cultural-specific endpoints"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_cultural_context_endpoint(self, client):
        """Test cultural context analysis endpoint"""
        message_data = {
            "message": "Eh brah, my ohana business need kokua with da kine marketing"
        }
        
        response = client.post("/analyze-cultural-context", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["uses_pidgin"] == True
        assert "ohana" in data["cultural_elements"]
        assert "kokua" in data["cultural_elements"]
        assert data["recommended_tone"] == "casual_pidgin"
    
    def test_hawaiian_greeting_endpoint(self, client):
        """Test time-appropriate Hawaiian greeting endpoint"""
        with patch('api_backend.main.datetime') as mock_datetime:
            # Set to morning time in HST
            mock_datetime.now.return_value.hour = 8
            
            response = client.get("/hawaiian-greeting")
            assert response.status_code == 200
            
            data = response.json()
            assert "greeting" in data
            assert "kakahiaka" in data["greeting"]  # Morning greeting


class TestErrorHandling:
    """Test API error handling"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_rasa_connection_error(self, client):
        """Test handling when Rasa is unavailable"""
        with patch('api_backend.main.conversation_router.route_message') as mock_route:
            mock_route.side_effect = Exception("Rasa connection failed")
            
            response = client.post("/chat", json={
                "message": "Hello",
                "session_id": "test123"
            })
            
            # Should fallback gracefully
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert any(word in data["response"].lower() for word in ["sorry", "issue", "moment"])
    
    def test_database_error_handling(self, client):
        """Test handling of database errors"""
        with patch('api_backend.main.lead_service.create_lead') as mock_create:
            mock_create.side_effect = Exception("Database connection error")
            
            response = client.post("/qualify-lead", json={
                "session_id": "test123",
                "email": "test@example.com",
                "business_type": "restaurant"
            })
            
            assert response.status_code == 500
            data = response.json()
            assert "error" in data


class TestRateLimiting:
    """Test API rate limiting"""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_chat_rate_limit(self, client):
        """Test rate limiting on chat endpoint"""
        # Make multiple rapid requests
        for i in range(35):  # Exceeds 30 req/s limit
            response = client.post("/chat", json={
                "message": f"Test message {i}",
                "session_id": "test123"
            })
        
        # Last requests should be rate limited
        assert response.status_code == 429
        assert "rate limit" in response.json()["detail"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])