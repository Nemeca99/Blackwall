"""
Optimized Memory Consolidation Algorithms for BlackwallV2

This module provides improved algorithms for memory consolidation,
focusing on efficient similarity detection and content processing.
"""

import re
import time
import hashlib
from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict


class OptimizedSimilarity:
    """
    Optimized text similarity calculation.
    Uses TF-IDF inspired approach for better performance.
    """
    
    def __init__(self):
        """Initialize the similarity calculator."""
        self.word_cache = {}
        
    def _get_word_set(self, text: str) -> Set[str]:
        """Extract words from text and cache the results."""
        if text in self.word_cache:
            return self.word_cache[text]
            
        # Normalize text and split into words
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        words = set(text.split())
        
        # Cache the result
        self.word_cache[text] = words
        return words
        
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts with optimizations.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Quick check for identical texts
        if text1 == text2:
            return 1.0
            
        # Early termination for empty texts
        if not text1 or not text2:
            return 0.0
            
        # Get word sets
        words1 = self._get_word_set(text1)
        words2 = self._get_word_set(text2)
        
        # Early termination for very different length texts
        len1, len2 = len(words1), len(words2)
        if len1 == 0 or len2 == 0:
            return 0.0
            
        # Length-based early termination
        if len1 > 2 * len2 or len2 > 2 * len1:
            return 0.0
            
        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
            
        return len(intersection) / len(union)


class OptimizedMemoryConsolidation:
    """
    Optimized memory consolidation algorithms for BlackwallV2.
    """
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Initialize optimized memory consolidation.
        
        Args:
            similarity_threshold: Threshold for considering memories similar
        """
        self.similarity_threshold = similarity_threshold
        self.similarity = OptimizedSimilarity()
        self.content_cache: Dict[str, List[str]] = {}
        
    def consolidate_by_tag(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Consolidate memories by tag.
        
        Args:
            memories: List of memory objects
            
        Returns:
            List of consolidated memories
        """
        if not memories:
            return []
            
        # Group memories by tag
        tag_groups = defaultdict(list)
        for memory in memories:
            tag = memory.get('tag', '')
            if tag:
                tag_groups[tag].append(memory)
                
        # Create consolidated memories
        consolidated = []
        for tag, group in tag_groups.items():
            if len(group) <= 1:
                continue
                
            # Extract contents
            contents = [memory.get('content', '') for memory in group]
            # Join related contents
            combined_content = ' | '.join(contents)
            
            # Create consolidated memory
            consolidated.append({
                'id': f"consolidated_{tag}_{int(time.time())}",
                'tag': tag,
                'type': 'consolidated_memory',
                'source_count': len(group),
                'source_ids': [memory.get('id', '') for memory in group],
                'content': combined_content,
                'timestamp': time.time()
            })
            
        return consolidated
        
    def consolidate_by_content(self, memories: List[Dict[str, Any]], 
                              batch_size: int = 100) -> List[Dict[str, Any]]:
        """
        Consolidate memories by content similarity.
        
        Args:
            memories: List of memory objects
            batch_size: Size of batches to process
            
        Returns:
            List of consolidated memories
        """
        if not memories:
            return []
            
        # Group memories by tag first for initial filtering
        tag_groups = defaultdict(list)
        for memory in memories:
            tag = memory.get('tag', '')
            tag_groups[tag].append(memory)
                
        # Process each tag group separately - this dramatically reduces comparisons
        similarity_groups = []
        
        for tag, group in tag_groups.items():
            # Skip tiny groups (nothing to consolidate)
            if len(group) <= 1:
                continue
                
            # Skip huge groups (likely generic tag)
            if len(group) > 100:
                continue  # Skip very large groups for performance
                
            # Extract texts for similarity checks
            texts = []
            for memory in group:
                content = memory.get('content', '')
                if content:
                    texts.append(content)
                else:
                    texts.append('')
                    
            # Find similar memories within this tag group
            for i, (mem1, text1) in enumerate(zip(group, texts)):
                # Skip empty content
                if not text1:
                    continue
                    
                # Use cached similarity results if available
                cache_key = mem1.get('id', '')
                if cache_key in self.content_cache:
                    similar_mem_ids = self.content_cache[cache_key]
                    # Create a similarity group from cached results
                    similar_group = [mem1]
                    for mem_id in similar_mem_ids:
                        for m in group:
                            if m.get('id') == mem_id:
                                similar_group.append(m)
                                break
                    
                    if len(similar_group) > 1:
                        similarity_groups.append(similar_group)
                    continue
                
                # Compare with other memories
                similar_mems = [mem1]
                similar_mem_ids = []
                
                # Compare only with remaining memories in this group
                for j in range(i + 1, len(group)):
                    mem2 = group[j]
                    text2 = texts[j]
                    
                    # Skip empty content
                    if not text2:
                        continue
                        
                    # Calculate similarity
                    similarity = self.similarity.similarity(text1, text2)
                    if similarity >= self.similarity_threshold:
                        similar_mems.append(mem2)
                        similar_mem_ids.append(mem2.get('id', ''))
                        
                        # Limit number of similar memories (prevents over-consolidation)
                        if len(similar_mems) >= 5:
                            break
                
                # Cache the results
                if similar_mem_ids:
                    self.content_cache[cache_key] = similar_mem_ids
                    
                # Add group if multiple memories are similar
                if len(similar_mems) > 1:
                    similarity_groups.append(similar_mems)
            
        # Create consolidated memories from similarity groups
        consolidated = []
        for group in similarity_groups:
            # Extract contents and tags
            contents = [memory.get('content', '') for memory in group]
            tags = set()
            for memory in group:
                tag = memory.get('tag', '')
                if tag:
                    tags.add(tag)
            
            # Join related contents
            combined_content = ' | '.join(contents)
            
            # Create consolidated memory
            consolidated.append({
                'id': f"consolidated_content_{int(time.time())}",
                'tag': ','.join(tags) if tags else 'consolidated',
                'type': 'consolidated_memory',
                'source_count': len(group),
                'source_ids': [memory.get('id', '') for memory in group],
                'content': combined_content,
                'timestamp': time.time(),
                'similarity_score': self.similarity_threshold
            })
            
        return consolidated
