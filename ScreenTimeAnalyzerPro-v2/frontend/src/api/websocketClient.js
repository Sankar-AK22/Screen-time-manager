class WebSocketClient {
  constructor() {
    this.ws = null;
    this.url = 'ws://127.0.0.1:8000/ws/usage';
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 999; // Unlimited reconnection attempts
    this.reconnectDelay = 5000; // 5 seconds between reconnection attempts
    this.listeners = {};
    this.isConnected = false;
    this.shouldReconnect = true;
    this.pingInterval = null;
  }

  connect() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    console.log('Connecting to WebSocket...');

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.emit('connected');

        // Request current session
        this.send('get_current');

        // Start ping interval (every 4 seconds to match backend heartbeat)
        this.startPingInterval();
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message:', data);

          if (data.event) {
            this.emit(data.event, data);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        this.isConnected = false;
        this.emit('error', error);
      };

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        this.isConnected = false;
        this.emit('disconnected');
        this.stopPingInterval();

        // Always attempt to reconnect
        if (this.shouldReconnect) {
          this.reconnectAttempts++;
          console.log(`🔄 Reconnecting... (attempt ${this.reconnectAttempts})`);
          setTimeout(() => this.connect(), this.reconnectDelay);
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.isConnected = false;

      // Retry connection
      if (this.shouldReconnect) {
        setTimeout(() => this.connect(), this.reconnectDelay);
      }
    }
  }

  disconnect() {
    this.shouldReconnect = false;
    this.stopPingInterval();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.isConnected = false;
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }

  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data));
    }
  }

  startPingInterval() {
    this.stopPingInterval(); // Clear any existing interval
    this.pingInterval = setInterval(() => {
      if (this.isConnected) {
        this.send('ping');
      }
    }, 4000); // Ping every 4 seconds to keep connection alive
  }

  stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  getConnectionStatus() {
    return this.isConnected;
  }
}

// Create singleton instance
const websocketClient = new WebSocketClient();

export default websocketClient;

