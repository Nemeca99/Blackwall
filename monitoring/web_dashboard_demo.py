"""
Web Dashboard Demo Script
------------------------

This script demonstrates the web-based visualization dashboard for BlackwallV2.
It simulates metrics from all components and starts a Flask web server.
"""

import time
import random
import os
import sys
from pathlib import Path
import logging

# Add the Implementation directory to the Python path if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
implementation_dir = os.path.dirname(script_dir)
if implementation_dir not in sys.path:
    sys.path.append(implementation_dir)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from monitoring.system_dashboard import SystemMonitoringDashboard
    from monitoring.media_metrics import MediaMetricsCollector
    from monitoring.web_visualization import DashboardWebServer
except ImportError as e:
    logger.error(f"Import error: {e}")
    print("\nDependency Error: Flask is required for the web dashboard.")
    print("Please install it using: pip install flask")
    print("Note: If you're seeing other import errors, make sure you're running this script from the correct directory.")
    sys.exit(1)

def simulate_all_metrics(dashboard, media_metrics):
    """
    Simulate metrics for all system components.
    
    Args:
        dashboard: System dashboard instance
        media_metrics: Media metrics collector instance
    """
    # Media processing metrics
    for media_type in ["text", "image", "audio", "video"]:
        # Simulate processing times
        if media_type == "text":
            processing_time = random.uniform(10, 50)  # 10-50ms
        elif media_type == "image":
            processing_time = random.uniform(50, 250)  # 50-250ms
        elif media_type == "audio":
            processing_time = random.uniform(100, 500)  # 100-500ms
        else:  # video
            processing_time = random.uniform(200, 1000)  # 200-1000ms
            
        # Record processing time
        media_metrics.record_processing_time(media_type, processing_time)
        
        # Record UML transform metrics
        success = random.random() > 0.05  # 95% success rate
        compression = random.uniform(0.4, 0.8) if success else 0
        media_metrics.record_uml_transform(media_type, success, compression)
        
        # Increment processed counter
        media_metrics.increment_processed(media_type)
        
        # Add to dashboard
        dashboard.metrics["media_processing"][f"{media_type}_processed"] = \
            media_metrics.media_counters["processed"][media_type]
        dashboard.metrics["media_processing"][f"{media_type}_avg_time"] = \
            sum(media_metrics.processing_times[media_type][-10:]) / max(1, len(media_metrics.processing_times[media_type][-10:]))
    
    # Memory system metrics
    used_memory = random.uniform(100, 500)  # MB
    free_memory = random.uniform(500, 1500)  # MB
    stored_items = random.randint(1000, 10000)
    compression_ratio = random.uniform(2.5, 6.0)
    cross_modal_links = random.randint(50, 500)
    
    dashboard.metrics["memory_system"]["used_memory"] = used_memory
    dashboard.metrics["memory_system"]["free_memory"] = free_memory
    dashboard.metrics["memory_system"]["stored_items"] = stored_items
    dashboard.metrics["memory_system"]["compression_ratio"] = compression_ratio
    dashboard.metrics["memory_system"]["cross_modal_links"] = cross_modal_links
    
    # Fragment routing metrics
    for media_type in ["text", "image", "audio", "video"]:
        efficiency = random.uniform(60, 95)  # 60-95% efficiency
        dashboard.metrics["fragment_performance"][f"{media_type}_efficiency"] = efficiency
    
    # System resources
    cpu_percent = random.uniform(5, 80)  # 5-80% CPU
    disk_io = random.uniform(0.1, 10.0)  # 0.1-10 MB/s
    
    dashboard.metrics["system_resources"]["cpu_percent"] = cpu_percent
    dashboard.metrics["system_resources"]["disk_io"] = disk_io
    
    # Update timestamps
    current_time = time.time()
    for category in dashboard.metrics:
        dashboard.metrics[category]["timestamp"] = current_time
    
    # Log update
    logger.info(f"Updated {len(dashboard.metrics)} metric categories")


def main():
    """Run the web dashboard demo."""
    print("="*80)
    print("BlackwallV2 Web Dashboard Demo")
    print("="*80)
    
    # Create dashboard and metrics collector
    dashboard = SystemMonitoringDashboard()
    media_metrics = MediaMetricsCollector(dashboard)
    
    # Create web server
    try:
        server = DashboardWebServer(dashboard)
        dashboard_url = server.start(background=True)
        print(f"\nDashboard is now available at: {dashboard_url}")
        print("Keep this terminal open to continue running the dashboard.")
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        print("\nError starting the web server. Please make sure Flask is installed:")
        print("pip install flask")
        return
    
    # Main loop to update metrics
    try:
        print("\nSimulating system metrics. Press Ctrl+C to stop...")
        while True:
            # Simulate metrics
            simulate_all_metrics(dashboard, media_metrics)
            
            # Sleep for a bit
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nStopping dashboard demo...")
    finally:
        print("Dashboard demo stopped. You can close this terminal window.")

if __name__ == "__main__":
    main()
