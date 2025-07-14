#!/bin/bash

echo "🌺 Hawaiian LeniLani Chatbot Startup Script"
echo "==========================================="

# Kill any existing processes on our ports
echo "🧹 Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start backend
echo -e "\n🚀 Starting Backend API..."
cd "$(dirname "$0")"
source venv/bin/activate
python start_app.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
echo -e "\n🧪 Testing backend..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
    echo "📖 API docs: http://localhost:8000/docs"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo -e "\n🚀 Starting Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo -e "\n✅ Application is starting up!"
echo "🌴 Frontend will be available at: http://localhost:3000"
echo "🌺 Chat widget will connect to backend automatically"
echo -e "\n🛑 Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo -e '\n🌙 Shutting down...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait