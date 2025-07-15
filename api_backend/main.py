"""
Hawaiian LeniLani Chatbot - FastAPI Backend
Main application entry point with Hawaiian business logic
"""
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import pytz
import httpx
from dotenv import load_dotenv

from models.hawaiian_business import BusinessInquiry, ConversationState, HawaiianBusinessResponse
from models.cultural_context import CulturalContext, IslandCulture
from services.hawaiian_conversation_router import HawaiianConversationRouter
from services.cultural_tone_manager import CulturalToneManager
from services.island_business_intelligence import IslandBusinessIntelligence
from services.hawaiian_timezone_handler import HawaiianTimezoneHandler
from config.hawaiian_cultural_config import HAWAIIAN_CONFIG
from config.island_business_config import ISLAND_BUSINESS_CONFIG
from services.startup_tasks import run_startup_tasks
try:
    from . import admin_routes
except ImportError:
    import admin_routes

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
conversation_router = HawaiianConversationRouter()
cultural_tone_manager = CulturalToneManager()
island_intelligence = IslandBusinessIntelligence()
timezone_handler = HawaiianTimezoneHandler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("🌺 Starting Hawaiian LeniLani Chatbot API...")
    
    # Run startup tasks (create directories, etc.)
    run_startup_tasks()
    
    logger.info(f"🏝️ Hawaii Time: {timezone_handler.get_current_hawaii_time()}")
    logger.info("🤙 Aloha! Ready to serve Hawaiian businesses!")
    
    yield
    
    # Shutdown
    logger.info("🌙 Shutting down Hawaiian LeniLani Chatbot API...")
    logger.info("A hui hou! Until we meet again!")


# Create FastAPI app
app = FastAPI(
    title="Hawaiian LeniLani Chatbot API",
    description="AI-powered chatbot for Hawaiian businesses with authentic cultural integration",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for production
default_origins = [
    "http://localhost:3000",  # Development
    "http://localhost:8000",  # Development API
    "http://localhost:8080",  # Widget demo server
    "http://127.0.0.1:8080",  # Widget demo server
    "https://hawaii.lenilani.com",  # Main website
    "https://www.hawaii.lenilani.com",  # WWW variant
    "https://lenilani.com",  # Alternative domain
    "https://www.lenilani.com",  # WWW variant
    "https://chat.lenilani.com",  # Chat subdomain
    "https://api.lenilani.com",  # API subdomain
    "https://hawaiian-ai-chatbot.lenilani.com",  # Landing page subdomain
    "https://www.hawaiian-ai-chatbot.lenilani.com",  # WWW variant
    "https://aibothawaii.lenilani.com",  # Alternative landing page subdomain
    "https://www.aibothawaii.lenilani.com",  # WWW variant
]

# Add origins from environment variable if provided
cors_origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
allowed_origins = default_origins + [origin.strip() for origin in cors_origins if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Serve static files (widget.js)
import os
public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
if os.path.exists(public_dir):
    app.mount("/public", StaticFiles(directory=public_dir), name="public")
    
    # Serve full landing page
    @app.get("/landing", response_class=HTMLResponse)
    async def serve_landing_page():
        """Serve the full landing page"""
        landing_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "landing-page.html")
        if os.path.exists(landing_path):
            with open(landing_path, 'r') as f:
                return HTMLResponse(content=f.read())
        return HTMLResponse("<h1>Landing page not found</h1>", status_code=404)
    
    # Serve widget.js at root level for convenience
    @app.get("/widget.js")
    async def serve_widget():
        # Serve the full Hawaiian widget
        widget_path = os.path.join(public_dir, "hawaiian-widget.js")
        if os.path.exists(widget_path):
            return FileResponse(widget_path, media_type="application/javascript")
        # Fallback to simple widget
        widget_path = os.path.join(public_dir, "widget.js")
        if os.path.exists(widget_path):
            return FileResponse(widget_path, media_type="application/javascript")
        raise HTTPException(status_code=404, detail="Widget not found")
    
    # Serve logo
    @app.get("/logo")
    async def serve_logo():
        logo_path = os.path.join(public_dir, "lenilani-logo.webp")
        if os.path.exists(logo_path):
            return FileResponse(logo_path, media_type="image/webp")
        raise HTTPException(status_code=404, detail="Logo not found")
    
    # Serve admin interface
    @app.get("/admin")
    async def serve_admin():
        admin_path = os.path.join(public_dir, "admin.html")
        if os.path.exists(admin_path):
            return FileResponse(admin_path, media_type="text/html")
        raise HTTPException(status_code=404, detail="Admin interface not found")
    
    # Serve lead viewer instructions
    @app.get("/view-leads")
    async def serve_lead_viewer():
        viewer_path = os.path.join(public_dir, "view-leads.html")
        if os.path.exists(viewer_path):
            return FileResponse(viewer_path, media_type="text/html")
        raise HTTPException(status_code=404, detail="Lead viewer not found")


# Request/Response Models
class HealthCheckResponse(BaseModel):
    status: str
    message: str
    hawaii_time: str
    greeting: str


class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str
    metadata: Dict[str, Any]
    suggestions: Optional[List[str]] = None
    quick_replies: Optional[List[str]] = None


class BusinessQualificationRequest(BaseModel):
    business_type: str
    island: str
    challenges: List[str]
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    contact_info: Optional[Dict[str, str]] = None


class ScheduleConsultationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company_name: Optional[str] = None
    business_type: Optional[str] = None
    island: Optional[str] = None
    preferred_time: Optional[str] = None
    message: Optional[str] = None


# Connection manager for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"🌺 New connection from client: {client_id}")
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"🌙 Client disconnected: {client_id}")
    
    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()

