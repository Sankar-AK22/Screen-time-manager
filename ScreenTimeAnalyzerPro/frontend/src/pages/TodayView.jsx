import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, Filter } from 'lucide-react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { api } from '../api/apiClient';
import socketClient from '../api/socketClient';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function TodayView() {
  const [sessions, setSessions] = useState([]);
  const [hourlyData, setHourlyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'productive', 'entertainment'

  const fetchData = async () => {
    try {
      const [sessionsRes, hourlyRes] = await Promise.all([
        api.getTodayUsage(50, 0),
        api.getHourlyUsage(),
      ]);
      
      setSessions(sessionsRes.data);
      setHourlyData(hourlyRes.data.hourly);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Listen for session end events to refresh
    const handleSessionEnd = () => {
      fetchData();
    };

    socketClient.on('session_end', handleSessionEnd);

    return () => {
      socketClient.off('session_end', handleSessionEnd);
    };
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  };

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  // Hourly chart data
  const hourlyChartData = {
    labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
    datasets: [
      {
        label: 'Screen Time (minutes)',
        data: hourlyData.map(sec => Math.round(sec / 60)),
        backgroundColor: 'rgba(0, 170, 255, 0.6)',
        borderColor: 'rgba(0, 170, 255, 1)',
        borderWidth: 2,
      },
    ],
  };

  const hourlyChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
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
            return `${context.parsed.y} minutes`;
          },
        },
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#ffffff',
        },
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: '#ffffff',
        },
        beginAtZero: true,
      },
    },
  };

  // Filter sessions
  const filteredSessions = sessions.filter(session => {
    if (filter === 'all') return true;
    if (filter === 'productive') {
      return ['Development', 'Productivity', 'Design'].includes(session.category);
    }
    if (filter === 'entertainment') {
      return session.category === 'Entertainment';
    }
    return true;
  });

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
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold mb-2">Today's Activity</h1>
          <p className="text-gray-400">
            Detailed breakdown of your screen time
          </p>
        </div>
        <div className="flex items-center gap-2 text-gray-400">
          <Calendar className="w-5 h-5" />
          <span>{new Date().toLocaleDateString()}</span>
        </div>
      </motion.div>

      {/* Hourly Distribution Chart */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h2 className="text-xl font-bold mb-4">Hourly Distribution</h2>
        <div className="h-64">
          <Bar data={hourlyChartData} options={hourlyChartOptions} />
        </div>
      </motion.div>

      {/* Sessions List */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Sessions</h2>
          
          {/* Filter */}
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent-color)]"
            >
              <option value="all">All</option>
              <option value="productive">Productive</option>
              <option value="entertainment">Entertainment</option>
            </select>
          </div>
        </div>

        {filteredSessions.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No sessions found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>App</th>
                  <th>Window</th>
                  <th>Category</th>
                  <th>Start Time</th>
                  <th>Duration</th>
                </tr>
              </thead>
              <tbody>
                {filteredSessions.map((session, index) => (
                  <tr key={index}>
                    <td className="font-medium">{session.app_name}</td>
                    <td className="text-gray-400 max-w-xs truncate">
                      {session.window_title || 'N/A'}
                    </td>
                    <td>
                      <span className="px-2 py-1 rounded-full text-xs bg-white/10">
                        {session.category}
                      </span>
                    </td>
                    <td className="text-gray-400">
                      {formatDateTime(session.start_time)}
                    </td>
                    <td className="font-bold" style={{ color: 'var(--accent-color)' }}>
                      {formatTime(session.duration_sec)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default TodayView;

