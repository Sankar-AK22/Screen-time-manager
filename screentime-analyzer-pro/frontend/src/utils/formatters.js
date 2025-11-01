// Format duration (handles both minutes and seconds)
export const formatDuration = (value, unit = 'minutes') => {
  if (!value) return '0s';

  let totalSeconds;

  if (unit === 'seconds') {
    totalSeconds = Math.floor(value);
  } else {
    // Assume minutes
    totalSeconds = Math.floor(value * 60);
  }

  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  if (hours > 0) {
    if (minutes === 0) return `${hours}h`;
    return `${hours}h ${minutes}m`;
  }

  if (minutes > 0) {
    if (seconds === 0) return `${minutes}m`;
    return `${minutes}m ${seconds}s`;
  }

  return `${seconds}s`;
};

// Format date
export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

// Format time
export const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Get productivity color
export const getProductivityColor = (score) => {
  if (score >= 7) return 'text-green-400';
  if (score >= 5) return 'text-yellow-400';
  return 'text-red-400';
};

// Get category color
export const getCategoryColor = (category) => {
  const colors = {
    Development: '#667eea',
    Productivity: '#4ade80',
    Browser: '#60a5fa',
    Communication: '#f59e0b',
    Entertainment: '#ec4899',
    Design: '#8b5cf6',
    Other: '#94a3b8'
  };
  return colors[category] || colors.Other;
};

// Get category icon
export const getCategoryIcon = (category) => {
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

// Calculate percentage
export const calculatePercentage = (value, total) => {
  if (!total) return 0;
  return Math.round((value / total) * 100);
};

