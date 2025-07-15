# Lead Capture Fix Documentation

## Problem Summary
The lead capture system was creating multiple partial leads for a single conversation instead of accumulating all contact information into one comprehensive lead record.

### Previous Behavior:
- Each time contact info was detected (name, email, phone), a NEW lead was created
- This resulted in fragmented data across multiple lead files
- A single user conversation could generate 3-4 separate lead files

### Fixed Behavior:
- Lead data is now stored in the conversation session
- Information accumulates as the conversation progresses
- Only ONE lead file is created per session when sufficient data is collected
- Duplicate lead creation is prevented with a `lead_captured` flag

## Technical Changes

### 1. Session Enhancement (`hawaiian_conversation_router.py`)
Added lead tracking to session state:
```python
"lead_data": {},          # Accumulates lead information
"lead_captured": False    # Prevents duplicate captures
```

### 2. Lead Extraction Rewrite
The `_extract_lead_info` method now:
- Retrieves existing lead data from session
- Updates only new/missing fields
- Stores accumulated data back in session
- Only triggers capture when sufficient data exists AND not already captured

### 3. Lead Capture Protection
The `_capture_lead` method now:
- Sets `lead_captured = True` after successful capture
- Stores the `lead_id` in session for reference
- Prevents any subsequent captures for the same session

### 4. New Features Added

#### Session Lead Data Endpoint
```
GET /session/{session_id}/lead-data
```
Returns current accumulated lead data for debugging.

#### Session End Endpoint
```
POST /session/{session_id}/end
```
Ends a session and captures any remaining lead data.

#### Enhanced Company Detection
Improved regex patterns to detect company names in various formats:
- "I own [Company Name]"
- "from [Company Name]"
- "[Company Name] company/business/restaurant"

## Testing

### Test Scripts Created:

1. **test_single_lead_capture.py**
   - Tests the accumulation of lead data
   - Verifies only one lead is created per session

2. **test_lead_accumulation.py**
   - HTTP-based test using the API endpoints
   - Shows the complete flow with debugging output

3. **check_leads.py**
   - Analyzes existing lead files
   - Identifies duplicates by email/phone/name
   - Shows recent leads

### How to Test:

1. Start the API server:
   ```bash
   python -m api_backend.main
   ```

2. Run the accumulation test:
   ```bash
   python test_lead_accumulation.py
   ```

3. Check lead files:
   ```bash
   python check_leads.py
   ```

## Usage Guidelines

### When Lead Capture Triggers:
Lead capture happens when BOTH conditions are met:
1. **Contact Info**: At least email OR phone number provided
2. **Context**: At least one of:
   - Name provided
   - Company provided
   - Business type identified
   - 3+ message exchanges

### Session Management:
- Sessions persist in memory (upgrade to Redis for production)
- Lead data accumulates throughout the conversation
- Only one lead captured per session
- Sessions can be explicitly ended to trigger final capture

### Best Practices:
1. Always use consistent `session_id` for a conversation
2. The chatbot naturally extracts information from conversation
3. No need to ask for all info at once
4. Lead quality score improves with more complete data

## Future Enhancements

1. **Redis Session Storage**: For production scalability
2. **Lead Enrichment**: Add more business context extraction
3. **Lead Scoring**: Enhance qualification algorithm
4. **Session Timeout**: Auto-capture leads after inactivity
5. **Lead Updates**: Allow updating existing leads in same session

## Troubleshooting

### No Lead Created:
- Check if session has both contact info AND context
- Verify session_id is consistent across messages
- Check logs for extraction patterns

### Duplicate Leads:
- Should not happen with fix
- Check `lead_captured` flag in session
- Run `check_leads.py` to identify duplicates

### Missing Information:
- Review regex patterns in `_extract_lead_info`
- Check if patterns match user's input format
- Enable DEBUG logging for detailed extraction info