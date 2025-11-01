import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Tracking control
export const startTracking = async () => {
  const response = await api.post('/tracking/start');
  return response.data;
};

export const stopTracking = async () => {
  const response = await api.post('/tracking/stop');
  return response.data;
};

export const getTrackingStatus = async () => {
  const response = await api.get('/tracking/status');
  return response.data;
};

// Usage data
export const getUsageData = async (params = {}) => {
  const response = await api.get('/usage', { params });
  return response.data;
};

export const getCurrentUsage = async () => {
  const response = await api.get('/usage/current');
  return response.data;
};

// Statistics
export const getStatistics = async (period = 'today') => {
  const response = await api.get('/stats', { params: { period } });
  return response.data;
};

export const getDailySummaries = async (days = 7) => {
  const response = await api.get('/stats/daily', { params: { days } });
  return response.data;
};

// Reports
export const generateReport = async (reportData) => {
  const response = await api.post('/report', reportData);
  return response.data;
};

// Summary
export const getSummary = async () => {
  const response = await api.get('/summary');
  return response.data;
};

// Categories
export const getCategories = async () => {
  const response = await api.get('/categories');
  return response.data;
};

export const createCategory = async (categoryData) => {
  const response = await api.post('/categories', categoryData);
  return response.data;
};

export default api;

