# Claude API Optimization for Build Tier

## Current Issues
- Claude API experiencing 529 (overloaded) errors during peak times
- Build tier has limited capacity
- Retries are failing due to continued high load

## Solutions Implemented

### 1. Enhanced Fallback Messages
Updated fallback responses to be more helpful when API is unavailable:
- Clear explanation that AI is temporarily unavailable
- Direct contact information for Reno
- Friendly, local tone maintained

### 2. Rate Limiting (Ready to implement)
Created `rate_limit_handler.py` with:
- Minimum 1.5s between requests
- Exponential backoff with jitter
- Smart retry logic for 529 errors
- Separate handling for rate limits vs overload

### 3. Model Selection Strategy
Consider using different models based on load:
- **claude-3-haiku-20240307**: Faster, cheaper, good for simple queries
- **claude-3-5-sonnet-20241022**: Current model, best quality
- **claude-3-opus-20250620**: Premium model (if available on your tier)

## Recommendations

### Immediate Actions
1. **Test with Haiku model** during high load times
2. **Implement request queuing** to prevent simultaneous requests
3. **Add caching** for common questions

### For Production
1. **Upgrade to higher tier** if budget allows
2. **Implement request batching** 
3. **Add monitoring** for API health
4. **Create static responses** for common queries

### Code Changes to Consider

```python
# In hawaiian_claude_client.py, add model fallback:
def get_model_for_load(self):
    if self.consecutive_errors > 2:
        return "claude-3-haiku-20240307"  # Faster model
    return "claude-3-5-sonnet-20241022"  # Default model
```

## Testing
Run `python test_api_limits.py` to test your current limits and find optimal settings.