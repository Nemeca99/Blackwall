"""
Media-Aware Fragment Routing

This module enhances the fragment routing system to handle different media types,
dynamically adjusting fragment weights based on input content.
"""

import time
import re
import random
from typing import Dict, Any, List, Tuple, Union

# Import the optimized fragment manager
from optimize.fragment_routing_optimized import OptimizedFragmentManager

# Import media detection
from media.media_feature_extraction import detect_media_type, feature_extractor

class MediaAwareFragmentRouter(OptimizedFragmentManager):
    """
    Fragment router that adapts fragment selection based on media types.
    Extends the OptimizedFragmentManager with media-specific routing features.
    """
    def __init__(self):
        super().__init__()
        
        # Register media-specific configurations
        self._register_media_configs()
        
        # Track media processing metrics
        self.media_metrics = {
            "processed_by_type": {"text": 0, "image": 0, "audio": 0, "video": 0, "unknown": 0},
            "routing_times_by_type": {"text": [], "image": [], "audio": [], "video": [], "unknown": []},
            "fragment_activity_by_media": {}  # Will track which fragments handle which media types
        }
    
    def _register_media_configs(self):
        """Register media-specific routing configurations"""
        self.media_configs = {
            # Configuration for image processing
            "image": {
                "fragment_weights": {
                    "Velastra": 0.8,   # Primary - visual processing
                    "Obelisk": 0.6,    # Secondary - pattern analysis
                    "Nyx": 0.6,        # Secondary - creative interpretation
                    "Lyra": 0.5,       # Tertiary - integration
                    "Seraphis": 0.4,   # Quaternary - emotional response
                    "Blackwall": 0.3,  # Minimal - security validation
                    "Echoe": 0.3       # Minimal - memory connection
                },
                "priority": 0.8  # High priority for visual processing
            },
            
            # Configuration for audio processing
            "audio": {
                "fragment_weights": {
                    "Seraphis": 0.8,   # Primary - emotional and tonal analysis
                    "Echoe": 0.7,      # Secondary - temporal patterns
                    "Nyx": 0.6,        # Secondary - creative interpretation
                    "Obelisk": 0.5,    # Tertiary - structural analysis
                    "Lyra": 0.5,       # Tertiary - integration
                    "Blackwall": 0.3,  # Minimal - security validation
                    "Velastra": 0.3    # Minimal - sensory connection
                },
                "priority": 0.7  # Medium-high priority
            },
            
            # Configuration for video processing
            "video": {
                "fragment_weights": {
                    "Velastra": 0.7,   # Primary - visual processing
                    "Echoe": 0.7,      # Primary - temporal sequencing
                    "Seraphis": 0.6,   # Secondary - emotional response
                    "Nyx": 0.6,        # Secondary - creative interpretation
                    "Lyra": 0.6,       # Secondary - integration
                    "Obelisk": 0.5,    # Tertiary - structural analysis
                    "Blackwall": 0.3   # Minimal - security validation
                },
                "priority": 0.9  # Highest priority for rich media
            },
            
            # Configuration for text processing (default)
            "text": {
                "fragment_weights": {
                    "Seraphis": 0.7,   # Primary - language processing
                    "Lyra": 0.6,       # Secondary - integration
                    "Blackwall": 0.6,  # Secondary - security and validation
                    "Obelisk": 0.5,    # Tertiary - logical analysis
                    "Nyx": 0.5,        # Tertiary - creative thought
                    "Echoe": 0.4,      # Quaternary - memory connection
                    "Velastra": 0.3    # Minimal - sensory connection
                },
                "priority": 0.6  # Default priority
            }
        }
    
    def process_media_input(self, input_data, media_type=None, context=None):
        """
        Process media input and route to appropriate fragments.
        
        Args:
            input_data: The media content to process
            media_type: Optional media type (auto-detected if not provided)
            context: Optional processing context
            
        Returns:
            Dict with processing results and selected fragment
        """
        # Detect media type if not provided
        if media_type is None:
            media_type = detect_media_type(input_data)
        
        # Extract features for non-text inputs
        features = None
        if media_type != "text":
            features = feature_extractor.extract_features(input_data, media_type)
        
        # Track media type processing
        self.media_metrics["processed_by_type"][media_type] = \
            self.media_metrics["processed_by_type"].get(media_type, 0) + 1
        
        # Get media-specific configuration
        config = self.media_configs.get(media_type, self.media_configs["text"])
        
        # Adjust fragment weights based on media type
        start_time = time.time()
        result = self.route_with_weights(input_data, config["fragment_weights"], 
                                        media_type=media_type, 
                                        features=features,
                                        context=context,
                                        priority=config["priority"])
        routing_time = time.time() - start_time
        
        # Track routing performance
        self.media_metrics["routing_times_by_type"].setdefault(media_type, []).append(routing_time)
        
        # Track which fragment was selected for this media type
        selected_fragment = result.get("selected_fragment", "unknown")
        if selected_fragment not in self.media_metrics["fragment_activity_by_media"]:
            self.media_metrics["fragment_activity_by_media"][selected_fragment] = {}
        
        self.media_metrics["fragment_activity_by_media"][selected_fragment][media_type] = \
            self.media_metrics["fragment_activity_by_media"][selected_fragment].get(media_type, 0) + 1
        
        return result
    
    def route_with_weights(self, input_data, weight_overrides=None, media_type=None, 
                        features=None, context=None, priority=0.5):
        """
        Route input with specific fragment weight overrides.
        
        Args:
            input_data: The input content to process
            weight_overrides: Dict of fragment name to weight override
            media_type: Type of media being processed
            features: Optional pre-extracted features
            context: Optional processing context
            priority: Priority level for processing (0-1)
            
        Returns:
            Dict with routing results and selected fragment
        """
        # Set up context if not provided
        if context is None:
            context = {}
        context["media_type"] = media_type
        if features:
            context["media_features"] = features
        context["priority"] = priority
        
        # Prepare fragments
        fragments = self.fragments.copy()
        if weight_overrides:
            for fragment_name, weight in weight_overrides.items():
                if fragment_name in fragments:
                    fragments[fragment_name]["weight"] = weight
        
        # Analyze input text or feature summary
        if media_type == "text":
            keywords = self._analyze_input(input_data)
        else:
            # For non-text inputs, generate a text summary from features
            feature_summary = self._generate_feature_summary(features)
            keywords = self._analyze_input(feature_summary)
        
        # Find active fragments based on keywords and weights
        active_fragments = self._find_active_fragments(keywords, fragments)
        
        # If no fragments are active, fall back to default fragment
        if not active_fragments:
            selected_fragment = self._get_default_fragment(media_type)
        else:
            # Select fragment based on weights and activation scores
            selected_fragment = self._select_fragment(active_fragments)
        
        # Prepare result
        result = {
            "selected_fragment": selected_fragment,
            "active_fragments": active_fragments,
            "keywords": keywords,
            "media_type": media_type,
            "priority": priority
        }
        
        # Add fragment activity for tracking
        self._record_fragment_activity(selected_fragment, media_type)
        
        return result
    
    def _generate_feature_summary(self, features):
        """Generate text summary from media features for keyword extraction"""
        if not features:
            return "unknown media content"
            
        media_type = features.get("media_type", "unknown")
        
        # Basic summary template
        summary = f"{media_type} content with "
        
        # Add media-specific details
        if media_type == "image":
            dimensions = features.get("dimensions", (0, 0))
            summary += f"dimensions {dimensions[0]}x{dimensions[1]} "
            
            # Add details about color and edges
            if "uml_features" in features:
                uml = features["uml_features"]
                summary += f"featuring color profile {uml.get('color_dimension', 0):.2f} "
                summary += f"and edge complexity {uml.get('edge_dimension', 0):.2f} "
                
        elif media_type == "audio":
            duration = features.get("duration", 0)
            summary += f"duration {duration:.1f} seconds "
            
            # Add details about spectral and rhythm features
            if "uml_features" in features:
                uml = features["uml_features"]
                summary += f"featuring spectral signature {uml.get('spectral_signature', 0):.2f} "
                summary += f"and rhythm signature {uml.get('rhythm_signature', 0):.2f} "
                
        elif media_type == "video":
            duration = features.get("duration", 0)
            frame_rate = features.get("frame_rate", 0)
            summary += f"duration {duration:.1f} seconds at {frame_rate} FPS "
            
            # Add details about key frames and motion
            if "uml_features" in features:
                uml = features["uml_features"]
                summary += f"featuring motion signature {uml.get('motion_signature', 0):.2f} "
                summary += f"and temporal variance {uml.get('temporal_variance', 0):.2f} "
        
        # Add fingerprint
        if "uml_fingerprint" in features:
            fingerprint = features["uml_fingerprint"]
            summary += f"with UML signature {fingerprint.get('mean_signature', 0):.2f}"
        
        return summary
    
    def _get_default_fragment(self, media_type):
        """Get default fragment for a given media type"""
        if media_type == "image":
            return "Velastra"
        elif media_type == "audio":
            return "Seraphis"
        elif media_type == "video":
            return "Echoe"
        else:
            return "Lyra"  # Default for text and unknown types
    
    def _record_fragment_activity(self, fragment_name, media_type):
        """Record fragment activity for analytics"""
        if fragment_name not in self.activity_log:
            self.activity_log[fragment_name] = {
                "total": 0,
                "by_media": {}
            }
            
        self.activity_log[fragment_name]["total"] += 1
        
        if media_type not in self.activity_log[fragment_name]["by_media"]:
            self.activity_log[fragment_name]["by_media"][media_type] = 0
            
        self.activity_log[fragment_name]["by_media"][media_type] += 1
    
    def get_media_stats(self):
        """Get statistics about media processing"""
        stats = {
            "processed_counts": self.media_metrics["processed_by_type"],
            "fragment_specialization": {}
        }
        
        # Calculate average routing times
        avg_times = {}
        for media_type, times in self.media_metrics["routing_times_by_type"].items():
            if times:
                avg_times[media_type] = sum(times) / len(times)
            else:
                avg_times[media_type] = 0
        
        stats["avg_routing_times"] = avg_times
        
        # Calculate fragment specialization
        for fragment, media_counts in self.media_metrics["fragment_activity_by_media"].items():
            total = sum(media_counts.values())
            if total > 0:
                specialization = {}
                for media_type, count in media_counts.items():
                    specialization[media_type] = count / total
                stats["fragment_specialization"][fragment] = specialization
        
        return stats
