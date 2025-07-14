import axios from 'axios';
import { io, Socket } from 'socket.io-client';
import { ChatResponse, BusinessQualification, HawaiianBusinessResponse } from '../types/chat';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:8000';

class ChatService {
  private apiClient = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  private socket: Socket | null = null;

  constructor() {
    // Add request interceptor for auth if needed
    this.apiClient.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('lenilani_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.apiClient.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
          localStorage.removeItem('lenilani_token');
        }
        return Promise.reject(error);
      }
    );
  }

  // REST API Methods
  async sendMessage(
    message: string,
    sessionId: string,
    userId?: string,
    metadata?: any
  ): Promise<ChatResponse> {
    try {
      console.log('Sending message to:', this.apiClient.defaults.baseURL + '/chat');
      console.log('Request data:', { message, session_id: sessionId, user_id: userId, metadata });
      
      const response = await this.apiClient.post<ChatResponse>('/chat', {
        message,
        session_id: sessionId,
        user_id: userId,
        metadata,
      });
      
      console.log('Response received:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error sending message:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      throw error;
    }
  }

  async qualifyBusiness(
    qualification: BusinessQualification
  ): Promise<HawaiianBusinessResponse> {
    try {
      const response = await this.apiClient.post<HawaiianBusinessResponse>(
        '/qualify-business',
        qualification
      );
      return response.data;
    } catch (error) {
      console.error('Error qualifying business:', error);
      throw error;
    }
  }

  async scheduleConsultation(consultationData: {
    name: string;
    email: string;
    phone?: string;
    company_name?: string;
    business_type?: string;
    island?: string;
    preferred_time?: string;
    message?: string;
  }): Promise<any> {
    try {
      const response = await this.apiClient.post(
        '/schedule-consultation',
        consultationData
      );
      return response.data;
    } catch (error) {
      console.error('Error scheduling consultation:', error);
      throw error;
    }
  }

  async getServices(): Promise<any> {
    try {
      const response = await this.apiClient.get('/services');
      return response.data;
    } catch (error) {
      console.error('Error fetching services:', error);
      throw error;
    }
  }

  async getIslandInsights(island: string): Promise<any> {
    try {
      const response = await this.apiClient.get(`/island-insights/${island}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching island insights:', error);
      throw error;
    }
  }

  // WebSocket Methods
  connectWebSocket(
    clientId: string,
    onMessage: (data: any) => void,
    onConnect?: () => void,
    onDisconnect?: () => void
  ) {
    if (this.socket?.connected) {
      return;
    }

    this.socket = io(WS_URL, {
      path: '/ws',
      query: { client_id: clientId },
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      onConnect?.();
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      onDisconnect?.();
    });

    this.socket.on('message', (data) => {
      onMessage(data);
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  disconnectWebSocket() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendWebSocketMessage(message: any) {
    if (this.socket?.connected) {
      this.socket.emit('message', message);
    } else {
      console.error('WebSocket not connected');
    }
  }

  // Utility Methods
  async checkHealth(): Promise<any> {
    try {
      const response = await this.apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  // Local Storage Methods
  saveConversation(sessionId: string, messages: any[]) {
    try {
      const conversations = this.getConversations();
      conversations[sessionId] = {
        messages,
        lastUpdated: new Date().toISOString(),
      };
      localStorage.setItem('lenilani_conversations', JSON.stringify(conversations));
    } catch (error) {
      console.error('Error saving conversation:', error);
    }
  }

  getConversations(): Record<string, any> {
    try {
      const stored = localStorage.getItem('lenilani_conversations');
      return stored ? JSON.parse(stored) : {};
    } catch (error) {
      console.error('Error retrieving conversations:', error);
      return {};
    }
  }

  clearConversations() {
    localStorage.removeItem('lenilani_conversations');
  }
}

export const chatService = new ChatService();