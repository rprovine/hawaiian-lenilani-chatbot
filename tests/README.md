# Hawaiian LeniLani Chatbot Test Suite

## 🧪 Overview

This directory contains comprehensive tests for the Hawaiian LeniLani AI Consulting Chatbot, ensuring proper functionality, cultural authenticity, and business logic accuracy.

## 📁 Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and test configuration
├── test_hawaiian_conversations.py # Hawaiian language and conversation tests
├── test_cultural_integration.py   # Cultural authenticity tests
├── test_api_endpoints.py         # FastAPI endpoint tests
├── test_rasa_actions.py          # Rasa custom action tests
├── test_integration.py           # End-to-end integration tests
└── README.md                     # This file
```

## 🏃 Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_hawaiian_conversations.py
```

### Run with coverage
```bash
pytest --cov=. --cov-report=html
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test
```bash
pytest tests/test_cultural_integration.py::TestCulturalAuthenticity::test_hawaiian_values_present
```

## 🧪 Test Categories

### 1. Hawaiian Conversation Tests (`test_hawaiian_conversations.py`)
- Time-aware Hawaiian greetings
- Pidgin language detection and responses
- Island-specific business logic
- Business qualification scoring
- Cultural value integration
- Hawaii Standard Time handling

### 2. Cultural Integration Tests (`test_cultural_integration.py`)
- Hawaiian values presence and accuracy
- Pidgin phrase authenticity
- Island knowledge verification
- Cultural sensitivity checks
- Business type understanding
- Time zone handling

### 3. API Endpoint Tests (`test_api_endpoints.py`)
- Health check endpoints
- Chat conversation endpoints
- Lead qualification endpoints
- WebSocket functionality
- Error handling
- Rate limiting

### 4. Rasa Action Tests (`test_rasa_actions.py`)
- Hawaiian greeting actions
- Business qualification logic
- Island-specific advice generation
- Appointment scheduling with HST
- Service recommendations
- HubSpot synchronization

### 5. Integration Tests (`test_integration.py`)
- End-to-end conversation flows
- Rasa-Claude integration
- Database persistence
- WebSocket communication
- Error handling across systems

## 🔧 Test Fixtures

Key fixtures available in `conftest.py`:

- `hawaii_timezone`: Pacific/Honolulu timezone
- `mock_datetime_hst`: Mock datetime in HST
- `sample_chat_message`: Sample chat message
- `sample_business_lead`: Sample lead data
- `mock_rasa_tracker`: Mock Rasa tracker
- `mock_dispatcher`: Mock Rasa dispatcher
- `mock_claude_client`: Mock Claude API client
- `island_business_contexts`: Island-specific data
- `hawaiian_greetings`: Time-based greetings
- `pidgin_phrases`: Common pidgin expressions

## 📊 Coverage Goals

Target coverage: 80%+

Key areas requiring coverage:
- All Rasa custom actions
- API endpoints
- Cultural intelligence logic
- Business qualification algorithms
- Island-specific recommendations
- Error handling paths

## 🏝️ Cultural Testing Guidelines

When writing tests for Hawaiian cultural elements:

1. **Respect**: Ensure tests respect Hawaiian culture
2. **Accuracy**: Verify cultural elements are accurate
3. **Sensitivity**: Test for cultural appropriation detection
4. **Language**: Test both pidgin and standard English
5. **Islands**: Cover all six main Hawaiian islands

## 🐛 Common Test Scenarios

### Pidgin Conversation Test
```python
def test_pidgin_conversation():
    response = chat("Eh brah, my store stay slow")
    assert "howzit" in response or "shoots" in response
```

### Island-Specific Test
```python
def test_maui_tourism():
    advice = get_island_advice("maui", "tourism")
    assert "wedding" in advice or "seasonal" in advice
```

### Time-Based Greeting Test
```python
def test_morning_greeting():
    with mock_time(hour=7):
        greeting = get_greeting()
        assert "Aloha kakahiaka" in greeting
```

## 🔍 Debugging Tests

### Enable detailed logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use pytest debugging
```bash
pytest --pdb  # Drop into debugger on failure
```

### Print test output
```bash
pytest -s  # Don't capture stdout
```

## 🚀 Continuous Integration

Tests should be run in CI/CD pipeline:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    pytest --cov=. --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## 📝 Writing New Tests

1. **Follow naming convention**: `test_*.py`
2. **Use descriptive test names**: `test_hawaiian_greeting_morning_time`
3. **Group related tests**: Use test classes
4. **Mock external dependencies**: Don't call real APIs
5. **Test edge cases**: Empty inputs, invalid data
6. **Document complex tests**: Add docstrings

Example test structure:
```python
class TestFeatureName:
    """Test description"""
    
    @pytest.fixture
    def setup_data(self):
        """Setup test data"""
        return {...}
    
    def test_normal_case(self, setup_data):
        """Test normal operation"""
        result = function(setup_data)
        assert result == expected
    
    def test_edge_case(self):
        """Test edge case handling"""
        with pytest.raises(ValueError):
            function(invalid_input)
```

## 🌺 Mahalo!

Thank you for maintaining test quality for the Hawaiian LeniLani Chatbot. Comprehensive testing ensures we provide reliable, culturally appropriate service to Hawaiian businesses.