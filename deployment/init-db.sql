-- Hawaiian LeniLani Chatbot Database Initialization

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone to Hawaii
SET TIME ZONE 'Pacific/Honolulu';

-- Create schemas
CREATE SCHEMA IF NOT EXISTS chatbot;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create custom types
CREATE TYPE chatbot.business_type AS ENUM (
    'tourism',
    'restaurant',
    'agriculture',
    'retail',
    'hospitality',
    'technology',
    'real_estate',
    'healthcare',
    'education',
    'other'
);

CREATE TYPE chatbot.island AS ENUM (
    'oahu',
    'maui',
    'big_island',
    'kauai',
    'molokai',
    'lanai'
);

CREATE TYPE chatbot.conversation_status AS ENUM (
    'active',
    'completed',
    'abandoned',
    'transferred'
);

-- Conversations table
CREATE TABLE chatbot.conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    status chatbot.conversation_status DEFAULT 'active',
    island chatbot.island,
    business_type chatbot.business_type,
    qualification_score DECIMAL(3,2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE chatbot.messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chatbot.conversations(id) ON DELETE CASCADE,
    sender VARCHAR(50) NOT NULL CHECK (sender IN ('user', 'bot')),
    message TEXT NOT NULL,
    intent VARCHAR(100),
    confidence DECIMAL(3,2),
    entities JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Leads table
CREATE TABLE chatbot.leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chatbot.conversations(id),
    email VARCHAR(255),
    phone VARCHAR(50),
    name VARCHAR(255),
    company_name VARCHAR(255),
    island chatbot.island,
    business_type chatbot.business_type,
    challenges TEXT[],
    budget_range VARCHAR(50),
    timeline VARCHAR(50),
    qualification_status VARCHAR(50),
    hubspot_contact_id VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE chatbot.appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES chatbot.leads(id),
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    meeting_type VARCHAR(50),
    google_event_id VARCHAR(255),
    meeting_link TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analytics events table
CREATE TABLE analytics.events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chatbot.conversations(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Service recommendations table
CREATE TABLE chatbot.recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chatbot.conversations(id),
    lead_id UUID REFERENCES chatbot.leads(id),
    service_type VARCHAR(100) NOT NULL,
    relevance_score DECIMAL(3,2),
    estimated_value DECIMAL(10,2),
    reasons TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Cultural insights table
CREATE TABLE chatbot.cultural_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chatbot.conversations(id),
    used_pidgin BOOLEAN DEFAULT FALSE,
    mentioned_values TEXT[],
    cultural_score INTEGER,
    island_specific_topics TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_conversations_session_id ON chatbot.conversations(session_id);
CREATE INDEX idx_conversations_user_id ON chatbot.conversations(user_id);
CREATE INDEX idx_conversations_status ON chatbot.conversations(status);
CREATE INDEX idx_conversations_created_at ON chatbot.conversations(created_at);

CREATE INDEX idx_messages_conversation_id ON chatbot.messages(conversation_id);
CREATE INDEX idx_messages_created_at ON chatbot.messages(created_at);
CREATE INDEX idx_messages_intent ON chatbot.messages(intent);

CREATE INDEX idx_leads_email ON chatbot.leads(email);
CREATE INDEX idx_leads_island ON chatbot.leads(island);
CREATE INDEX idx_leads_business_type ON chatbot.leads(business_type);
CREATE INDEX idx_leads_created_at ON chatbot.leads(created_at);

CREATE INDEX idx_appointments_scheduled_at ON chatbot.appointments(scheduled_at);
CREATE INDEX idx_appointments_lead_id ON chatbot.appointments(lead_id);

CREATE INDEX idx_events_conversation_id ON analytics.events(conversation_id);
CREATE INDEX idx_events_event_type ON analytics.events(event_type);
CREATE INDEX idx_events_created_at ON analytics.events(created_at);

-- Create update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON chatbot.conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON chatbot.leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON chatbot.appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for analytics
CREATE VIEW analytics.daily_conversations AS
SELECT 
    DATE(created_at AT TIME ZONE 'Pacific/Honolulu') as date,
    COUNT(*) as total_conversations,
    COUNT(DISTINCT user_id) as unique_users,
    AVG(CASE WHEN qualification_score IS NOT NULL THEN qualification_score ELSE 0 END) as avg_qualification_score,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_conversations
FROM chatbot.conversations
GROUP BY DATE(created_at AT TIME ZONE 'Pacific/Honolulu');

CREATE VIEW analytics.island_metrics AS
SELECT 
    island,
    COUNT(*) as total_conversations,
    COUNT(DISTINCT CASE WHEN l.id IS NOT NULL THEN c.id END) as converted_leads,
    AVG(c.qualification_score) as avg_qualification_score
FROM chatbot.conversations c
LEFT JOIN chatbot.leads l ON c.id = l.conversation_id
WHERE island IS NOT NULL
GROUP BY island;

CREATE VIEW analytics.service_performance AS
SELECT 
    r.service_type,
    COUNT(*) as times_recommended,
    AVG(r.relevance_score) as avg_relevance_score,
    AVG(r.estimated_value) as avg_estimated_value,
    COUNT(DISTINCT l.id) as unique_leads
FROM chatbot.recommendations r
JOIN chatbot.leads l ON r.lead_id = l.id
GROUP BY r.service_type;

-- Insert initial data
INSERT INTO analytics.events (event_type, event_data) 
VALUES ('system_initialized', '{"message": "Hawaiian LeniLani Chatbot Database Initialized", "version": "1.0.0"}');

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA chatbot TO lenilani;
GRANT ALL PRIVILEGES ON SCHEMA analytics TO lenilani;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA chatbot TO lenilani;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO lenilani;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA chatbot TO lenilani;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO lenilani;