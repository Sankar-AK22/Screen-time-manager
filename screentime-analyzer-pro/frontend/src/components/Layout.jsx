import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Settings, 
  Play, 
  Pause,
  Activity
} from 'lucide-react';
import { getTrackingStatus, startTracking, stopTracking } from '../services/api';
import toast from 'react-hot-toast';

const Layout = ({ children }) => {
  const location = useLocation();
  const [isTracking, setIsTracking] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const status = await getTrackingStatus();
      setIsTracking(status.tracking_active);
    } catch (error) {
      console.error('Error checking status:', error);
    }
  };

  const toggleTracking = async () => {
    setLoading(true);
    try {
      if (isTracking) {
        await stopTracking();
        setIsTracking(false);
        toast.success('Tracking stopped');
      } else {
        await startTracking();
        setIsTracking(true);
        toast.success('Tracking started');
      }
    } catch (error) {
      toast.error('Failed to toggle tracking');
    }
    setLoading(false);
  };

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/analytics', icon: TrendingUp, label: 'Analytics' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: 0 }}
        className="w-64 glass-card m-4 rounded-2xl p-6 flex flex-col"
      >
        {/* Logo */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl">
              <Activity className="w-6 h-6" />
            </div>
            <h1 className="text-xl font-bold gradient-text">
              ScreenTime Pro
            </h1>
          </div>
          <p className="text-xs text-gray-400 ml-11">Analyze & Optimize</p>
        </div>

        {/* Tracking Status */}
        <div className="mb-6 p-4 bg-white/5 rounded-xl border border-white/10">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm text-gray-400">Tracking Status</span>
            <div className={`w-2 h-2 rounded-full ${isTracking ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
          </div>
          <button
            onClick={toggleTracking}
            disabled={loading}
            className={`w-full py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all ${
              isTracking
                ? 'bg-red-500/20 hover:bg-red-500/30 text-red-400'
                : 'bg-green-500/20 hover:bg-green-500/30 text-green-400'
            }`}
          >
            {loading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-current" />
            ) : (
              <>
                {isTracking ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                {isTracking ? 'Stop' : 'Start'}
              </>
            )}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                    : 'text-gray-400 hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="mt-auto pt-6 border-t border-white/10">
          <p className="text-xs text-gray-500 text-center">
            ScreenTime Analyzer Pro v1.0
          </p>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;

