import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../api/apiClient';

function Insights() {
  const [insights, setInsights] = useState(null);
  const [hourly, setHourly] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [insightsRes, hourlyRes] = await Promise.all([
        api.getInsights(),
        api.getHourlyDistribution()
      ]);
      
      setInsights(insightsRes.data);
      setHourly(hourlyRes.data.hourly || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching insights:', error);
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
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
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-2">
          <BarChart3 className="w-8 h-8 text-accent" />
          <h1 className="text-4xl font-bold">Insights</h1>
        </div>
        <p className="text-gray-400">Compare your usage and discover patterns</p>
      </motion.div>

      {/* Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6"
        >
          <h3 className="text-sm text-gray-400 mb-2">Screen Time Change</h3>
          <div className="flex items-center gap-3">
            {insights?.time_change_percent >= 0 ? (
              <TrendingUp className="w-8 h-8 text-red-500" />
            ) : (
              <TrendingDown className="w-8 h-8 text-green-500" />
            )}
            <div>
              <p className={`text-3xl font-bold ${insights?.time_change_percent >= 0 ? 'text-red-500' : 'text-green-500'}`}>
                {Math.abs(insights?.time_change_percent || 0).toFixed(1)}%
              </p>
              <p className="text-sm text-gray-400">vs yesterday</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-6"
        >
          <h3 className="text-sm text-gray-400 mb-2">Productivity Change</h3>
          <div className="flex items-center gap-3">
            {insights?.productivity_change >= 0 ? (
              <TrendingUp className="w-8 h-8 text-green-500" />
            ) : (
              <TrendingDown className="w-8 h-8 text-red-500" />
            )}
            <div>
              <p className={`text-3xl font-bold ${insights?.productivity_change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                {Math.abs((insights?.productivity_change || 0) * 100).toFixed(0)}%
              </p>
              <p className="text-sm text-gray-400">vs yesterday</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card p-6"
        >
          <h3 className="text-sm text-gray-400 mb-2">Most Used Category</h3>
          <div>
            <p className="text-3xl font-bold text-primary mb-2">
              {insights?.most_used_category || 'None'}
            </p>
            <p className="text-sm text-gray-400">Today's focus</p>
          </div>
        </motion.div>
      </div>

      {/* Hourly Distribution */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="glass-card p-6"
      >
        <h2 className="text-2xl font-bold mb-6">Hourly Distribution</h2>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={hourly}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="hour" 
                stroke="#9CA3AF"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#9CA3AF"
                style={{ fontSize: '12px' }}
                label={{ value: 'Minutes', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }}
              />
              <Tooltip 
                contentStyle={{ 
                  background: '#1E1E1E', 
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px'
                }}
                formatter={(value) => [`${value} min`, 'Usage']}
              />
              <Bar dataKey="minutes" fill="#007BFF" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Today vs Yesterday */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card p-6"
        >
          <h3 className="text-xl font-bold mb-4">Today</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Total Time</span>
              <span className="font-bold">{formatTime(insights?.today?.total_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Productive</span>
              <span className="font-bold text-green-500">{formatTime(insights?.today?.productive_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Entertainment</span>
              <span className="font-bold text-accent">{formatTime(insights?.today?.entertainment_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Apps Used</span>
              <span className="font-bold">{insights?.today?.unique_apps || 0}</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6"
        >
          <h3 className="text-xl font-bold mb-4">Yesterday</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Total Time</span>
              <span className="font-bold">{formatTime(insights?.yesterday?.total_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Productive</span>
              <span className="font-bold text-green-500">{formatTime(insights?.yesterday?.productive_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Entertainment</span>
              <span className="font-bold text-accent">{formatTime(insights?.yesterday?.entertainment_seconds || 0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Apps Used</span>
              <span className="font-bold">{insights?.yesterday?.unique_apps || 0}</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default Insights;

