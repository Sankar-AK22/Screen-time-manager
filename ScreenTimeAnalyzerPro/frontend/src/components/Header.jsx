import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Monitor, Download, Settings, Sun, Moon } from 'lucide-react';
import { api } from '../api/apiClient';

function Header({ theme, onThemeToggle, isConnected }) {
  const location = useLocation();
  const [isExporting, setIsExporting] = useState(false);

  const handleExportCSV = async () => {
    try {
      setIsExporting(true);
      const response = await api.exportCSV();
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `screentime_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting CSV:', error);
      alert('Failed to export CSV');
    } finally {
      setIsExporting(false);
    }
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="glass-card mx-4 mt-4 p-4">
      <div className="container mx-auto max-w-7xl">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <Monitor className="w-8 h-8" style={{ color: 'var(--accent-color)' }} />
            <div>
              <h1 className="text-2xl font-bold gradient-text">
                ScreenTime Analyzer Pro
              </h1>
              <p className="text-xs text-gray-400">Real-time tracking & analytics</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/dashboard"
              className={`text-sm font-medium transition-colors ${
                isActive('/dashboard')
                  ? 'text-[var(--accent-color)]'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/today"
              className={`text-sm font-medium transition-colors ${
                isActive('/today')
                  ? 'text-[var(--accent-color)]'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Today
            </Link>
            <Link
              to="/insights"
              className={`text-sm font-medium transition-colors ${
                isActive('/insights')
                  ? 'text-[var(--accent-color)]'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Insights
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-4">
            {/* Connection Status */}
            <div className="flex items-center gap-2">
              <div
                className={`w-2 h-2 rounded-full ${
                  isConnected ? 'bg-green-500 pulse' : 'bg-red-500'
                }`}
              />
              <span className="text-xs text-gray-400">
                {isConnected ? 'Live' : 'Offline'}
              </span>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={onThemeToggle}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              title={`Switch to ${theme === 'blue' ? 'orange' : 'blue'} theme`}
            >
              {theme === 'blue' ? (
                <Sun className="w-5 h-5 text-orange-500" />
              ) : (
                <Moon className="w-5 h-5 text-blue-500" />
              )}
            </button>

            {/* Export Button */}
            <button
              onClick={handleExportCSV}
              disabled={isExporting}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[var(--accent-color)] hover:opacity-90 transition-opacity disabled:opacity-50"
              title="Export today's data as CSV"
            >
              <Download className="w-4 h-4" />
              <span className="text-sm font-medium">
                {isExporting ? 'Exporting...' : 'Export'}
              </span>
            </button>

            {/* Settings Link */}
            <Link
              to="/settings"
              className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

