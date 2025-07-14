#!/bin/bash

echo "🌺 Starting Hawaiian LeniLani Chatbot"
echo "===================================="

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start backend in background
echo -e "\n🚀 Starting Backend API on port 8000..."
cd "$(dirname "$0")"
source venv/bin/activate
cd api_backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend in new terminal (macOS)
echo -e "\n🚀 Starting Frontend on port 3000..."
cd ../frontend

# Open new terminal for frontend
osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && npm start"'

echo -e "\n✅ Services are starting!"
echo "📱 Frontend will open at: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API docs: http://localhost:8000/docs"
echo -e "\n💡 The frontend will open in a new Terminal window"
echo "🛑 Press Ctrl+C here to stop the backend"

# Keep backend running
wait $BACKEND_PID