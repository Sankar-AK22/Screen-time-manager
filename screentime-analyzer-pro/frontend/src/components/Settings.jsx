import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Database, Bell, Shield } from 'lucide-react';

const Settings = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Settings
        </h1>
        <p className="text-gray-400">
          Configure your ScreenTime Analyzer Pro
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <Database className="w-6 h-6 text-purple-400" />
          <h3 className="text-xl font-semibold">Data Management</h3>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
            <div>
              <p className="font-medium">Auto-save data</p>
              <p className="text-sm text-gray-400">Automatically save usage data every minute</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
            <div>
              <p className="font-medium">Data retention</p>
              <p className="text-sm text-gray-400">Keep data for 90 days</p>
            </div>
            <select className="bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white">
              <option value="30">30 days</option>
              <option value="60">60 days</option>
              <option value="90" selected>90 days</option>
              <option value="365">1 year</option>
            </select>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <Bell className="w-6 h-6 text-purple-400" />
          <h3 className="text-xl font-semibold">Notifications</h3>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
            <div>
              <p className="font-medium">Daily summary</p>
              <p className="text-sm text-gray-400">Receive daily usage summary</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" defaultChecked />
              <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
            </label>
          </div>

          <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
            <div>
              <p className="font-medium">Break reminders</p>
              <p className="text-sm text-gray-400">Remind to take breaks every 2 hours</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-500"></div>
            </label>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <Shield className="w-6 h-6 text-purple-400" />
          <h3 className="text-xl font-semibold">Privacy</h3>
        </div>
        
        <div className="space-y-4">
          <div className="p-4 bg-white/5 rounded-lg">
            <p className="font-medium mb-2">Data Privacy</p>
            <p className="text-sm text-gray-400 mb-4">
              All your data is stored locally on your device. We don't collect or share any personal information.
            </p>
            <button className="btn-secondary text-sm">
              View Privacy Policy
            </button>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="glass-card p-6"
      >
        <h3 className="text-xl font-semibold mb-4">About</h3>
        <div className="space-y-2 text-gray-400">
          <p><span className="text-white font-medium">Version:</span> 1.0.0</p>
          <p><span className="text-white font-medium">Platform:</span> Windows/macOS/Linux</p>
          <p><span className="text-white font-medium">Database:</span> SQLite</p>
          <p className="pt-4 text-sm">
            ScreenTime Analyzer Pro - A complete Data Science project for tracking and analyzing screen time.
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Settings;

