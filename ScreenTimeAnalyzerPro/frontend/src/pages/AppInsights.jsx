import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Lightbulb, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react';
import { Doughnut } from 'react-chartjs-2';
import { api } from '../api/apiClient';

function AppInsights() {
  const [insights, setInsights] = useState(null);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [insightsRes, categoriesRes] = await Promise.all([
        api.getInsights(),
        api.getCategoryUsage(),
      ]);
      
      setInsights(insightsRes.data);
      setCategories(categoriesRes.data.categories);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching insights:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
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

  // Category chart data
  const categoryChartData = {
    labels: Object.keys(categories),
    datasets: [
      {
        data: Object.values(categories),
        backgroundColor: [
          'rgba(0, 170, 255, 0.8)',
          'rgba(255, 138, 0, 0.8)',
          'rgba(0, 255, 127, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(153, 102, 255, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
        borderColor: [
          'rgba(0, 170, 255, 1)',
          'rgba(255, 138, 0, 1)',
          'rgba(0, 255, 127, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const categoryChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
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
        <h1 className="text-3xl font-bold mb-2">App Insights</h1>
        <p className="text-gray-400">
          Productivity analysis and recommendations
        </p>
      </motion.div>

      {/* Productivity Score */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">Productivity Score</h2>
        </div>
        
        <div className="text-center py-8">
          <div className="inline-block relative">
            <svg className="w-48 h-48">
              <circle
                cx="96"
                cy="96"
                r="80"
                fill="none"
                stroke="rgba(255, 255, 255, 0.1)"
                strokeWidth="12"
              />
              <circle
                cx="96"
                cy="96"
                r="80"
                fill="none"
                stroke="var(--accent-color)"
                strokeWidth="12"
                strokeDasharray={`${(insights?.productivity_score || 0) * 502.4} 502.4`}
                strokeLinecap="round"
                transform="rotate(-90 96 96)"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <p className="text-5xl font-bold" style={{ color: 'var(--accent-color)' }}>
                  {Math.round((insights?.productivity_score || 0) * 100)}%
                </p>
                <p className="text-sm text-gray-400 mt-2">Productivity</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Category Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <h2 className="text-xl font-bold mb-6">Category Breakdown</h2>
        
        {Object.keys(categories).length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No data available</p>
          </div>
        ) : (
          <div className="h-80">
            <Doughnut data={categoryChartData} options={categoryChartOptions} />
          </div>
        )}
      </motion.div>

      {/* Top Apps */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Most Productive App */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle className="w-6 h-6 text-green-500" />
            <h2 className="text-xl font-bold">Most Productive</h2>
          </div>
          
          <div className="text-center py-6">
            <p className="text-3xl font-bold mb-2">
              {insights?.top_productive_app || 'N/A'}
            </p>
            <p className="text-sm text-gray-400">
              Keep up the great work!
            </p>
          </div>
        </motion.div>

        {/* Top Distraction */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-6 h-6 text-orange-500" />
            <h2 className="text-xl font-bold">Top Distraction</h2>
          </div>
          
          <div className="text-center py-6">
            <p className="text-3xl font-bold mb-2">
              {insights?.top_distraction || 'N/A'}
            </p>
            <p className="text-sm text-gray-400">
              Consider limiting usage
            </p>
          </div>
        </motion.div>
      </div>

      {/* Recommendations */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <Lightbulb className="w-6 h-6 text-yellow-500" />
          <h2 className="text-xl font-bold">Recommendations</h2>
        </div>
        
        {insights?.recommendations && insights.recommendations.length > 0 ? (
          <ul className="space-y-3">
            {insights.recommendations.map((rec, index) => (
              <li
                key={index}
                className="flex items-start gap-3 p-4 rounded-lg bg-white/5"
              >
                <div className="w-6 h-6 rounded-full bg-[var(--accent-color)] flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-sm font-bold">{index + 1}</span>
                </div>
                <p className="text-gray-300">{rec}</p>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-400">No recommendations available</p>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default AppInsights;

