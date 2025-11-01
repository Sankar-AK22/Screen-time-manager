/**
 * WebSocket Service for Real-Time Screen Time Tracking
 * Connects to backend WebSocket and handles real-time updates
 */

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000;
    this.listeners = new Map();
    this.isConnecting = false;
    this.isConnected = false;
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    if (this.isConnecting || this.isConnected) {
      console.log('WebSocket already connected or connecting');
      return;
    }

    this.isConnecting = true;

    try {
      // Determine WebSocket URL based on current location
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.hostname;
      const port = 8000; // Backend port
      const wsUrl = `${protocol}//${host}:${port}/api/v1/ws/realtime`;

      console.log('🔌 Connecting to WebSocket:', wsUrl);

      this.ws = new WebSocket(wsUrl);

      // Connection opened
      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.isConnected = true;
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.emit('connected', { timestamp: new Date() });
      };

      // Listen for messages
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message:', data);
          
          // Emit event based on message type
          if (data.type) {
            this.emit(data.type, data);
          }
          
          // Emit general message event
          this.emit('message', data);
        } catch (error) {
          console.error('❌ Error parsing WebSocket message:', error);
        }
      };

      // Connection closed
      this.ws.onclose = (event) => {
        console.log('🔌 WebSocket disconnected:', event.code, event.reason);
        this.isConnected = false;
        this.isConnecting = false;
        this.emit('disconnected', { code: event.code, reason: event.reason });

        // Attempt to reconnect
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`🔄 Reconnecting... (Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          setTimeout(() => this.connect(), this.reconnectDelay);
        } else {
          console.error('❌ Max reconnection attempts reached');
          this.emit('reconnect_failed', { attempts: this.reconnectAttempts });
        }
      };

      // Connection error
      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        this.isConnecting = false;
        this.emit('error', { error });
      };

    } catch (error) {
      console.error('❌ Error creating WebSocket:', error);
      this.isConnecting = false;
      this.emit('error', { error });
    }
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.ws) {
      console.log('🔌 Disconnecting WebSocket...');
      this.reconnectAttempts = this.maxReconnectAttempts; // Prevent auto-reconnect
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
      this.isConnecting = false;
    }
  }

  /**
   * Send message to WebSocket server
   */
  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
      console.log('📤 Sent WebSocket message:', data);
    } else {
      console.warn('⚠️  WebSocket not connected, cannot send message');
    }
  }

  /**
   * Send ping to keep connection alive
   */
  ping() {
    this.send({ type: 'ping' });
  }

  /**
   * Request current session info
   */
  getCurrentSession() {
    this.send({ type: 'get_current' });
  }

  /**
   * Add event listener
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
   * Emit event to all listeners
   */
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`❌ Error in event listener for '${event}':`, error);
        }
      });
    }
  }

  /**
   * Remove all event listeners
   */
  removeAllListeners() {
    this.listeners.clear();
  }

  /**
   * Get connection status
   */
  getStatus() {
    return {
      isConnected: this.isConnected,
      isConnecting: this.isConnecting,
      reconnectAttempts: this.reconnectAttempts,
      readyState: this.ws ? this.ws.readyState : null
    };
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

export default websocketService;

