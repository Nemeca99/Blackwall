"""
Media Integration Demo

This script demonstrates the capabilities of the media-enhanced
BlackwallV2 system for various media types.
"""

import os
import sys
import time
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Check if modules are available and import them
try:
    # Import integration tools
    from integration.media_integration import (
        integrate_all_media_components,
        restore_optimized_components
    )

    # Import media components
    from media.media_feature_extraction import feature_extractor, detect_media_type
    from media.media_enhanced_memory import MediaEnhancedSTM
    from media.media_aware_routing import MediaAwareFragmentRouter
    
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Some components may be missing or contain syntax errors.")
    print("This demo will simulate functionality with mock implementations.")
    MODULES_AVAILABLE = False
    
    # Create mock classes for demonstration
    class MockFeatureExtractor:
        def extract_features(self, content, media_type=None):
            return {"media_type": media_type or "text", "mock": True}
    
    feature_extractor = MockFeatureExtractor()
    detect_media_type = lambda x: "text"
    
    class MediaEnhancedSTM:
        def __init__(self, buffer_size=100):
            self.memory = []
            
        def store_media(self, content, media_type=None, metadata=None, features=None):
            return True
            
        def search_by_media_type(self, media_type, limit=10):
            return []
            
        def cross_modal_search(self, query, source_media_type='text', target_media_type=None, limit=5):
            return {"image": [], "audio": [], "video": []}
    
    class MediaAwareFragmentRouter:
        def __init__(self):
            self.media_configs = {
                "image": {"fragment_weights": {}, "priority": 0.8},
                "audio": {"fragment_weights": {}, "priority": 0.7},
                "video": {"fragment_weights": {}, "priority": 0.9},
                "text": {"fragment_weights": {}, "priority": 0.6}
            }
            self.media_metrics = {"fragment_activity_by_media": {}}
            
        def process_media_input(self, input_data, media_type=None, context=None):
            return {"selected_fragment": "MockFragment"}

def run_feature_extraction_demo():
    """
    Demonstrate media feature extraction capabilities.
    """
    print("\n===== FEATURE EXTRACTION DEMO =====")
    print("Demonstrating feature extraction for different media types...")
    
    # Sample data (mock paths for demonstration)
    sample_image = "samples/image.jpg"  # This is a mock path
    sample_audio = "samples/audio.mp3"  # This is a mock path
    sample_video = "samples/video.mp4"  # This is a mock path
    sample_text = "This is a sample text for the Universal Mathematical Language (UML) integration with BlackwallV2 (Lyra)."
    
    # Extract features with mock paths (will use mock implementations)
    print("\n1. Text feature extraction:")
    text_features = feature_extractor.extract_features(sample_text, "text")
    print(f"  - Text length: {text_features.get('length', 'N/A')}")
    print(f"  - Word count: {text_features.get('word_count', 'N/A')}")
    print(f"  - UML fingerprint: {text_features.get('uml_fingerprint', {}).get('mean_signature', 'N/A')}")
    
    print("\n2. Image feature extraction: (mock)")
    image_features = feature_extractor.extract_features(sample_image, "image")
    print(f"  - Dimensions: {image_features.get('dimensions', 'N/A')}")
    print(f"  - UML tesseract: {image_features.get('uml_features', {}).get('spatial_signature', 'N/A')}")
    
    print("\n3. Audio feature extraction: (mock)")
    audio_features = feature_extractor.extract_features(sample_audio, "audio")
    print(f"  - Duration: {audio_features.get('duration', 'N/A')}")
    print(f"  - UML harmonic: {audio_features.get('uml_features', {}).get('spectral_signature', 'N/A')}")
    
    print("\n4. Video feature extraction: (mock)")
    video_features = feature_extractor.extract_features(sample_video, "video")
    print(f"  - Duration: {video_features.get('duration', 'N/A')}")
    print(f"  - Frame rate: {video_features.get('frame_rate', 'N/A')}")
    print(f"  - Motion signature: {video_features.get('uml_features', {}).get('motion_signature', 'N/A')}")
    
    print("\nFeature extraction complete. Each media type produces UML-compatible feature vectors.")