# Include admin routes
app.include_router(admin_routes.router)


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve landing page with chatbot"""
    # Check if request wants JSON (API call)
    if request.headers.get("accept", "").startswith("application/json"):
        current_time = timezone_handler.get_current_hawaii_time()
        greeting = timezone_handler.get_time_based_greeting()
        return JSONResponse(content={
            "status": "healthy",
            "message": "Hawaiian LeniLani Chatbot API is running! 🌺",
            "hawaii_time": current_time["formatted"],
            "greeting": greeting
        })
    
    # Serve the full landing page
    # Try public directory first (more reliable in Docker)
    landing_path = os.path.join(public_dir, "landing-page.html")
    logger.info(f"Looking for landing page at: {landing_path}")
    logger.info(f"File exists: {os.path.exists(landing_path)}")
    
    if os.path.exists(landing_path):
        try:
            with open(landing_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Successfully loaded landing page, size: {len(content)} bytes")
                return HTMLResponse(content=content)
        except Exception as e:
            logger.error(f"Error reading landing page: {e}")
    
    # Fallback to simple landing page if file not found
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hawaiian AI Business Assistant - LeniLani Consulting</title>
    <meta name="description" content="AI-powered business consulting for Hawaiian companies. Combining technology with aloha spirit.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0081a7 0%, #00afb9 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        .container { max-width: 800px; animation: fadeIn 1s ease-out; }
        h1 { font-size: 3.5em; margin-bottom: 20px; }
        .tagline { font-size: 1.5em; margin-bottom: 30px; opacity: 0.95; }
        .description { font-size: 1.1em; margin-bottom: 40px; opacity: 0.9; line-height: 1.6; }
        .cta-buttons { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
        .cta {
            display: inline-block;
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
        }
        .cta-primary {
            background: white;
            color: #0081a7;
        }
        .cta-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .cta-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        .cta-secondary:hover {
            background: white;
            color: #0081a7;
        }
        .features {
            margin-top: 60px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .feature-icon { font-size: 2em; margin-bottom: 10px; }
        .chat-hint {
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 12px 20px;
            border-radius: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            animation: pulse 2s infinite;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        @media (max-width: 768px) {
            h1 { font-size: 2.5em; }
            .tagline { font-size: 1.2em; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌺 Aloha! Welcome to Hawaiian AI</h1>
        <p class="tagline">Where Technology Meets the Spirit of Aloha</p>
        <p class="description">
            We empower Hawaiian businesses with cutting-edge AI technology while preserving 
            our island values and culture. From local shops to tourism companies, we help you 
            thrive in the digital age without losing your authentic Hawaiian touch.
        </p>
        
        <div class="cta-buttons">
            <a href="https://lenilani.com" class="cta cta-primary">Visit LeniLani Consulting</a>
            <a href="mailto:reno@lenilani.com" class="cta cta-secondary">Contact Us</a>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>AI Integration</h3>
                <p>Smart technology that respects island ways</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📊</div>
                <h3>Data Analytics</h3>
                <p>Insights for Hawaii's unique market</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🌴</div>
                <h3>Local Expertise</h3>
                <p>We understand island business</p>
            </div>
        </div>
    </div>
    
    <div class="chat-hint">
        💬 Try our AI assistant →
    </div>
    
    <!-- Chatbot Widget -->
    <script>
        window.LENILANI_CHATBOT_URL = window.location.origin;
    </script>
    <script src="/widget.js"></script>
</body>
</html>
    """)


