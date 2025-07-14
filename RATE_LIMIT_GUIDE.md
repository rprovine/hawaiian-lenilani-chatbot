# Anthropic API Rate Limits Guide

## Current Rate Limits (as of 2024)

The Anthropic API has several rate limits depending on your usage tier:

### Free Tier
- **5 requests per minute**
- **300,000 tokens per day**
- **Rate limit resets**: Every minute

### Paid Tiers
- **Build Tier 1**: 50 requests/minute, 1M tokens/day
- **Build Tier 2**: 1,000 requests/minute, 2.5M tokens/day
- **Build Tier 3**: 2,000 requests/minute, 5M tokens/day
- **Build Tier 4**: 4,000 requests/minute, 10M tokens/day

## Your Chatbot's Built-in Protection

Your Hawaiian chatbot already includes rate limit handling:

1. **Minimum Request Interval**: 1.5 seconds between requests
2. **Automatic Retry**: With exponential backoff
3. **Error Handling**: Graceful degradation when limits are hit

## Symptoms of Rate Limiting

When you hit rate limits, you'll see:
- Error 429: "Rate limit exceeded"
- Error 529: "API overloaded"
- Slow responses or timeouts
- Messages like "Ho brah, I stay having some technical difficulties"

## Solutions

### 1. Immediate Fix - Wait
- Rate limits reset every minute
- Just wait 60 seconds and try again
- The chatbot will automatically retry with backoff

### 2. Check Your Usage
Visit the Anthropic Console to check your current usage:
- https://console.anthropic.com/settings/usage

### 3. Upgrade Your Tier
If you're on the free tier and need more capacity:
1. Go to https://console.anthropic.com/settings/plans
2. Add a payment method
3. Select a paid tier based on your needs

### 4. Optimize Usage
- **Shorter Conversations**: Keep messages concise
- **Cache Responses**: For common questions
- **Rate Limit UI**: Add typing delays or cooldowns

## Testing Without Hitting Limits

For development and testing:

1. **Use Mock Responses** during development:
```python
# In test mode, return canned responses
if os.getenv("TEST_MODE"):
    return {"response": "Aloha! This is a test response."}
```

2. **Add Cooldown Timer** in the widget:
```javascript
// Disable send button for 2 seconds after each message
sendBtn.disabled = true;
setTimeout(() => { sendBtn.disabled = false; }, 2000);
```

3. **Implement Request Queue**:
- Queue messages if sending too fast
- Process queue with delays

## Monitor Your Usage

Add logging to track API usage:

```python
# Log each request
logger.info(f"API Request #{request_count} at {timestamp}")
```

## Environment Variables

You can adjust rate limiting behavior:

```bash
# In Render environment variables
MIN_REQUEST_INTERVAL=2.0  # Seconds between requests
MAX_RETRIES=5             # Number of retry attempts
```

## When to Upgrade

Consider upgrading when:
- You have more than 5 users chatting simultaneously
- Daily token usage exceeds 300k
- You need faster response times
- Business requires high availability

## Cost Estimates

- **Build Tier 1** ($5/month): ~1,000 conversations/day
- **Build Tier 2** ($25/month): ~5,000 conversations/day
- **Build Tier 3** ($250/month): ~10,000 conversations/day

## Contact Support

If you're hitting limits unexpectedly:
1. Check Anthropic status: https://status.anthropic.com
2. Contact Anthropic support: support@anthropic.com
3. Review your API key usage in the console

---

Remember: Rate limits are per API key, so each deployment needs its own key!