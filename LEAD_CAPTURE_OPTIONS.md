# Lead Capture Options - Choose What Works Best

## 🚀 Quick Start Options (No Email Setup Required)

### Option 1: Webhook (Easiest - Works with Zapier, Make, etc.)

1. **Get a webhook URL** from:
   - [Webhook.site](https://webhook.site) - Free testing
   - [Zapier Webhooks](https://zapier.com/apps/webhook/integrations) - Connect to 5000+ apps
   - [Make (Integromat)](https://www.make.com) - Visual automation
   - [RequestBin](https://requestbin.com) - Free testing

2. **Add to .env**:
   ```
   LEAD_WEBHOOK_URL=https://hook.zapier.com/your-webhook-url
   LEAD_WEBHOOK_SECRET=optional-secret-for-security
   ```

3. **What gets sent**:
   ```json
   {
     "name": "John Doe",
     "email": "john@example.com",
     "phone": "808-555-1234",
     "business_type": "Restaurant",
     "location": "Maui",
     "lead_score": 85,
     "lead_quality": "🔥 HOT - Ready to buy",
     "recommended_action": "URGENT: Call within 1 hour"
   }
   ```

### Option 2: Local JSON Files (Simplest)

Leads are automatically saved to `logs/leads/` directory as JSON files.
- No setup required
- Check the folder periodically
- Each lead is a separate JSON file with timestamp

### Option 3: View in Backend Logs

Run this to see leads in real-time:
```bash
tail -f logs/hawaiian_chatbot.log | grep -i "lead"
```

## 📧 Email Setup (Gmail)

If you want email notifications:

1. **Enable 2-Factor Auth** on your Gmail account

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail"
   - Copy the 16-character password

3. **Update .env**:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   LEAD_EMAIL=reno@lenilani.com
   ```

## 🔗 HubSpot Integration

### Using HubSpot Forms:
```
HUBSPOT_PORTAL_ID=your-portal-id
HUBSPOT_FORM_GUID=your-form-guid
```

### Using HubSpot API:
```
HUBSPOT_API_KEY=your-private-app-token
```

## 🎯 Zapier Automation Ideas

With webhook URL, you can automatically:
- Send SMS via Twilio when HOT lead comes in
- Create Google Sheet row for each lead
- Send Slack notification for qualified leads
- Add to your CRM (Salesforce, Pipedrive, etc.)
- Create Trello/Asana task for follow-up
- Send to Discord/Teams channel

## 🧪 Testing Your Setup

1. **Test webhook**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "My email is test@example.com, phone 808-555-1234", "session_id": "test"}'
   ```

2. **Check if lead was captured**:
   - Webhook: Check your webhook URL dashboard
   - Email: Check your inbox
   - Local: Check `logs/leads/` folder

## 📊 Lead Scoring Reminder

- **80-100**: 🔥 HOT - Call within 1 hour
- **60-79**: 🌟 WARM - Call within 24 hours
- **40-59**: 💫 COOL - Follow up in 2-3 days
- **0-39**: ❄️ COLD - Add to nurture campaign

## ⚡ No Technical Setup Required

If you don't want to deal with any setup:
1. Leads are automatically saved locally
2. Check `logs/leads/` folder daily
3. Each file contains complete lead information