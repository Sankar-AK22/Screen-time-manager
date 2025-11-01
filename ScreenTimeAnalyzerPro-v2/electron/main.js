const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#0B0B0B',
    icon: path.join(__dirname, '../frontend/public/icon.png'),
    title: 'ScreenTime Analyzer Pro'
  });

  // Load the frontend
  mainWindow.loadURL('http://localhost:3000');

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startBackend() {
  console.log('Starting backend server...');
  
  const pythonPath = process.platform === 'win32' 
    ? path.join(__dirname, '../backend/venv/Scripts/python.exe')
    : path.join(__dirname, '../backend/venv/bin/python');
  
  const backendPath = path.join(__dirname, '../backend/main.py');
  
  backendProcess = spawn(pythonPath, [backendPath], {
    cwd: path.join(__dirname, '../backend'),
    stdio: 'inherit'
  });

  backendProcess.on('error', (error) => {
    console.error('Failed to start backend:', error);
  });

  backendProcess.on('exit', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
}

function stopBackend() {
  if (backendProcess) {
    console.log('Stopping backend server...');
    backendProcess.kill();
    backendProcess = null;
  }
}

app.on('ready', () => {
  // Start backend first
  startBackend();
  
  // Wait 3 seconds for backend to start, then create window
  setTimeout(() => {
    createWindow();
  }, 3000);
});

app.on('window-all-closed', () => {
  stopBackend();
  app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', () => {
  stopBackend();
});

