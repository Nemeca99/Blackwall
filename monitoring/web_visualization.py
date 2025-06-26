"""
Web-Based Visualization for BlackwallV2 Monitoring Dashboard
-----------------------------------------------------------

This module provides a web interface for the system monitoring dashboard,
allowing real-time visualization of system metrics through a browser.

It uses Flask to serve the dashboard and charts.js for visualization.
"""

import os
import time
import json
import threading
from flask import Flask, render_template, jsonify
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashboardWebServer:
    """Web server for visualizing BlackwallV2 system metrics."""
    
    def __init__(self, dashboard, host='localhost', port=5000):
        """Initialize the web server with dashboard connection.
        
        Args:
            dashboard: SystemMonitoringDashboard instance to visualize
            host: Host address to bind the server (default: localhost)
            port: Port to run the server on (default: 5000)
        """
        self.dashboard = dashboard
        self.host = host
        self.port = port
        
        # Create Flask app
        self.app = Flask(
            __name__, 
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_static"),
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_templates")
        )
        
        # Ensure directories exist
        self._create_web_directories()
        
        # Set up routes
        self._setup_routes()
        
        # Server thread
        self._server_thread = None
    
    def _create_web_directories(self):
        """Create necessary directories for web assets."""
        web_static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_static")
        web_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_templates")
        
        Path(web_static).mkdir(parents=True, exist_ok=True)
        Path(web_templates).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(web_static, "js")).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(web_static, "css")).mkdir(parents=True, exist_ok=True)
        
        # Create CSS file
        self._create_css_file()
        
        # Create JavaScript file
        self._create_js_file()
        
        # Create HTML template
        self._create_html_template()
    
    def _create_css_file(self):
        """Create CSS file for the dashboard."""
        css_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "web_static/css/dashboard.css"
        )
        
        if not os.path.exists(css_path):
            with open(css_path, 'w') as f:
                f.write("""
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

.container {
    width: 90%;
    margin: 20px auto;
}

header {
    background-color: #222;
    color: white;
    padding: 1em;
    text-align: center;
}

h1 {
    margin: 0;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 20px;
    margin-top: 20px;
}

.card {
    background-color: white;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    padding: 15px;
}

.card-header {
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h2 {
    margin: 0;
    font-size: 1.2rem;
}

.chart-container {
    height: 250px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 15px;
}

.metric-box {
    background-color: #f9f9f9;
    border-radius: 3px;
    padding: 10px;
    text-align: center;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 5px 0;
}

.metric-label {
    color: #666;
    font-size: 0.9rem;
}

footer {
    margin-top: 30px;
    text-align: center;
    color: #666;
    font-size: 0.9rem;
    padding: 10px;
}

.refresh-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
}

.refresh-button:hover {
    background-color: #45a049;
}
                """)
    
    def _create_js_file(self):
        """Create JavaScript file for the dashboard."""
        js_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "web_static/js/dashboard.js"
        )
        
        if not os.path.exists(js_path):
            with open(js_path, 'w') as f:
                f.write("""
// Dashboard refresh interval in milliseconds
const REFRESH_INTERVAL = 5000;

// Chart instances
let charts = {};

// Create colors for charts
const chartColors = [
    'rgb(255, 99, 132)',
    'rgb(54, 162, 235)',
    'rgb(255, 206, 86)',
    'rgb(75, 192, 192)',
    'rgb(153, 102, 255)',
    'rgb(255, 159, 64)'
];

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    updateDashboard();
    
    // Set up automatic refresh
    setInterval(updateDashboard, REFRESH_INTERVAL);
    
    // Manual refresh button
    document.getElementById('refresh-button').addEventListener('click', updateDashboard);
});

// Initialize all charts
function initCharts() {
    initMediaProcessingChart();
    initMemoryUsageChart();
    initFragmentRoutingChart();
    initSystemResourcesChart();
}

// Initialize the media processing chart
function initMediaProcessingChart() {
    const ctx = document.getElementById('media-processing-chart').getContext('2d');
    charts.mediaProcessing = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Text (ms)',
                    data: [],
                    borderColor: chartColors[0],
                    backgroundColor: 'transparent',
                    tension: 0.1
                },
                {
                    label: 'Image (ms)',
                    data: [],
                    borderColor: chartColors[1],
                    backgroundColor: 'transparent',
                    tension: 0.1
                },
                {
                    label: 'Audio (ms)',
                    data: [],
                    borderColor: chartColors[2],
                    backgroundColor: 'transparent',
                    tension: 0.1
                },
                {
                    label: 'Video (ms)',
                    data: [],
                    borderColor: chartColors[3],
                    backgroundColor: 'transparent',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Processing Time (ms)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// Initialize the memory usage chart
function initMemoryUsageChart() {
    const ctx = document.getElementById('memory-usage-chart').getContext('2d');
    charts.memoryUsage = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Used Memory (MB)',
                    data: [],
                    borderColor: chartColors[0],
                    backgroundColor: 'transparent',
                    tension: 0.1
                },
                {
                    label: 'Free Memory (MB)',
                    data: [],
                    borderColor: chartColors[1],
                    backgroundColor: 'transparent',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Memory (MB)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// Initialize the fragment routing chart
function initFragmentRoutingChart() {
    const ctx = document.getElementById('fragment-routing-chart').getContext('2d');
    charts.fragmentRouting = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Text', 'Image', 'Audio', 'Video'],
            datasets: [
                {
                    label: 'Routing Efficiency',
                    data: [0, 0, 0, 0],
                    backgroundColor: [
                        chartColors[0],
                        chartColors[1],
                        chartColors[2],
                        chartColors[3]
                    ]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Efficiency (%)'
                    }
                }
            }
        }
    });
}

// Initialize the system resources chart
function initSystemResourcesChart() {
    const ctx = document.getElementById('system-resources-chart').getContext('2d');
    charts.systemResources = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU Usage (%)',
                    data: [],
                    borderColor: chartColors[0],
                    backgroundColor: 'transparent',
                    tension: 0.1
                },
                {
                    label: 'Disk I/O (MB/s)',
                    data: [],
                    borderColor: chartColors[1],
                    backgroundColor: 'transparent',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Usage'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// Update all dashboard components
function updateDashboard() {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            updateLastUpdated(data.timestamp);
            updateMetricsCards(data.metrics);
            updateCharts(data);
        })
        .catch(error => console.error('Error fetching metrics:', error));
}

// Update the last updated timestamp
function updateLastUpdated(timestamp) {
    const date = new Date(timestamp * 1000);
    document.getElementById('last-updated').textContent = date.toLocaleTimeString();
}

// Update all metric cards
function updateMetricsCards(metrics) {
    // Media processing metrics
    if (metrics.media_processing) {
        updateMetricValue('text-processed', metrics.media_processing.text_processed || 0);
        updateMetricValue('image-processed', metrics.media_processing.image_processed || 0);
        updateMetricValue('audio-processed', metrics.media_processing.audio_processed || 0);
        updateMetricValue('video-processed', metrics.media_processing.video_processed || 0);
    }
    
    // Memory system metrics
    if (metrics.memory_system) {
        updateMetricValue('memory-usage', formatMemory(metrics.memory_system.used_memory || 0));
        updateMetricValue('memory-items', metrics.memory_system.stored_items || 0);
        updateMetricValue('memory-ratio', formatRatio(metrics.memory_system.compression_ratio || 0));
        updateMetricValue('cross-modal-links', metrics.memory_system.cross_modal_links || 0);
    }
    
    // Fragment routing metrics
    if (metrics.fragment_performance) {
        updateMetricValue('text-efficiency', formatPercent(metrics.fragment_performance.text_efficiency || 0));
        updateMetricValue('image-efficiency', formatPercent(metrics.fragment_performance.image_efficiency || 0));
        updateMetricValue('audio-efficiency', formatPercent(metrics.fragment_performance.audio_efficiency || 0));
        updateMetricValue('video-efficiency', formatPercent(metrics.fragment_performance.video_efficiency || 0));
    }
    
    // System resources
    if (metrics.system_resources) {
        updateMetricValue('cpu-usage', formatPercent(metrics.system_resources.cpu_percent || 0));
        updateMetricValue('disk-io', formatIO(metrics.system_resources.disk_io || 0));
    }
}

// Update a metric value by ID
function updateMetricValue(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

// Format memory size
function formatMemory(value) {
    return `${Math.round(value)} MB`;
}

// Format ratio
function formatRatio(value) {
    return value.toFixed(2) + ':1';
}

// Format percentage
function formatPercent(value) {
    return `${Math.round(value)}%`;
}

// Format I/O rate
function formatIO(value) {
    return `${value.toFixed(1)} MB/s`;
}

// Update all charts
function updateCharts(data) {
    const timeLabel = new Date().toLocaleTimeString();
    
    // Update media processing chart
    if (data.metrics.media_processing) {
        updateTimeSeriesChart(
            charts.mediaProcessing,
            timeLabel,
            [
                data.metrics.media_processing.text_avg_time || 0,
                data.metrics.media_processing.image_avg_time || 0,
                data.metrics.media_processing.audio_avg_time || 0,
                data.metrics.media_processing.video_avg_time || 0
            ]
        );
    }
    
    // Update memory usage chart
    if (data.metrics.memory_system) {
        updateTimeSeriesChart(
            charts.memoryUsage,
            timeLabel,
            [
                data.metrics.memory_system.used_memory || 0,
                data.metrics.memory_system.free_memory || 0
            ]
        );
    }
    
    // Update fragment routing chart
    if (data.metrics.fragment_performance) {
        charts.fragmentRouting.data.datasets[0].data = [
            data.metrics.fragment_performance.text_efficiency || 0,
            data.metrics.fragment_performance.image_efficiency || 0,
            data.metrics.fragment_performance.audio_efficiency || 0,
            data.metrics.fragment_performance.video_efficiency || 0
        ];
        charts.fragmentRouting.update();
    }
    
    // Update system resources chart
    if (data.metrics.system_resources) {
        updateTimeSeriesChart(
            charts.systemResources,
            timeLabel,
            [
                data.metrics.system_resources.cpu_percent || 0,
                data.metrics.system_resources.disk_io || 0
            ]
        );
    }
}

// Update a time series chart
function updateTimeSeriesChart(chart, timeLabel, values) {
    chart.data.labels.push(timeLabel);
    
    // Keep only the last 10 points for readability
    if (chart.data.labels.length > 10) {
        chart.data.labels.shift();
    }
    
    // Update each dataset
    for (let i = 0; i < values.length; i++) {
        chart.data.datasets[i].data.push(values[i]);
        
        // Keep only the last 10 points
        if (chart.data.datasets[i].data.length > 10) {
            chart.data.datasets[i].data.shift();
        }
    }
    
    chart.update();
}
                """)
    
    def _create_html_template(self):
        """Create HTML template for the dashboard."""
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "web_templates/dashboard.html"
        )
        
        if not os.path.exists(template_path):
            with open(template_path, 'w') as f:
                f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlackwallV2 Monitoring Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <header>
        <h1>BlackwallV2 Monitoring Dashboard</h1>
        <p>Last updated: <span id="last-updated">-</span> 
           <button id="refresh-button" class="refresh-button">Refresh</button></p>
    </header>
    
    <div class="container">
        <div class="dashboard">
            <!-- Media Processing Card -->
            <div class="card">
                <div class="card-header">
                    <h2>Media Processing Performance</h2>
                </div>
                <div class="chart-container">
                    <canvas id="media-processing-chart"></canvas>
                </div>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-value" id="text-processed">0</div>
                        <div class="metric-label">Text Items</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="image-processed">0</div>
                        <div class="metric-label">Image Items</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="audio-processed">0</div>
                        <div class="metric-label">Audio Items</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="video-processed">0</div>
                        <div class="metric-label">Video Items</div>
                    </div>
                </div>
            </div>
            
            <!-- Memory System Card -->
            <div class="card">
                <div class="card-header">
                    <h2>Memory System</h2>
                </div>
                <div class="chart-container">
                    <canvas id="memory-usage-chart"></canvas>
                </div>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-value" id="memory-usage">0 MB</div>
                        <div class="metric-label">Memory Usage</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="memory-items">0</div>
                        <div class="metric-label">Stored Items</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="memory-ratio">0:1</div>
                        <div class="metric-label">Compression Ratio</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="cross-modal-links">0</div>
                        <div class="metric-label">Cross-modal Links</div>
                    </div>
                </div>
            </div>
            
            <!-- Fragment Routing Card -->
            <div class="card">
                <div class="card-header">
                    <h2>Fragment Routing Efficiency</h2>
                </div>
                <div class="chart-container">
                    <canvas id="fragment-routing-chart"></canvas>
                </div>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-value" id="text-efficiency">0%</div>
                        <div class="metric-label">Text Efficiency</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="image-efficiency">0%</div>
                        <div class="metric-label">Image Efficiency</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="audio-efficiency">0%</div>
                        <div class="metric-label">Audio Efficiency</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="video-efficiency">0%</div>
                        <div class="metric-label">Video Efficiency</div>
                    </div>
                </div>
            </div>
            
            <!-- System Resources Card -->
            <div class="card">
                <div class="card-header">
                    <h2>System Resources</h2>
                </div>
                <div class="chart-container">
                    <canvas id="system-resources-chart"></canvas>
                </div>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <div class="metric-value" id="cpu-usage">0%</div>
                        <div class="metric-label">CPU Usage</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value" id="disk-io">0 MB/s</div>
                        <div class="metric-label">Disk I/O</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <p>BlackwallV2 (Lyra) Monitoring System | &copy; 2025 UML Calculator</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
