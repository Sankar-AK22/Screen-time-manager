import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import TodayView from './pages/TodayView';
import AppInsights from './pages/AppInsights';
import Settings from './pages/Settings';
import socketClient from './api/socketClient';

function App() {
  const [theme, setTheme] = useState('blue'); // 'blue' or 'orange'
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    socketClient.connect();

    // Listen for connection events
    socketClient.on('connected', () => {
      console.log('✅ Connected to server');
      setIsConnected(true);
    });

    socketClient.on('disconnected', () => {
      console.log('❌ Disconnected from server');
      setIsConnected(false);
    });

    // Cleanup on unmount
    return () => {
      socketClient.disconnect();
    };
  }, []);

  useEffect(() => {
    // Apply theme
    if (theme === 'orange') {
      document.documentElement.setAttribute('data-theme', 'orange');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'blue' ? 'orange' : 'blue');
  };

  return (
    <Router>
      <div className="min-h-screen bg-black">
        <Header 
          theme={theme} 
          onThemeToggle={toggleTheme}
          isConnected={isConnected}
        />
        
        <main className="container mx-auto px-4 py-8 max-w-7xl">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/today" element={<TodayView />} />
            <Route path="/insights" element={<AppInsights />} />
            <Route path="/settings" element={<Settings theme={theme} onThemeChange={setTheme} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

