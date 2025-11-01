/**
 * WebSocket client for real-time usage updates.
 */

class SocketClient {
  constructor() {
    this.ws = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.isConnecting = false;
    this.shouldReconnect = true;
  }

  /**
   * Connect to WebSocket server
   */
  connect(url = 'ws://127.0.0.1:8000/ws/usage') {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    if (this.isConnecting) {
      console.log('WebSocket connection already in progress');
      return;
    }

    this.isConnecting = true;
    console.log(`🔌 Connecting to WebSocket: ${url}`);

    try {
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.emit('connected');

        // Start ping interval
        this.startPingInterval();
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message:', data.event);
          
          // Emit event to listeners
          this.emit(data.event, data);
          this.emit('message', data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        this.emit('error', error);
      };

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        this.isConnecting = false;
        this.stopPingInterval();
        this.emit('disconnected');

        // Attempt reconnection
        if (this.shouldReconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`🔄 Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          
          setTimeout(() => {
            this.connect(url);
          }, this.reconnectDelay);
        } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          console.error('❌ Max reconnection attempts reached');
          this.emit('max_reconnect_reached');
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.isConnecting = false;
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    this.shouldReconnect = false;
    this.stopPingInterval();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Send message to server
   */
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      if (typeof data === 'string') {
        this.ws.send(data);
      } else {
        this.ws.send(JSON.stringify(data));
      }
    } else {
      console.warn('WebSocket not connected');
    }
  }

  /**
   * Send ping to keep connection alive
   */
  ping() {
    this.send('ping');
  }

  /**
   * Request current session
   */
  getCurrentSession() {
    this.send('get_current');
  }

  /**
   * Start ping interval
   */
  startPingInterval() {
    this.stopPingInterval();
    this.pingInterval = setInterval(() => {
      this.ping();
    }, 30000); // Ping every 30 seconds
  }

  /**
   * Stop ping interval
   */
  stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  /**
   * Register event listener
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * Emit event to listeners
   */
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in ${event} listener:`, error);
        }
      });
    }
  }

  /**
   * Get connection status
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

// Export singleton instance
const socketClient = new SocketClient();
export default socketClient;

