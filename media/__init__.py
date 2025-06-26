"""
Media Integration Package for BlackwallV2

This package provides media-specific enhancements to the BlackwallV2 system,
enabling efficient processing of diverse media types using UML principles.
"""

from media.media_feature_extraction import feature_extractor, detect_media_type, MediaFeatureExtractor
from media.media_enhanced_memory import MediaEnhancedSTM
from media.media_aware_routing import MediaAwareFragmentRouter

__all__ = [
    'feature_extractor',
    'detect_media_type',
    'MediaFeatureExtractor',
    'MediaEnhancedSTM',
    'MediaAwareFragmentRouter',
]
