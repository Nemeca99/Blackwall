"""
Monitoring Dashboard Demo Script
-------------------------------

This script demonstrates the use of the BlackwallV2 monitoring dashboard
with simulated media processing workloads. It can run in either console mode
or web dashboard mode.
"""

import time
import random
import json
import os
import sys
import argparse
from pathlib import Path

# Add the Implementation directory to the Python path if needed
script_dir = os.path.dirname(os.path.abspath(__file__))
implementation_dir = os.path.dirname(script_dir)
if implementation_dir not in sys.path:
    sys.path.append(implementation_dir)

# Import monitoring components
from monitoring.system_dashboard import SystemMonitoringDashboard
from monitoring.media_metrics import MediaMetricsCollector

# Try to import web visualization if available
try:
    from monitoring.web_visualization import DashboardWebServer
    WEB_DASHBOARD_AVAILABLE = True
except ImportError:
    WEB_DASHBOARD_AVAILABLE = False

def simulate_media_processing(dashboard, media_metrics, duration=30):
    """
    Simulate media processing workload to generate metrics.
    
    Args:
        dashboard: The system monitoring dashboard
        media_metrics: The media metrics collector
        duration: Duration of simulation in seconds
    """
    print(f"Simulating media processing for {duration} seconds...")
    
    media_types = ["text", "image", "audio", "video"]
    processing_times = {
        "text": (10, 50),      # 10-50ms
        "image": (50, 250),    # 50-250ms
        "audio": (100, 500),   # 100-500ms
        "video": (200, 1000)   # 200-1000ms
    }
    
    start_time = time.time()
    count = 0
    
    while time.time() - start_time < duration:
        # Select a random media type
        media_type = random.choice(media_types)
        
        # Simulate processing time
        min_time, max_time = processing_times[media_type]
        proc_time = random.uniform(min_time, max_time)
        
        # Simulate success/failure
        success = random.random() < 0.95  # 95% success rate
        
        # Record metrics
        media_metrics.record_processing_time(media_type, proc_time)
        media_metrics.record_media_processed(media_type, success)
        
        # Simulate UML transform metrics occasionally
        if random.random() < 0.1:  # 10% chance
            success_rate = random.uniform(0.8, 0.98)
            compression = random.uniform(0.4, 0.8)
            media_metrics.record_uml_transform_metrics(
                media_type, success_rate, compression
            )
        
        count += 1
        
        # Small delay to prevent CPU hogging
        time.sleep(0.01)
    
    return count

def display_metrics_summary(dashboard, media_metrics):
    """Display a summary of collected metrics."""
    # Get dashboard data
    system_metrics = dashboard.get_dashboard_data()
    media_summary = media_metrics.get_media_metrics_summary()
    
    # Print summary
    print("\n" + "="*80)
    print("MONITORING DASHBOARD DEMO - METRICS SUMMARY")
    print("="*80)
    
    print("\nMEDIA PROCESSING METRICS:")
    print("--------------------------")
    print(f"Processed counts: {json.dumps(media_summary['processed_counts'], indent=2)}")
    print(f"Success rates: {json.dumps(media_summary['success_rates'], indent=2)}")
    print(f"Avg. processing times (ms): {json.dumps(media_summary['avg_processing_times'], indent=2)}")
    
    if 'metrics' in system_metrics and 'media_processing' in system_metrics['metrics']:
        print("\nSYSTEM DASHBOARD METRICS:")
        print("------------------------")
        for key, value in system_metrics['metrics']['media_processing'].items():
            if isinstance(value, dict):
                print(f"{key}: {json.dumps(value, indent=2)}")
            else:
                print(f"{key}: {value}")
    
    print("\nNote: This is a demo with simulated metrics.")
    print("In a production environment, these metrics would be visualized in a web dashboard.")
    print("="*80)

def run_web_dashboard(dashboard, media_metrics, duration=60):
    """Run the web-based dashboard demo.
    
    Args:
        dashboard: System dashboard instance
        media_metrics: Media metrics collector
        duration: How long to run in seconds, or None for indefinite
    """
    if not WEB_DASHBOARD_AVAILABLE:
        print("\nError: Web dashboard is not available.")
        print("Please make sure Flask is installed: pip install flask")
        return False
    
    try:
        # Initialize web server
        web_server = DashboardWebServer(dashboard)
        dashboard_url = web_server.start(background=True)
        
        print("\n" + "="*70)
        print(f"Web dashboard is now available at: {dashboard_url}")
        print("="*70)
        print("\nKeep this terminal open to continue running the dashboard.")
        print("Press Ctrl+C to stop the dashboard.")
        
        # Start continuous monitoring
        dashboard.start_monitoring()
        
        # Loop to simulate metrics
        start_time = time.time()
        count = 0
        
        while duration is None or time.time() - start_time < duration:
            # Run a short simulation
            count += simulate_media_processing(dashboard, media_metrics, duration=5)
            print(f"Processed {count} simulated media items so far...")
            
            # Collect additional metrics
            dashboard.collect_all_metrics()
            
            # Short pause
            time.sleep(2)
        
        return True
        
    except KeyboardInterrupt:
        print("\nStopping web dashboard...")
        return True
    except Exception as e:
        print(f"\nError running web dashboard: {e}")
        return False
    finally:
        dashboard.stop_monitoring()
        print("\nMonitoring stopped.")

def main():
    """Run the monitoring dashboard demo."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="BlackwallV2 Monitoring Dashboard Demo")
    parser.add_argument('--web', action='store_true', help='Launch web-based dashboard')
    parser.add_argument('--duration', type=int, default=10, 
                        help='Duration in seconds for the demo (default: 10, 0 for indefinite)')
    args = parser.parse_args()
    
    print("Initializing BlackwallV2 Monitoring Dashboard Demo")
    print("="*60)
    
    # Create a temporary directory for demo data
    demo_data_dir = os.path.join(script_dir, "temp_monitoring_data")
    Path(demo_data_dir).mkdir(exist_ok=True)
    print(f"Using temporary data directory: {demo_data_dir}")
    
    # Initialize the dashboard and metrics collector
    dashboard = SystemMonitoringDashboard(data_dir=demo_data_dir)
    media_metrics = MediaMetricsCollector(dashboard)
    
    # Determine the mode to run in
    if args.web:
        # Web dashboard mode
        duration = None if args.duration == 0 else args.duration
        run_web_dashboard(dashboard, media_metrics, duration)
    else:
        # Console mode
        print("Starting monitoring system...")
        dashboard.start_monitoring()
        
        try:
            # Run the simulation
            duration = args.duration if args.duration > 0 else 10
            processed_count = simulate_media_processing(
                dashboard, media_metrics, duration=duration
            )
            print(f"Processed {processed_count} simulated media items")
            
            # Collect additional system metrics
            print("Collecting system metrics...")
            dashboard.collect_all_metrics()
            
            # Display the metrics summary
            display_metrics_summary(dashboard, media_metrics)
            
            # Save a metrics snapshot
            snapshot_file = dashboard.save_metrics_snapshot()
            print(f"\nMetrics snapshot saved to: {snapshot_file}")
        
        finally:
            # Stop monitoring
            dashboard.stop_monitoring()
            print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
