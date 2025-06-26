"""
Standalone Media Integration Demo

This script demonstrates the capabilities of the media-enhanced components
without requiring imports from the existing codebase.
"""

import os
import sys
import time
import random
from pathlib import Path
from collections import defaultdict

class MockOptimizedSTM:
    """Mock implementation of OptimizedShortTermMemory for demonstration"""
    
    def __init__(self, buffer_size=100):
        self.buffer_size = buffer_size
        self.memory = []
        self.memory_last_access = {}
        self.dirty = False
    
    def store(self, item):
        """Store an item in memory"""
        self.memory.append(item)
        self.memory_last_access[len(self.memory) - 1] = time.time()
        self.dirty = True
        return True
        
    def search(self, query, limit=10):
        """Search memory for items matching query"""
        return self.memory[-limit:]
    
    def _delayed_save(self):
        """Mock delayed save"""
        self.dirty = False
        
class MediaFeatureExtractor:
    """Media feature extraction for different media types"""
    
    def extract_features(self, content, media_type=None):
        """Extract features from media content"""
        # Auto-detect media type if not provided
        if media_type is None:
            if isinstance(content, str):
                if content.endswith(('.jpg', '.jpeg', '.png')):
                    media_type = "image"
                elif content.endswith(('.mp3', '.wav')):
                    media_type = "audio"
                elif content.endswith(('.mp4', '.avi')):
                    media_type = "video"
                else:
                    media_type = "text"
            else:
                media_type = "unknown"
        
        # Mock features for each media type
        features = {
            "media_type": media_type,
            "extraction_time": time.time()
        }
        
        if media_type == "text":
            if isinstance(content, str):
                words = content.split()
                features.update({
                    "length": len(content),
                    "word_count": len(words),
                    "average_word_length": sum(len(w) for w in words) / max(1, len(words)),
                    "unique_words": len(set(words))
                })
        elif media_type == "image":
            features.update({
                "dimensions": (800, 600),
                "color_histogram": [random.random() for _ in range(10)]
            })
        elif media_type == "audio":
            features.update({
                "duration": 120.5,
                "spectral_features": [random.random() for _ in range(8)]
            })
        elif media_type == "video":
            features.update({
                "duration": 300.0,
                "frame_rate": 30,
                "key_frames": 3
            })
        
        # Add UML fingerprint
        features["uml_fingerprint"] = {
            "mean_signature": random.random(),
            "variance_signature": random.random(),
            "tfid_hash": hash(str(media_type) + str(time.time())),
            "timestamp": time.time()
        }
        
        return features

class MediaEnhancedSTM(MockOptimizedSTM):
    """Media-enhanced Short-Term Memory for demonstration"""
    
    def __init__(self, buffer_size=100):
        super().__init__(buffer_size)
        self.media_type_index = defaultdict(list)
        self.feature_extractor = MediaFeatureExtractor()
        
    def store_media(self, content, media_type=None, features=None, metadata=None):
        """Store media content with features"""
        if features is None:
            features = self.feature_extractor.extract_features(content, media_type)
            
        if media_type is None:
            media_type = features.get("media_type", "text")
        
        # Create item
        item = {
            "content": content,
            "media_type": media_type,
            "features": features,
            "timestamp": time.time()
        }
        
        if metadata:
            item["metadata"] = metadata
            
        # Store and index
        idx = len(self.memory)
        self.memory.append(item)
        self.memory_last_access[idx] = time.time()
        self.media_type_index[media_type].append(idx)
        
        return True
        
    def search_by_media_type(self, media_type, limit=10):
        """Search memory by media type"""
        if media_type in self.media_type_index:
            indices = self.media_type_index[media_type]
            results = [self.memory[i] for i in indices[-limit:]]
            return results
        return []
    
    def cross_modal_search(self, query, source_media_type='text', target_media_type=None, limit=5):
        """Cross-modal search demonstration"""
        results = {}
        
        # Simulate finding related media items
        for media_type in self.media_type_index:
            if target_media_type is None or media_type == target_media_type:
                if media_type != source_media_type:
                    items = []
                    for i in self.media_type_index[media_type]:
                        item = self.memory[i]
                        # Simple mock similarity check
                        if "metadata" in item and "description" in item["metadata"]:
                            if any(word in item["metadata"]["description"].lower() 
                                for word in query.lower().split()):
                                items.append({**item, "similarity": 0.7})
                    results[media_type] = items[:limit]
        
        return results

