# Quick Fix for Chatbot Issues

## Issue
The chatbot is showing an error because the Claude API key is invalid.

## Solution

### Option 1: Update the API Key

1. Get a valid API key from https://console.anthropic.com/
2. Update the `.env` file:
```bash
ANTHROPIC_API_KEY=your-valid-api-key-here
```

### Option 2: Test with Mock Responses (Development Only)

If you just want to see the UI working, I can create a mock backend:

```bash
# Stop the current server (Ctrl+C)
# Then run the mock server
python mock_backend.py
```

## What's Happening

The error log shows:
- ✅ Backend server is running
- ✅ Frontend is connecting
- ❌ Claude API authentication is failing (401 error)

The chatbot tries to send your message to Claude AI, but the API key is invalid, so it returns the fallback error message.

## To Fix Permanently

1. Go to https://console.anthropic.com/
2. Sign up/login to get an API key
3. Replace the API key in `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR-ACTUAL-KEY-HERE
   ```
4. Restart the backend server

The current key in your .env file appears to be invalid or expired.