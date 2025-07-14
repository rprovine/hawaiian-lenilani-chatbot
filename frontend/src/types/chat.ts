export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  metadata?: {
    intent?: string;
    confidence?: number;
    cultural_context?: any;
    [key: string]: any;
  };
}

export interface QuickReply {
  text: string;
  action?: () => void;
}

export interface ChatState {
  sessionId: string;
  userId: string;
  context: {
    businessType?: string;
    island?: string;
    challenges?: string[];
    lastIntent?: string;
    [key: string]: any;
  };
}

export interface ChatResponse {
  response: string;
  metadata?: {
    cultural_context?: any;
    timestamp?: string;
    intent?: string;
    confidence?: number;
    [key: string]: any;
  };
  suggestions?: string[];
  quick_replies?: string[];
}

export interface BusinessQualification {
  business_type: string;
  island: string;
  challenges: string[];
  budget_range?: string;
  timeline?: string;
  contact_info?: {
    name?: string;
    email?: string;
    phone?: string;
    company_name?: string;
  };
}

export interface ServiceRecommendation {
  service_type: string;
  service_name: string;
  description: string;
  relevance_score: number;
  estimated_roi: string;
  implementation_time: string;
  price_range: string;
  local_examples: string[];
  why_recommended: string[];
  cultural_fit: string;
}

export interface IslandContext {
  island: string;
  market_conditions: Record<string, string>;
  opportunities: string[];
  challenges: string[];
  competitive_landscape: string;
  seasonal_patterns: Record<string, string>;
  cultural_considerations: string[];
  success_factors: string[];
}

export interface HawaiianBusinessResponse {
  inquiry_id: string;
  recommendations: ServiceRecommendation[];
  island_insights: IslandContext;
  estimated_total_investment: string;
  implementation_roadmap: Array<Record<string, string>>;
  expected_outcomes: string[];
  local_references: Array<Record<string, string>>;
  cultural_notes: string[];
  next_steps: string[];
  created_at: string;
}