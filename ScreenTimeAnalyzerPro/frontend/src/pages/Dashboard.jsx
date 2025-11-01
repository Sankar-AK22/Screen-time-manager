import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Clock, TrendingUp, Target, Zap } from 'lucide-react';
import LiveNowCard from '../components/LiveNowCard';
import TopAppsCard from '../components/TopAppsCard';
import { api } from '../api/apiClient';
import socketClient from '../api/socketClient';

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchSummary = async () => {
    try {
      const response = await api.getTodaySummary();
      setSummary(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching summary:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();

    // Poll for updates every 5 seconds
    const pollInterval = setInterval(fetchSummary, 5000);

    // Listen for summary updates from WebSocket (if connected)
    const handleSummaryUpdate = (data) => {
      if (data.today_total_sec !== undefined) {
        setSummary(prev => ({
          ...prev,
          total_seconds: data.today_total_sec,
        }));
      }
    };

    socketClient.on('summary_update', handleSummaryUpdate);

    return () => {
      clearInterval(pollInterval);
      socketClient.off('summary_update', handleSummaryUpdate);
    };
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
      return `${minutes}m`;
    } else {
      return `${seconds}s`;
    }
  };

  const formatPercentage = (value) => {
    return `${Math.round(value * 100)}%`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Title */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-400">
          Real-time overview of your screen time today
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Screen Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card stat-card"
        >
          <Clock className="w-8 h-8 mb-3" style={{ color: 'var(--accent-color)' }} />
          <p className="stat-label">Total Screen Time</p>
          <p className="stat-value">
            {summary ? formatTime(summary.total_seconds) : '0h 0m'}
          </p>
        </motion.div>

        {/* Productive Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card stat-card"
        >
          <Target className="w-8 h-8 mb-3 text-green-500" />
          <p className="stat-label">Productive Time</p>
          <p className="stat-value text-green-500">
            {summary ? formatTime(summary.productive_seconds) : '0h 0m'}
          </p>
        </motion.div>

        {/* Entertainment Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card stat-card"
        >
          <Zap className="w-8 h-8 mb-3 text-orange-500" />
          <p className="stat-label">Entertainment</p>
          <p className="stat-value text-orange-500">
            {summary ? formatTime(summary.entertainment_seconds) : '0h 0m'}
          </p>
        </motion.div>

        {/* Productivity Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card stat-card"
        >
          <TrendingUp className="w-8 h-8 mb-3 text-purple-500" />
          <p className="stat-label">Productivity Score</p>
          <p className="stat-value text-purple-500">
            {summary ? formatPercentage(summary.productivity_score) : '0%'}
          </p>
        </motion.div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Live Now Card */}
        <LiveNowCard />

        {/* Top Apps Card */}
        <TopAppsCard />
      </div>

      {/* Quick Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="glass-card p-6"
      >
        <h2 className="text-xl font-bold mb-4">Quick Info</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-white/5">
            <p className="text-sm text-gray-400 mb-1">Most Productive Hour</p>
            <p className="text-lg font-bold">
              {summary?.most_productive_hour || 'N/A'}
            </p>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <p className="text-sm text-gray-400 mb-1">Apps Used Today</p>
            <p className="text-lg font-bold">
              {summary?.unique_apps || 0}
            </p>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <p className="text-sm text-gray-400 mb-1">Sessions</p>
            <p className="text-lg font-bold">
              {summary?.total_sessions || 0}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default Dashboard;

