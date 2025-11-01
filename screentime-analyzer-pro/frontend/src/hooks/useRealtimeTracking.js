/**
 * React Hook for Real-Time Screen Time Tracking
 * Manages WebSocket connection and provides real-time data
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import websocketService from '../services/websocket';

export const useRealtimeTracking = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const [sessionHistory, setSessionHistory] = useState([]);
  const [error, setError] = useState(null);
  const mountedRef = useRef(true);

  // Handle session start
  const handleSessionStart = useCallback((data) => {
    if (!mountedRef.current) return;
    
    console.log('🟢 Session started:', data);
    setCurrentSession({
      app_name: data.app_name,
      window_title: data.window_title,
      category: data.category,
      duration_seconds: 0,
      start_time: data.timestamp
    });
  }, []);

  // Handle duration update
  const handleDurationUpdate = useCallback((data) => {
    if (!mountedRef.current) return;
    
    setCurrentSession(prev => {
      if (!prev || prev.app_name !== data.app_name) {
        // New session
        return {
          app_name: data.app_name,
          window_title: data.window_title,
          category: data.category,
          duration_seconds: data.duration_seconds,
          start_time: data.timestamp
        };
      }
      
      // Update existing session
      return {
        ...prev,
        duration_seconds: data.duration_seconds,
        window_title: data.window_title
      };
    });
  }, []);

  // Handle session end
  const handleSessionEnd = useCallback((data) => {
    if (!mountedRef.current) return;
    
    console.log('🔴 Session ended:', data);
    
    // Add to history
    setSessionHistory(prev => [{
      app_name: data.app_name,
      window_title: data.window_title,
      category: data.category,
      duration_seconds: data.duration_seconds,
      timestamp: data.timestamp
    }, ...prev.slice(0, 9)]); // Keep last 10 sessions
    
    // Clear current session
    setCurrentSession(null);
  }, []);

  // Handle current session info
  const handleCurrentSession = useCallback((data) => {
    if (!mountedRef.current) return;
    
    console.log('📊 Current session:', data);
    setCurrentSession({
      app_name: data.app_name,
      window_title: data.window_title,
      category: data.category,
      duration_seconds: data.duration_seconds,
      start_time: data.start_time
    });
  }, []);

  // Handle no active session
  const handleNoActiveSession = useCallback((data) => {
    if (!mountedRef.current) return;
    
    console.log('⚪ No active session');
    setCurrentSession(null);
  }, []);

  // Handle connection status
  const handleConnected = useCallback(() => {
    if (!mountedRef.current) return;
    
    console.log('✅ WebSocket connected');
    setIsConnected(true);
    setError(null);
    
    // Request current session info
    setTimeout(() => {
      websocketService.getCurrentSession();
    }, 500);
  }, []);

  const handleDisconnected = useCallback(() => {
    if (!mountedRef.current) return;
    
    console.log('❌ WebSocket disconnected');
    setIsConnected(false);
  }, []);

  const handleError = useCallback((data) => {
    if (!mountedRef.current) return;
    
    console.error('❌ WebSocket error:', data);
    setError(data.error || 'WebSocket connection error');
  }, []);

  const handleReconnectFailed = useCallback(() => {
    if (!mountedRef.current) return;
    
    console.error('❌ WebSocket reconnection failed');
    setError('Failed to reconnect to server');
    setIsConnected(false);
  }, []);

  // Connect to WebSocket on mount
  useEffect(() => {
    mountedRef.current = true;

    // Register event listeners
    websocketService.on('connected', handleConnected);
    websocketService.on('disconnected', handleDisconnected);
    websocketService.on('error', handleError);
    websocketService.on('reconnect_failed', handleReconnectFailed);
    websocketService.on('session_start', handleSessionStart);
    websocketService.on('session_end', handleSessionEnd);
    websocketService.on('duration_update', handleDurationUpdate);
    websocketService.on('current_session', handleCurrentSession);
    websocketService.on('no_active_session', handleNoActiveSession);

    // Connect to WebSocket
    websocketService.connect();

    // Ping every 30 seconds to keep connection alive
    const pingInterval = setInterval(() => {
      if (websocketService.getStatus().isConnected) {
        websocketService.ping();
      }
    }, 30000);

    // Cleanup on unmount
    return () => {
      mountedRef.current = false;
      clearInterval(pingInterval);
      
      // Remove event listeners
      websocketService.off('connected', handleConnected);
      websocketService.off('disconnected', handleDisconnected);
      websocketService.off('error', handleError);
      websocketService.off('reconnect_failed', handleReconnectFailed);
      websocketService.off('session_start', handleSessionStart);
      websocketService.off('session_end', handleSessionEnd);
      websocketService.off('duration_update', handleDurationUpdate);
      websocketService.off('current_session', handleCurrentSession);
      websocketService.off('no_active_session', handleNoActiveSession);
      
      // Disconnect WebSocket
      websocketService.disconnect();
    };
  }, [
    handleConnected,
    handleDisconnected,
    handleError,
    handleReconnectFailed,
    handleSessionStart,
    handleSessionEnd,
    handleDurationUpdate,
    handleCurrentSession,
    handleNoActiveSession
  ]);

  // Refresh current session
  const refreshCurrentSession = useCallback(() => {
    websocketService.getCurrentSession();
  }, []);

  return {
    isConnected,
    currentSession,
    sessionHistory,
    error,
    refreshCurrentSession
  };
};

export default useRealtimeTracking;

