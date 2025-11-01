import { motion } from 'framer-motion';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { getCategoryColor, getCategoryIcon } from '../utils/formatters';

ChartJS.register(ArcElement, Tooltip, Legend);

const CategoryChart = ({ data }) => {
  const labels = Object.keys(data);
  const values = Object.values(data);
  
  const chartData = {
    labels: labels,
    datasets: [
      {
        data: values,
        backgroundColor: labels.map(label => getCategoryColor(label)),
        borderColor: labels.map(() => 'rgba(255, 255, 255, 0.1)'),
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#fff',
          padding: 15,
          font: {
            size: 12,
          },
          generateLabels: (chart) => {
            const data = chart.data;
            return data.labels.map((label, i) => ({
              text: `${getCategoryIcon(label)} ${label}`,
              fillStyle: data.datasets[0].backgroundColor[i],
              hidden: false,
              index: i,
            }));
          },
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const hours = Math.floor(value / 60);
            const mins = Math.round(value % 60);
            return `${label}: ${hours}h ${mins}m`;
          },
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
      <h3 className="text-xl font-semibold mb-4">Usage by Category</h3>
      <div className="h-80">
        {labels.length > 0 ? (
          <Doughnut data={chartData} options={options} />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No data available
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default CategoryChart;