@app.get("/test")
async def test():
    """Simple test endpoint"""
    return {"message": "Test successful"}

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    current_time = timezone_handler.get_current_hawaii_time()
    greeting = timezone_handler.get_time_based_greeting()
    
    return HealthCheckResponse(
        status="healthy",
        message="All systems operational! Mahalo for checking! 🤙",
        hawaii_time=current_time["formatted"],
        greeting=greeting
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, request: Request):
    """Main chat endpoint for Hawaiian business conversations"""
    # Log request details to debug double calls
    request_id = request.headers.get("X-Request-ID", "no-id")
    logger.info(f"Chat request received - Session: {message.session_id}, Request ID: {request_id}, Message: {message.message[:50]}")
    
    try:
        # Get cultural context
        cultural_context = cultural_tone_manager.get_cultural_context()
        
        # Route conversation appropriately
        response = await conversation_router.route_message(
            user_message=message.message,
            session_id=message.session_id,
            user_id=message.user_id,
            metadata=message.metadata
        )
        
        # Add cultural tone enhancement for more pidgin flavor
        enhanced_response = cultural_tone_manager.enhance_response(
            response["response"],
            cultural_context
        )
        
        # Add suggestions based on conversation state
        suggestions = conversation_router.get_suggestions(message.message)
        
        # No quick replies for Claude-only implementation
        quick_replies = []
        
        return ChatResponse(
            response=enhanced_response,
            metadata={
                "cultural_context": cultural_context,
                "timestamp": datetime.now(pytz.timezone('Pacific/Honolulu')).isoformat(),
                "intent": response.get("intent"),
                "confidence": response.get("confidence")
            },
            suggestions=suggestions,
            quick_replies=quick_replies
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Ho brah, something went wrong! Try again or contact Reno at reno@lenilani.com (808-766-1164).")


@app.post("/qualify-business", response_model=HawaiianBusinessResponse)
async def qualify_business(request: BusinessQualificationRequest):
    """Qualify a Hawaiian business and provide recommendations"""
    try:
        # Create business inquiry
        inquiry = BusinessInquiry(
            business_type=request.business_type,
            island=request.island,
            challenges=request.challenges,
            budget_range=request.budget_range,
            timeline=request.timeline,
            contact_info=request.contact_info
        )
        
        # Get island-specific intelligence
        island_insights = island_intelligence.get_island_insights(
            request.island,
            request.business_type
        )
        
        # Generate recommendations
        recommendations = island_intelligence.generate_recommendations(
            inquiry,
            island_insights
        )
        
        # Create response
        response = HawaiianBusinessResponse(
            recommendations=recommendations,
            island_insights=island_insights,
            cultural_notes=cultural_tone_manager.get_business_cultural_notes(
                request.business_type,
                request.island
            ),
            next_steps=[
                "Schedule a free 30-minute talk story session",
                "Review our case studies from similar Hawaiian businesses",
                "Connect with our local business references",
                "Get a customized proposal for your needs"
            ]
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error qualifying business: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing business qualification")


@app.post("/schedule-consultation")
async def schedule_consultation(request: ScheduleConsultationRequest):
    """Schedule a consultation with Hawaiian business"""
    try:
        # Here you would integrate with Google Calendar API
        # For now, we'll simulate the scheduling
        
        consultation_data = {
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "company_name": request.company_name,
            "business_type": request.business_type,
            "island": request.island,
            "preferred_time": request.preferred_time,
            "message": request.message,
            "scheduled_at": datetime.now(pytz.timezone('Pacific/Honolulu')).isoformat()
        }
        
        # Send to HubSpot (would be actual integration)
        # await send_to_hubspot(consultation_data)
        
        # Send confirmation email (would be actual email)
        # await send_confirmation_email(request.email, consultation_data)
        
        return {
            "status": "success",
            "message": f"Shoots! Consultation scheduled! We'll email {request.email} with details. Looking forward to talking story!",
            "consultation_id": f"CONSULT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "next_steps": [
                "Check your email for confirmation and calendar invite",
                "Prepare any questions about your business challenges",
                "Think about your technology goals",
                "We'll call you at the scheduled time"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error scheduling consultation: {str(e)}")
        raise HTTPException(status_code=500, detail="Error scheduling consultation")


@app.get("/services")
async def get_services():
    """Get list of Hawaiian business services"""
    return {
        "services": ISLAND_BUSINESS_CONFIG["services"],
        "islands_served": list(ISLAND_BUSINESS_CONFIG["islands"].keys()),
        "cultural_commitment": HAWAIIAN_CONFIG["cultural_values"]
    }


@app.get("/island-insights/{island}")
async def get_island_insights(island: str):
    """Get insights for specific Hawaiian island"""
    island_lower = island.lower()
    if island_lower not in ISLAND_BUSINESS_CONFIG["islands"]:
        raise HTTPException(status_code=404, detail=f"Island '{island}' not found")
    
    insights = island_intelligence.get_island_insights(island_lower)
    return {
        "island": island,
        "insights": insights,
        "top_opportunities": island_intelligence.get_top_opportunities(island_lower),
        "success_stories": island_intelligence.get_success_stories(island_lower)
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, client_id)
    
    # Send welcome message
    welcome_msg = {
        "type": "welcome",
        "message": timezone_handler.get_time_based_greeting() + " Ready for talk story!",
        "timestamp": datetime.now(pytz.timezone('Pacific/Honolulu')).isoformat()
    }
    await manager.send_message(str(welcome_msg), client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Process message
            response = await conversation_router.route_message(
                user_message=data.get("message", ""),
                session_id=client_id,
                user_id=data.get("user_id"),
                metadata=data.get("metadata")
            )
            
            # Skip cultural tone enhancement - Claude handles this
            # enhanced_response = cultural_tone_manager.enhance_response(
            #     response["response"],
            #     cultural_tone_manager.get_cultural_context()
            # )
            enhanced_response = response["response"]
            
            # Send response
            response_msg = {
                "type": "response",
                "message": enhanced_response,
                "metadata": response.get("metadata", {}),
                "timestamp": datetime.now(pytz.timezone('Pacific/Honolulu')).isoformat()
            }
            await manager.send_message(str(response_msg), client_id)
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected from WebSocket")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )