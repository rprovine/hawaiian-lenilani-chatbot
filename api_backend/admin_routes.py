"""
Admin routes for lead management
Secure endpoints for viewing and exporting leads
"""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse, StreamingResponse
import secrets
import csv
import io

# Create router
router = APIRouter(prefix="/admin", tags=["admin"])

# Basic auth for security
security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify admin credentials"""
    # Get credentials from environment
    correct_username = os.getenv("ADMIN_USERNAME", "admin")
    correct_password = os.getenv("ADMIN_PASSWORD", "")
    
    if not correct_password:
        raise HTTPException(
            status_code=500,
            detail="Admin password not configured"
        )
    
    # Verify credentials
    is_valid_username = secrets.compare_digest(
        credentials.username.encode("utf8"),
        correct_username.encode("utf8")
    )
    is_valid_password = secrets.compare_digest(
        credentials.password.encode("utf8"),
        correct_password.encode("utf8")
    )
    
    if not (is_valid_username and is_valid_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username

@router.get("/leads")
async def get_leads(
    username: str = Depends(verify_credentials),
    limit: int = Query(100, description="Maximum number of leads to return"),
    quality: Optional[str] = Query(None, description="Filter by quality: hot, warm, cold")
):
    """Get all captured leads"""
    leads_dir = Path("logs/leads")
    
    if not leads_dir.exists():
        return {"leads": [], "total": 0, "message": "No leads directory found"}
    
    leads = []
    lead_files = sorted(leads_dir.glob("lead_*.json"), reverse=True)
    
    for lead_file in lead_files[:limit]:
        try:
            with open(lead_file, 'r') as f:
                lead = json.load(f)
                
                # Apply quality filter if specified
                if quality:
                    lead_quality = lead.get('lead_quality', '').lower()
                    if quality.lower() not in lead_quality:
                        continue
                
                leads.append(lead)
        except Exception as e:
            continue
    
    # Calculate summary stats
    summary = {
        "total": len(leads),
        "hot": sum(1 for l in leads if 'HOT' in l.get('lead_quality', '')),
        "warm": sum(1 for l in leads if 'WARM' in l.get('lead_quality', '')),
        "cold": sum(1 for l in leads if 'COLD' in l.get('lead_quality', '')),
    }
    
    return {
        "leads": leads,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/leads/export")
async def export_leads(
    username: str = Depends(verify_credentials),
    format: str = Query("json", description="Export format: json or csv")
):
    """Export all leads as JSON or CSV"""
    leads_dir = Path("logs/leads")
    
    if not leads_dir.exists():
        raise HTTPException(status_code=404, detail="No leads found")
    
    leads = []
    lead_files = sorted(leads_dir.glob("lead_*.json"), reverse=True)
    
    for lead_file in lead_files:
        try:
            with open(lead_file, 'r') as f:
                leads.append(json.load(f))
        except:
            continue
    
    if format.lower() == "csv":
        # Create CSV in memory
        output = io.StringIO()
        
        if leads:
            fieldnames = [
                'lead_id', 'captured_at', 'name', 'email', 'phone',
                'company', 'business_type', 'location', 'main_challenge',
                'budget_range', 'qualification_score', 'lead_quality',
                'conversation_summary'
            ]
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for lead in leads:
                writer.writerow({k: lead.get(k, '') for k in fieldnames})
        
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=leads_export_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )
    
    else:
        # Return JSON
        return JSONResponse(
            content={
                "leads": leads,
                "total": len(leads),
                "exported_at": datetime.now().isoformat()
            },
            headers={
                "Content-Disposition": f"attachment; filename=leads_export_{datetime.now().strftime('%Y%m%d')}.json"
            }
        )

@router.get("/leads/{lead_id}")
async def get_lead(
    lead_id: str,
    username: str = Depends(verify_credentials)
):
    """Get a specific lead by ID"""
    lead_file = Path(f"logs/leads/{lead_id}.json")
    
    if not lead_file.exists():
        raise HTTPException(status_code=404, detail="Lead not found")
    
    try:
        with open(lead_file, 'r') as f:
            lead = json.load(f)
        return lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading lead: {str(e)}")

@router.delete("/leads/{lead_id}")
async def delete_lead(
    lead_id: str,
    username: str = Depends(verify_credentials)
):
    """Delete a specific lead"""
    lead_file = Path(f"logs/leads/{lead_id}.json")
    
    if not lead_file.exists():
        raise HTTPException(status_code=404, detail="Lead not found")
    
    try:
        lead_file.unlink()
        return {"message": f"Lead {lead_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting lead: {str(e)}")

@router.get("/stats")
async def get_stats(username: str = Depends(verify_credentials)):
    """Get chatbot statistics"""
    leads_dir = Path("logs/leads")
    
    stats = {
        "leads": {
            "total": 0,
            "by_quality": {"hot": 0, "warm": 0, "cold": 0},
            "by_location": {},
            "by_business_type": {},
            "last_captured": None
        }
    }
    
    if leads_dir.exists():
        lead_files = list(leads_dir.glob("lead_*.json"))
        stats["leads"]["total"] = len(lead_files)
        
        # Get most recent lead time
        if lead_files:
            most_recent = max(lead_files, key=lambda f: f.stat().st_mtime)
            stats["leads"]["last_captured"] = datetime.fromtimestamp(
                most_recent.stat().st_mtime
            ).isoformat()
        
        # Analyze leads
        for lead_file in lead_files:
            try:
                with open(lead_file, 'r') as f:
                    lead = json.load(f)
                    
                    # Quality
                    if 'HOT' in lead.get('lead_quality', ''):
                        stats["leads"]["by_quality"]["hot"] += 1
                    elif 'WARM' in lead.get('lead_quality', ''):
                        stats["leads"]["by_quality"]["warm"] += 1
                    else:
                        stats["leads"]["by_quality"]["cold"] += 1
                    
                    # Location
                    location = lead.get('location', 'Unknown')
                    stats["leads"]["by_location"][location] = \
                        stats["leads"]["by_location"].get(location, 0) + 1
                    
                    # Business type
                    btype = lead.get('business_type', 'Unknown')
                    stats["leads"]["by_business_type"][btype] = \
                        stats["leads"]["by_business_type"].get(btype, 0) + 1
            except:
                continue
    
    return stats