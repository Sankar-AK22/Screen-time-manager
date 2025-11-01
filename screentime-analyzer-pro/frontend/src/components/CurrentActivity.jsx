import { motion } from 'framer-motion';
import { Activity } from 'lucide-react';
import { formatDuration, getCategoryIcon } from '../utils/formatters';

const CurrentActivity = ({ app }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6 border-2 border-purple-500/30"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl animate-pulse">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm text-gray-400 mb-1">Currently Active</p>
            <div className="flex items-center gap-2">
              <span className="text-2xl">{getCategoryIcon(app.category)}</span>
              <h3 className="text-2xl font-bold">{app.app_name}</h3>
            </div>
            <p className="text-sm text-gray-400 mt-1">{app.category}</p>
          </div>
        </div>
        
        <div className="text-right">
          <p className="text-sm text-gray-400 mb-1">Duration</p>
          <p className="text-3xl font-bold text-purple-400">
            {formatDuration(app.duration_minutes)}
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default CurrentActivity;

