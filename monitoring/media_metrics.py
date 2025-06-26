"""
Media Metrics Module for BlackwallV2 Monitoring Dashboard
--------------------------------------------------------

This module collects and processes metrics specific to media handling components.
It integrates with the main system dashboard to provide detailed insights
into media processing performance.
"""

import time
import json
from collections import defaultdict

class MediaMetricsCollector:
    """
    Collector for media-specific metrics in the BlackwallV2 system.
    
    Tracks performance metrics related to media processing, including:
    - Processing time by media type
    - Feature extraction efficiency
    - UML transformation metrics
    - Cross-modal processing statistics
    """
    
    def __init__(self, dashboard=None):
        """Initialize the media metrics collector."""
        self.dashboard = dashboard
        self.metrics = defaultdict(list)
        self.media_counters = {
            "processed": {"text": 0, "image": 0, "audio": 0, "video": 0},
            "failed": {"text": 0, "image": 0, "audio": 0, "video": 0}
        }
        self.processing_times = {
            "text": [], "image": [], "audio": [], "video": []
        }
        self.uml_transform_metrics = {
            "text": {"success_rate": 0.0, "compression_ratio": 0.0},
            "image": {"success_rate": 0.0, "compression_ratio": 0.0},
            "audio": {"success_rate": 0.0, "compression_ratio": 0.0},
            "video": {"success_rate": 0.0, "compression_ratio": 0.0}
        }
    
    def record_processing_time(self, media_type, duration_ms):
        """
        Record the processing time for a media item.
        
        Args:
            media_type: Type of the media (text, image, audio, video)
            duration_ms: Processing duration in milliseconds
        """
        if media_type not in self.processing_times:
            return False
            
        self.processing_times[media_type].append(duration_ms)
        
        # Keep only the most recent 1000 measurements
        if len(self.processing_times[media_type]) > 1000:
            self.processing_times[media_type] = self.processing_times[media_type][-1000:]
            
        # Update dashboard if available
        if self.dashboard:
            self.dashboard.track_media_metric(
                f"{media_type}_processing_time", 
                self._calculate_avg_processing_time(media_type)
            )
        
        return True
    
    def record_media_processed(self, media_type, success=True):
        """
        Record a processed media item.
        
        Args:
            media_type: Type of media processed
            success: Whether processing was successful
        """
        if media_type not in self.media_counters["processed"]:
            return False
            
        self.media_counters["processed"][media_type] += 1
        if not success:
            self.media_counters["failed"][media_type] += 1
        
        # Update dashboard if available
        if self.dashboard:
            self.dashboard.track_media_metric(
                "processed_count", 
                self.media_counters["processed"]
            )
            self.dashboard.track_media_metric(
                "success_rate",
                self._calculate_success_rates()
            )
        
        return True
    
    def record_uml_transform_metrics(self, media_type, success_rate, compression_ratio):
        """
        Record metrics for UML transformations.
        
        Args:
            media_type: Type of media transformed
            success_rate: Success rate of the transformation
            compression_ratio: Compression ratio achieved
        """
        if media_type not in self.uml_transform_metrics:
            return False
            
        self.uml_transform_metrics[media_type]["success_rate"] = success_rate
        self.uml_transform_metrics[media_type]["compression_ratio"] = compression_ratio
        
        # Update dashboard if available
        if self.dashboard:
            self.dashboard.track_media_metric(
                "uml_transform_metrics", 
                self.uml_transform_metrics
            )
        
        return True
    
    def _calculate_avg_processing_time(self, media_type):
        """Calculate the average processing time for a media type."""
        times = self.processing_times.get(media_type, [])
        if not times:
            return 0
        return sum(times) / len(times)
    
    def _calculate_success_rates(self):
        """Calculate the success rates for all media types."""
        rates = {}
        for media_type in self.media_counters["processed"]:
            processed = self.media_counters["processed"][media_type]
            failed = self.media_counters["failed"][media_type]
            
            if processed == 0:
                rates[media_type] = 0
            else:
                rates[media_type] = (processed - failed) / processed
        
        return rates
    
    def get_media_metrics_summary(self):
        """Get a summary of all media metrics."""
        summary = {
            "timestamp": time.time(),
            "processed_counts": self.media_counters["processed"].copy(),
            "success_rates": self._calculate_success_rates(),
            "avg_processing_times": {
                media_type: self._calculate_avg_processing_time(media_type)
                for media_type in self.processing_times
            },
            "uml_transform_metrics": self.uml_transform_metrics.copy()
        }
        return summary
    
    def export_metrics_to_json(self, filepath):
        """Export metrics to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.get_media_metrics_summary(), f, indent=2)
        return True


# Example usage
if __name__ == "__main__":
    collector = MediaMetricsCollector()
    
    # Simulate recording some metrics
    print("Recording simulated media metrics...")
    
    # Record processing times
    collector.record_processing_time("text", 50)
    collector.record_processing_time("image", 150)
    collector.record_processing_time("audio", 200)
    collector.record_processing_time("video", 500)
    
    # Record processed items
    for _ in range(100):
        collector.record_media_processed("text", success=True)
    for _ in range(80):
        collector.record_media_processed("image", success=True)
    for _ in range(20):
        collector.record_media_processed("image", success=False)
    for _ in range(30):
        collector.record_media_processed("audio", success=True)
    for _ in range(10):
        collector.record_media_processed("video", success=True)
    
    # Record UML transform metrics
    collector.record_uml_transform_metrics("text", 0.95, 0.7)
    collector.record_uml_transform_metrics("image", 0.85, 0.5)
    collector.record_uml_transform_metrics("audio", 0.8, 0.6)
    collector.record_uml_transform_metrics("video", 0.75, 0.4)
    
    # Print summary
    summary = collector.get_media_metrics_summary()
    print("\nMedia Metrics Summary:")
    print(json.dumps(summary, indent=2))
    
    print("\nNote: This is a placeholder implementation for the media metrics collector.")
