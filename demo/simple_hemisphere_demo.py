"""
Simple Hemisphere Optimization Demo

This script demonstrates the performance improvements of the optimized hemisphere memory
implementations compared to the original versions.
"""

import os
import sys
import time
import json
import random
from collections import defaultdict

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import original hemisphere implementations
try:
    from root.Left_Hemisphere import ShortTermMemory
    from root.Right_Hemisphere import LongTermMemory
    print("Successfully imported original hemisphere implementations")
except Exception as e:
    print(f"Error importing original implementations: {e}")
    sys.exit(1)

# Optimized ShortTermMemory (Left Hemisphere) implementation
class OptimizedShortTermMemory:
    """
    Optimized implementation of the ShortTermMemory (Left Hemisphere).
    """
    def __init__(self, buffer_size=100):
        self.memory = []
        self.buffer_size = buffer_size
        self.memshort_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'memshort')
        self.stm_file = os.path.join(self.memshort_dir, 'stm_buffer_opt.json')  # Different file to avoid conflicts
        
        # Optimization additions
        self.last_save_time = 0
        self.save_interval = 5  # seconds between saves
        self.dirty = False
        self.index = defaultdict(list)  # Word -> list of memory indices
        self.memory_last_access = {}  # Memory index -> timestamp of last access
        
        self._ensure_dir()
        self.load()
        self._build_index()
        
    def _ensure_dir(self):
        os.makedirs(self.memshort_dir, exist_ok=True)
    
    def _build_index(self):
        """Build a search index for faster retrieval"""
        self.index = defaultdict(list)
        for i, item in enumerate(self.memory):
            content = item.get('content', '').lower()
            words = set(content.split())
            for word in words:
                if len(word) > 2:
                    self.index[word].append(i)
    
    def store(self, item):
        """Store a memory item and update the index"""
        self.memory.append(item)
        
        # Update index with new item
        content = item.get('content', '').lower()
        words = set(content.split())
        idx = len(self.memory) - 1
        for word in words:
            if len(word) > 2:
                self.index[word].append(idx)
        
        self.dirty = True
        self._check_buffer_size()
        self._delayed_save()
        return True
    
    def _check_buffer_size(self):
        """Check if the buffer size has been exceeded and trim if necessary"""
        if len(self.memory) > self.buffer_size:
            # Smart trimming - remove least important/accessed items
            to_remove = len(self.memory) - self.buffer_size
            
            # Calculate combined score (importance + recency of access)
            scores = []
            for i, item in enumerate(self.memory):
                importance = item.get('importance', 0)
                last_access = self.memory_last_access.get(i, 0)
                recency = (time.time() - last_access) / 3600  # Hours since last access
                
                # Lower score = more likely to be kept
                score = recency - (importance * 10)  # Importance weighted more heavily
                scores.append((score, i))
            
            # Sort by score (highest first = most likely to be removed)
            scores.sort(reverse=True)
            
            # Get indices to remove
            indices_to_remove = [idx for _, idx in scores[:to_remove]]
            indices_to_remove.sort(reverse=True)  # Remove from end to avoid shifting issues
            
            # Remove items
            for idx in indices_to_remove:
                self.memory.pop(idx)
            
            # Rebuild index after significant changes
            self._build_index()
            self.dirty = True
    
    def search(self, query, limit=10):
        """
        Search memory using the optimized index.
        Returns results sorted by relevance.
        """
        query = query.lower()
        query_words = [word for word in query.split() if len(word) > 2]
        
        if not query_words:
            # If no meaningful query words, return most recent memories
            results = sorted(
                self.memory[-limit*2:], 
                key=lambda x: x.get('importance', 0), 
                reverse=True
            )[:limit]
            
            # Update access timestamps
            now = time.time()
            for i, item in enumerate(self.memory[-limit*2:]):
                if item in results:
                    idx = len(self.memory) - limit*2 + i
                    self.memory_last_access[idx] = now
                    
            return results
        
        # Use the index for faster search
        candidate_indices = set()
        for word in query_words:
            if word in self.index:
                if not candidate_indices:
                    candidate_indices = set(self.index[word])
                else:
                    candidate_indices.intersection_update(self.index[word])
        
        # If no exact matches, use any word match
        if not candidate_indices:
            for word in query_words:
                for indexed_word in self.index:
                    if word in indexed_word:
                        candidate_indices.update(self.index[indexed_word])
        
        # Score candidates by relevance
        scored_results = []
        for idx in candidate_indices:
            if idx < len(self.memory):  # Safety check
                item = self.memory[idx]
                content = item.get('content', '').lower()
                
                # Calculate match score
                score = 0
                for word in query_words:
                    if word in content:
                        score += content.count(word)
                
                # Boost by importance
                score *= (1 + item.get('importance', 0))
                
                scored_results.append((score, item))
        
        # Sort by score and return top results
        results = [item for _, item in sorted(scored_results, reverse=True)][:limit]
        
        # Update access timestamps
        now = time.time()
        for idx in candidate_indices:
            if idx < len(self.memory) and self.memory[idx] in results:
                self.memory_last_access[idx] = now
        
        return results
    
    def _delayed_save(self):
        """Save to disk only periodically to reduce I/O overhead"""
        now = time.time()
        if self.dirty and (now - self.last_save_time) > self.save_interval:
            self.save()
    
    def save(self):
        """Save memory buffer to disk"""
        with open(self.stm_file, 'w') as f:
            json.dump(self.memory, f)
        self.last_save_time = time.time()
        self.dirty = False
        return True
    
    def load(self):
        """Load memory buffer from disk"""
        if os.path.exists(self.stm_file):
            try:
                with open(self.stm_file, 'r') as f:
                    self.memory = json.load(f)
                return True
            except:
                return False
        return False

    def trim_buffer(self):
        """Legacy method for compatibility"""
        self._check_buffer_size()
        return True


