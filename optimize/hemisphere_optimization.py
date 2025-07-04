"
# Hemisphere Optimization Module
#
# This module provides optimized implementations of the memory operations
# for both the Left Hemisphere (Short-Term Memory) and Right Hemisphere (Long-Term Memory)
# of the BlackwallV2 system.

import os
import json
import time
import random
from collections import defaultdict
import bisect

class OptimizedShortTermMemory:
    '''
    Optimized implementation of the ShortTermMemory (Left Hemisphere).
    '''
    def __init__(self, buffer_size=100):
        self.memory = []
        self.buffer_size = buffer_size
        self.memshort_dir = os.path.join(os.path.dirname(__file__), '..', 'memshort')
        self.stm_file = os.path.join(self.memshort_dir, 'stm_buffer.json')
        
        # Optimization additions
        self.last_save_time = 0
        self.save_interval = 5  # seconds between saves
        self.dirty = False
        self.index = defaultdict(list)  # Word -> list of memory indices
        self.memory_last_access = {}  # Memory index -> timestamp of last access
        self.body = None
        
        self._ensure_dir()
        self.load()
        self._build_index()
        
    def _ensure_dir(self):
        os.makedirs(self.memshort_dir, exist_ok=True)
    
    def _build_index(self):
        self.index = defaultdict(list)
        for i, item in enumerate(self.memory):
            content = item.get('content', '').lower()
            words = set(content.split())
            for word in words:
                if len(word) > 2:
                    self.index[word].append(i)
    
    def store(self, item):
        self.memory.append(item)
        
        # Update index
        idx = len(self.memory) - 1
        content = item.get('content', '').lower()
        words = set(content.split())
        for word in words:
            if len(word) > 2:
                self.index[word].append(idx)
        
        # Update access time
        self.memory_last_access[idx] = time.time()
        
        # Trim if needed
        if len(self.memory) > self.buffer_size:
            self._trim_memory()
        
        # Mark as dirty and save if needed
        self.dirty = True
        self._delayed_save()
        
        return True
    
    def _trim_memory(self):
        excess = len(self.memory) - self.buffer_size
        if excess <= 0:
            return
            
        # Calculate scores for each memory item
        scores = []
        for idx, item in enumerate(self.memory):
            recency_score = self.memory_last_access.get(idx, 0)
            importance = item.get('importance', 0.5)
            score = recency_score * importance
            scores.append((idx, score))
        
        # Sort by score (ascending) and get indices to remove
        scores.sort(key=lambda x: x[1])
        indices_to_remove = [x[0] for x in scores[:excess]]
        indices_to_remove.sort(reverse=True)
        
        # Remove items and update indices
        for idx in indices_to_remove:
            removed_item = self.memory.pop(idx)
            
            # Remove from index and adjust remaining indices
            content = removed_item.get('content', '').lower()
            words = set(content.split())
            for word in words:
                if len(word) > 2 and word in self.index:
                    if idx in self.index[word]:
                        self.index[word].remove(idx)
                    
                    # Adjust higher indices
                    self.index[word] = [i if i < idx else i-1 for i in self.index[word]]
            
            # Update memory_last_access
            if idx in self.memory_last_access:
                del self.memory_last_access[idx]
            
            # Adjust indices in memory_last_access
            updated_access = {}
            for i, timestamp in self.memory_last_access.items():
                if i < idx:
                    updated_access[i] = timestamp
                elif i > idx:
                    updated_access[i-1] = timestamp
            self.memory_last_access = updated_access
    
    def get_recent(self, count=5):
        result = self.memory[-count:] if self.memory else []
        
        # Update access times
        current_time = time.time()
        for i in range(max(0, len(self.memory) - count), len(self.memory)):
            self.memory_last_access[i] = current_time
            
        return result

    def get_all(self):
        # Update all access times
        current_time = time.time()
        for i in range(len(self.memory)):
            self.memory_last_access[i] = current_time
            
        return self.memory

    def search(self, query, limit=5):
        query_words = set(query.lower().split())
        matching_indices = set()
        
        # First pass: find exact matching words using the index
        for word in query_words:
            if len(word) > 2 and word in self.index:
                # For first word, initialize the set
                if not matching_indices:
                    matching_indices.update(self.index[word])
                else:
                    # For subsequent words, retain only indices that match all words
                    matching_indices.intersection_update(self.index[word])
        
        results = []
        
        # If we found exact matches using the index
        if matching_indices:
            # Sort by recency (higher index = more recent)
            sorted_indices = sorted(matching_indices, reverse=True)
            for idx in sorted_indices[:limit]:
                results.append(self.memory[idx])
                self.memory_last_access[idx] = time.time()  # Update access time
        
        # If we need more results or didn't find any through the index
        if len(results) < limit:
            # Fall back to linear search for remaining slots
            remaining_limit = limit - len(results)
            seen_indices = set(idx for idx, _ in enumerate(results))
            
            # Do a more flexible search for partial matches
            for idx in range(len(self.memory) - 1, -1, -1):
                if idx not in seen_indices:
                    content = self.memory[idx].get('content', '').lower()
                    
                    # Check if any word in the query appears in the content
                    if any(word.lower() in content for word in query_words):
                        results.append(self.memory[idx])
                        self.memory_last_access[idx] = time.time()
                        if len(results) >= limit:
                            break
        
        return results

    def receive_signal(self, source, payload):
        message_type = payload.get('type', '')
        data = payload.get('data', {})
        print(f'[STM] Received signal from {source}: {message_type}')
        if message_type == 'store':
            item = data.get('item')
            if item:
                self.store(item)
                
        elif message_type == 'search':
            query = data.get('query')
            limit = data.get('limit', 5)
            if query:
                results = self.search(query, limit)
                if self.body:
                    self.body.emit_event('search_results', {
                        'source': 'stm',
                        'query': query,
                        'results': results
                    })
        
        # Force save after any signal processing
        self.save()
        return True

    def register_with_body(self, body):
        if body:
            self.body = body
            result = body.register_module('stm', self)
            print('[ShortTermMemory] Registered with body system')
            return result
        return False
        
    def _delayed_save(self):
        current_time = time.time()
        if self.dirty and (current_time - self.last_save_time) > self.save_interval:
            self.save()
            self.last_save_time = current_time
            self.dirty = False

    def save(self):
        try:
            with open(self.stm_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            self.dirty = False
            return True
        except Exception as e:
            print(f'[STM] Error saving memory: {e}')
            return False

    def load(self):
        try:
            if os.path.exists(self.stm_file):
                with open(self.stm_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                
                # Initialize access times for all loaded memories
                current_time = time.time()
                for i in range(len(self.memory)):
                    self.memory_last_access[i] = current_time
                
                return True
            return False
        except Exception as e:
            print(f'[STM] Error loading memory: {e}')
            self.memory = []
            return False


class OptimizedLongTermMemory:
    '''
    Optimized implementation of the LongTermMemory (Right Hemisphere).
    '''
    def __init__(self):
        self.memory = []
        self.memlong_dir = os.path.join(os.path.dirname(__file__), '..', 'memlong')
        self.ltm_file = os.path.join(self.memlong_dir, 'ltm_buffer.json')
        
        # Optimization additions
        self.last_save_time = 0
        self.save_interval = 10  # seconds between saves
        self.dirty = False
        self.word_index = defaultdict(list)  # Word -> list of memory indices
        self.tag_index = defaultdict(list)   # Tag -> list of memory indices
        self.date_index = {}                 # Date -> list of memory indices
        self.importance_index = []           # List of (importance, memory_index) tuples
        self.body = None
        
        self._ensure_dir()
        self.load()
        self._build_indices()

    def _ensure_dir(self):
        os.makedirs(self.memlong_dir, exist_ok=True)
    
    def _build_indices(self):
        self.word_index = defaultdict(list)
        self.tag_index = defaultdict(list)
        self.date_index = {}
        self.importance_index = []
        
        for i, item in enumerate(self.memory):
            # Word index from summary text
            summary = item.get('summary', '').lower()
            words = set(summary.split())
            for word in words:
                if len(word) > 2:
                    self.word_index[word].append(i)
            
            # Tag index
            tags = item.get('tags', [])
            for tag in tags:
                self.tag_index[tag.lower()].append(i)
            
            # Date index
            date = item.get('date', '')
            if date:
                if date not in self.date_index:
                    self.date_index[date] = []
                self.date_index[date].append(i)
            
            # Importance index (sorted by importance)
            importance = item.get('importance', 0.5)
            bisect.insort(self.importance_index, (importance, i))

    def store(self, summary):
        # Add timestamp if not present
        if 'date' not in summary:
            summary['date'] = time.strftime('%Y-%m-%d')
        
        # Set default importance if not present
        if 'importance' not in summary:
            summary['importance'] = 0.5
        
        # Store the memory
        self.memory.append(summary)
        idx = len(self.memory) - 1
        
        # Update word index
        summary_text = summary.get('summary', '').lower()
        words = set(summary_text.split())
        for word in words:
            if len(word) > 2:
                self.word_index[word].append(idx)
        
        # Update tag index
        tags = summary.get('tags', [])
        for tag in tags:
            self.tag_index[tag.lower()].append(idx)
        
        # Update date index
        date = summary.get('date', '')
        if date:
            if date not in self.date_index:
                self.date_index[date] = []
            self.date_index[date].append(idx)
        
        # Update importance index
        importance = summary.get('importance', 0.5)
        bisect.insort(self.importance_index, (importance, idx))
        
        # Mark as dirty and save
        self.dirty = True
        self._delayed_save()
        
        return True

    def get_all(self):
        return self.memory
        
    def search(self, query, limit=5):
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []
        seen_indices = set()
        
        # 1. First try tag matches (exact matches)
        for tag_word in query_words:
            if tag_word in self.tag_index:
                for idx in self.tag_index[tag_word]:
                    if idx not in seen_indices:
                        results.append(self.memory[idx])
                        seen_indices.add(idx)
                        if len(results) >= limit:
                            return results
        
        # 2. Try word index matches
        matching_indices = set()
        query_word_matches = {}
        
        # Count matches per index for each query word
        for word in query_words:
            if len(word) > 2 and word in self.word_index:
                for idx in self.word_index[word]:
                    if idx not in seen_indices:
                        if idx not in query_word_matches:
                            query_word_matches[idx] = 0
                        query_word_matches[idx] += 1
        
        # Sort by number of matching words (most matches first)
        sorted_matches = sorted(
            query_word_matches.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Add results by match strength
        for idx, _ in sorted_matches:
            if len(results) >= limit:
                break
            results.append(self.memory[idx])
            seen_indices.add(idx)
        
        # 3. If we need more results, do a full-text search
        if len(results) < limit:
            for i in range(len(self.memory) - 1, -1, -1):
                if i not in seen_indices:
                    summary = self.memory[i].get('summary', '').lower()
                    if query_lower in summary:
                        results.append(self.memory[i])
                        if len(results) >= limit:
                            break
        
        return results
        
    def search_by_tags(self, tags, limit=5):
        if not tags:
            return []
            
        tags_lower = [tag.lower() for tag in tags]
        matching_indices = None
        
        # Find memories that have ALL the specified tags
        for tag in tags_lower:
            if tag in self.tag_index:
                tag_indices = set(self.tag_index[tag])
                if matching_indices is None:
                    matching_indices = tag_indices
                else:
                    matching_indices.intersection_update(tag_indices)
            else:
                # If any tag doesn't exist, there can't be any matches
                return []
        
        if not matching_indices:
            return []
        
        # Sort by recency (higher index = more recent) and return up to limit
        sorted_indices = sorted(matching_indices, reverse=True)
        return [self.memory[idx] for idx in sorted_indices[:limit]]

    def receive_signal(self, source, payload):
        message_type = payload.get('type', '')
        data = payload.get('data', {})
        print(f'[LTM] Received signal from {source}: {message_type}')
        
        if message_type == 'store':
            summary = data.get('summary')
            if summary:
                self.store(summary)
                print(f'[LTM] Stored summary from signal')
                
        elif message_type == 'search':
            query = data.get('query')
            limit = data.get('limit', 5)
            if query:
                results = self.search(query, limit)
                if hasattr(self, 'body') and self.body:
                    self.body.emit_event('search_results', {
                        'source': 'ltm',
                        'query': query,
                        'results': results
                    })
        
        # Force save after signal processing
        self.save()
        return True

    def register_with_body(self, body):
        if body:
            self.body = body
            result = body.register_module('ltm', self)
            print('[LongTermMemory] Registered with body system')
            return result
        return False
        
    def _delayed_save(self):
        current_time = time.time()
        if self.dirty and (current_time - self.last_save_time) > self.save_interval:
            self.save()
            self.last_save_time = current_time
            self.dirty = False

    def save(self):
        try:
            with open(self.ltm_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            self.dirty = False
            return True
        except Exception as e:
            print(f'[LTM] Error saving memory: {e}')
            return False

    def load(self):
        try:
            if os.path.exists(self.ltm_file):
                with open(self.ltm_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                if not isinstance(self.memory, list):
                    print('[LTM] Warning: Loaded memory is not a list, resetting to empty list.')
                    self.memory = []
                return True
            return False
        except Exception as e:
            print(f'[LTM] Error loading memory: {e}')
            self.memory = []
            return False


def benchmark_hemisphere_operations(
    original_stm, original_ltm,
    optimized_stm, optimized_ltm,
    num_operations=100
):
    '''Benchmark performance between original and optimized implementations.'''
    results = {
        'stm_store': {'original': 0, 'optimized': 0},
        'stm_search': {'original': 0, 'optimized': 0},
        'ltm_store': {'original': 0, 'optimized': 0},
        'ltm_search': {'original': 0, 'optimized': 0}
    }
    
    # Generate test data
    test_memories = []
    search_queries = []
    
    for i in range(num_operations):
        memory = {
            'content': f'Test memory {i} about topic {i % 10} with keywords test{i} benchmark{i//5}',
            'timestamp': time.time(),
            'importance': random.random()
        }
        test_memories.append(memory)
        
        if i % 10 == 0:
            search_queries.append(f'test{i}')
    
    # Benchmark STM store operations
    start_time = time.time()
    for memory in test_memories:
        original_stm.store(memory)
    results['stm_store']['original'] = time.time() - start_time
    
    start_time = time.time()
    for memory in test_memories:
        optimized_stm.store(memory)
    results['stm_store']['optimized'] = time.time() - start_time
    
    # Benchmark STM search operations
    start_time = time.time()
    for query in search_queries:
        original_stm.search(query)
    results['stm_search']['original'] = time.time() - start_time
    
    start_time = time.time()
    for query in search_queries:
        optimized_stm.search(query)
    results['stm_search']['optimized'] = time.time() - start_time
    
    # Prepare LTM test data
    ltm_memories = []
    for i in range(num_operations):
        memory = {
            'summary': f'Summary of topic {i % 10} with keywords test{i} benchmark{i//5}',
            'tags': [f'topic{i%10}', 'test', f'benchmark{i//5}'],
            'date': time.strftime('%Y-%m-%d'),
            'importance': random.random()
        }
        ltm_memories.append(memory)
    
    # Benchmark LTM store operations
    start_time = time.time()
    for memory in ltm_memories:
        original_ltm.store(memory)
    results['ltm_store']['original'] = time.time() - start_time
    
    start_time = time.time()
    for memory in ltm_memories:
        optimized_ltm.store(memory)
    results['ltm_store']['optimized'] = time.time() - start_time
    
    # Benchmark LTM search operations
    start_time = time.time()
    for query in search_queries:
        original_ltm.search(query)
    results['ltm_search']['original'] = time.time() - start_time
    
    start_time = time.time()
    for query in search_queries:
        optimized_ltm.search(query)
    results['ltm_search']['optimized'] = time.time() - start_time
    
    return results
"
