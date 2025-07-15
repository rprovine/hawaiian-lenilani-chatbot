# HubSpot CRM Integration Setup Guide

## 🌺 Hawaiian Chatbot → HubSpot Integration

This guide will help you connect your Hawaiian AI Chatbot leads directly to HubSpot CRM.

## Prerequisites

1. HubSpot account (Free tier works!)
2. Access to your Render dashboard
3. About 10 minutes

## Step 1: Get Your HubSpot Private App Key

1. Log into [HubSpot](https://app.hubspot.com)
2. Go to **Settings** (gear icon)
3. Navigate to **Integrations** → **Private Apps**
4. Click **Create a private app**
5. Name it: "Hawaiian AI Chatbot Integration"
6. Go to **Scopes** tab and select:
   - `crm.objects.contacts.read`
   - `crm.objects.contacts.write`
   - `crm.objects.deals.read`
   - `crm.objects.deals.write`
7. Click **Create app**
8. Copy the **Access Token** (starts with `pat-`)

## Step 2: Add to Render Environment Variables

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your `hawaiian-lenilani-chatbot` service
3. Go to **Environment** tab
4. Add these variables:

```
HUBSPOT_API_KEY=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
HUBSPOT_PORTAL_ID=12345678
```

To find your Portal ID:
- In HubSpot, click the settings gear
- Look in the URL: `https://app.hubspot.com/settings/12345678/...`
- The number after `/settings/` is your Portal ID

5. Click **Save Changes**

## Step 3: Test the Integration

1. Visit your chatbot: https://aibothawaii.lenilani.com
2. Have a test conversation:
   - "I need help with my restaurant"
   - Provide a test email: test@example.com
   - Provide a phone: 808-555-0123
   - Mention your company name

3. Check HubSpot:
   - Go to **Contacts** in HubSpot
   - You should see the new contact!
   - If score > 70, a deal will also be created

## What Gets Sent to HubSpot

### Contact Fields:
- **Email** - Primary identifier
- **First Name** & **Last Name** - Parsed from name
- **Phone** - Phone number provided
- **Company** - Company name
- **Lead Source** - "Hawaiian AI Chatbot - Reno Provine"
- **Island Location** - Which Hawaiian island
- **Business Type** - Restaurant, Tourism, etc.
- **Primary Challenge** - Main business need
- **Lead Score** - 0-100 qualification score
- **Cultural Alignment** - Excellent/Good/Moderate

### Automatic Deal Creation (if score ≥ 70):
- **Deal Name** - "[Company] - AI Solutions"
- **Amount** - Estimated based on services
- **Pipeline Stage** - "Appointment Scheduled"
- **Close Date** - Based on timeline urgency

## Custom Properties (Optional)

To track Hawaiian-specific data, create these custom properties in HubSpot:

1. Go to **Settings** → **Properties** → **Contact Properties**
2. Create custom properties:
   - `island_location` (Dropdown: Oahu, Maui, Big Island, Kauai, Molokai, Lanai)
   - `business_type_hawaii` (Text)
   - `primary_challenge` (Text)
   - `budget_range` (Dropdown: Under $10k, $10k-$25k, $25k-$50k, Over $50k)
   - `cultural_alignment` (Dropdown: Excellent, Good, Moderate, Developing)

## Troubleshooting

### Leads not appearing in HubSpot?

1. Check Render logs:
   ```bash
   # In Render Shell
   grep -i "hubspot" logs/*.log
   ```

2. Verify API key is correct:
   - No extra spaces
   - Starts with `pat-`
   - Has proper scopes

3. Test the connection:
   ```python
   # In Render Shell
   python -c "
   import os
   key = os.getenv('HUBSPOT_API_KEY')
   print(f'Key configured: {\"Yes\" if key else \"No\"}')
   print(f'Key format valid: {\"Yes\" if key and key.startswith(\"pat-\") else \"No\"}')
   "
   ```

### Rate Limits

HubSpot Free Tier Limits:
- 100 API calls per 10 seconds
- 250,000 API calls per day

This is plenty for chatbot usage!

## Next Steps

1. **Create Views** in HubSpot:
   - Hot Leads (Score > 80)
   - Hawaiian Businesses by Island
   - This Week's Chatbot Leads

2. **Set Up Automation**:
   - Auto-assign hot leads to sales
   - Send welcome email to new contacts
   - Create tasks for follow-up

3. **Track Performance**:
   - Which islands generate most leads?
   - What business types convert best?
   - Average lead scores by source

## Support

Questions? Contact Reno:
- Email: reno@lenilani.com
- Phone: 808-766-1164

---

🌺 Aloha! Your leads will now flow automatically from chatbot to CRM!