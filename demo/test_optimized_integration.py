"""
Optimized Component Integration Test

This script tests the integration of optimized components into the BlackwallV2 system.
It runs basic operations using both original and optimized components for comparison.
"""

import os
import sys
import time
import json
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import integration tools
from integration import integration_tools

def generate_test_data(num_items=100):
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
    for i in range(0, num_items, num_items // 10):
        queries.append(f"test{i}")
    
    return stm_items, ltm_items, queries

def test_memory_integration(num_items=100):
    """Test memory system integration with both original and optimized components."""
    print("\nTesting Memory Integration")
    print("=========================")
    
    # Restore original components to get baseline
    integration_tools.restore_original_components()
    
    # Import memory components
    from root.Left_Hemisphere import ShortTermMemory
    from root.Right_Hemisphere import LongTermMemory
    
    # Generate test data
    stm_items, ltm_items, queries = generate_test_data(num_items)
    
    # Test with original components
    print("\nTesting with original memory components...")
    original_stm = ShortTermMemory(buffer_size=num_items+10)
    original_ltm = LongTermMemory()
    
    # Measure store performance
    start_time = time.time()
    for item in stm_items:
        original_stm.store(item)
    original_stm_store_time = time.time() - start_time
    print(f"Original STM: Stored {num_items} items in {original_stm_store_time:.4f}s")
    
    start_time = time.time()
    for item in ltm_items:
        original_ltm.store(item)
    original_ltm_store_time = time.time() - start_time
    print(f"Original LTM: Stored {num_items} items in {original_ltm_store_time:.4f}s")
    
    # Measure search performance
    start_time = time.time()
    for query in queries:
        results = original_stm.search(query)
    original_stm_search_time = time.time() - start_time
    print(f"Original STM: Performed {len(queries)} searches in {original_stm_search_time:.4f}s")
    
    start_time = time.time()
    for query in queries:
        results = original_ltm.search(query)
    original_ltm_search_time = time.time() - start_time
    print(f"Original LTM: Performed {len(queries)} searches in {original_ltm_search_time:.4f}s")
    
    # Calculate total time
    original_total_time = original_stm_store_time + original_ltm_store_time + original_stm_search_time + original_ltm_search_time
    
    # Now integrate optimized components
    integration_tools.integrate_optimized_memory()
    
    # Re-import to get the optimized versions
    from root.Left_Hemisphere import ShortTermMemory as OptimizedSTM
    from root.Right_Hemisphere import LongTermMemory as OptimizedLTM
    
    # Test with optimized components
    print("\nTesting with optimized memory components...")
    optimized_stm = OptimizedSTM(buffer_size=num_items+10)
    optimized_ltm = OptimizedLTM()
    
    # Measure store performance
    start_time = time.time()
    for item in stm_items:
        optimized_stm.store(item)
    optimized_stm_store_time = time.time() - start_time
    print(f"Optimized STM: Stored {num_items} items in {optimized_stm_store_time:.4f}s")
    
    start_time = time.time()
    for item in ltm_items:
        optimized_ltm.store(item)
    optimized_ltm_store_time = time.time() - start_time
    print(f"Optimized LTM: Stored {num_items} items in {optimized_ltm_store_time:.4f}s")
    
    # Measure search performance
    start_time = time.time()
    for query in queries:
        results = optimized_stm.search(query)
    optimized_stm_search_time = time.time() - start_time
    print(f"Optimized STM: Performed {len(queries)} searches in {optimized_stm_search_time:.4f}s")
    
    start_time = time.time()
    for query in queries:
        results = optimized_ltm.search(query)
    optimized_ltm_search_time = time.time() - start_time
    print(f"Optimized LTM: Performed {len(queries)} searches in {optimized_ltm_search_time:.4f}s")
    
    # Calculate total time
    optimized_total_time = optimized_stm_store_time + optimized_ltm_store_time + optimized_stm_search_time + optimized_ltm_search_time
    
    # Calculate improvements
    stm_store_improvement = (original_stm_store_time - optimized_stm_store_time) / original_stm_store_time * 100
    ltm_store_improvement = (original_ltm_store_time - optimized_ltm_store_time) / original_ltm_store_time * 100
    stm_search_improvement = (original_stm_search_time - optimized_stm_search_time) / original_stm_search_time * 100
    ltm_search_improvement = (original_ltm_search_time - optimized_ltm_search_time) / original_ltm_search_time * 100
    total_improvement = (original_total_time - optimized_total_time) / original_total_time * 100
    
    # Display results
    print("\nMemory Integration Results:")
    print("=========================")
    print(f"STM Store Speed Improvement: {stm_store_improvement:.2f}%")
    print(f"LTM Store Speed Improvement: {ltm_store_improvement:.2f}%")
    print(f"STM Search Speed Improvement: {stm_search_improvement:.2f}%")
    print(f"LTM Search Speed Improvement: {ltm_search_improvement:.2f}%")
    print(f"Overall Memory Speed Improvement: {total_improvement:.2f}%")
    
    # Restore original components
    integration_tools.restore_original_components()

if __name__ == "__main__":
    print("BlackwallV2 Optimized Component Integration Test")
    print("=========================================")
    print("This script tests the integration of optimized components.")
    
    # Check current integration status
    print("\nInitial Integration Status:")
    integration_tools.view_integration_status()
    
    # Run memory integration test
    test_memory_integration(100)
    
    # Final status check
    print("\nFinal Integration Status:")
    integration_tools.view_integration_status()
