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
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const api = {
  // Get current active app
  getActiveApp: () => apiClient.get('/active-app'),
  
  // Get daily summary
  getSummary: (date = null) => {
    const params = date ? { date } : {};
    return apiClient.get('/summary', { params });
  },
  
  // Get top apps
  getTopApps: (date = null, limit = 10) => {
    const params = { limit };
    if (date) params.date = date;
    return apiClient.get('/apps', { params });
  },
  
  // Get hourly distribution
  getHourlyDistribution: (date = null) => {
    const params = date ? { date } : {};
    return apiClient.get('/hourly', { params });
  },
  
  // Get insights
  getInsights: () => apiClient.get('/insights'),
  
  // Export to CSV
  exportCSV: (date = null) => {
    const params = date ? { date } : {};
    return apiClient.get('/export/csv', { 
      params,
      responseType: 'blob'
    });
  },
  
  // Export to PDF
  exportPDF: (date = null) => {
    const params = date ? { date } : {};
    return apiClient.get('/export/pdf', { 
      params,
      responseType: 'blob'
    });
  },
  
  // Get categories
  getCategories: () => apiClient.get('/categories'),
  
  // Update category
  updateCategory: (appName, category) => 
    apiClient.post(`/categories/${appName}`, { category }),
};

export default apiClient;

