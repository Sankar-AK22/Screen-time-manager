import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { getDailySummaries } from '../services/api';
import { formatDate } from '../utils/formatters';
import toast from 'react-hot-toast';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Analytics = () => {
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(7);

  const fetchData = async () => {
    try {
      const data = await getDailySummaries(days);
      setSummaries(data.reverse());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      toast.error('Failed to load analytics data');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [days]);

  const screenTimeData = {
    labels: summaries.map(s => formatDate(s.date)),
    datasets: [
      {
        label: 'Screen Time (hours)',
        data: summaries.map(s => (s.total_screen_time_minutes / 60).toFixed(2)),
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const productivityData = {
    labels: summaries.map(s => formatDate(s.date)),
    datasets: [
      {
        label: 'Productivity Score',
        data: summaries.map(s => s.productivity_score),
        borderColor: '#4ade80',
        backgroundColor: 'rgba(74, 222, 128, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#fff',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#9ca3af',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      x: {
        ticks: {
          color: '#9ca3af',
        },
        grid: {
          display: false,
        },
      },
    },
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-between items-center"
      >
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">
            Analytics & Trends
          </h1>
          <p className="text-gray-400">
            Visualize your usage patterns over time
          </p>
        </div>
        
        <div className="flex gap-2">
          {[7, 14, 30].map(d => (
            <button
              key={d}
              onClick={() => setDays(d)}
              className={`px-4 py-2 rounded-lg transition-all ${
                days === d
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              {d} Days
            </button>
          ))}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h3 className="text-xl font-semibold mb-4">Screen Time Trend</h3>
        <div className="h-80">
          <Line data={screenTimeData} options={options} />
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <h3 className="text-xl font-semibold mb-4">Productivity Trend</h3>
        <div className="h-80">
          <Line data={productivityData} options={options} />
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6"
      >
        <h3 className="text-xl font-semibold mb-4">Daily Summary</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-gray-400">Date</th>
                <th className="text-left py-3 px-4 text-gray-400">Screen Time</th>
                <th className="text-left py-3 px-4 text-gray-400">Apps Used</th>
                <th className="text-left py-3 px-4 text-gray-400">Most Used</th>
                <th className="text-left py-3 px-4 text-gray-400">Productivity</th>
              </tr>
            </thead>
            <tbody>
              {summaries.map((summary, index) => (
                <motion.tr
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-b border-white/5 hover:bg-white/5"
                >
                  <td className="py-3 px-4">{formatDate(summary.date)}</td>
                  <td className="py-3 px-4">
                    {(summary.total_screen_time_minutes / 60).toFixed(1)}h
                  </td>
                  <td className="py-3 px-4">{summary.total_apps_used}</td>
                  <td className="py-3 px-4">{summary.most_used_app || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <span className={`font-semibold ${
                      summary.productivity_score >= 7 ? 'text-green-400' :
                      summary.productivity_score >= 5 ? 'text-yellow-400' :
                      'text-red-400'
                    }`}>
                      {summary.productivity_score.toFixed(1)}/10
                    </span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics;

