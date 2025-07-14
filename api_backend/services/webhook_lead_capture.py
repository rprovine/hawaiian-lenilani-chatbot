"""
Webhook-based Lead Capture - Send leads to any webhook URL (Zapier, Make, etc.)
"""
import os
import logging
import requests
import json
from typing import Dict, Any
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)


class WebhookLeadCapture:
    """Send leads to webhook URLs for easy integration"""
    
    def __init__(self):
        # Webhook URL from environment or use RequestBin for testing
        self.webhook_url = os.getenv("LEAD_WEBHOOK_URL", "")
        logger.info(f"Webhook URL from env: {self.webhook_url[:50]}..." if self.webhook_url else "No webhook URL found")
        
        self.webhook_headers = {
            "Content-Type": "application/json",
            "User-Agent": "LeniLani-Chatbot/1.0"
        }
        
        # Optional webhook secret for security
        self.webhook_secret = os.getenv("LEAD_WEBHOOK_SECRET", "")
        if self.webhook_secret:
            self.webhook_headers["X-Webhook-Secret"] = self.webhook_secret
        
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
        logger.info(f"Webhook Lead Capture initialized. URL configured: {bool(self.webhook_url)}")
    
    async def send_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send lead to webhook"""
        if not self.webhook_url:
            logger.warning("No webhook URL configured. Set LEAD_WEBHOOK_URL in .env")
            return {
                "success": False,
                "error": "No webhook URL configured"
            }
        
        try:
            # Add timestamp and source
            lead_data["captured_at"] = datetime.now(self.hawaii_tz).isoformat()
            lead_data["source"] = "Leni Begonia Chatbot"
            lead_data["source_url"] = "https://hawaii.lenilani.com"
            
            # Send to webhook
            response = requests.post(
                self.webhook_url,
                headers=self.webhook_headers,
                json=lead_data,
                timeout=10
            )
            
            response.raise_for_status()
            
            logger.info(f"Lead sent to webhook successfully. Status: {response.status_code}")
            
            return {
                "success": True,
                "webhook_response": response.text[:200],
                "status_code": response.status_code
            }
            
        except requests.exceptions.Timeout:
            logger.error("Webhook timeout")
            return {
                "success": False,
                "error": "Webhook timeout"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Webhook error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


def create_zapier_friendly_lead(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format lead data for Zapier/automation tools"""
    return {
        # Basic Info
        "name": lead_data.get("name", ""),
        "email": lead_data.get("email", ""),
        "phone": lead_data.get("phone", ""),
        "company": lead_data.get("company", ""),
        
        # Business Details
        "business_type": lead_data.get("business_type", ""),
        "location": lead_data.get("location", ""),
        "island": lead_data.get("location", ""),
        "main_challenge": lead_data.get("main_challenge", ""),
        "budget_range": lead_data.get("budget_range", ""),
        
        # Lead Quality
        "lead_score": lead_data.get("qualification_score", 0),
        "lead_quality": lead_data.get("lead_quality", ""),
        "is_hot_lead": lead_data.get("qualification_score", 0) >= 80,
        
        # Conversation
        "conversation_summary": lead_data.get("conversation_summary", ""),
        "message_count": lead_data.get("message_count", 0),
        
        # Metadata
        "captured_at": lead_data.get("captured_at", ""),
        "lead_id": lead_data.get("lead_id", ""),
        
        # Recommended Action
        "recommended_action": _get_recommended_action(lead_data.get("qualification_score", 0))
    }


def _get_recommended_action(score: int) -> str:
    """Get recommended action based on lead score"""
    if score >= 80:
        return "URGENT: Call within 1 hour"
    elif score >= 60:
        return "HIGH: Call within 24 hours"
    elif score >= 40:
        return "MEDIUM: Follow up in 2-3 days"
    else:
        return "LOW: Add to nurture campaign"