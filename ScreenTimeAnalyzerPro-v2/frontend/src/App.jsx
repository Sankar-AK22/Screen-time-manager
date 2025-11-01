import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Today from './pages/Today';
import Insights from './pages/Insights';
import Settings from './pages/Settings';
import websocketClient from './api/websocketClient';

function App() {
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    websocketClient.connect();

    // Listen for connection status
    websocketClient.on('connected', () => {
      setIsOnline(true);
    });

    websocketClient.on('disconnected', () => {
      setIsOnline(false);
    });

    // Cleanup on unmount
    return () => {
      websocketClient.disconnect();
    };
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-dark-bg">
        <Navbar isOnline={isOnline} />
        <main className="container mx-auto px-4 py-8 max-w-7xl">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/today" element={<Today />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