</body>
</html>
                """)
    
    def _setup_routes(self):
        """Set up Flask routes for the dashboard."""
        
        @self.app.route('/')
        def index():
            """Render the dashboard home page."""
            return render_template('dashboard.html')
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """API endpoint for fetching current metrics."""
            return jsonify(self.dashboard.get_dashboard_data())
    
    def start(self, background=True):
        """Start the dashboard web server.
        
        Args:
            background: If True, start the server in a background thread
        
        Returns:
            URL of the dashboard if started in the background
        """
        if background:
            if self._server_thread and self._server_thread.is_alive():
                logger.warning("Dashboard server already running")
                return f"http://{self.host}:{self.port}"
            
            self._server_thread = threading.Thread(
                target=self.app.run,
                kwargs={'host': self.host, 'port': self.port, 'debug': False}
            )
            self._server_thread.daemon = True  # Thread will exit when main thread exits
            self._server_thread.start()
            logger.info(f"Dashboard server started in background at http://{self.host}:{self.port}/")
            return f"http://{self.host}:{self.port}"
        else:
            logger.info(f"Starting dashboard server at http://{self.host}:{self.port}/")
            self.app.run(host=self.host, port=self.port)
            return None
    
    def stop(self):
        """Stop the dashboard server if running in the background."""
        if self._server_thread and self._server_thread.is_alive():
            # Flask doesn't provide a clean way to stop from another thread
            logger.info("Dashboard server shutdown requested, but Flask doesn't support clean shutdown from another thread")
            logger.info("Server will terminate when the main application exits")
        else:
            logger.info("Dashboard server not running")


# Example usage
if __name__ == "__main__":
    # Create a mock dashboard for testing
    from system_dashboard import SystemMonitoringDashboard
    
    dashboard = SystemMonitoringDashboard()
    server = DashboardWebServer(dashboard)
      # Start the server (not in background for this example)
    server.start(background=False)
