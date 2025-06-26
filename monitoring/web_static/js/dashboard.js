
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
                