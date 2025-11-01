import React from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Palette, Info } from 'lucide-react';

function Settings({ theme, onThemeChange }) {
  return (
    <div className="space-y-6">
      {/* Page Title */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">Settings</h1>
        <p className="text-gray-400">
          Customize your ScreenTime Analyzer Pro experience
        </p>
      </motion.div>

      {/* Theme Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <Palette className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">Theme</h2>
        </div>

        <div className="space-y-4">
          <p className="text-gray-400">Choose your accent color</p>
          
          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => onThemeChange('blue')}
              className={`p-6 rounded-lg border-2 transition-all ${
                theme === 'blue'
                  ? 'border-blue-500 bg-blue-500/20'
                  : 'border-white/10 hover:border-blue-500/50'
              }`}
            >
              <div className="w-12 h-12 rounded-full bg-blue-500 mx-auto mb-3" />
              <p className="text-center font-medium">Blue</p>
            </button>

            <button
              onClick={() => onThemeChange('orange')}
              className={`p-6 rounded-lg border-2 transition-all ${
                theme === 'orange'
                  ? 'border-orange-500 bg-orange-500/20'
                  : 'border-white/10 hover:border-orange-500/50'
              }`}
            >
              <div className="w-12 h-12 rounded-full bg-orange-500 mx-auto mb-3" />
              <p className="text-center font-medium">Orange</p>
            </button>
          </div>
        </div>
      </motion.div>

      {/* About */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <Info className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">About</h2>
        </div>

        <div className="space-y-4">
          <div>
            <p className="text-sm text-gray-400 mb-1">Version</p>
            <p className="text-lg font-medium">1.0.0</p>
          </div>

          <div>
            <p className="text-sm text-gray-400 mb-1">Description</p>
            <p className="text-gray-300">
              ScreenTime Analyzer Pro is a real-time screen time tracking and analytics tool
              that helps you understand your digital habits and improve productivity.
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-400 mb-1">Features</p>
            <ul className="list-disc list-inside space-y-2 text-gray-300">
              <li>Real-time app tracking with 1-second precision</li>
              <li>Automatic idle detection (3-minute threshold)</li>
              <li>Productivity scoring and insights</li>
              <li>Category-based analytics</li>
              <li>Hourly distribution charts</li>
              <li>CSV export functionality</li>
              <li>Cross-platform support (Windows, macOS, Linux)</li>
            </ul>
          </div>

          <div>
            <p className="text-sm text-gray-400 mb-1">Technology Stack</p>
            <div className="flex flex-wrap gap-2 mt-2">
              {['Python', 'FastAPI', 'React', 'WebSocket', 'SQLite', 'Chart.js', 'Tailwind CSS'].map(
                (tech) => (
                  <span
                    key={tech}
                    className="px-3 py-1 rounded-full text-sm bg-white/10"
                  >
                    {tech}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* System Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <SettingsIcon className="w-6 h-6" style={{ color: 'var(--accent-color)' }} />
          <h2 className="text-xl font-bold">System</h2>
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 rounded-lg bg-white/5">
            <span className="text-gray-400">Backend API</span>
            <span className="font-medium">http://127.0.0.1:8000</span>
          </div>

          <div className="flex justify-between items-center p-4 rounded-lg bg-white/5">
            <span className="text-gray-400">WebSocket</span>
            <span className="font-medium">ws://127.0.0.1:8000/ws/usage</span>
          </div>

          <div className="flex justify-between items-center p-4 rounded-lg bg-white/5">
            <span className="text-gray-400">Tracking Interval</span>
            <span className="font-medium">1 second</span>
          </div>

          <div className="flex justify-between items-center p-4 rounded-lg bg-white/5">
            <span className="text-gray-400">Idle Threshold</span>
            <span className="font-medium">3 minutes</span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

export default Settings;

