import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Clock, TrendingUp, Activity, Zap } from 'lucide-react';
import { getSummary, getCurrentUsage } from '../services/api';
import { formatDuration, getProductivityColor, getCategoryIcon } from '../utils/formatters';
import StatCard from './StatCard';
import CategoryChart from './CategoryChart';
import TopAppsChart from './TopAppsChart';
import CurrentActivity from './CurrentActivity';
import RealtimeActivity from './RealtimeActivity';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [currentApp, setCurrentApp] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [summaryData, currentData] = await Promise.all([
        getSummary(),
        getCurrentUsage()
      ]);
      
      setSummary(summaryData);
      setCurrentApp(currentData.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Refresh every 60 seconds
    const interval = setInterval(fetchData, 60000);
    
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Dashboard Overview
        </h1>
        <p className="text-gray-400">
          Track your screen time and boost productivity
        </p>
      </motion.div>

      {/* Real-Time Activity */}
      <RealtimeActivity />

      {/* Legacy Current Activity (fallback) */}
      {currentApp && !summary?.current_app && <CurrentActivity app={currentApp} />}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<Clock className="w-8 h-8" />}
          title="Screen Time Today"
          value={formatDuration(summary?.total_screen_time_minutes || 0)}
          subtitle={`${summary?.total_screen_time_hours || 0} hours`}
          color="from-blue-500 to-cyan-500"
        />
        
        <StatCard
          icon={<Activity className="w-8 h-8" />}
          title="Apps Used"
          value={summary?.total_apps_used || 0}
          subtitle="Different applications"
          color="from-purple-500 to-pink-500"
        />
        
        <StatCard
          icon={<TrendingUp className="w-8 h-8" />}
          title="Productivity Score"
          value={`${summary?.productivity_score || 0}/10`}
          subtitle="Based on app usage"
          color="from-green-500 to-emerald-500"
          valueClass={getProductivityColor(summary?.productivity_score || 0)}
        />
        
        <StatCard
          icon={<Zap className="w-8 h-8" />}
          title="Most Used"
          value={summary?.top_apps?.[0]?.app_name || 'N/A'}
          subtitle={formatDuration(summary?.top_apps?.[0]?.duration || 0)}
          color="from-orange-500 to-red-500"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CategoryChart data={summary?.category_breakdown || {}} />
        <TopAppsChart apps={summary?.top_apps || []} />
      </div>

      {/* Insights */}
      {summary?.productivity_score && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-6"
        >
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Zap className="w-6 h-6 text-yellow-400" />
            Quick Insights
          </h3>
          <div className="space-y-3">
            {summary.productivity_score >= 7 ? (
              <div className="flex items-start gap-3 p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                <span className="text-2xl">🎉</span>
                <div>
                  <p className="font-semibold text-green-400">Excellent Productivity!</p>
                  <p className="text-sm text-gray-300">You're having a highly productive day. Keep up the great work!</p>
                </div>
              </div>
            ) : summary.productivity_score >= 5 ? (
              <div className="flex items-start gap-3 p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                <span className="text-2xl">💪</span>
                <div>
                  <p className="font-semibold text-yellow-400">Good Progress</p>
                  <p className="text-sm text-gray-300">You're doing well! Try focusing more on productive apps to boost your score.</p>
                </div>
              </div>
            ) : (
              <div className="flex items-start gap-3 p-4 bg-red-500/10 rounded-lg border border-red-500/20">
                <span className="text-2xl">⚠️</span>
                <div>
                  <p className="font-semibold text-red-400">Room for Improvement</p>
                  <p className="text-sm text-gray-300">Consider reducing time on entertainment apps and taking regular breaks.</p>
                </div>
              </div>
            )}
            
            {summary.total_screen_time_hours > 8 && (
              <div className="flex items-start gap-3 p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                <span className="text-2xl">👀</span>
                <div>
                  <p className="font-semibold text-orange-400">High Screen Time</p>
                  <p className="text-sm text-gray-300">You've been on screen for over 8 hours. Remember to take breaks and rest your eyes!</p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Dashboard;

