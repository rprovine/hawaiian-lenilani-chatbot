# Lead Capture Setup Guide

## Overview
The chatbot automatically captures and sends qualified leads to you via email and/or HubSpot CRM.

## Lead Qualification Scoring

The system scores leads from 0-100 based on:
- **Contact Info (30 points)**
  - Email provided: +20 points
  - Phone provided: +10 points
- **Business Details (30 points)**
  - Business type identified: +10 points
  - Location/island specified: +10 points
  - Main challenge discussed: +10 points
- **Engagement Level (40 points)**
  - 5+ messages exchanged: +40 points
  - 3-4 messages: +25 points
  - 2 messages: +15 points

### Lead Quality Ratings:
- 🔥 **HOT (80-100)**: Ready to buy - call within 1 hour
- 🌟 **WARM (60-79)**: High interest - call within 24 hours
- 💫 **COOL (40-59)**: Needs nurturing - follow up in 2-3 days
- ❄️ **COLD (0-39)**: Early stage - add to nurture campaign

## Email Setup

### 1. Gmail Setup (Recommended)
Add these to your `.env` file:
```
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
LEAD_EMAIL=reno@lenilani.com
```

**Important**: Use an App Password, not your regular Gmail password:
1. Go to https://myaccount.google.com/security
2. Enable 2-factor authentication
3. Generate an App Password for "Mail"
4. Use that password in SMTP_PASSWORD

### 2. Other Email Providers
```
# SendGrid
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key

# Office 365
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

## HubSpot Setup

### Option 1: Using HubSpot Forms (Easier)
1. Create a form in HubSpot with these fields:
   - Email
   - First Name
   - Last Name
   - Phone
   - Company
   - Lead Quality
   - Business Type
   - Main Challenge

2. Get the form details:
   - Go to Marketing > Forms
   - Click on your form
   - Click "Share" 
   - Copy the Form GUID from the embed code

3. Add to `.env`:
```
HUBSPOT_PORTAL_ID=your-portal-id
HUBSPOT_FORM_GUID=your-form-guid
```

### Option 2: Using HubSpot API (More Control)
1. Get your API key:
   - Go to Settings > Integrations > API Key
   - Generate a key

2. Add to `.env`:
```
HUBSPOT_API_KEY=your-private-app-token
```

## Testing Lead Capture

1. Test with a sample conversation:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My email is test@example.com and phone is 808-555-1234",
    "session_id": "test-lead"
  }'
```

2. Check your email for the lead notification

3. Check HubSpot for the new contact

## Lead Notification Email Format

When a lead is captured, you'll receive an email like this:

```
Subject: 🌺 New Lead: John Doe - Restaurant

Lead Quality: 🔥 HOT - Ready to buy

Contact Information:
- Name: John Doe
- Email: john@example.com
- Phone: 808-555-1234
- Company: Doe's Diner

Business Details:
- Type: Restaurant
- Location: Maui
- Challenge: Inventory waste
- Budget Range: $5,000-$12,000

Conversation Summary:
Business: restaurant | Location: Maui | Main challenge: inventory waste | Messages exchanged: 6

Recommended Next Steps:
Call within 1 hour! This lead is ready to move forward.
```

## Automatic Lead Capture Triggers

Leads are automatically captured when:
1. User provides email or phone number
2. Conversation exceeds 6 messages (engaged prospect)
3. User explicitly asks to schedule consultation
4. User asks about pricing and continues engaging

## Privacy & Compliance

- All lead data is stored securely
- Email/phone extraction only happens from user-provided info
- Leads are logged locally in `logs/leads/` directory
- GDPR/privacy compliance through consent in chat

## Troubleshooting

### Emails not sending:
- Check SMTP credentials in .env
- Verify "Less secure app access" or App Password for Gmail
- Check firewall isn't blocking SMTP ports

### HubSpot not receiving:
- Verify API key has correct permissions
- Check form GUID matches exactly
- Test API connection with: `curl https://api.hubapi.com/crm/v3/objects/contacts -H "Authorization: Bearer YOUR_API_KEY"`

### Lead not captured:
- Check logs: `tail -f logs/hawaiian_chatbot.log`
- Verify lead has enough qualification points
- Check email/phone regex patterns match your format