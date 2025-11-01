/**
 * REST API client for ScreenTime Analyzer Pro.
 */

import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`📤 API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`📥 API Response: ${response.config.url}`, response.status);
    return response;
  },
  (error) => {
    console.error(`❌ API Error: ${error.config?.url}`, error.message);
    return Promise.reject(error);
  }
);

/**
 * API methods
 */
export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // Summary endpoints
  getTodaySummary: () => apiClient.get('/summary/today'),
  getSummaryByDate: (date) => apiClient.get(`/summary/${date}`),

  // Usage endpoints
  getTodayUsage: (limit = 100, offset = 0) =>
    apiClient.get('/usage/today', { params: { limit, offset } }),
  
  getTopApps: (limit = 5) =>
    apiClient.get('/usage/top', { params: { limit } }),
  
  getHourlyUsage: () => apiClient.get('/usage/hourly'),
  
  getCategoryUsage: () => apiClient.get('/usage/categories'),

  // Insights
  getInsights: () => apiClient.get('/insights'),

  // Current session
  getCurrentSession: () => apiClient.get('/current'),

  // Export
  exportCSV: (date = null) => {
    const params = date ? { date_str: date } : {};
    return apiClient.get('/export/csv', {
      params,
      responseType: 'blob',
    });
  },
};

export default apiClient;

