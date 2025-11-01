const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting ScreenTime Analyzer Pro...\n');

// Start backend
console.log('📡 Starting backend server...');
const backendPath = path.join(__dirname, '../backend');
const backendCmd = process.platform === 'win32' 
  ? 'cmd'
  : 'bash';
const backendArgs = process.platform === 'win32'
  ? ['/c', 'venv\\Scripts\\activate && python main.py']
  : ['-c', 'source venv/bin/activate && python main.py'];

const backend = spawn(backendCmd, backendArgs, {
  cwd: backendPath,
  shell: true,
  stdio: 'inherit'
});

// Wait 3 seconds for backend to start
setTimeout(() => {
  console.log('\n🎨 Starting frontend...');
  const frontendPath = path.join(__dirname, '../frontend');
  const frontendCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
  
  const frontend = spawn(frontendCmd, ['run', 'dev'], {
    cwd: frontendPath,
    shell: true,
    stdio: 'inherit'
  });

  frontend.on('error', (error) => {
    console.error('Failed to start frontend:', error);
  });
}, 3000);

backend.on('error', (error) => {
  console.error('Failed to start backend:', error);
});

// Handle exit
process.on('SIGINT', () => {
  console.log('\n\n🛑 Shutting down...');
  process.exit();
});

