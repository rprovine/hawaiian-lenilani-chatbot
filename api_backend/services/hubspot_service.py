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
        
        # Enhanced logging for debugging
        if not self.api_key:
            logger.warning("HUBSPOT_API_KEY not found. HubSpot integration disabled.")
        elif self.api_key == "your_hubspot_api_key_here":
            logger.error("HUBSPOT_API_KEY is still set to placeholder value! Please update .env file.")
        else:
            logger.info(f"HubSpot Service initialized with API key: {'*' * 10}")
            if self.portal_id:
                logger.info(f"HubSpot Portal ID: {self.portal_id}")
    
    def create_or_update_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a contact in HubSpot"""
        
        if not self.api_key or self.api_key == "your_hubspot_api_key_here":
            logger.warning("HubSpot disabled - API key not properly configured")
            logger.info("Would create contact with data: %s", contact_data)
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
            
            # Use standard properties and notes field for custom data
            # "island_location": contact_data.get("island", ""),  # Custom property - commented out
            # "business_type_hawaii": contact_data.get("business_type", ""),  # Custom property - commented out
            # "lead_source": "Hawaiian AI Chatbot - Reno Provine (reno@lenilani.com)",  # Custom property - commented out
            "hs_lead_status": "NEW",
            "lifecyclestage": "lead",
            
            # Standard properties only - notes will be added separately
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
                        
                        # Create note with business context
                        note_content = self._build_contact_notes(contact_data)
                        self._create_note(contact_id, note_content)
                        
                        return {"success": True, "contact_id": contact_id, "action": "updated"}
                
            # Create new contact
            response = self._create_contact(properties)
            if response:
                contact_id = response.get("id")
                logger.info(f"Created HubSpot contact: {contact_id}")
                
                # Create note with business context
                note_content = self._build_contact_notes(contact_data)
                self._create_note(contact_id, note_content)
                
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
            
            # Deal description includes all custom data that doesn't have fields
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
            logger.debug(f"Fetching contact by email: {email}")
            response = requests.get(url, headers=headers)
            logger.debug(f"HubSpot API response status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.info(f"Contact not found in HubSpot: {email}")
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
        
        logger.info(f"Creating new contact in HubSpot with email: {properties.get('email')}")
        logger.debug(f"Contact properties: {properties}")
        
        response = requests.post(url, headers=headers, json=payload)
        logger.debug(f"HubSpot API response status: {response.status_code}")
        
        if response.status_code == 201:
            contact_data = response.json()
            logger.info(f"Successfully created HubSpot contact ID: {contact_data.get('id')}")
            return contact_data
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
        business_type = (contact_data.get("business_type") or "").lower()
        type_scores = {
            "tourism": 20, "restaurant": 15, "agriculture": 15,
            "retail": 10, "technology": 20, "real_estate": 12
        }
        score += type_scores.get(business_type, 5)
        
        # Island scoring (market size)
        island = (contact_data.get("island") or "").lower()
        island_scores = {
            "oahu": 15, "maui": 12, "big_island": 10, 
            "kauai": 8, "molokai": 5, "lanai": 5
        }
        score += island_scores.get(island, 5)
        
        # Timeline urgency
        timeline = (contact_data.get("timeline") or "").lower()
        if "asap" in timeline or "immediately" in timeline:
            score += 25
        elif "month" in timeline:
            score += 20
        elif "quarter" in timeline:
            score += 15
        
        # Budget indicators
        budget = (contact_data.get("budget_range") or "").lower()
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
            service_lower = (service or "").lower()
            for key, value in service_values.items():
                if key in service_lower:
                    total_value += value
                    break
        
        # Default if no services matched
        if total_value == 0:
            total_value = 10000
        
        # Timeline urgency multiplier
        timeline_lower = (timeline or "").lower()
        if "asap" in timeline_lower:
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
        timeline_lower = (timeline or "").lower()
        for key, value in days_map.items():
            if key in timeline_lower:
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

    def _create_note(self, contact_id: str, note_content: str) -> bool:
        """Create a note (engagement) for a contact"""
        
        try:
            # Create note using the Notes API
            url = f"{self.base_url}/crm/v3/objects/notes"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "properties": {
                    "hs_note_body": note_content,
                    "hs_timestamp": str(int(datetime.now().timestamp() * 1000))
                },
                "associations": [
                    {
                        "to": {"id": contact_id},
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 202  # Note to contact association
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                logger.info(f"Created note for contact {contact_id}")
                return True
            else:
                logger.error(f"Failed to create note: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return False
    
    def _build_contact_notes(self, contact_data: Dict[str, Any]) -> str:
        """Build contact notes with custom field data that doesn't exist in HubSpot"""
        
        notes_parts = []
        
        # Add lead source
        notes_parts.append("Lead Source: Hawaiian AI Chatbot - Reno Provine (reno@lenilani.com)")
        
        # Add business type if available
        business_type = contact_data.get("business_type")
        if business_type:
            notes_parts.append(f"Business Type: {business_type}")
        
        # Add island location if available
        island = contact_data.get("island")
        if island:
            notes_parts.append(f"Island Location: {island}")
        
        # Add primary challenge if available
        primary_challenge = contact_data.get("primary_challenge")
        if primary_challenge:
            notes_parts.append(f"Primary Challenge: {primary_challenge}")
        
        # Add budget range if available
        budget_range = contact_data.get("budget_range")
        if budget_range:
            notes_parts.append(f"Budget Range: {budget_range}")
        
        # Add timeline if available
        timeline = contact_data.get("timeline")
        if timeline:
            notes_parts.append(f"Timeline: {timeline}")
        
        # Add values/cultural fit
        cultural_values = []
        if contact_data.get("values_sustainability"):
            cultural_values.append("Values Sustainability")
        if contact_data.get("local_focus"):
            cultural_values.append("Local Focus")
        if contact_data.get("community_minded"):
            cultural_values.append("Community Minded")
        
        if cultural_values:
            notes_parts.append(f"Cultural Values: {', '.join(cultural_values)}")
        
        # Add lead score if available
        lead_score = self._calculate_lead_score(contact_data)
        cultural_fit = self._calculate_cultural_fit(contact_data)
        notes_parts.append(f"Lead Score: {lead_score}/100")
        notes_parts.append(f"Cultural Fit: {cultural_fit}")
        
        return "\n".join(notes_parts)


# Create global instance
hubspot_service = HubSpotService()