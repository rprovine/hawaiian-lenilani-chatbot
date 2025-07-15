# HubSpot Integration Debug Guide

## Current Status

Based on the test results, here's what's happening:

### ✅ Working:
- Lead capture service is functioning
- Leads are being saved locally to `logs/leads/`
- Webhook integration is working (sending to webhook.site)
- Lead extraction from conversations is working

### ❌ Not Working:
- HubSpot API integration (API key is placeholder)
- Email notifications (Gmail credentials invalid)

## Why Leads Aren't Appearing in HubSpot

The main issue is that your `.env` file still has placeholder values:

```
HUBSPOT_API_KEY=your_hubspot_api_key_here  # ← This needs to be replaced
HUBSPOT_PORTAL_ID=your_portal_id           # ← This needs to be replaced
```

## How to Fix HubSpot Integration

### Step 1: Get Your HubSpot API Key

1. Log in to HubSpot: https://app.hubspot.com
2. Click the settings icon (gear) in the top navigation
3. In the left sidebar, navigate to: **Integrations** → **API Key**
4. Click "Generate API key" if you don't have one
5. Copy the API key (it starts with `pat-na1-` or similar)

### Step 2: Get Your Portal ID

1. In HubSpot, click your account name in the top right
2. You'll see your Portal ID (also called Hub ID) - it's a number like `12345678`

### Step 3: Update Your .env File

Replace the placeholders in your `.env` file:

```env
# HubSpot Integration
HUBSPOT_API_KEY=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
HUBSPOT_PORTAL_ID=12345678
```

### Step 4: Restart Your Application

After updating the `.env` file, restart your backend:

```bash
# If running locally
python run_backend.py

# Or if using the startup script
./start_backend.sh
```

## Testing the Integration

### 1. Test HubSpot Connection

```bash
python test_hubspot_integration.py
```

You should see:
- ✅ HubSpot API key is configured
- ✅ Successfully created HubSpot contact

### 2. Test Full Lead Capture

```bash
python test_full_lead_capture.py
```

### 3. Check HubSpot CRM

1. Go to HubSpot: https://app.hubspot.com
2. Navigate to **Contacts** → **Contacts**
3. Look for the test contacts created

## Viewing Captured Leads

Even without HubSpot configured, leads are being saved locally:

```bash
# View all captured leads
python show_leads.py

# View lead files directly
ls -la logs/leads/
```

## Enhanced Logging

The code has been updated with enhanced logging. To see detailed HubSpot API calls:

1. Set logging to DEBUG in your application
2. Watch the logs when a lead is captured
3. Look for messages like:
   - "Attempting to send lead to HubSpot..."
   - "Creating new contact in HubSpot with email..."
   - "HubSpot API response status..."

## Common Issues and Solutions

### Issue: "HubSpot API key not configured"
**Solution**: Update HUBSPOT_API_KEY in .env file

### Issue: API key is correct but still not working
**Check**:
1. API key has correct permissions (Contacts scope)
2. No extra spaces in the .env file
3. Portal ID matches your HubSpot account

### Issue: Contacts created but custom fields missing
**Solution**: Create custom properties in HubSpot:
- Go to Settings → Properties → Contact Properties
- Create: island_location, business_type_hawaii, etc.

## Alternative: Using Webhook Integration

If HubSpot API is not available, the webhook integration is working:

1. The webhook URL in `.env`: `LEAD_WEBHOOK_URL=https://webhook.site/...`
2. You can integrate with Zapier, Make.com, or n8n
3. These tools can then push to HubSpot, Google Sheets, etc.

## Email Notification Fix

To fix email notifications:

1. Use an App Password for Gmail (not your regular password)
2. Enable 2-factor authentication on your Google account
3. Generate app password: https://myaccount.google.com/apppasswords
4. Update `.env`:
   ```
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   ```

## Next Steps

1. **Immediate**: Update HubSpot API key in `.env`
2. **Test**: Run `python test_hubspot_integration.py`
3. **Verify**: Check HubSpot CRM for test contacts
4. **Optional**: Fix email notifications with Gmail app password
5. **Monitor**: Check `logs/leads/` directory for captured leads

## Support

If you're still having issues after following this guide:

1. Check the application logs for detailed error messages
2. Verify API key permissions in HubSpot
3. Test with a simple curl command to HubSpot API
4. Review the enhanced logging output