# Optimized LongTermMemory (Right Hemisphere) implementation
class OptimizedLongTermMemory:
    """
    Optimized implementation of the LongTermMemory (Right Hemisphere).
    """
    def __init__(self):
        self.memory = []
        self.memlong_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'memlong')
        self.ltm_file = os.path.join(self.memlong_dir, 'ltm_buffer_opt.json')  # Different file to avoid conflicts
        
        # Optimization additions
        self.last_save_time = 0
        self.save_interval = 10  # seconds between saves
        self.dirty = False
        self.tag_index = defaultdict(list)  # Tag -> list of memory indices
        self.content_index = defaultdict(list)  # Word -> list of memory indices
        self.date_index = defaultdict(list)  # Date -> list of memory indices
        self.memory_last_access = {}  # Memory index -> timestamp of last access
        
        self._ensure_dir()
        self.load()
        self._build_indices()
        
    def _ensure_dir(self):
        os.makedirs(self.memlong_dir, exist_ok=True)
    
    def _build_indices(self):
        """Build search indices for faster retrieval"""
        self.tag_index = defaultdict(list)
        self.content_index = defaultdict(list)
        self.date_index = defaultdict(list)
        
        for i, item in enumerate(self.memory):
            # Index by tags
            for tag in item.get('tags', []):
                self.tag_index[tag.lower()].append(i)
            
            # Index by content words
            summary = item.get('summary', '').lower()
            words = set(summary.split())
            for word in words:
                if len(word) > 2:
                    self.content_index[word].append(i)
            
            # Index by date
            date = item.get('date', '')
            if date:
                self.date_index[date].append(i)
    
    def store(self, item):
        """Store a memory item and update indices"""
        self.memory.append(item)
        
        # Update indices with new item
        idx = len(self.memory) - 1
        
        # Update tag index
        for tag in item.get('tags', []):
            self.tag_index[tag.lower()].append(idx)
        
        # Update content index
        summary = item.get('summary', '').lower()
        words = set(summary.split())
        for word in words:
            if len(word) > 2:
                self.content_index[word].append(idx)
        
        # Update date index
        date = item.get('date', '')
        if date:
            self.date_index[date].append(idx)
        
        self.dirty = True
        self._delayed_save()
        return True
    
    def search(self, query, limit=10):
        """
        Search LTM using optimized indices.
        Returns results sorted by relevance.
        """
        query = query.lower()
        query_words = query.split()
        
        # Check if it's a tag search
        if query.startswith('#') or query.startswith('tag:'):
            tag = query[1:] if query.startswith('#') else query[4:]
            tag = tag.lower().strip()
            
            if tag in self.tag_index:
                indices = self.tag_index[tag]
                results = [self.memory[idx] for idx in indices if idx < len(self.memory)]
                
                # Sort by importance
                results = sorted(results, key=lambda x: x.get('importance', 0), reverse=True)
                
                # Update access timestamps
                now = time.time()
                for idx in indices:
                    if idx < len(self.memory) and self.memory[idx] in results[:limit]:
                        self.memory_last_access[idx] = now
                        
                return results[:limit]
        
        # Check if it's a date search
        if query.startswith('date:'):
            date = query[5:].strip()
            
            if date in self.date_index:
                indices = self.date_index[date]
                results = [self.memory[idx] for idx in indices if idx < len(self.memory)]
                
                # Sort by importance
                results = sorted(results, key=lambda x: x.get('importance', 0), reverse=True)
                
                # Update access timestamps
                now = time.time()
                for idx in indices:
                    if idx < len(self.memory) and self.memory[idx] in results[:limit]:
                        self.memory_last_access[idx] = now
                        
                return results[:limit]
        
        # Content-based search
        candidate_indices = set()
        
        # First try exact word matches
        for word in query_words:
            if word in self.content_index:
                if not candidate_indices:
                    candidate_indices = set(self.content_index[word])
                else:
                    candidate_indices.intersection_update(self.content_index[word])
        
        # If no exact matches, use any word match or tag partial matches
        if not candidate_indices:
            for word in query_words:
                # Check content words
                for indexed_word in self.content_index:
                    if word in indexed_word:
                        candidate_indices.update(self.content_index[indexed_word])
                
                # Check tags
                for tag in self.tag_index:
                    if word in tag:
                        candidate_indices.update(self.tag_index[tag])
        
        # Score candidates by relevance
        scored_results = []
        for idx in candidate_indices:
            if idx < len(self.memory):  # Safety check
                item = self.memory[idx]
                summary = item.get('summary', '').lower()
                tags = [tag.lower() for tag in item.get('tags', [])]
                
                # Calculate match score
                score = 0
                
                # Score by content matches
                for word in query_words:
                    if word in summary:
                        score += summary.count(word) * 2  # Content matches weighted more
                
                # Score by tag matches
                for word in query_words:
                    for tag in tags:
                        if word in tag:
                            score += 10  # Tag matches are highly weighted
                            if word == tag:
                                score += 5  # Exact tag match bonus
                
                # Boost by importance
                score *= (1 + item.get('importance', 0))
                
                scored_results.append((score, item))
        
        # Sort by score and return top results
        results = [item for _, item in sorted(scored_results, reverse=True)][:limit]
        
        # Update access timestamps
        now = time.time()
        for idx in candidate_indices:
            if idx < len(self.memory) and self.memory[idx] in results:
                self.memory_last_access[idx] = now
        
        return results
    
    def _delayed_save(self):
        """Save to disk only periodically to reduce I/O overhead"""
        now = time.time()
        if self.dirty and (now - self.last_save_time) > self.save_interval:
            self.save()
    
    def save(self):
        """Save memories to disk"""
        with open(self.ltm_file, 'w') as f:
            json.dump(self.memory, f)
        self.last_save_time = time.time()
        self.dirty = False
        return True
    
    def load(self):
        """Load memories from disk"""
        if os.path.exists(self.ltm_file):
            try:
                with open(self.ltm_file, 'r') as f:
                    self.memory = json.load(f)
                return True
            except:
                return False
        return False


