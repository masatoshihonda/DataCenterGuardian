// Server data
const servers = [
    { id: 1, name: 'Web Server 01', ip: '192.168.1.10', cpu: 45, memory: 62, status: 'online', type: 'web' },
    { id: 2, name: 'Database Primary', ip: '192.168.1.20', cpu: 78, memory: 85, status: 'warning', type: 'database' },
    { id: 3, name: 'API Gateway', ip: '192.168.1.30', cpu: 32, memory: 48, status: 'online', type: 'api' },
    { id: 4, name: 'Cache Server', ip: '192.168.1.40', cpu: 25, memory: 72, status: 'online', type: 'cache' },
    { id: 5, name: 'Worker Node 01', ip: '192.168.1.50', cpu: 88, memory: 91, status: 'warning', type: 'worker' },
    { id: 6, name: 'Load Balancer', ip: '192.168.1.60', cpu: 15, memory: 35, status: 'online', type: 'network' },
    { id: 7, name: 'Storage Server', ip: '192.168.1.70', cpu: 22, memory: 68, status: 'online', type: 'storage' },
    { id: 8, name: 'Backup Server', ip: '192.168.1.80', cpu: 5, memory: 45, status: 'offline', type: 'backup' },
];

// Alert data
const alerts = [
    { id: 1, type: 'critical', title: 'High Memory Usage', description: 'Worker Node 01 memory usage exceeded 90%', time: '5 min ago', icon: '🔴' },
    { id: 2, type: 'critical', title: 'Database Connection Pool', description: 'Database Primary connection pool at 95% capacity', time: '12 min ago', icon: '🔴' },
    { id: 3, type: 'warning', title: 'CPU Spike Detected', description: 'Database Primary CPU usage above 75%', time: '23 min ago', icon: '🟡' },
    { id: 4, type: 'info', title: 'Backup Completed', description: 'Daily backup completed successfully', time: '1 hour ago', icon: '🔵' },
    { id: 5, type: 'warning', title: 'Disk Space Warning', description: 'Storage Server disk usage at 82%', time: '2 hours ago', icon: '🟡' },
];

// Server type icons
const serverIcons = {
    web: '🌐',
    database: '🗄️',
    api: '⚡',
    cache: '💾',
    worker: '⚙️',
    network: '🔀',
    storage: '📦',
    backup: '💿',
};

// Render server list
function renderServers() {
    const serverList = document.getElementById('server-list');
    serverList.innerHTML = servers.map(server => `
        <div class="server-item">
            <div class="server-info">
                <span class="server-icon">${serverIcons[server.type]}</span>
                <div>
                    <div class="server-name">${server.name}</div>
                    <div class="server-ip">${server.ip}</div>
                </div>
            </div>
            <div class="server-metrics">
                <div class="metric">
                    <span>${server.cpu}%</span>
                    <span class="metric-label">CPU</span>
                </div>
                <div class="metric">
                    <span>${server.memory}%</span>
                    <span class="metric-label">MEM</span>
                </div>
            </div>
            <span class="server-status-badge ${server.status}">${server.status}</span>
        </div>
    `).join('');
}

// Render alerts
function renderAlerts() {
    const alertsList = document.getElementById('alerts-list');
    alertsList.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.type}">
            <span class="alert-icon">${alert.icon}</span>
            <div class="alert-content">
                <div class="alert-title">${alert.title}</div>
                <div class="alert-description">${alert.description}</div>
            </div>
            <span class="alert-time">${alert.time}</span>
        </div>
    `).join('');
}

// Update last updated timestamp
function updateTimestamp() {
    const now = new Date();
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('last-updated').textContent = now.toLocaleDateString('en-US', options);
}

// Simulate data refresh
function refreshData() {
    // Simulate random metric updates
    servers.forEach(server => {
        if (server.status !== 'offline') {
            server.cpu = Math.min(100, Math.max(5, server.cpu + (Math.random() * 20 - 10)));
            server.memory = Math.min(100, Math.max(20, server.memory + (Math.random() * 10 - 5)));

            // Update status based on metrics
            if (server.cpu > 85 || server.memory > 90) {
                server.status = 'warning';
            } else {
                server.status = 'online';
            }
        }
    });

    // Update stats
    const avgCpu = Math.round(servers.filter(s => s.status !== 'offline').reduce((sum, s) => sum + s.cpu, 0) / servers.filter(s => s.status !== 'offline').length);
    document.getElementById('cpu-usage').textContent = avgCpu + '%';

    const warningCount = servers.filter(s => s.status === 'warning').length +
                         alerts.filter(a => a.type === 'critical' || a.type === 'warning').length;
    document.getElementById('alerts').textContent = warningCount;

    renderServers();
    updateTimestamp();

    // Visual feedback
    const btn = document.querySelector('.refresh-btn');
    btn.textContent = '✓ Updated';
    setTimeout(() => {
        btn.textContent = '🔄 Refresh';
    }, 1000);
}

// Auto-refresh every 30 seconds
setInterval(() => {
    refreshData();
}, 30000);

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    renderServers();
    renderAlerts();
    updateTimestamp();
});
