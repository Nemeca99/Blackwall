"""
Media-Enhanced Memory System

This module extends the OptimizedShortTermMemory and OptimizedLongTermMemory classes
to support efficient storage and retrieval of multimedia content.
"""

import os
import time
import json
import hashlib
import random
from collections import defaultdict
from typing import Dict, Any, List, Tuple, Union

# Import the base optimized memory classes
from optimize.hemisphere_optimization import OptimizedShortTermMemory, OptimizedLongTermMemory

# Import media feature extraction
from media.media_feature_extraction import feature_extractor, detect_media_type

class MediaEnhancedSTM(OptimizedShortTermMemory):
    """
    Media-enhanced Short-Term Memory with optimized indexing for multimedia content.
    Extends the OptimizedShortTermMemory with media-specific features.
    """
    def __init__(self, buffer_size=100):
        super().__init__(buffer_size)
        
        # Additional media-specific indices
        self.media_type_index = defaultdict(list)  # MediaType -> list of memory indices
        self.feature_index = {}  # Feature hash -> list of memory indices
        self.cross_modal_index = defaultdict(dict)  # Word -> {MediaType -> list of memory indices}
        
        # Rebuild indices to include media information
        self._build_media_indices()
    
    def _build_media_indices(self):
        """Build media-specific indices from existing memory items"""
        for i, item in enumerate(self.memory):
            # Index by media type if available
            media_type = item.get('media_type', 'text')  # Default to text
            self.media_type_index[media_type].append(i)
            
            # Index by feature hash if available
            features = item.get('features', {})
            if features:
                feature_hash = self._hash_features(features)
                if feature_hash not in self.feature_index:
                    self.feature_index[feature_hash] = []
                self.feature_index[feature_hash].append(i)
            
            # Build cross-modal index
            content = item.get('content', '').lower()
            words = set(content.split())
            for word in words:
                if len(word) > 2:
                    if media_type not in self.cross_modal_index[word]:
                        self.cross_modal_index[word][media_type] = []
                    self.cross_modal_index[word][media_type].append(i)
    
    def _hash_features(self, features: Dict[str, Any]) -> str:
        """Create a hash of feature values for indexing"""
        # Convert complex feature dictionary to a string representation
        feature_str = json.dumps(features, sort_keys=True)
        return hashlib.md5(feature_str.encode()).hexdigest()
    
    def store_media(self, content, media_type=None, features=None, metadata=None):
        """
        Store media content with automatic feature extraction.
        
        Args:
            content: The media content (could be file path, raw data, or text)
            media_type: Optional media type (auto-detected if not provided)
            features: Pre-extracted features (if available)
            metadata: Additional metadata for the media item
            
        Returns:
            bool: Success status
        """
        # Detect media type if not provided
        if media_type is None:
            media_type = detect_media_type(content)
        
        # Extract features if not provided
        if features is None:
            features = feature_extractor.extract_features(content, media_type)
        
        # Create memory item
        item = {
            "content": content,
            "media_type": media_type,
            "features": features,
            "timestamp": time.time(),
            "importance": self._calculate_media_importance(features)
        }
        
        # Add metadata if available
        if metadata:
            item.update(metadata)
        
        # Store in memory
        idx = len(self.memory)
        self.memory.append(item)
        self.dirty = True
        
        # Update media indices
        self.media_type_index[media_type].append(idx)
        
        # Update feature index
        feature_hash = self._hash_features(features)
        if feature_hash not in self.feature_index:
            self.feature_index[feature_hash] = []
        self.feature_index[feature_hash].append(idx)
        
        # Update cross-modal index for text content or text metadata
        text_content = ''
        if media_type == 'text':
            text_content = content if isinstance(content, str) else str(content)
        elif metadata and 'description' in metadata:
            text_content = metadata['description']
            
        if text_content:
            words = set(text_content.lower().split())
            for word in words:
                if len(word) > 2:
                    if media_type not in self.cross_modal_index[word]:
                        self.cross_modal_index[word][media_type] = []
                    self.cross_modal_index[word][media_type].append(idx)
        
        # Schedule delayed save
        self._delayed_save()
        return True
    
    def search_by_media_type(self, media_type, limit=10):
        """Search memory by media type"""
        if media_type in self.media_type_index:
            indices = self.media_type_index[media_type]
            results = [self.memory[i] for i in indices[-limit:]]
            # Update access times
            current_time = time.time()
            for i in indices[-limit:]:
                self.memory_last_access[i] = current_time
            return results
        return []
    
    def search_similar_media(self, features, threshold=0.7, limit=5):
        """
        Search for media with similar features.
        
        Args:
            features: Feature dictionary to match against
            threshold: Similarity threshold (0-1)
            limit: Maximum results to return
            
        Returns:
            List of matching memory items
        """
        # Compare features with stored items
        scores = []
        for i, item in enumerate(self.memory):
            if 'features' in item:
                similarity = self._calculate_feature_similarity(features, item['features'])
                if similarity >= threshold:
                    scores.append((i, similarity))
        
        # Sort by similarity score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Update access times and return top results
        current_time = time.time()
        results = []
        for i, score in scores[:limit]:
            self.memory_last_access[i] = current_time
            results.append({**self.memory[i], 'similarity': score})
        
        return results
    
    def cross_modal_search(self, query, source_media_type='text', target_media_type=None, limit=5):
        """
        Cross-modal search - find media of one type related to media of another type.
        
        Args:
            query: Search query
            source_media_type: The media type of the query
            target_media_type: The desired media type (None for all non-source types)
            limit: Maximum results per media type
            
        Returns:
            Dict mapping media types to search results
        """
        results = {}
        
        # Text to media search
        if source_media_type == 'text':
            words = set(query.lower().split())
            candidate_indices = set()
            
            # Find matches in cross-modal index
            for word in words:
                if word in self.cross_modal_index:
                    for media_type, indices in self.cross_modal_index[word].items():
                        if target_media_type is None or media_type == target_media_type:
                            if media_type != source_media_type:
                                for idx in indices:
                                    candidate_indices.add((media_type, idx))
            
            # Group by media type
            media_groups = defaultdict(list)
            for media_type, idx in candidate_indices:
                media_groups[media_type].append(idx)
            
            # Build results
            for media_type, indices in media_groups.items():
                # Sort by timestamp (most recent first)
                sorted_indices = sorted(indices, 
                    key=lambda i: self.memory[i].get('timestamp', 0), 
                    reverse=True)
                
                # Update access times
                current_time = time.time()
                for i in sorted_indices[:limit]:
                    self.memory_last_access[i] = current_time
                
                # Add to results
                results[media_type] = [self.memory[i] for i in sorted_indices[:limit]]
        
        # Media to media search (via features)
        elif source_media_type in self.media_type_index:
            # Find all items of the source media type containing the query
            if isinstance(query, str):
                source_items = self.search(query)
            else:
                # If query is a feature set, find similar items
                source_items = [self.memory[i] for i in self.media_type_index[source_media_type]]
            
            # Extract features from source items
            source_features = []
            for item in source_items:
                if 'features' in item:
                    source_features.append(item['features'])
            
            # Find similar items of different media types
            for media_type in self.media_type_index:
                if target_media_type is None or media_type == target_media_type:
                    if media_type != source_media_type:
                        media_results = []
                        
                        # Compare with each source feature
                        for feature in source_features:
                            for i in self.media_type_index[media_type]:
                                item = self.memory[i]
                                if 'features' in item:
                                    similarity = self._calculate_feature_similarity(
                                        feature, item['features'])
                                    if similarity >= 0.5:  # Threshold
                                        media_results.append((i, similarity))
                        
                        # Sort by similarity
                        media_results.sort(key=lambda x: x[1], reverse=True)
                        
                        # Update access times
                        current_time = time.time()
                        for i, _ in media_results[:limit]:
                            self.memory_last_access[i] = current_time
                        
                        # Add to results
                        if media_results:
                            results[media_type] = [
                                {**self.memory[i], 'similarity': score} 
                                for i, score in media_results[:limit]
                            ]
        
        return results
    
    def _calculate_media_importance(self, features):
        """Calculate importance score for media item based on features"""
        # Media items are generally more important than plain text
        base_importance = 0.6
        
        # Adjust importance based on media type
        media_type = features.get("media_type", "text")
        if media_type == "image":
            base_importance += 0.1
        elif media_type == "video":
            base_importance += 0.2
        elif media_type == "audio":
            base_importance += 0.15
        
        # Add random variance
        variance = 0.1 * (0.5 - random.random())
        
        return min(0.95, max(0.1, base_importance + variance))
    
    def _calculate_feature_similarity(self, features1, features2):
        """Calculate similarity between two feature sets"""
        # Extract UML fingerprints if available
        fp1 = features1.get('uml_fingerprint', {})
        fp2 = features2.get('uml_fingerprint', {})
        
        if not fp1 or not fp2:
            return 0.0
            
        # Calculate similarity based on UML signatures
        mean_diff = abs(fp1.get('mean_signature', 0) - fp2.get('mean_signature', 0))
        var_diff = abs(fp1.get('variance_signature', 0) - fp2.get('variance_signature', 0))
        
        # Normalize differences
        mean_sim = max(0, 1 - (mean_diff / max(abs(fp1.get('mean_signature', 0)), 1)))
        var_sim = max(0, 1 - (var_diff / max(abs(fp1.get('variance_signature', 0)), 1)))
        
        # Combine similarity scores
        similarity = (mean_sim * 0.7) + (var_sim * 0.3)
        return similarity


