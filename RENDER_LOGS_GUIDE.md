# Render Logs Analysis Guide

## How to Access Render Logs

### 1. Via Render Dashboard
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your service: `hawaiian-chatbot-api`
3. Navigate to the "Logs" tab
4. You can:
   - View live logs streaming
   - Download logs as a file
   - Filter by time range

### 2. Via Render CLI (if installed)
```bash
render logs hawaiian-chatbot-api --tail
```

### 3. Download and Analyze
1. Download logs from Render dashboard
2. Run the analysis script:
```bash
python check_render_logs.py downloaded_logs.txt
```

## Common Error Patterns to Look For

### 🔴 Critical Errors (Causing "Busy" Messages)

#### 1. Rate Limit Errors (429)
```
Error 429: Rate limit exceeded
httpx.HTTPStatusError: Client error '429 Too Many Requests'
```
**Impact**: Users get busy/error messages
**Fix**: Upgrade Anthropic tier or implement better rate limiting

#### 2. API Overload Errors (529)
```
Error 529: API overloaded
overloaded_error
```
**Impact**: Anthropic's servers are busy
**Fix**: Implement exponential backoff, retry logic

#### 3. Missing API Key
```
ANTHROPIC_API_KEY not found in environment variables
ValueError: ANTHROPIC_API_KEY not found
```
**Impact**: Chatbot can't initialize
**Fix**: Set API key in Render environment variables

### 🟡 Warning Errors

#### 4. Timeout Errors
```
TimeoutError
Request timed out
```
**Impact**: Slow or failed responses
**Fix**: Increase timeout, optimize prompts

#### 5. Connection Errors
```
ConnectionError
ECONNREFUSED
```
**Impact**: Can't reach Anthropic API
**Fix**: Check network, API status

### 🟢 Info/Expected Patterns

#### 6. Fallback Responses
```
Using fallback response
Ho brah, I stay having some technical difficulties
```
**Impact**: User sees generic error message
**Fix**: This is working as designed

#### 7. Lead Capture Logs
```
Lead extraction result: None
Lead captured successfully
```
**Impact**: None - normal operation

## Real-Time Monitoring

### Check Current Status
```bash
# Check if API is healthy
curl https://your-render-url.onrender.com/health

# Test chat endpoint
curl -X POST https://your-render-url.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "session_id": "test"}'
```

### Monitor Rate Limits
The chatbot includes built-in rate limit protection:
- Minimum 1.5 seconds between requests
- Exponential backoff on errors
- Maximum 3 retry attempts

## Error Response Flow

1. **First Attempt** → Claude API
2. **If Rate Limited (429)** → Wait 60 seconds, retry
3. **If Overloaded (529)** → Exponential backoff (2s, 4s, 8s...)
4. **If Max Retries** → Fallback message with contact info

## Debugging Busy Errors

### 1. Check Recent Logs
Look for patterns in the last hour:
- Multiple 429 errors = Rate limiting
- Multiple 529 errors = API overload
- Timeout errors = Slow responses
- No errors = Check client-side

### 2. Verify Configuration
```python
# In Render environment variables:
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_TIER=build1  # or your tier
MIN_REQUEST_INTERVAL=1.5
MAX_RETRIES=3
```

### 3. Test API Directly
```python
# Test script to verify API works
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "test"}]
)
print(response.content[0].text)
```

## Preventive Measures

### 1. Implement Request Queue
```javascript
// In frontend widget
const requestQueue = [];
let processing = false;

async function processQueue() {
    if (processing || requestQueue.length === 0) return;
    processing = true;
    
    const request = requestQueue.shift();
    await sendMessage(request);
    
    // Wait before next request
    setTimeout(() => {
        processing = false;
        processQueue();
    }, 2000);
}
```

### 2. Add User-Facing Rate Limit
```javascript
// Disable send button temporarily
function rateLimitUI() {
    sendButton.disabled = true;
    sendButton.textContent = "Please wait...";
    
    setTimeout(() => {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
    }, 3000);
}
```

### 3. Monitor Usage Patterns
- Peak hours (typically 9am-5pm HST)
- Burst usage (multiple users at once)
- Long conversations (high token usage)

## Emergency Fixes

### If Users Report Busy Errors:

1. **Immediate**: Check Render logs for last 10 minutes
2. **Quick Fix**: Restart the service in Render
3. **Temporary**: Increase MIN_REQUEST_INTERVAL to 3.0
4. **Long-term**: Upgrade Anthropic tier if needed

### Manual Restart:
```bash
# In Render dashboard
Services → hawaiian-chatbot-api → Manual Deploy → Deploy
```

## Contact for Help

If errors persist:
- Anthropic Status: https://status.anthropic.com
- Anthropic Support: support@anthropic.com
- Render Status: https://status.render.com
- Your Implementation: Review rate_limit_handler.py

## Log Analysis Output Example

When you run `check_render_logs.py`, you'll see:

```
🌺 Hawaiian Chatbot Log Analysis Report
========================================

📊 Total lines analyzed: 10,000

🚨 Error Summary:
----------------------------------------

⚠️  Rate Limit (429): 45 occurrences (0.45%)
  └─ Critical - Users getting blocked
  └─ Frequency: 1 every 222 lines
  └─ Examples:
     1. 2024-01-14 10:23:45 - Error 429: Rate limit exceeded
     2. 2024-01-14 10:24:15 - httpx.HTTPStatusError: 429

💬 Busy Messages: 23 occurrences (0.23%)
  └─ User-facing error messages
  └─ Frequency: 1 every 435 lines

⏰ Peak Error Hours (24-hour format):
----------------------------------------
  10:00 - 34 errors
  11:00 - 28 errors
  14:00 - 19 errors

💡 Recommendations:
----------------------------------------
🔴 HIGH PRIORITY: Frequent rate limiting detected!
   - Check current Anthropic tier and upgrade if needed
   - Implement request queuing or throttling
   - Add longer delays between requests

📈 Overall Error Rate: 0.68%
   Total Errors: 68
   Total Lines: 10,000
```

This will help you identify patterns and root causes of busy errors!