"""
Media Feature Extraction Module

This module provides feature extraction functions for various media types
to support the UML-Lyra integration for multimedia processing.
"""

import os
import time
import hashlib
import numpy as np
from typing import Dict, Any, List, Tuple, Union

# Import UML core for feature transformation
try:
    from UML_Core.uml_core import recursive_compress, tfid_anchor
except ImportError:
    # Mock implementation if UML_Core is not available
    def recursive_compress(value):
        """Mock implementation of recursive compression"""
        if isinstance(value, (int, float)):
            return value * 0.618  # Golden ratio approximation as a simple transform
        return value
    
    def tfid_anchor(value):
        """Mock implementation of TFID anchoring"""
        return {
            "value": value,
            "timestamp": time.time(),
            "tfid_hash": int(hashlib.md5(str(value).encode()).hexdigest(), 16) % (10 ** 10)
        }

def detect_media_type(content: Any) -> str:
    """
    Detect media type from content.
    
    Args:
        content: The content to analyze
        
    Returns:
        str: Media type ("image", "audio", "video", "text", "unknown")
    """
    if isinstance(content, str):
        # Check if it's a file path
        if os.path.exists(content):
            ext = os.path.splitext(content)[1].lower()
            if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.gif'):
                return "image"
            elif ext in ('.mp3', '.wav', '.ogg', '.flac'):
                return "audio"
            elif ext in ('.mp4', '.avi', '.mov', '.mkv'):
                return "video"
        # If not a file or not recognized extension, assume it's text
        return "text"
    
    # If content is bytes or numpy array, try to determine type
    if isinstance(content, (bytes, bytearray, np.ndarray)):
        # This is a simplification - in a real system, we'd need more sophisticated detection
        return "binary_data"
    
    # Default
    return "unknown"