def generate_test_data(num_items=1000, num_queries=50):
    """Generate test data for benchmarking."""
    # Generate STM test data
    stm_items = []
    for i in range(num_items):
        item = {
            "content": f"Test memory {i} about topic {i % 20} with keywords test{i} benchmark{i//5}",
            "timestamp": time.time(),
            "importance": random.random()
        }
        stm_items.append(item)
    
    # Generate LTM test data
    ltm_items = []
    for i in range(num_items):
        item = {
            "summary": f"Summary of topic {i % 20} with keywords test{i} benchmark{i//5}",
            "tags": [f"topic{i%10}", "test", f"benchmark{i//5}"],
            "date": time.strftime("%Y-%m-%d"),
            "importance": random.random()
        }
        ltm_items.append(item)
    
    # Generate search queries
    queries = []
    for i in range(0, num_items, num_items // num_queries):
        queries.append(f"test{i}")
    
    return stm_items, ltm_items, queries


def run_benchmark(num_items=100, num_queries=10):
    """Run the benchmark and report performance."""
    print("="*80)
    print(f"Running Hemisphere Optimization Demo with {num_items} memories")
    print("="*80)
    
    # Generate test data
    print("Generating test data...")
    stm_items, ltm_items, queries = generate_test_data(num_items, num_queries)
    
    # Initialize memory modules
    print("\nInitializing memory modules...")
    original_stm = ShortTermMemory(buffer_size=num_items+10)  # Ensure no trimming during test
    optimized_stm = OptimizedShortTermMemory(buffer_size=num_items+10)
    
    original_ltm = LongTermMemory()
    optimized_ltm = OptimizedLongTermMemory()
    
    # BENCHMARK 1: Store Operations
    print("\n----- Store Operation Benchmark -----")
    
    # Original STM store
    start_time = time.time()
    for item in stm_items:
        original_stm.store(item)
    original_stm_store_time = time.time() - start_time
    print(f"Original STM: Stored {num_items} items in {original_stm_store_time:.4f}s")
    
    # Optimized STM store
    start_time = time.time()
    for item in stm_items:
        optimized_stm.store(item)
    optimized_stm_store_time = time.time() - start_time
    print(f"Optimized STM: Stored {num_items} items in {optimized_stm_store_time:.4f}s")
    
    stm_store_improvement = (original_stm_store_time - optimized_stm_store_time) / original_stm_store_time * 100
    print(f"STM Store Speed Improvement: {stm_store_improvement:.2f}%")
    
    # Original LTM store
    start_time = time.time()
    for item in ltm_items:
        original_ltm.store(item)
    original_ltm_store_time = time.time() - start_time
    print(f"Original LTM: Stored {num_items} items in {original_ltm_store_time:.4f}s")
    
    # Optimized LTM store
    start_time = time.time()
    for item in ltm_items:
        optimized_ltm.store(item)
    optimized_ltm_store_time = time.time() - start_time
    print(f"Optimized LTM: Stored {num_items} items in {optimized_ltm_store_time:.4f}s")
    
    ltm_store_improvement = (original_ltm_store_time - optimized_ltm_store_time) / original_ltm_store_time * 100
    print(f"LTM Store Speed Improvement: {ltm_store_improvement:.2f}%")
    
    # BENCHMARK 2: Search Operations
    print("\n----- Search Operation Benchmark -----")
    
    # Original STM search
    start_time = time.time()
    for query in queries:
        results = original_stm.search(query)
    original_stm_search_time = time.time() - start_time
    print(f"Original STM: Performed {len(queries)} searches in {original_stm_search_time:.4f}s")
    
    # Optimized STM search
    start_time = time.time()
    for query in queries:
        results = optimized_stm.search(query)
    optimized_stm_search_time = time.time() - start_time
    print(f"Optimized STM: Performed {len(queries)} searches in {optimized_stm_search_time:.4f}s")
    
    stm_search_improvement = (original_stm_search_time - optimized_stm_search_time) / original_stm_search_time * 100
    print(f"STM Search Speed Improvement: {stm_search_improvement:.2f}%")
    
    # Original LTM search
    start_time = time.time()
    for query in queries:
        results = original_ltm.search(query)
    original_ltm_search_time = time.time() - start_time
    print(f"Original LTM: Performed {len(queries)} searches in {original_ltm_search_time:.4f}s")
    
    # Optimized LTM search
    start_time = time.time()
    for query in queries:
        results = optimized_ltm.search(query)
    optimized_ltm_search_time = time.time() - start_time
    print(f"Optimized LTM: Performed {len(queries)} searches in {optimized_ltm_search_time:.4f}s")
    
    ltm_search_improvement = (original_ltm_search_time - optimized_ltm_search_time) / original_ltm_search_time * 100
    print(f"LTM Search Speed Improvement: {ltm_search_improvement:.2f}%")
    
    # Overall improvement
    overall_original_time = original_stm_store_time + original_ltm_store_time + original_stm_search_time + original_ltm_search_time
    overall_optimized_time = optimized_stm_store_time + optimized_ltm_store_time + optimized_stm_search_time + optimized_ltm_search_time
    overall_improvement = (overall_original_time - overall_optimized_time) / overall_original_time * 100
    
    print("\n----- Overall Performance -----")
    print(f"Original implementation: {overall_original_time:.4f}s")
    print(f"Optimized implementation: {overall_optimized_time:.4f}s")
    print(f"Overall Performance Improvement: {overall_improvement:.2f}%")
    
    return {
        "stm_store_improvement": stm_store_improvement,
        "ltm_store_improvement": ltm_store_improvement,
        "stm_search_improvement": stm_search_improvement,
        "ltm_search_improvement": ltm_search_improvement,
        "overall_improvement": overall_improvement
    }


if __name__ == "__main__":
    print("\nSIMPLE HEMISPHERE OPTIMIZATION DEMO\n")
    print("This demo compares the performance of original hemisphere implementations")
    print("with the optimized versions featuring indexing and faster operations.")
    print("\nRunning benchmarks...")
    
    try:
        # Run with smaller dataset first for quick demo
        print("\n\n=== SMALL DATASET TEST (100 items) ===")
        small_results = run_benchmark(100, 10)
        
        # Run with larger dataset for more realistic comparison
        print("\n\n=== MEDIUM DATASET TEST (1000 items) ===")
        medium_results = run_benchmark(1000, 50)
        
        print("\n\nSUMMARY OF IMPROVEMENTS:")
        print(f"Small dataset overall improvement: {small_results['overall_improvement']:.2f}%")
        print(f"Medium dataset overall improvement: {medium_results['overall_improvement']:.2f}%")
        
        print("\nNotes:")
        print("- Search operations show the most significant improvements due to indexed lookups")
        print("- Storage operations benefit from deferred I/O and more efficient indexing")
        print("- Larger datasets show greater performance benefits from optimizations")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
