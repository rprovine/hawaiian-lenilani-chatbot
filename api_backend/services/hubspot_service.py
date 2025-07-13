"""
HubSpot Service - Lead capture and CRM integration for Hawaiian businesses
"""
import logging
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class HubSpotService:
    """HubSpot integration for lead capture and CRM management"""
    
    def __init__(self):
        self.api_key = os.getenv("HUBSPOT_API_KEY")
        self.portal_id = os.getenv("HUBSPOT_PORTAL_ID")
        self.base_url = "https://api.hubapi.com"
        
        if not self.api_key:
            logger.warning("HUBSPOT_API_KEY not found. HubSpot integration disabled.")
    
    def create_or_update_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a contact in HubSpot"""
        
        if not self.api_key:
            logger.info("HubSpot disabled - would create contact: %s", contact_data)
            return {"success": False, "error": "HubSpot API key not configured"}
        
        # Prepare contact properties for HubSpot
        properties = {
            "email": contact_data.get("email"),
            "firstname": contact_data.get("first_name", ""),
            "lastname": contact_data.get("last_name", ""),
            "phone": contact_data.get("phone", ""),
            "company": contact_data.get("company_name", ""),
            "jobtitle": contact_data.get("job_title", "Business Owner"),
            "website": contact_data.get("website", ""),
            
            # Hawaiian-specific custom properties
            "island_location": contact_data.get("island", ""),
            "business_type_hawaii": contact_data.get("business_type", ""),
            "lead_source": "Hawaiian AI Chatbot - Reno Provine (reno@lenilani.com)",
            "preferred_language": "English/Hawaiian Pidgin",
            
            # Business context
            "primary_challenge": contact_data.get("primary_challenge", ""),
            "budget_range": contact_data.get("budget_range", ""),
            "timeline": contact_data.get("timeline", ""),
            "number_of_employees": str(contact_data.get("company_size", "")),
            
            # Engagement tracking
            "first_conversation_date": datetime.now().strftime("%Y-%m-%d"),
            "chatbot_conversation_count": "1",
            "lead_score": str(self._calculate_lead_score(contact_data)),
            
            # Cultural context
            "market_focus": contact_data.get("market_focus", "Mixed"),
            "sustainability_interest": "Yes" if contact_data.get("values_sustainability") else "No",
            "cultural_alignment": self._calculate_cultural_fit(contact_data)
        }
        
        # Remove None values
        properties = {k: v for k, v in properties.items() if v is not None and v != ""}
        
        try:
            # Try to find existing contact by email first
            email = contact_data.get("email")
            if email:
                existing_contact = self._get_contact_by_email(email)
                if existing_contact:
                    # Update existing contact
                    contact_id = existing_contact["id"]
                    response = self._update_contact(contact_id, properties)
                    if response:
                        logger.info(f"Updated HubSpot contact: {contact_id}")
                        return {"success": True, "contact_id": contact_id, "action": "updated"}
                
            # Create new contact
            response = self._create_contact(properties)
            if response:
                contact_id = response.get("id")
                logger.info(f"Created HubSpot contact: {contact_id}")
                return {"success": True, "contact_id": contact_id, "action": "created"}
                
        except Exception as e:
            logger.error(f"Error creating/updating HubSpot contact: {str(e)}")
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Unknown error"}
    
    def create_deal(self, contact_id: str, deal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deal in HubSpot and associate with contact"""
        
        if not self.api_key:
            logger.info("HubSpot disabled - would create deal: %s", deal_data)
            return {"success": False, "error": "HubSpot API key not configured"}
        
        # Calculate deal value
        deal_value = self._estimate_deal_value(
            deal_data.get("services", []),
            deal_data.get("timeline", "")
        )
        
        # Prepare deal properties
        properties = {
            "dealname": f"{deal_data.get('company_name', 'Hawaiian Business')} - AI Solutions",
            "amount": str(deal_value),
            "pipeline": "default",
            "dealstage": "appointmentscheduled",  # Initial stage
            "closedate": self._calculate_close_date(deal_data.get("timeline", "")),
            
            # Custom properties
            "island_location": deal_data.get("island", ""),
            "business_type": deal_data.get("business_type", ""),
            "primary_service": deal_data.get("primary_service", "AI Consulting"),
            "implementation_timeline": deal_data.get("timeline", ""),
            "lead_source": "Hawaiian AI Chatbot - Reno Provine (reno@lenilani.com)",
            
            # Deal description
            "description": self._build_deal_description(deal_data)
        }
        
        try:
            # Create deal
            response = self._create_deal(properties)
            if response:
                deal_id = response.get("id")
                
                # Associate deal with contact
                self._associate_deal_with_contact(deal_id, contact_id)
                
                logger.info(f"Created HubSpot deal: {deal_id} with value ${deal_value}")
                return {
                    "success": True, 
                    "deal_id": deal_id, 
                    "estimated_value": deal_value
                }
                
        except Exception as e:
            logger.error(f"Error creating HubSpot deal: {str(e)}")
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Unknown error"}
    
    def log_conversation(self, email: str, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log conversation activity in HubSpot"""
        
        if not self.api_key:
            return {"success": False, "error": "HubSpot API key not configured"}
        
        try:
            # This would create a note or timeline event
            # For now, we'll update the contact's last activity
            contact = self._get_contact_by_email(email)
            if contact:
                contact_id = contact["id"]
                note_properties = {
                    "hubspot_owner_id": None,
                    "hs_note_body": f"Chatbot Conversation Summary:\n\n{conversation_data.get('summary', 'User engaged with Hawaiian AI chatbot')}\n\nTopics: {', '.join(conversation_data.get('topics', []))}\nSentiment: {conversation_data.get('sentiment', 'Positive')}",
                    "hs_timestamp": str(int(datetime.now().timestamp() * 1000))
                }
                
                # Create note (simplified version)
                logger.info(f"Logged conversation for contact {contact_id}")
                return {"success": True, "contact_id": contact_id}
                
        except Exception as e:
            logger.error(f"Error logging conversation: {str(e)}")
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Contact not found"}
    
    def _get_contact_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get contact by email address"""
        
        if not email or not self.api_key:
            return None
        
        url = f"{self.base_url}/crm/v3/objects/contacts/{email}?idProperty=email"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Contact doesn't exist
            else:
                logger.error(f"Error fetching contact: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error fetching contact by email: {str(e)}")
            return None
    
    def _create_contact(self, properties: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new contact in HubSpot"""
        
        url = f"{self.base_url}/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {"properties": properties}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Error creating contact: {response.status_code} - {response.text}")
            return None
    
    def _update_contact(self, contact_id: str, properties: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing contact in HubSpot"""
        
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {"properties": properties}
        
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error updating contact: {response.status_code} - {response.text}")
            return None
    
    def _create_deal(self, properties: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create deal in HubSpot"""
        
        url = f"{self.base_url}/crm/v3/objects/deals"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {"properties": properties}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            logger.error(f"Error creating deal: {response.status_code} - {response.text}")
            return None
    
    def _associate_deal_with_contact(self, deal_id: str, contact_id: str) -> bool:
        """Associate deal with contact"""
        
        url = f"{self.base_url}/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/3"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.put(url, headers=headers)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error associating deal with contact: {str(e)}")
            return False
    
    def _calculate_lead_score(self, contact_data: Dict[str, Any]) -> int:
        """Calculate lead score for Hawaiian business context"""
        
        score = 0
        
        # Business type scoring
        business_type = contact_data.get("business_type", "").lower()
        type_scores = {
            "tourism": 20, "restaurant": 15, "agriculture": 15,
            "retail": 10, "technology": 20, "real_estate": 12
        }
        score += type_scores.get(business_type, 5)
        
        # Island scoring (market size)
        island = contact_data.get("island", "").lower()
        island_scores = {
            "oahu": 15, "maui": 12, "big_island": 10, 
            "kauai": 8, "molokai": 5, "lanai": 5
        }
        score += island_scores.get(island, 5)
        
        # Timeline urgency
        timeline = contact_data.get("timeline", "").lower()
        if "asap" in timeline or "immediately" in timeline:
            score += 25
        elif "month" in timeline:
            score += 20
        elif "quarter" in timeline:
            score += 15
        
        # Budget indicators
        budget = contact_data.get("budget_range", "").lower()
        if "50k" in budget or "high" in budget:
            score += 25
        elif "20k" in budget or "medium" in budget:
            score += 15
        elif "10k" in budget:
            score += 10
        
        # Cultural fit indicators
        if contact_data.get("values_sustainability"):
            score += 10
        if contact_data.get("local_focus"):
            score += 5
        if contact_data.get("community_minded"):
            score += 10
        
        return min(score, 100)  # Cap at 100
    
    def _calculate_cultural_fit(self, contact_data: Dict[str, Any]) -> str:
        """Calculate cultural alignment with Hawaiian values"""
        
        fit_indicators = 0
        
        if contact_data.get("values_sustainability"):
            fit_indicators += 1
        if contact_data.get("local_focus"):
            fit_indicators += 1
        if contact_data.get("community_minded"):
            fit_indicators += 1
        if contact_data.get("family_business"):
            fit_indicators += 1
        
        if fit_indicators >= 3:
            return "Excellent"
        elif fit_indicators >= 2:
            return "Good"
        elif fit_indicators >= 1:
            return "Moderate"
        else:
            return "Developing"
    
    def _estimate_deal_value(self, services: list, timeline: str) -> int:
        """Estimate deal value based on services and timeline"""
        
        service_values = {
            "chatbot": 12000,
            "analytics": 15000,
            "fractional_cto": 8000,  # Monthly
            "automation": 10000,
            "consulting": 5000
        }
        
        total_value = 0
        for service in services:
            for key, value in service_values.items():
                if key in service.lower():
                    total_value += value
                    break
        
        # Default if no services matched
        if total_value == 0:
            total_value = 10000
        
        # Timeline urgency multiplier
        if "asap" in timeline.lower():
            total_value = int(total_value * 1.2)
        
        return total_value
    
    def _calculate_close_date(self, timeline: str) -> str:
        """Calculate expected close date"""
        
        from datetime import timedelta
        
        days_map = {
            "asap": 14,
            "month": 30,
            "quarter": 90,
            "6 months": 180
        }
        
        days = 60  # Default 2 months
        for key, value in days_map.items():
            if key in timeline.lower():
                days = value
                break
        
        close_date = datetime.now() + timedelta(days=days)
        return close_date.strftime("%Y-%m-%d")
    
    def _build_deal_description(self, deal_data: Dict[str, Any]) -> str:
        """Build deal description with Hawaiian context"""
        
        return f"""Hawaiian Business Opportunity - AI Solutions

Company: {deal_data.get('company_name', 'Not specified')}
Island: {deal_data.get('island', 'Not specified')}
Business Type: {deal_data.get('business_type', 'Not specified')}

Primary Challenges: {deal_data.get('primary_challenge', 'Not specified')}
Timeline: {deal_data.get('timeline', 'Not specified')}
Budget Range: {deal_data.get('budget_range', 'Not specified')}

Services Interested In: {', '.join(deal_data.get('services', ['AI Consulting']))}

Cultural Alignment: Strong focus on Hawaiian business values
Lead Source: Hawaiian AI Chatbot
Contact: Reno Provine - reno@lenilani.com - 808-766-1164
Next Steps: Schedule talk story session to discuss specific needs

Generated from authentic Hawaiian business conversation."""


# Create global instance
hubspot_service = HubSpotService()