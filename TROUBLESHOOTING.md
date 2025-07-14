# Troubleshooting Hawaiian LeniLani Chatbot

## If the chatbot isn't working:

### 1. Check Backend is Running
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy","timezone":"HST","aloha":"Aloha! E komo mai!"}`

### 2. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'
```

### 3. Debug Mode
Visit http://localhost:3000?debug to see the debug interface

### 4. Common Issues:

#### API Key Issues
- Check .env file has ANTHROPIC_API_KEY set correctly
- Restart backend after changing .env

#### CORS Issues
- Backend should be running on http://localhost:8000
- Frontend expects backend at this address

#### Long Responses
- Responses are configured to be 1-2 sentences
- If getting long responses, restart backend

### 5. Restart Everything
```bash
# Kill all processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Start fresh
./start.sh
```

### 6. Check Browser Console
- Open Developer Tools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

### 7. Manual Backend Start
```bash
cd api_backend
source ../venv/bin/activate
export PYTHONPATH="$PWD:$PYTHONPATH"
source ../.env
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 8. Manual Frontend Start
```bash
cd frontend
npm start
```