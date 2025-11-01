import { motion } from 'framer-motion';
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
import { formatDuration, getCategoryColor } from '../utils/formatters';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const TopAppsChart = ({ apps }) => {
  const topApps = apps.slice(0, 5);
  
  const chartData = {
    labels: topApps.map(app => app.app_name),
    datasets: [
      {
        label: 'Usage Time (minutes)',
        data: topApps.map(app => app.duration),
        backgroundColor: topApps.map(app => getCategoryColor(app.category)),
        borderColor: topApps.map(() => 'rgba(255, 255, 255, 0.2)'),
        borderWidth: 1,
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = context.parsed.y || 0;
            return `Time: ${formatDuration(value)}`;
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#9ca3af',
          callback: (value) => formatDuration(value),
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

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-6"
    >
      <h3 className="text-xl font-semibold mb-4">Top 5 Applications</h3>
      <div className="h-80">
        {topApps.length > 0 ? (
          <Bar data={chartData} options={options} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No data available
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default TopAppsChart;

