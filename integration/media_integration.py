"""
Media Integration Module

This module provides functions to integrate media-aware components 
into the BlackwallV2 system.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import media-enhanced components
try:
    from media.media_enhanced_memory import MediaEnhancedSTM
    from media.media_aware_routing import MediaAwareFragmentRouter
    from media.media_feature_extraction import MediaFeatureExtractor, feature_extractor
except ImportError as e:
    print(f"Error importing media-enhanced components: {e}")
    sys.exit(1)

def integrate_media_enhanced_memory():
    """
    Replace optimized memory components with media-enhanced versions.
    """
    import root.Left_Hemisphere
    from optimize.hemisphere_optimization import OptimizedShortTermMemory
    
    # Create backup of optimized memory class if needed
    if not hasattr(root.Left_Hemisphere, 'OptimizedShortTermMemory'):
        root.Left_Hemisphere.OptimizedShortTermMemory = root.Left_Hemisphere.ShortTermMemory
    
    # Replace with media-enhanced version
    root.Left_Hemisphere.ShortTermMemory = MediaEnhancedSTM
    
    print("✅ Media-enhanced STM integrated")
    return True

def integrate_media_aware_routing():
    """
    Replace optimized fragment routing with media-aware version.
    """
    import root.fragment_manager
    from optimize.fragment_routing_optimized import OptimizedFragmentManager
    
    # Create backup of optimized fragment manager
    if not hasattr(root.fragment_manager, 'OptimizedFragmentManager'):
        root.fragment_manager.OptimizedFragmentManager = root.fragment_manager.FragmentManager
    
    # Replace with media-aware version
    root.fragment_manager.FragmentManager = MediaAwareFragmentRouter
    
    print("✅ Media-aware fragment routing integrated")
    return True

def register_feature_extractor():
    """
    Register the feature extractor with the system.
    """
    import root
    
    # Add feature extractor to the root namespace
    if not hasattr(root, 'media_feature_extractor'):
        root.media_feature_extractor = feature_extractor
        print("✅ Media feature extractor registered")
        return True
    return False

def integrate_all_media_components():
    """
    Integrate all media-enhanced components.
    """
    success = True
    success &= integrate_media_enhanced_memory()
    success &= integrate_media_aware_routing()
    success &= register_feature_extractor()
    
    if success:
        print("✅ All media components successfully integrated")
    else:
        print("⚠️ Some media components could not be integrated")
    
    return success

def restore_optimized_components():
    """
    Restore optimized components (removing media enhancements).
    """
    try:
        import root.Left_Hemisphere
        import root.fragment_manager
        from optimize.hemisphere_optimization import OptimizedShortTermMemory
        from optimize.fragment_routing_optimized import OptimizedFragmentManager
        
        # Restore optimized memory system
        if hasattr(root.Left_Hemisphere, 'OptimizedShortTermMemory'):
            root.Left_Hemisphere.ShortTermMemory = root.Left_Hemisphere.OptimizedShortTermMemory
        
        # Restore optimized fragment manager
        if hasattr(root.fragment_manager, 'OptimizedFragmentManager'):
            root.fragment_manager.FragmentManager = root.fragment_manager.OptimizedFragmentManager
        
        # Remove feature extractor reference if present
        if hasattr(root, 'media_feature_extractor'):
            delattr(root, 'media_feature_extractor')
        
        print("✅ Reverted to optimized components")
        return True
        
    except Exception as e:
        print(f"Error restoring optimized components: {e}")
        return False

if __name__ == "__main__":
    # Simple command-line interface
    import argparse
    
    parser = argparse.ArgumentParser(description="Media Component Integration Tool")
    parser.add_argument('action', choices=['integrate', 'restore'], 
                        help="Action to perform: 'integrate' media components or 'restore' optimized components")
    
    args = parser.parse_args()
    
    if args.action == 'integrate':
        integrate_all_media_components()
    elif args.action == 'restore':
        restore_optimized_components()
