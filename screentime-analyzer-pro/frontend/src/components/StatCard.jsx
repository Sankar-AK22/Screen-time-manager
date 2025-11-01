import { motion } from 'framer-motion';

const StatCard = ({ icon, title, value, subtitle, color, valueClass = '' }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05 }}
      className="glass-card p-6 cursor-pointer"
    >
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-xl bg-gradient-to-br ${color}`}>
          {icon}
        </div>
      </div>
      
      <h3 className="text-gray-400 text-sm font-medium mb-2">{title}</h3>
      <p className={`text-3xl font-bold mb-1 ${valueClass || 'text-white'}`}>
        {value}
      </p>
      <p className="text-gray-500 text-sm">{subtitle}</p>
    </motion.div>
  );
};

export default StatCard;

