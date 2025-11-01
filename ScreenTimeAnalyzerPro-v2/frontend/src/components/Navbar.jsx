import { Link, useLocation } from 'react-router-dom';
import { Monitor, Download, Settings, TrendingUp, Calendar } from 'lucide-react';
import { api } from '../api/apiClient';

function Navbar({ isOnline }) {
  const location = useLocation();

  const handleExport = async () => {
    try {
      const response = await api.exportCSV();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `screentime_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export data');
    }
  };

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Monitor },
    { path: '/today', label: 'Today', icon: Calendar },
    { path: '/insights', label: 'Insights', icon: TrendingUp },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <nav className="glass-card mx-4 mt-4 p-4">
      <div className="container mx-auto max-w-7xl flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center">
            <Monitor className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold">ScreenTime Analyzer Pro</h1>
            <p className="text-xs text-gray-400">Real-time tracking & analytics</p>
          </div>
        </div>

        {/* Navigation Links */}
        <div className="flex items-center gap-6">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
                  isActive
                    ? 'bg-primary text-white'
                    : 'text-gray-400 hover:text-white hover:bg-dark-card'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Status and Export */}
        <div className="flex items-center gap-4">
          {/* Online Status */}
          <div className={isOnline ? 'status-online' : 'status-offline'}>
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500 live-dot' : 'bg-red-500'}`} />
            <span>{isOnline ? 'Online' : 'Offline'}</span>
          </div>

          {/* Export Button */}
          <button
            onClick={handleExport}
            className="btn-accent flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