class MediaFeatureExtractor:
    """Media feature extraction for different media types"""
    
    def __init__(self):
        # Load models if needed
        self._load_models()
    
    def _load_models(self):
        """Load feature extraction models"""
        # In a real implementation, we would load models for different media types
        self.models = {}
    
    def extract_features(self, content: Any, media_type: str = None) -> Dict[str, Any]:
        """
        Extract features from media content.
        
        Args:
            content: The media content
            media_type: Optional media type (auto-detected if not provided)
            
        Returns:
            Dict with extracted features and metadata
        """
        # Auto-detect media type if not provided
        if media_type is None:
            media_type = detect_media_type(content)
        
        # Extract features based on media type
        if media_type == "image":
            features = self._extract_image_features(content)
        elif media_type == "audio":
            features = self._extract_audio_features(content)
        elif media_type == "video":
            features = self._extract_video_features(content)
        elif media_type == "text":
            features = self._extract_text_features(content)
        else:
            features = {"error": f"Unsupported media type: {media_type}"}
        
        # Add metadata
        features["media_type"] = media_type
        features["extraction_time"] = time.time()
        
        # Apply UML transforms
        features = self._apply_uml_transform(features, media_type)
        
        return features
    
    def _extract_image_features(self, image_content) -> Dict[str, Any]:
        """Extract features from image content"""
        # Placeholder for actual image feature extraction
        # In a real implementation, this would use computer vision techniques
        
        # Mock features
        features = {
            "dimensions": (640, 480),  # Placeholder values
            "color_histogram": np.random.rand(16).tolist(),  # Simplified color histogram
            "edge_features": np.random.rand(8).tolist(),  # Simplified edge features
            "key_points": [(100, 100), (200, 200), (300, 300)]  # Example keypoints
        }
        
        return features
    
    def _extract_audio_features(self, audio_content) -> Dict[str, Any]:
        """Extract features from audio content"""
        # Placeholder for actual audio feature extraction
        # In a real implementation, this would use audio analysis techniques
        
        # Mock features
        features = {
            "duration": 120.5,  # Placeholder duration in seconds
            "spectral_features": np.random.rand(10).tolist(),
            "rhythm_features": np.random.rand(5).tolist(),
            "mfcc": np.random.rand(13).tolist()  # Simplified MFCC features
        }
        
        return features
    
    def _extract_video_features(self, video_content) -> Dict[str, Any]:
        """Extract features from video content"""
        # Placeholder for actual video feature extraction
        # In a real implementation, this would analyze video frames and motion
        
        # Mock features
        features = {
            "duration": 300.0,  # Placeholder duration in seconds
            "frame_rate": 30,
            "key_frame_features": [
                {"timestamp": 10.0, "features": np.random.rand(10).tolist()},
                {"timestamp": 30.0, "features": np.random.rand(10).tolist()},
                {"timestamp": 60.0, "features": np.random.rand(10).tolist()}
            ],
            "motion_features": np.random.rand(8).tolist()
        }
        
        return features
    
    def _extract_text_features(self, text_content) -> Dict[str, Any]:
        """Extract features from text content"""
        # Simple text feature extraction
        if not isinstance(text_content, str):
            text_content = str(text_content)
            
        # Calculate basic text features
        words = text_content.split()
        
        features = {
            "length": len(text_content),
            "word_count": len(words),
            "average_word_length": sum(len(w) for w in words) / max(1, len(words)),
            "unique_words": len(set(words)),
            "keyword_frequency": self._extract_keywords(text_content)
        }
        
        return features
    
    def _extract_keywords(self, text: str) -> Dict[str, int]:
        """Extract keywords and their frequencies from text"""
        # Simple keyword extraction (in a real system, use NLP)
        words = text.lower().split()
        word_count = {}
        
        for word in words:
            if len(word) > 3:  # Skip short words
                word_count[word] = word_count.get(word, 0) + 1
        
        # Return top 10 keywords by frequency
        keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
        return dict(keywords)
    
    def _apply_uml_transform(self, features: Dict[str, Any], media_type: str) -> Dict[str, Any]:
        """Apply UML transformation to the features based on media type"""
        # Copy original features
        transformed = features.copy()
        
        # Add UML-specific features
        if media_type == "image":
            transformed["uml_features"] = self._uml_transform_image(features)
        elif media_type == "audio":
            transformed["uml_features"] = self._uml_transform_audio(features)
        elif media_type == "video":
            transformed["uml_features"] = self._uml_transform_video(features)
        elif media_type == "text":
            transformed["uml_features"] = self._uml_transform_text(features)
        
        # Generate UML fingerprint using recursive compression
        transformed["uml_fingerprint"] = self._generate_uml_fingerprint(features)
        
        return transformed
    
    def _uml_transform_image(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply UML transformation to image features using tesseract-based mapping"""
        # Extract relevant feature vectors
        color_hist = np.array(features.get("color_histogram", []))
        edge_features = np.array(features.get("edge_features", []))
        
        # Apply recursive compression to each vector
        compressed_colors = [recursive_compress(x) for x in color_hist]
        compressed_edges = [recursive_compress(x) for x in edge_features]
        
        # Generate UML tesseract representation
        tesseract = {
            "color_dimension": np.mean(compressed_colors),
            "edge_dimension": np.mean(compressed_edges),
            "spatial_signature": self._generate_spatial_signature(features)
        }
        
        return tesseract
    
    def _uml_transform_audio(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply UML transformation to audio features using harmonic mapping"""
        # Extract relevant feature vectors
        spectral = np.array(features.get("spectral_features", []))
        rhythm = np.array(features.get("rhythm_features", []))
        mfcc = np.array(features.get("mfcc", []))
        
        # Apply recursive compression
        compressed_spectral = [recursive_compress(x) for x in spectral]
        compressed_rhythm = [recursive_compress(x) for x in rhythm]
        compressed_mfcc = [recursive_compress(x) for x in mfcc]
        
        # Generate harmonic UML representation
        harmonic = {
            "spectral_signature": np.mean(compressed_spectral),
            "rhythm_signature": np.mean(compressed_rhythm),
            "timbre_signature": np.mean(compressed_mfcc)
        }
        
        return harmonic
    
    def _uml_transform_video(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply UML transformation to video features using temporal-spatial mapping"""
        # Extract key frame features and apply transformations
        key_frames = features.get("key_frame_features", [])
        
        # Transform each key frame
        transformed_frames = []
        for frame in key_frames:
            frame_features = np.array(frame.get("features", []))
            compressed = [recursive_compress(x) for x in frame_features]
            transformed_frames.append({
                "timestamp": frame.get("timestamp"),
                "compressed_features": compressed,
                "signature": np.mean(compressed)
            })
        
        # Generate temporal-spatial UML representation
        temporal_spatial = {
            "frame_signatures": [f["signature"] for f in transformed_frames],
            "motion_signature": recursive_compress(np.mean(features.get("motion_features", []))),
            "temporal_variance": np.std([f["signature"] for f in transformed_frames])
        }
        
        return temporal_spatial
    
    def _uml_transform_text(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Apply UML transformation to text features using semantic mapping"""
        # Apply recursive compression to numeric features
        compressed_length = recursive_compress(features.get("length", 0))
        compressed_word_count = recursive_compress(features.get("word_count", 0))
        compressed_avg_length = recursive_compress(features.get("average_word_length", 0))
        compressed_unique = recursive_compress(features.get("unique_words", 0))
        
        # Generate semantic UML representation
        semantic = {
            "length_signature": compressed_length,
            "complexity_signature": compressed_avg_length * compressed_unique / max(1, compressed_word_count),
            "vocabulary_signature": compressed_unique / max(1, compressed_word_count)
        }
        
        return semantic
    
    def _generate_spatial_signature(self, features: Dict[str, Any]) -> float:
        """Generate spatial signature for image features"""
        key_points = features.get("key_points", [])
        if not key_points:
            return 0.0
            
        # Calculate center of mass
        x_sum = sum(p[0] for p in key_points)
        y_sum = sum(p[1] for p in key_points)
        center_x = x_sum / len(key_points)
        center_y = y_sum / len(key_points)
        
        # Calculate average distance from center
        avg_distance = sum(((p[0] - center_x)**2 + (p[1] - center_y)**2)**0.5 for p in key_points) / len(key_points)
        
        # Apply recursive compression
        return recursive_compress(avg_distance)
    
    def _generate_uml_fingerprint(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Generate UML fingerprint for media features"""
        # Convert features to a flat list of values
        flat_values = self._flatten_features(features)
        
        # Calculate standard features
        if flat_values:
            mean_value = np.mean(flat_values)
            std_value = np.std(flat_values)
        else:
            mean_value = 0
            std_value = 0
        
        # Apply recursive compression
        compressed_mean = recursive_compress(mean_value)
        compressed_std = recursive_compress(std_value)
        
        # Generate TFID anchor
        tfid = tfid_anchor(compressed_mean)
        
        return {
            "mean_signature": compressed_mean,
            "variance_signature": compressed_std,
            "tfid_hash": tfid["tfid_hash"],
            "timestamp": tfid["timestamp"]
        }
    
    def _flatten_features(self, features: Dict[str, Any]) -> List[float]:
        """Flatten a nested feature dictionary into a list of numeric values"""
        result = []
        
        def extract_numbers(item):
            if isinstance(item, (int, float)):
                return [float(item)]
            elif isinstance(item, (list, tuple)):
                numbers = []
                for sub_item in item:
                    numbers.extend(extract_numbers(sub_item))
                return numbers
            elif isinstance(item, dict):
                numbers = []
                for key, value in item.items():
                    if key not in ("timestamp", "extraction_time", "media_type", "error"):
                        numbers.extend(extract_numbers(value))
                return numbers
            return []
        
        return extract_numbers(features)

# Create singleton instance
feature_extractor = MediaFeatureExtractor()
