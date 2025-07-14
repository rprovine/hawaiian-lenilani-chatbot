"""
Lead Capture Service - Sends qualified leads to Reno via email and HubSpot
"""
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from datetime import datetime
import pytz
import requests
import json

logger = logging.getLogger(__name__)


class LeadCaptureService:
    """Captures and sends qualified leads to Reno"""
    
    def __init__(self):
        # Email configuration
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.lead_email = os.getenv("LEAD_EMAIL", "reno@lenilani.com")
        
        # HubSpot configuration
        self.hubspot_api_key = os.getenv("HUBSPOT_API_KEY", "")
        self.hubspot_portal_id = os.getenv("HUBSPOT_PORTAL_ID", "")
        self.hubspot_form_guid = os.getenv("HUBSPOT_FORM_GUID", "")
        
        # Hawaii timezone
        self.hawaii_tz = pytz.timezone('Pacific/Honolulu')
        
        logger.info("Lead Capture Service initialized")
    
    async def capture_lead(
        self,
        lead_data: Dict[str, Any],
        conversation_summary: str,
        qualification_score: int = 0
    ) -> Dict[str, Any]:
        """
        Capture and send lead information
        
        Args:
            lead_data: Dictionary containing lead information
            conversation_summary: Summary of the chat conversation
            qualification_score: Lead quality score (0-100)
        
        Returns:
            Status of lead capture
        """
        try:
            logger.info(f"Attempting to capture lead with data: {lead_data}")
            
            # Enrich lead data
            enriched_lead = self._enrich_lead_data(lead_data, conversation_summary, qualification_score)
            logger.info(f"Enriched lead data: {enriched_lead}")
            
            # Send via email
            email_sent = await self._send_email_notification(enriched_lead)
            logger.info(f"Email sent status: {email_sent}")
            
            # Send to HubSpot if configured
            hubspot_sent = False
            if self.hubspot_api_key:
                hubspot_sent = await self._send_to_hubspot(enriched_lead)
            
            # Send to webhook if configured
            webhook_sent = False
            try:
                from .webhook_lead_capture import WebhookLeadCapture, create_zapier_friendly_lead
                webhook_service = WebhookLeadCapture()
                zapier_lead = create_zapier_friendly_lead(enriched_lead)
                webhook_result = await webhook_service.send_lead(zapier_lead)
                webhook_sent = webhook_result.get("success", False)
                if webhook_sent:
                    logger.info("Lead sent to webhook successfully")
            except Exception as e:
                logger.warning(f"Webhook send failed: {str(e)}")
            
            # Log the lead locally
            self._log_lead(enriched_lead)
            
            return {
                "success": True,
                "email_sent": email_sent,
                "hubspot_sent": hubspot_sent,
                "lead_id": enriched_lead.get("lead_id"),
                "message": "Lead captured successfully!"
            }
            
        except Exception as e:
            logger.error(f"Error capturing lead: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to capture lead, but don't worry - we'll follow up!"
            }
    
    def _enrich_lead_data(
        self,
        lead_data: Dict[str, Any],
        conversation_summary: str,
        qualification_score: int
    ) -> Dict[str, Any]:
        """Enrich lead data with additional information"""
        hawaii_time = datetime.now(self.hawaii_tz)
        
        enriched = {
            "lead_id": f"lead_{hawaii_time.strftime('%Y%m%d_%H%M%S')}",
            "captured_at": hawaii_time.isoformat(),
            "qualification_score": qualification_score,
            "conversation_summary": conversation_summary,
            **lead_data
        }
        
        # Add lead quality rating
        if qualification_score >= 80:
            enriched["lead_quality"] = "🔥 HOT - Ready to buy"
        elif qualification_score >= 60:
            enriched["lead_quality"] = "🌟 WARM - High interest"
        elif qualification_score >= 40:
            enriched["lead_quality"] = "💫 COOL - Needs nurturing"
        else:
            enriched["lead_quality"] = "❄️ COLD - Early stage"
        
        return enriched
    
    async def _send_email_notification(self, lead_data: Dict[str, Any]) -> bool:
        """Send email notification to Reno"""
        try:
            logger.info(f"Email config - SMTP User: {self.smtp_user}, Has password: {bool(self.smtp_password)}")
            
            if not self.smtp_user or not self.smtp_password:
                logger.warning("Email not configured, skipping email notification")
                logger.info(f"SMTP_USER: {self.smtp_user}, SMTP_PASSWORD exists: {bool(self.smtp_password)}")
                return False
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🌺 New Lead: {lead_data.get('name', 'Unknown')} - {lead_data.get('business_type', 'Unknown Business')}"
            msg['From'] = self.smtp_user
            msg['To'] = self.lead_email
            
            # Create email body
            html_body = self._create_email_body(lead_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully for lead {lead_data.get('lead_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _create_email_body(self, lead_data: Dict[str, Any]) -> str:
        """Create formatted email body"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h2 style="color: #0081a7;">🌺 New Lead from Leni Begonia Chatbot</h2>
                
                <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Lead Quality: {lead_data.get('lead_quality', 'Unknown')}</h3>
                    
                    <h4>Contact Information:</h4>
                    <ul>
                        <li><strong>Name:</strong> {lead_data.get('name', 'Not provided')}</li>
                        <li><strong>Email:</strong> {lead_data.get('email', 'Not provided')}</li>
                        <li><strong>Phone:</strong> {lead_data.get('phone', 'Not provided')}</li>
                        <li><strong>Company:</strong> {lead_data.get('company', 'Not provided')}</li>
                    </ul>
                    
                    <h4>Business Details:</h4>
                    <ul>
                        <li><strong>Type:</strong> {lead_data.get('business_type', 'Not specified')}</li>
                        <li><strong>Location:</strong> {lead_data.get('location', 'Not specified')}</li>
                        <li><strong>Challenge:</strong> {lead_data.get('main_challenge', 'Not specified')}</li>
                        <li><strong>Budget Range:</strong> {lead_data.get('budget_range', 'Not discussed')}</li>
                    </ul>
                    
                    <h4>Conversation Summary:</h4>
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                        {lead_data.get('conversation_summary', 'No summary available')}
                    </div>
                    
                    <h4>Recommended Next Steps:</h4>
                    <ul>
                        <li>{self._get_follow_up_recommendation(lead_data)}</li>
                    </ul>
                    
                    <p style="margin-top: 20px; color: #666;">
                        <small>Lead captured at: {lead_data.get('captured_at', 'Unknown time')}</small>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    async def _send_to_hubspot(self, lead_data: Dict[str, Any]) -> bool:
        """Send lead to HubSpot CRM"""
        try:
            if not self.hubspot_form_guid:
                # Use Contacts API instead
                return await self._create_hubspot_contact(lead_data)
            
            # Use Forms API
            form_url = f"https://api.hsforms.com/submissions/v3/integration/submit/{self.hubspot_portal_id}/{self.hubspot_form_guid}"
            
            form_data = {
                "fields": [
                    {"name": "email", "value": lead_data.get("email", "")},
                    {"name": "firstname", "value": lead_data.get("name", "").split()[0] if lead_data.get("name") else ""},
                    {"name": "lastname", "value": " ".join(lead_data.get("name", "").split()[1:]) if lead_data.get("name") and len(lead_data.get("name", "").split()) > 1 else ""},
                    {"name": "phone", "value": lead_data.get("phone", "")},
                    {"name": "company", "value": lead_data.get("company", "")},
                    {"name": "lead_quality", "value": lead_data.get("lead_quality", "")},
                    {"name": "business_type", "value": lead_data.get("business_type", "")},
                    {"name": "main_challenge", "value": lead_data.get("main_challenge", "")},
                ],
                "context": {
                    "pageUri": "https://hawaii.lenilani.com",
                    "pageName": "Leni Begonia Chatbot"
                }
            }
            
            response = requests.post(form_url, json=form_data)
            response.raise_for_status()
            
            logger.info(f"Lead sent to HubSpot successfully: {lead_data.get('lead_id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send to HubSpot: {str(e)}")
            return False
    
    async def _create_hubspot_contact(self, lead_data: Dict[str, Any]) -> bool:
        """Create contact using HubSpot Contacts API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.hubspot_api_key}",
                "Content-Type": "application/json"
            }
            
            contact_data = {
                "properties": {
                    "email": lead_data.get("email", ""),
                    "firstname": lead_data.get("name", "").split()[0] if lead_data.get("name") else "",
                    "lastname": " ".join(lead_data.get("name", "").split()[1:]) if lead_data.get("name") and len(lead_data.get("name", "").split()) > 1 else "",
                    "phone": lead_data.get("phone", ""),
                    "company": lead_data.get("company", ""),
                    "hs_lead_status": "NEW",
                    "lead_source": "Leni Begonia Chatbot",
                    "business_type": lead_data.get("business_type", ""),
                    "main_challenge": lead_data.get("main_challenge", ""),
                    "lead_quality_score": str(lead_data.get("qualification_score", 0))
                }
            }
            
            response = requests.post(
                "https://api.hubapi.com/crm/v3/objects/contacts",
                headers=headers,
                json=contact_data
            )
            response.raise_for_status()
            
            logger.info(f"HubSpot contact created: {response.json().get('id')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create HubSpot contact: {str(e)}")
            return False
    
    def _get_follow_up_recommendation(self, lead_data: Dict[str, Any]) -> str:
        """Get follow-up recommendation based on lead quality"""
        score = lead_data.get("qualification_score", 0)
        
        if score >= 80:
            return "Call within 1 hour! This lead is ready to move forward."
        elif score >= 60:
            return "Call within 24 hours. Schedule a consultation ASAP."
        elif score >= 40:
            return "Follow up within 2-3 days with educational content."
        else:
            return "Add to nurture campaign. Not ready for direct sales."
    
    def _log_lead(self, lead_data: Dict[str, Any]):
        """Log lead information locally"""
        try:
            log_dir = "logs/leads"
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f"{lead_data.get('lead_id')}.json")
            with open(log_file, 'w') as f:
                json.dump(lead_data, f, indent=2)
            
            logger.info(f"Lead logged to {log_file}")
        except Exception as e:
            logger.error(f"Failed to log lead: {str(e)}")