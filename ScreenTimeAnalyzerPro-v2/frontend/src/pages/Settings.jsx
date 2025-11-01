import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Download, FileText, Trash2 } from 'lucide-react';
import { api } from '../api/apiClient';

function Settings() {
  const handleExportCSV = async () => {
    try {
      const response = await api.exportCSV();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `screentime_${new Date().toISOString().split('T')[0]}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      alert('CSV exported successfully!');
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export CSV');
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await api.exportPDF();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `screentime_${new Date().toISOString().split('T')[0]}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      alert('PDF exported successfully!');
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export PDF');
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-2">
          <SettingsIcon className="w-8 h-8 text-primary" />
          <h1 className="text-4xl font-bold">Settings</h1>
        </div>
        <p className="text-gray-400">Manage your preferences and data</p>
      </motion.div>

      {/* Export Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h2 className="text-2xl font-bold mb-4">Export Data</h2>
        <p className="text-gray-400 mb-6">Download your screen time data in different formats</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={handleExportCSV}
            className="flex items-center justify-center gap-3 p-4 bg-primary/20 hover:bg-primary/30 border border-primary/30 rounded-lg transition-all"
          >
            <FileText className="w-6 h-6 text-primary" />
            <div className="text-left">
              <p className="font-bold">Export as CSV</p>
              <p className="text-sm text-gray-400">Spreadsheet format</p>
            </div>
          </button>

          <button
            onClick={handleExportPDF}
            className="flex items-center justify-center gap-3 p-4 bg-accent/20 hover:bg-accent/30 border border-accent/30 rounded-lg transition-all"
          >
            <Download className="w-6 h-6 text-accent" />
            <div className="text-left">
              <p className="font-bold">Export as PDF</p>
              <p className="text-sm text-gray-400">Report format</p>
            </div>
          </button>
        </div>
      </motion.div>

      {/* App Categories */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <h2 className="text-2xl font-bold mb-4">App Categories</h2>
        <p className="text-gray-400 mb-6">How apps are categorized for productivity tracking</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-white/5 rounded-lg">
            <h3 className="font-bold text-green-500 mb-2">Productive</h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>• Development (VS Code, PyCharm)</li>
              <li>• Productivity (Excel, Word)</li>
              <li>• Design (Photoshop, Figma)</li>
            </ul>
          </div>

          <div className="p-4 bg-white/5 rounded-lg">
            <h3 className="font-bold text-accent mb-2">Entertainment</h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>• Entertainment (Spotify, Netflix)</li>
              <li>• Browser (Chrome, Edge)</li>
            </ul>
          </div>

          <div className="p-4 bg-white/5 rounded-lg">
            <h3 className="font-bold text-blue-500 mb-2">Communication</h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>• WhatsApp, Discord</li>
              <li>• Slack, Teams, Zoom</li>
            </ul>
          </div>

          <div className="p-4 bg-white/5 rounded-lg">
            <h3 className="font-bold text-gray-400 mb-2">Other</h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>• Uncategorized apps</li>
              <li>• System utilities</li>
            </ul>
          </div>
        </div>
      </motion.div>

      {/* About */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6"
      >
        <h2 className="text-2xl font-bold mb-4">About</h2>
        <div className="space-y-2 text-gray-400">
          <p><span className="font-semibold text-white">Version:</span> 2.0.0</p>
          <p><span className="font-semibold text-white">Platform:</span> Windows</p>
          <p><span className="font-semibold text-white">Tracking:</span> Real-time (1s polling)</p>
          <p><span className="font-semibold text-white">Idle Threshold:</span> 2 minutes</p>
        </div>
      </motion.div>
    </div>
  );
}

export default Settings;

