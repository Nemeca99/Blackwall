# BlackwallV2 System Monitoring Dashboard

This package provides a comprehensive monitoring dashboard for the BlackwallV2 (Lyra) system, with a special focus on media processing metrics. The dashboard supports both console-based summaries and an interactive web-based visualization.

## Overview

The monitoring dashboard collects, processes, and visualizes metrics from various system components, providing insights into:

- Media processing performance
- Memory system efficiency
- Fragment routing performance
- System resource utilization

## Visualization Options

The dashboard offers two visualization modes:

1. **Console Output**: Text-based summaries of system metrics
2. **Web Dashboard**: Interactive visualization with real-time charts

## Components

### 1. System Dashboard (`system_dashboard.py`)

The main dashboard component that:

- Collects metrics from all system components
- Schedules periodic metric collection
- Saves metric snapshots
- Provides data for visualization

### 2. Media Metrics Collector (`media_metrics.py`)

Specialized collector for media-specific metrics:

- Tracks processing time by media type
- Monitors media processing success rates
- Records UML transformation efficiency
- Calculates media-specific performance indicators

### 3. Web Visualization (`web_visualization.py`)

Interactive web-based dashboard:

- Real-time metric visualization with Chart.js
- Time-series tracking of system performance
- Media-specific performance charts
- System resource monitoring

## Usage

### Running the Console Demo

To run the demo with console output:

```bash
python monitoring_demo.py
```

### Running the Web Dashboard

To launch the interactive web dashboard:

```bash
python monitoring_demo.py --web
```

For an extended demo run:

```bash
python monitoring_demo.py --web --duration 120
```

For indefinite running:

```bash
python monitoring_demo.py --web --duration 0
```

## Future Enhancements

Additional features planned for future development:

### 1. Advanced Alert System

- Threshold-based alerts
- Anomaly detection
- Notification system

### 2. Comprehensive API

- Data export capabilities
- Integration with external monitoring tools
- Custom metric registration

## Code Examples

```python
# Import the dashboard
from monitoring.system_dashboard import SystemMonitoringDashboard
from monitoring.media_metrics import MediaMetricsCollector

# Initialize the dashboard
dashboard = SystemMonitoringDashboard()

# Initialize the media metrics collector with the dashboard
media_metrics = MediaMetricsCollector(dashboard)

# Start monitoring
dashboard.start_monitoring()

# Record media-specific metrics
media_metrics.record_processing_time("image", 150)
media_metrics.record_media_processed("image", success=True)

# Get the current metrics
metrics = dashboard.get_dashboard_data()

# Stop monitoring when done
dashboard.stop_monitoring()
```

## Integration Points

The monitoring dashboard is designed to integrate with:

1. `media_feature_extraction.py` - for tracking feature extraction performance
2. `media_enhanced_memory.py` - for monitoring memory usage and retrieval efficiency
3. `media_aware_routing.py` - for tracking fragment routing performance
4. `integration/media_integration.py` - for system-level metrics

## Expected Completion

The web-based visualization component is expected to be completed by July 15, 2025.
