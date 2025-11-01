import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Clock } from 'lucide-react';
import socketClient from '../api/socketClient';
import { api } from '../api/apiClient';

function LiveNowCard() {
  const [currentSession, setCurrentSession] = useState(null);
  const [elapsedTime, setElapsedTime] = useState(0);

  // Fetch current session from API (fallback when WebSocket isn't working)
  const fetchCurrentSession = async () => {
    try {
      const response = await api.getCurrentSession();
      const data = response.data;

      if (data.active && data.session) {
        setCurrentSession({
          app: data.session.app,
          windowTitle: data.session.window_title,
          category: data.session.category,
          startTime: new Date(data.session.start_time),
        });
        setElapsedTime(data.session.elapsed_sec || 0);
      } else {
        setCurrentSession(null);
        setElapsedTime(0);
      }
    } catch (error) {
      console.error('Error fetching current session:', error);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchCurrentSession();

    // Poll every 2 seconds for real-time updates
    const pollInterval = setInterval(fetchCurrentSession, 2000);

    // Listen for session events from WebSocket (if connected)
    const handleSessionStart = (data) => {
      console.log('Session started:', data);
      setCurrentSession({
        app: data.app,
        windowTitle: data.window_title,
        category: data.category,
        startTime: new Date(data.timestamp),
      });
      setElapsedTime(0);
    };

    const handleHeartbeat = (data) => {
      console.log('Heartbeat:', data);
      setElapsedTime(data.elapsed_sec);

      // Update session if exists
      if (currentSession && data.app === currentSession.app) {
        setCurrentSession(prev => ({
          ...prev,
          windowTitle: data.window_title,
        }));
      }
    };

    const handleSessionEnd = (data) => {
      console.log('Session ended:', data);
      // Keep showing the last session briefly
      setTimeout(() => {
        setCurrentSession(null);
        setElapsedTime(0);
      }, 1000);
    };

    const handleCurrentSession = (data) => {
      console.log('Current session:', data);
      if (data.app) {
        setCurrentSession({
          app: data.app,
          windowTitle: data.window_title,
          category: data.category,
          startTime: new Date(data.start_time),
        });
        setElapsedTime(data.elapsed_sec || 0);
      }
    };

    const handleNoActiveSession = () => {
      setCurrentSession(null);
      setElapsedTime(0);
    };

    socketClient.on('session_start', handleSessionStart);
    socketClient.on('heartbeat', handleHeartbeat);
    socketClient.on('session_end', handleSessionEnd);
    socketClient.on('current_session', handleCurrentSession);
    socketClient.on('no_active_session', handleNoActiveSession);

    // Request current session on mount if WebSocket is connected
    if (socketClient.isConnected()) {
      socketClient.getCurrentSession();
    }

    return () => {
      clearInterval(pollInterval);
      socketClient.off('session_start', handleSessionStart);
      socketClient.off('heartbeat', handleHeartbeat);
      socketClient.off('session_end', handleSessionEnd);
      socketClient.off('current_session', handleCurrentSession);
      socketClient.off('no_active_session', handleNoActiveSession);
    };
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
      return `${minutes}m ${secs}s`;
    } else {
      return `${secs}s`;
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      Development: 'from-blue-500 to-cyan-500',
      Browser: 'from-purple-500 to-pink-500',
      Communication: 'from-green-500 to-emerald-500',
      Entertainment: 'from-red-500 to-orange-500',
      Productivity: 'from-yellow-500 to-amber-500',
      Design: 'from-indigo-500 to-purple-500',
      Other: 'from-gray-500 to-slate-500',
    };
    return colors[category] || colors.Other;
  };

  if (!currentSession) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <Activity className="w-6 h-6 text-gray-400" />
          <h2 className="text-xl font-bold">Live Now</h2>
        </div>
        <div className="text-center py-8">
          <p className="text-gray-400">No active session</p>
          <p className="text-sm text-gray-500 mt-2">
            Start using an application to see live tracking
          </p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6 relative overflow-hidden accent-glow"
    >
      {/* Animated background gradient */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${getCategoryColor(
          currentSession.category
        )} opacity-10`}
      />

      {/* Content */}
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Activity className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
            <h2 className="text-xl font-bold">Live Now</h2>
          </div>
          <div className="live-indicator">
            <div className="live-dot" />
            <span>LIVE</span>
          </div>
        </div>

        <div className="space-y-4">
          {/* App Name */}
          <div>
            <p className="text-sm text-gray-400 mb-1">Application</p>
            <p className="text-2xl font-bold">{currentSession.app}</p>
          </div>

          {/* Window Title */}
          {currentSession.windowTitle && (
            <div>
              <p className="text-sm text-gray-400 mb-1">Window</p>
              <p className="text-lg text-gray-300 truncate">
                {currentSession.windowTitle}
              </p>
            </div>
          )}

          {/* Category and Time */}
          <div className="flex items-center justify-between pt-4 border-t border-white/10">
            <div>
              <p className="text-sm text-gray-400 mb-1">Category</p>
              <span
                className={`inline-block px-3 py-1 rounded-full text-sm font-medium bg-gradient-to-r ${getCategoryColor(
                  currentSession.category
                )}`}
              >
                {currentSession.category}
              </span>
            </div>

            <div className="text-right">
              <p className="text-sm text-gray-400 mb-1">Duration</p>
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-[var(--accent-color)]" />
                <p className="text-2xl font-bold tabular-nums">
                  {formatTime(elapsedTime)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default LiveNowCard;