class MediaAwareFragmentRouter:
    """Media-aware fragment router for demonstration"""
    
    def __init__(self):
        # Register fragment weights for different media types
        self.media_configs = {
            "image": {
                "fragment_weights": {
                    "Velastra": 0.8, "Obelisk": 0.6, "Nyx": 0.6,
                    "Lyra": 0.5, "Seraphis": 0.4, "Blackwall": 0.3
                },
                "priority": 0.8
            },
            "audio": {
                "fragment_weights": {
                    "Seraphis": 0.8, "Echoe": 0.7, "Nyx": 0.6,
                    "Obelisk": 0.5, "Lyra": 0.5, "Blackwall": 0.3
                },
                "priority": 0.7
            },
            "video": {
                "fragment_weights": {
                    "Velastra": 0.7, "Echoe": 0.7, "Seraphis": 0.6,
                    "Nyx": 0.6, "Lyra": 0.6, "Obelisk": 0.5
                },
                "priority": 0.9
            },
            "text": {
                "fragment_weights": {
                    "Seraphis": 0.7, "Lyra": 0.6, "Blackwall": 0.6,
                    "Obelisk": 0.5, "Nyx": 0.5, "Echoe": 0.4
                },
                "priority": 0.6
            }
        }
        
        # Track metrics
        self.media_metrics = {
            "processed_by_type": defaultdict(int),
            "fragment_activity_by_media": defaultdict(lambda: defaultdict(int))
        }
    
    def process_media_input(self, input_data, media_type=None, context=None):
        """Process media input with appropriate fragment selection"""
        feature_extractor = MediaFeatureExtractor()
        
        # Detect media type if not provided
        if media_type is None:
            if isinstance(input_data, str):
                if input_data.endswith(('.jpg', '.jpeg', '.png')):
                    media_type = "image"
                elif input_data.endswith(('.mp3', '.wav')):
                    media_type = "audio"
                elif input_data.endswith(('.mp4', '.avi')):
                    media_type = "video"
                else:
                    media_type = "text"
            else:
                media_type = "unknown"
        
        # Get configuration for this media type
        config = self.media_configs.get(media_type, self.media_configs["text"])
        
        # Select fragment based on weights
        fragments = list(config["fragment_weights"].items())
        fragments.sort(key=lambda x: x[1], reverse=True)
        selected_fragment = fragments[0][0]
        
        # Track metrics
        self.media_metrics["processed_by_type"][media_type] += 1
        self.media_metrics["fragment_activity_by_media"][selected_fragment][media_type] += 1
        
        # Return result
        return {
            "selected_fragment": selected_fragment,
            "media_type": media_type,
            "priority": config["priority"],
            "processing_time": random.random() * 0.1
        }

def run_feature_extraction_demo():
    """Demonstrate feature extraction for different media types"""
    print("\n===== FEATURE EXTRACTION DEMO =====")
    print("Demonstrating feature extraction for different media types...")
    
    extractor = MediaFeatureExtractor()
    
    # Sample data
    sample_text = "The UML Calculator integrates with BlackwallV2 through optimized memory systems and fragment routing."
    sample_image = "samples/demo_image.jpg"
    sample_audio = "samples/demo_audio.mp3"
    sample_video = "samples/demo_video.mp4"
    
    # Extract features
    text_features = extractor.extract_features(sample_text, "text")
    image_features = extractor.extract_features(sample_image, "image")
    audio_features = extractor.extract_features(sample_audio, "audio")
    video_features = extractor.extract_features(sample_video, "video")
    
    # Display results
    print("\n1. Text feature extraction:")
    print(f"  - Length: {text_features.get('length', 'N/A')}")
    print(f"  - Word count: {text_features.get('word_count', 'N/A')}")
    print(f"  - UML fingerprint: {text_features.get('uml_fingerprint', {}).get('mean_signature', 'N/A'):.4f}")
    
    print("\n2. Image feature extraction:")
    print(f"  - Dimensions: {image_features.get('dimensions', 'N/A')}")
    print(f"  - UML fingerprint: {image_features.get('uml_fingerprint', {}).get('mean_signature', 'N/A'):.4f}")
    
    print("\n3. Audio feature extraction:")
    print(f"  - Duration: {audio_features.get('duration', 'N/A')} seconds")
    print(f"  - UML fingerprint: {audio_features.get('uml_fingerprint', {}).get('mean_signature', 'N/A'):.4f}")
    
    print("\n4. Video feature extraction:")
    print(f"  - Duration: {video_features.get('duration', 'N/A')} seconds")
    print(f"  - Frame rate: {video_features.get('frame_rate', 'N/A')} fps")
    print(f"  - UML fingerprint: {video_features.get('uml_fingerprint', {}).get('mean_signature', 'N/A'):.4f}")
    
    print("\nFeature extraction complete. Each media type produces UML-compatible feature vectors.")

def run_memory_demo():
    """Demonstrate media-enhanced memory capabilities"""
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
    """Demonstrate media-aware fragment routing"""
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
    """Run a full demonstration of all media-enhanced components"""
    print("\n===== FULL MEDIA INTEGRATION DEMO =====")
    print("Demonstrating media integration capabilities...\n")
    
    # Run individual component demos
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
