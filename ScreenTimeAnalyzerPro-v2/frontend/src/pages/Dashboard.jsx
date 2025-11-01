import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Clock, Target, Zap, TrendingUp, Activity } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { api } from '../api/apiClient';
import websocketClient from '../api/websocketClient';

const COLORS = ['#007BFF', '#FF8800', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899'];

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [topApps, setTopApps] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [isOnline, setIsOnline] = useState(true);
  const pollingIntervalRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  // Fetch data with error handling
  const fetchData = async () => {
    try {
      const [summaryRes, appsRes] = await Promise.all([
        api.getSummary(),
        api.getTopApps(null, 5)
      ]);

      setSummary(summaryRes.data);
      setTopApps(appsRes.data.apps || []);
      setLastUpdate(new Date());
      setIsOnline(true);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setIsOnline(false);
      setLoading(false);

      // Attempt to reconnect after 5 seconds
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      reconnectTimeoutRef.current = setTimeout(() => {
        console.log('Attempting to reconnect...');
        fetchData();
      }, 5000);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchData();

    // Poll every 4 seconds (fallback for WebSocket)
    pollingIntervalRef.current = setInterval(fetchData, 4000);

    // WebSocket listeners
    const handleSessionStart = (data) => {
      console.log('Session started:', data);
      setCurrentSession({
        app: data.app,
        window: data.window,
        category: data.category,
        elapsed: 0
      });
      setLastUpdate(new Date());
      setIsOnline(true);
      // Refresh summary data
      fetchData();
    };

    const handleHeartbeat = (data) => {
      console.log('Heartbeat:', data);
      setCurrentSession({
        app: data.app,
        window: data.window,
        category: data.category,
        elapsed: data.elapsed_sec
      });
      setLastUpdate(new Date());
      setIsOnline(true);
    };

    const handleSessionEnd = () => {
      console.log('Session ended');
      setCurrentSession(null);
      fetchData(); // Refresh summary
    };

    const handleCurrentSession = (data) => {
      console.log('Current session:', data);
      if (data.app) {
        setCurrentSession({
          app: data.app,
          window: data.window_title,
          category: data.category,
          elapsed: data.elapsed_sec
        });
        setLastUpdate(new Date());
        setIsOnline(true);
      }
    };

    const handleConnected = () => {
      console.log('WebSocket connected');
      setIsOnline(true);
    };

    const handleDisconnected = () => {
      console.log('WebSocket disconnected');
      setIsOnline(false);
    };

    // Register listeners
    websocketClient.on('session_start', handleSessionStart);
    websocketClient.on('heartbeat', handleHeartbeat);
    websocketClient.on('session_end', handleSessionEnd);
    websocketClient.on('current_session', handleCurrentSession);
    websocketClient.on('connected', handleConnected);
    websocketClient.on('disconnected', handleDisconnected);

    return () => {
      // Cleanup
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }

      // Remove listeners
      websocketClient.off('session_start', handleSessionStart);
      websocketClient.off('heartbeat', handleHeartbeat);
      websocketClient.off('session_end', handleSessionEnd);
      websocketClient.off('current_session', handleCurrentSession);
      websocketClient.off('connected', handleConnected);
      websocketClient.off('disconnected', handleDisconnected);
    };
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);

    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  const formatDuration = (seconds) => {
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

  const formatLastUpdate = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    });
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

  const chartData = topApps.map(app => ({
    name: app.app,
    value: app.total_seconds
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-400">Real-time overview of your screen time today</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Screen Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card stat-card"
        >
          <Clock className="w-8 h-8 mb-3 text-primary" />
          <p className="stat-label">TOTAL SCREEN TIME</p>
          <AnimatePresence mode="wait">
            <motion.p
              key={summary?.total_seconds || 0}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.3 }}
              className="stat-value text-primary"
            >
              {summary ? formatTime(summary.total_seconds) : '0m'}
            </motion.p>
          </AnimatePresence>
        </motion.div>

        {/* Productive Time */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-card stat-card"
        >
          <Target className="w-8 h-8 mb-3 text-green-500" />
          <p className="stat-label">PRODUCTIVE TIME</p>
          <AnimatePresence mode="wait">
            <motion.p
              key={summary?.productive_seconds || 0}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.3 }}
              className="stat-value text-green-500"
            >
              {summary ? formatTime(summary.productive_seconds) : '0s'}
            </motion.p>
          </AnimatePresence>
        </motion.div>

        {/* Entertainment */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-card stat-card"
        >
          <Zap className="w-8 h-8 mb-3 text-accent" />
          <p className="stat-label">ENTERTAINMENT</p>
          <AnimatePresence mode="wait">
            <motion.p
              key={summary?.entertainment_seconds || 0}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.3 }}
              className="stat-value text-accent"
            >
              {summary ? formatTime(summary.entertainment_seconds) : '0s'}
            </motion.p>
          </AnimatePresence>
        </motion.div>

        {/* Productivity Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass-card stat-card"
        >
          <TrendingUp className="w-8 h-8 mb-3 text-purple-500" />
          <p className="stat-label">PRODUCTIVITY SCORE</p>
          <AnimatePresence mode="wait">
            <motion.p
              key={summary?.productivity_score || 0}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              transition={{ duration: 0.3 }}
              className="stat-value text-purple-500"
            >
              {summary ? `${Math.round(summary.productivity_score * 100)}%` : '0%'}
            </motion.p>
          </AnimatePresence>
        </motion.div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Live Now Card */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <Activity className="w-6 h-6 text-primary" />
              <h2 className="text-2xl font-bold">Live Now</h2>
            </div>
            {currentSession && (
              <div className="flex items-center gap-2 px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full live-dot" />
                <span className="text-green-500 text-sm font-semibold">LIVE</span>
              </div>
            )}
          </div>

          {currentSession ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-400 mb-1">Application</p>
                <p className="text-3xl font-bold">{currentSession.app}</p>
              </div>

              {currentSession.window && (
                <div>
                  <p className="text-sm text-gray-400 mb-1">Window</p>
                  <p className="text-lg text-gray-300 truncate">{currentSession.window}</p>
                </div>
              )}

              <div className="flex items-center justify-between pt-4 border-t border-white/10">
                <div>
                  <p className="text-sm text-gray-400 mb-2">Category</p>
                  <span className={`category-badge ${getCategoryClass(currentSession.category)}`}>
                    {currentSession.category}
                  </span>
                </div>

                <div className="text-right">
                  <p className="text-sm text-gray-400 mb-2">Duration</p>
                  <div className="flex items-center gap-2">
                    <Clock className="w-5 h-5 text-primary" />
                    <p className="text-2xl font-bold tabular-nums">
                      {formatDuration(currentSession.elapsed)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-400 text-lg">No active session</p>
              <p className="text-sm text-gray-500 mt-2">
                Start using an application to see live tracking
              </p>
            </div>
          )}
        </motion.div>

        {/* Top Apps Card */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="glass-card p-6"
        >
          <div className="flex items-center gap-3 mb-6">
            <TrendingUp className="w-6 h-6 text-accent" />
            <h2 className="text-2xl font-bold">Top Apps</h2>
          </div>

          {topApps.length > 0 ? (
            <div className="space-y-6">
              {/* Pie Chart */}
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={chartData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={90}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => formatTime(value)}
                      contentStyle={{ 
                        background: '#1E1E1E', 
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* App List */}
              <div className="space-y-3">
                {topApps.map((app, index) => (
                  <div
                    key={app.app}
                    className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <div>
                        <p className="font-semibold">{app.app}</p>
                        <span className={`category-badge ${getCategoryClass(app.category)} text-xs`}>
                          {app.category}
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-lg">{formatTime(app.total_seconds)}</p>
                      <p className="text-xs text-gray-400">{app.percentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-400">No data available</p>
            </div>
          )}
        </motion.div>
      </div>

      {/* Footer with Last Update */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
        className="flex items-center justify-between text-sm text-gray-400 px-4 py-3 glass-card"
      >
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`} />
          <span>{isOnline ? 'Connected' : '⚠️ Offline – reconnecting…'}</span>
        </div>
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4" />
          <span>Last updated: {formatLastUpdate(lastUpdate)}</span>
        </div>
      </motion.div>
    </div>
  );
}

export default Dashboard;