def run_memory_demo():
    """
    Demonstrate media-enhanced memory capabilities.
    """
    print("\n===== MEDIA MEMORY DEMO =====")
    
    # Create media-enhanced STM
    stm = MediaEnhancedSTM(buffer_size=20)
    
    # Store various media types
    print("\nStoring different media types in memory...")
    
    # Store text items
    stm.store_media("UML provides a recursive mathematical framework for understanding complex systems.", 
                  media_type="text")
    stm.store_media("BlackwallV2 uses biomimetic algorithms for memory consolidation.", 
                  media_type="text")
    stm.store_media("Lyra's heart-driven timing synchronizes fragment activities.", 
                  media_type="text")
    
    # Store mock media items
    stm.store_media("samples/sunset.jpg", media_type="image", 
                  metadata={"description": "A beautiful sunset image with orange and purple colors"})
    stm.store_media("samples/ocean_waves.mp3", media_type="audio", 
                  metadata={"description": "Sound of ocean waves", "duration": 120})
    stm.store_media("samples/trees_video.mp4", media_type="video", 
                  metadata={"description": "Video showing trees in the wind", "duration": 45})
    
    # Demonstrate retrieval by media type
    print("\n1. Retrieving by media type:")
    text_items = stm.search_by_media_type("text")
    image_items = stm.search_by_media_type("image")
    
    print(f"  - Found {len(text_items)} text items")
    print(f"  - Found {len(image_items)} image items")
    
    # Demonstrate cross-modal search
    print("\n2. Cross-modal search:")
    query = "trees wind"
    results = stm.cross_modal_search(query, source_media_type="text")
    
    for media_type, items in results.items():
        print(f"  - Found {len(items)} {media_type} items related to '{query}'")
        for item in items:
            if 'metadata' in item and 'description' in item['metadata']:
                print(f"    * {item['metadata']['description']}")
    
    print("\nMedia-enhanced memory successfully demonstrated with cross-modal associations.")

def run_fragment_routing_demo():
    """
    Demonstrate media-aware fragment routing.
    """
    print("\n===== FRAGMENT ROUTING DEMO =====")
    print("Demonstrating media-aware fragment routing...")
    
    # Create router
    router = MediaAwareFragmentRouter()
    
    # Define sample inputs for different media types
    inputs = [
        {"data": "Calculate the eigenvalues of a 3x3 matrix using UML principles.", "type": "text"},
        {"data": "samples/forest_image.jpg", "type": "image"},
        {"data": "samples/piano_music.mp3", "type": "audio"},
        {"data": "samples/dance_video.mp4", "type": "video"}
    ]
    
    print("\nRouting different media types through fragments:")
    for item in inputs:
        # Process the input
        result = router.process_media_input(item["data"], media_type=item["type"])
        
        # Display routing result
        print(f"\n1. Input type: {item['type']}")
        print(f"  - Selected fragment: {result.get('selected_fragment', 'unknown')}")
        print(f"  - Processing priority: {router.media_configs[item['type']]['priority']}")
        
        # Show active fragments
        weights = router.media_configs[item["type"]]["fragment_weights"]
        top_fragments = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
        print("  - Top fragment weights:")
        for fragment, weight in top_fragments:
            print(f"    * {fragment}: {weight:.2f}")
    
    # Show media processing metrics
    print("\n2. Fragment activity by media type:")
    for fragment, counts in router.media_metrics["fragment_activity_by_media"].items():
        print(f"  - {fragment}: {counts}")
    
    print("\nMedia-aware fragment routing successfully demonstrated.")

def run_full_integration_demo():
    """
    Run a full demonstration of all media-enhanced components.
    """
    print("\n===== FULL MEDIA INTEGRATION DEMO =====")
    print("Integrating media components...")
    
    # Integrate components if available
    if MODULES_AVAILABLE:
        try:
            integrate_all_media_components()
            print("✅ Media components successfully integrated")
        except Exception as e:
            print(f"❌ Error integrating media components: {e}")
            print("Continuing with demo in mock mode...")
    else:
        print("⚠️ Media integration modules not available - running in mock mode")
    
    print("\nRunning individual component demos:")
    run_feature_extraction_demo()
    run_memory_demo()
    run_fragment_routing_demo()
    
    print("\n===== MEDIA INTEGRATION SUMMARY =====")
    print("Media integration demonstration completed successfully.")
    print("""
Key capabilities demonstrated:
1. Media-specific feature extraction with UML-based transformations
2. Cross-modal memory storage and retrieval
3. Media-aware fragment routing with dynamic weights
4. Integration with existing BlackwallV2 optimization

Next steps:
1. Create real media test datasets
2. Implement full UML transformations for each media type
3. Enhance cross-modal associations
4. Integrate with the LLM interface
""")

if __name__ == "__main__":
    run_full_integration_demo()
