import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp } from 'lucide-react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { api } from '../api/apiClient';
import socketClient from '../api/socketClient';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

function TopAppsCard() {
  const [topApps, setTopApps] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTopApps = async () => {
    try {
      const response = await api.getTopApps(5);
      setTopApps(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching top apps:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTopApps();

    // Poll for updates every 5 seconds
    const pollInterval = setInterval(fetchTopApps, 5000);

    // Listen for summary updates from WebSocket (if connected)
    const handleSummaryUpdate = (data) => {
      if (data.top_apps) {
        setTopApps(data.top_apps.map(app => ({
          app: app.app,
          total_seconds: app.sec,
        })));
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

  const chartData = {
    labels: topApps.map(app => app.app),
    datasets: [
      {
        data: topApps.map(app => app.total_seconds),
        backgroundColor: [
          'rgba(0, 170, 255, 0.8)',
          'rgba(255, 138, 0, 0.8)',
          'rgba(0, 255, 127, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(153, 102, 255, 0.8)',
        ],
        borderColor: [
          'rgba(0, 170, 255, 1)',
          'rgba(255, 138, 0, 1)',
          'rgba(0, 255, 127, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#ffffff',
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#ffffff',
        bodyColor: '#ffffff',
        borderColor: 'var(--accent-color)',
        borderWidth: 1,
        padding: 12,
        displayColors: true,
        callbacks: {
          label: function (context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            return `${label}: ${formatTime(value)}`;
          },
        },
      },
    },
  };

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">Top Apps</h2>
        </div>
        <div className="flex items-center justify-center h-64">
          <div className="spinner" />
        </div>
      </motion.div>
    );
  }

  if (topApps.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">Top Apps</h2>
        </div>
        <div className="text-center py-8">
          <p className="text-gray-400">No data available</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <TrendingUp className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
        <h2 className="text-xl font-bold">Top Apps</h2>
      </div>

      {/* Chart */}
      <div className="h-64 mb-6">
        <Pie data={chartData} options={chartOptions} />
      </div>

      {/* List */}
      <div className="space-y-3">
        {topApps.map((app, index) => (
          <div
            key={app.app}
            className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold"
                style={{
                  backgroundColor: chartData.datasets[0].backgroundColor[index],
                }}
              >
                {index + 1}
              </div>
              <span className="font-medium">{app.app}</span>
            </div>
            <span className="text-[var(--accent-color)] font-bold">
              {formatTime(app.total_seconds)}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

export default TopAppsCard;