class MediaEnhancedLTM(OptimizedLongTermMemory):
    """
    Media-enhanced Long-Term Memory with optimized indexing for multimedia content.
    Extends the OptimizedLongTermMemory with media-specific features.
    """
    def __init__(self):
        super().__init__()
        
        # Additional media-specific indices
        self.media_type_index = defaultdict(list)  # MediaType -> list of memory indices
        self.media_feature_index = {}  # Feature category -> feature value -> list of memory indices
        
        # Media-specific paths
        self.media_dir = os.path.join(self.memlong_dir, 'media')
        self._ensure_media_dir()
        
        # Build media indices from existing memory
        self._build_media_indices()
    
    def _ensure_media_dir(self):
        """Ensure media directory exists"""
        os.makedirs(self.media_dir, exist_ok=True)
    
    def _build_media_indices(self):
        """Build media-specific indices from existing memory items"""
        self.media_type_index = defaultdict(list)
        self.media_feature_index = defaultdict(lambda: defaultdict(list))
        
        for i, item in enumerate(self.memory):
            # Index by media type if available
            media_type = item.get('media_type', '')
            if media_type:
                self.media_type_index[media_type].append(i)
            
            # Index by media features
            if 'uml_features' in item:
                for feature_type, feature_value in item['uml_features'].items():
                    if isinstance(feature_value, (int, float)):
                        value_bucket = round(feature_value * 10) / 10  # Round to nearest 0.1
                        self.media_feature_index[feature_type][value_bucket].append(i)
    
    def store_media_summary(self, summary, media_type, uml_features, tags=None, importance=None):
        """
        Store a summary of media content in long-term memory.
        
        Args:
            summary: Text summary of the media content
            media_type: Type of media ('image', 'audio', 'video', etc.)
            uml_features: UML feature representation of the media
            tags: Optional list of tags for the media
            importance: Optional importance score (0-1)
            
        Returns:
            bool: Success status
        """
        # Create memory item
        if tags is None:
            tags = []
        
        # Add media type to tags
        if media_type and media_type not in tags:
            tags.append(media_type)
        
        # Calculate importance if not provided
        if importance is None:
            # Base importance on feature complexity
            if isinstance(uml_features, dict) and len(uml_features) > 0:
                importance = min(0.95, 0.5 + (len(uml_features) / 20))
            else:
                importance = 0.5
        
        # Create memory item
        item = {
            'summary': summary,
            'media_type': media_type,
            'uml_features': uml_features,
            'tags': tags,
            'date': time.strftime("%Y-%m-%d"),
            'importance': importance
        }
        
        # Store in memory
        idx = len(self.memory)
        self.memory.append(item)
        self.dirty = True
        
        # Update indices
        self.media_type_index[media_type].append(idx)
        
        # Update tag index
        for tag in tags:
            self.tag_index[tag.lower()].append(idx)
        
        # Update date index
        date = item['date']
        if date not in self.date_index:
            self.date_index[date] = []
        self.date_index[date].append(idx)
        
        # Update importance index
        self.importance_index.append((importance, idx))
        
        # Update feature index
        if isinstance(uml_features, dict):
            for feature_type, feature_value in uml_features.items():
                if isinstance(feature_value, (int, float)):
                    value_bucket = round(feature_value * 10) / 10  # Round to nearest 0.1
                    self.media_feature_index[feature_type][value_bucket].append(idx)
        
        # Schedule delayed save
        self._delayed_save()
        return True
    
    def search_by_media_type(self, media_type, limit=10):
        """Search memory by media type"""
        if media_type in self.media_type_index:
            indices = self.media_type_index[media_type]
            return [self.memory[i] for i in indices[-limit:]]
        return []
    
    def search_by_feature(self, feature_type, feature_value, tolerance=0.1, limit=10):
        """
        Search for media by specific feature value.
        
        Args:
            feature_type: The feature category to search
            feature_value: The target feature value
            tolerance: Value tolerance (+/-)
            limit: Maximum results to return
            
        Returns:
            List of matching memory items
        """
        if feature_type not in self.media_feature_index:
            return []
            
        # Find buckets within tolerance range
        min_bucket = round((feature_value - tolerance) * 10) / 10
        max_bucket = round((feature_value + tolerance) * 10) / 10
        
        # Collect all indices within range
        indices = []
        for bucket_value in self.media_feature_index[feature_type]:
            if min_bucket <= bucket_value <= max_bucket:
                indices.extend(self.media_feature_index[feature_type][bucket_value])
        
        # Sort by importance and timestamp (more important and newer first)
        sorted_indices = sorted(indices, 
            key=lambda i: (self.memory[i].get('importance', 0), 
                          self.memory[i].get('date', '')),
            reverse=True)
        
        return [self.memory[i] for i in sorted_indices[:limit]]
    
    def find_related_media(self, item_index, limit=5):
        """
        Find media items related to the specified item.
        
        Args:
            item_index: Index of the item to find related media for
            limit: Maximum results to return
            
        Returns:
            List of related memory items
        """
        if item_index >= len(self.memory):
            return []
            
        item = self.memory[item_index]
        
        # Find related items based on tags
        related_by_tags = self.search_by_tags(item.get('tags', []), limit=limit*2)
        
        # Find related items based on features
        related_by_features = []
        if 'uml_features' in item:
            for feature_type, feature_value in item['uml_features'].items():
                if isinstance(feature_value, (int, float)):
                    feature_matches = self.search_by_feature(
                        feature_type, feature_value, tolerance=0.2, limit=limit)
                    related_by_features.extend(feature_matches)
        
        # Combine results, removing duplicates and the original item
        seen = {item_index}
        results = []
        
        # Add tag matches first
        for related_item in related_by_tags:
            related_index = self.memory.index(related_item)
            if related_index not in seen:
                results.append(related_item)
                seen.add(related_index)
                if len(results) >= limit:
                    break
        
        # Then add feature matches
        for related_item in related_by_features:
            related_index = self.memory.index(related_item)
            if related_index not in seen:
                results.append(related_item)
                seen.add(related_index)
                if len(results) >= limit:
                    break
        
        return results
