import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock } from 'lucide-react';
import { api } from '../api/apiClient';

function Today() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApps();
    const interval = setInterval(fetchApps, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchApps = async () => {
    try {
      const response = await api.getTopApps(null, 20);
      setApps(response.data.apps || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching apps:', error);
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    }
    return `${secs}s`;
  };

  const getCategoryClass = (category) => {
    const classes = {
      'Browser': 'category-browser',
      'Development': 'category-development',
      'Communication': 'category-communication',
      'Entertainment': 'category-entertainment',
      'Productivity': 'category-productivity',
      'Design': 'category-design',
      'Other': 'category-other'
    };
    return classes[category] || 'category-other';
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
          <Calendar className="w-8 h-8 text-primary" />
          <h1 className="text-4xl font-bold">Today</h1>
        </div>
        <p className="text-gray-400">Detailed breakdown of all apps used today</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-4 px-4 text-gray-400 font-semibold">#</th>
                <th className="text-left py-4 px-4 text-gray-400 font-semibold">Application</th>
                <th className="text-left py-4 px-4 text-gray-400 font-semibold">Category</th>
                <th className="text-right py-4 px-4 text-gray-400 font-semibold">Time</th>
                <th className="text-right py-4 px-4 text-gray-400 font-semibold">Sessions</th>
                <th className="text-right py-4 px-4 text-gray-400 font-semibold">%</th>
              </tr>
            </thead>
            <tbody>
              {apps.map((app, index) => (
                <motion.tr
                  key={app.app}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-b border-white/5 hover:bg-white/5 transition-colors"
                >
                  <td className="py-4 px-4 text-gray-400">{index + 1}</td>
                  <td className="py-4 px-4">
                    <p className="font-semibold text-lg">{app.app}</p>
                  </td>
                  <td className="py-4 px-4">
                    <span className={`category-badge ${getCategoryClass(app.category)}`}>
                      {app.category}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Clock className="w-4 h-4 text-primary" />
                      <span className="font-bold text-lg">{formatTime(app.total_seconds)}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-right text-gray-400">
                    {app.session_count}
                  </td>
                  <td className="py-4 px-4 text-right">
                    <span className="font-semibold text-primary">{app.percentage}%</span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>

          {apps.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-400">No apps tracked yet today</p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default Today;

