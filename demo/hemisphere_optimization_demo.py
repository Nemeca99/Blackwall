"""
Hemisphere Optimization Demo

This script demonstrates the optimized versions of the Left and Right Hemisphere
(Short-Term Memory and Long-Term Memory) in action.
"""

import os
import sys
import time
import json
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import original hemisphere implementations
from root.Left_Hemisphere import ShortTermMemory
from root.Right_Hemisphere import LongTermMemory

# Import optimized hemisphere implementations
from optimize.hemisphere_optimization import OptimizedShortTermMemory, OptimizedLongTermMemory

def format_memory_display(memory_item):
    """Format a memory item for display."""
    if 'content' in memory_item:
        return f"STM: {memory_item.get('content', '')[:50]}..."
    elif 'summary' in memory_item:
        return f"LTM: {memory_item.get('summary', '')[:50]}..."
    else:
        return str(memory_item)

def run_demo():
    """Run a demonstration of the optimized memory hemispheres."""
    # Welcome message
    print("\n" + "="*80)
    print("BlackwallV2 Memory Hemisphere Optimization Demo")
    print("="*80)
    
    print("\nThis demo showcases the capabilities of the optimized memory hemispheres.")
    print("It will demonstrate memory operations on both original and optimized implementations.")
    
    # Initialize memory modules
    print("\nInitializing memory systems...")
    original_stm = ShortTermMemory(buffer_size=50)
    optimized_stm = OptimizedShortTermMemory(buffer_size=50)
    
    original_ltm = LongTermMemory()
    optimized_ltm = OptimizedLongTermMemory()
    
    # Demo data
    print("\nPreparing demo data...")
    demo_memories = []
    for i in range(20):
        topic = random.choice(["science", "math", "philosophy", "art", "music", "technology"])
        memory = {
            "content": f"Memory {i+1}: A thought about {topic} and its importance in recursive systems theory.",
            "timestamp": time.time(),
            "importance": random.random()
        }
        demo_memories.append(memory)
    
    print("\nStoring memories in original and optimized systems...")
    for i, memory in enumerate(demo_memories):
        print(f"Storing memory {i+1}/{len(demo_memories)}", end='\r')
        original_stm.store(memory)
        optimized_stm.store(memory)
        
        # For every 5th memory, consolidate to LTM
        if (i+1) % 5 == 0:
            summary = {
                "summary": f"Consolidated memory about {memory['content'].split('about ')[1].split(' and')[0]}",
                "tags": [memory['content'].split('about ')[1].split(' and')[0], "recursive", "theory"],
                "importance": memory["importance"]
            }
            original_ltm.store(summary)
            optimized_ltm.store(summary)
    
    print("\n\nMemory storage complete!")
    
    # Demonstrate search capabilities
    print("\n" + "-"*80)
    print("SEARCH DEMONSTRATION")
    print("-"*80)
    
    search_terms = ["recursive", "science", "technology", "music"]
    
    for term in search_terms:
        print(f"\nSearching for '{term}':")
        
        print("\nOriginal STM results:")
        start_time = time.time()
        results = original_stm.search(term)
        orig_stm_time = time.time() - start_time
        
        for result in results:
            print(f"  - {format_memory_display(result)}")
        print(f"Search completed in {orig_stm_time:.6f} seconds")
        
        print("\nOptimized STM results:")
        start_time = time.time()
        results = optimized_stm.search(term)
        opt_stm_time = time.time() - start_time
        
        for result in results:
            print(f"  - {format_memory_display(result)}")
        print(f"Search completed in {opt_stm_time:.6f} seconds")
        
        speedup = (orig_stm_time - opt_stm_time) / orig_stm_time * 100 if orig_stm_time > 0 else 0
        print(f"Speedup: {speedup:.2f}%")
        
        print("\nOriginal LTM results:")
        start_time = time.time()
        results = original_ltm.search(term)
        orig_ltm_time = time.time() - start_time
        
        for result in results:
            print(f"  - {format_memory_display(result)}")
        print(f"Search completed in {orig_ltm_time:.6f} seconds")
        
        print("\nOptimized LTM results:")
        start_time = time.time()
        results = optimized_ltm.search(term)
        opt_ltm_time = time.time() - start_time
        
        for result in results:
            print(f"  - {format_memory_display(result)}")
        print(f"Search completed in {opt_ltm_time:.6f} seconds")
        
        speedup = (orig_ltm_time - opt_ltm_time) / orig_ltm_time * 100 if orig_ltm_time > 0 else 0
        print(f"Speedup: {speedup:.2f}%")
    
    # Demonstrate advanced features of optimized LTM
    print("\n" + "-"*80)
    print("ADVANCED FEATURES DEMONSTRATION")
    print("-"*80)
    
    print("\nOptimized LTM Tag-Based Search:")
    start_time = time.time()
    results = optimized_ltm.search_by_tags(["science", "recursive"])
    search_time = time.time() - start_time
    
    for result in results:
        print(f"  - {format_memory_display(result)}")
    print(f"Tag-based search completed in {search_time:.6f} seconds")
    
    # Summary
    print("\n" + "="*80)
    print("DEMONSTRATION SUMMARY")
    print("="*80)
    
    print("\nThe optimized memory hemispheres provide several advantages:")
    print("  1. Faster search operations through multi-level indexing")
    print("  2. More efficient memory organization and retrieval")
    print("  3. Additional search capabilities (tag-based, date-based, importance-based)")
    print("  4. Improved memory management with smart trimming")
    print("  5. Reduced disk I/O through delayed/batched writes")
    
    print("\nRun the full benchmark with run_hemisphere_benchmark.bat to see detailed performance metrics.")
    print("="*80)

if __name__ == "__main__":
    run_demo()
