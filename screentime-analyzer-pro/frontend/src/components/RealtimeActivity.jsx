/**
 * Real-Time Activity Component
 * Displays live screen time tracking with WebSocket updates
 */

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Clock, Zap, Wifi, WifiOff } from 'lucide-react';
import { useRealtimeTracking } from '../hooks/useRealtimeTracking';
import { formatDuration } from '../utils/formatters';

const RealtimeActivity = () => {
  const { isConnected, currentSession, sessionHistory, error } = useRealtimeTracking();
  const [displayDuration, setDisplayDuration] = useState(0);

  // Update display duration every second
  useEffect(() => {
    if (!currentSession) {
      setDisplayDuration(0);
      return;
    }

    // Set initial duration
    setDisplayDuration(currentSession.duration_seconds);

    // Update every second
    const interval = setInterval(() => {
      setDisplayDuration(prev => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [currentSession]);

  // Get category color
  const getCategoryColor = (category) => {
    const colors = {
      Development: 'from-blue-500 to-cyan-500',
      Productivity: 'from-green-500 to-emerald-500',
      Browser: 'from-purple-500 to-pink-500',
      Communication: 'from-yellow-500 to-orange-500',
      Entertainment: 'from-red-500 to-rose-500',
      Design: 'from-indigo-500 to-violet-500',
      Other: 'from-gray-500 to-slate-500'
    };
    return colors[category] || colors.Other;
  };

  // Get category icon
  const getCategoryIcon = (category) => {
    const icons = {
      Development: '💻',
      Productivity: '📊',
      Browser: '🌐',
      Communication: '💬',
      Entertainment: '🎮',
      Design: '🎨',
      Other: '📱'
    };
    return icons[category] || icons.Other;
  };

  return (
    <div className="space-y-4">
      {/* Connection Status */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold gradient-text">Live Activity</h2>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <>
              <Wifi className="w-5 h-5 text-green-400" />
              <span className="text-sm text-green-400 font-medium">Connected</span>
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            </>
          ) : (
            <>
              <WifiOff className="w-5 h-5 text-red-400" />
              <span className="text-sm text-red-400 font-medium">Disconnected</span>
              <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
            </>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-4 border-red-500/50"
        >
          <div className="flex items-center gap-2 text-red-400">
            <Zap className="w-5 h-5" />
            <span className="font-medium">{error}</span>
          </div>
        </motion.div>
      )}

      {/* Current Session */}
      <AnimatePresence mode="wait">
        {currentSession ? (
          <motion.div
            key="active-session"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="glass-card p-6 relative overflow-hidden"
          >
            {/* Animated Background */}
            <div className={`absolute inset-0 bg-gradient-to-br ${getCategoryColor(currentSession.category)} opacity-10`}></div>
            
            {/* Content */}
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{getCategoryIcon(currentSession.category)}</div>
                  <div>
                    <h3 className="text-xl font-bold text-white">{currentSession.app_name}</h3>
                    <p className="text-sm text-gray-400">{currentSession.window_title || 'No title'}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full">
                  <Activity className="w-4 h-4 text-green-400 animate-pulse" />
                  <span className="text-sm font-medium text-green-400">Active</span>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-purple-400" />
                  <div>
                    <p className="text-xs text-gray-400">Duration</p>
                    <p className="text-2xl font-bold text-white tabular-nums">
                      {formatDuration(displayDuration, 'seconds')}
                    </p>
                  </div>
                </div>

                <div className="flex-1">
                  <p className="text-xs text-gray-400 mb-1">Category</p>
                  <div className={`inline-flex items-center gap-2 px-3 py-1 bg-gradient-to-r ${getCategoryColor(currentSession.category)} rounded-full`}>
                    <span className="text-sm font-medium text-white">{currentSession.category}</span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mt-4">
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full bg-gradient-to-r ${getCategoryColor(currentSession.category)}`}
                    initial={{ width: '0%' }}
                    animate={{ width: '100%' }}
                    transition={{ duration: 60, ease: 'linear', repeat: Infinity }}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="no-session"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="glass-card p-8 text-center"
          >
            <div className="text-6xl mb-4">⏸️</div>
            <h3 className="text-xl font-bold text-white mb-2">No Active Session</h3>
            <p className="text-gray-400">Waiting for activity...</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Session History */}
      {sessionHistory.length > 0 && (
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold text-white mb-4">Recent Sessions</h3>
          <div className="space-y-2">
            {sessionHistory.map((session, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="text-2xl">{getCategoryIcon(session.category)}</div>
                  <div>
                    <p className="text-sm font-medium text-white">{session.app_name}</p>
                    <p className="text-xs text-gray-400">{session.category}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold text-white">{formatDuration(session.duration_seconds, 'seconds')}</p>
                  <p className="text-xs text-gray-400">
                    {new Date(session.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default RealtimeActivity;

