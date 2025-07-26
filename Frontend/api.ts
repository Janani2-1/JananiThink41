import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatRequest {
  message: string;
  session_id?: string;
  user_id?: string;
  context?: Record<string, any>;
}

export interface ChatResponse {
  message: string;
  session_id: string;
  timestamp: string;
  suggestions?: string[];
  quick_replies?: string[];
  metadata?: Record<string, any>;
}

export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await api.post('/api/chat', request);
    return response.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
};

export const startChat = async (): Promise<ChatResponse> => {
  try {
    const response = await api.post('/api/chat/start');
    return response.data;
  } catch (error) {
    console.error('Error starting chat:', error);
    throw error;
  }
};

export const getChatHistory = async (sessionId: string, limit: number = 50) => {
  try {
    const response = await api.get(`/api/chat/session/${sessionId}/history?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw error;
  }
};

export const endChatSession = async (sessionId: string) => {
  try {
    const response = await api.delete(`/api/chat/session/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error ending chat session:', error);
    throw error;
  }
};

// Product API
export const getProducts = async (params?: {
  query?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  colors?: string[];
  sizes?: string[];
  in_stock_only?: boolean;
  page?: number;
  limit?: number;
}) => {
  try {
    const response = await api.get('/api/products', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

export const getProduct = async (productId: string) => {
  try {
    const response = await api.get(`/api/products/${productId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

// Order API
export const getOrders = async (params?: {
  user_id?: string;
  status?: string;
}) => {
  try {
    const response = await api.get('/api/orders', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
};

export const getOrder = async (orderId: string) => {
  try {
    const response = await api.get(`/api/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching order:', error);
    throw error;
  }
};

export const getOrderTracking = async (orderId: string) => {
  try {
    const response = await api.get(`/api/orders/${orderId}/tracking`);
    return response.data;
  } catch (error) {
    console.error('Error fetching order tracking:', error);
    throw error;
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

// Training API
export const getTrainingStatus = async () => {
  try {
    const response = await api.get('/api/training/status');
    return response.data;
  } catch (error) {
    console.error('Error getting training status:', error);
    throw error;
  }
};

export const retrainChatbot = async () => {
  try {
    const response = await api.post('/api/training/retrain');
    return response.data;
  } catch (error) {
    console.error('Error retraining chatbot:', error);
    throw error;
  }
};

export const getTrainingAnalytics = async () => {
  try {
    const response = await api.get('/api/training/analytics');
    return response.data;
  } catch (error) {
    console.error('Error getting training analytics:', error);
    throw error;
  }
};

export const getTrainingKnowledge = async () => {
  try {
    const response = await api.get('/api/training/knowledge');
    return response.data;
  } catch (error) {
    console.error('Error getting training knowledge:', error);
    throw error;
  }
};

export const getTrainingScenarios = async () => {
  try {
    const response = await api.get('/api/training/scenarios');
    return response.data;
  } catch (error) {
    console.error('Error getting training scenarios:', error);
    throw error;
  }
};

export const testTrainingResponse = async (message: string) => {
  try {
    const response = await api.post('/api/training/test', { message });
    return response.data;
  } catch (error) {
    console.error('Error testing training response:', error);
    throw error;
  }
}; 