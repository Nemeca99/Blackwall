#!/usr/bin/env python3
"""
BlackwallV2 Profiling Script

This script profiles the core biomimetic algorithms in BlackwallV2 to identify
bottlenecks and optimization opportunities before LLM integration.
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import profiler
from tools.performance_profiler import ComponentProfiler

# Import modules to profile
from root.dream_manager import DreamManager
from root.fragment_manager import FragmentManager
from root.Right_Hemisphere import LongTermMemory
from root.Left_Hemisphere import ShortTermMemory
from root.body import Body 
from root.heart import Heart

# Import logger
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Profiler")


def profile_memory_consolidation():
    """
    Profile the memory consolidation algorithms in DreamManager.
    """
    logger.info("=== Profiling Memory Consolidation ===")
    
    # Initialize dependencies
    ltm = LongTermMemory()
    body = Body()
    heart = Heart(body=body)
    
    # Generate test data - memories with various tags
    tags = ["concept", "experience", "emotion", "math", "language"]
    for i in range(500):  # Generate 500 test memories
        tag = tags[i % len(tags)]
        ltm.store({
            "id": f"mem_{i}",
            "tag": tag,
            "content": f"Test memory {i} with tag {tag} for profiling memory consolidation.",
            "timestamp": datetime.now().isoformat()
        })
    
    # Initialize DreamManager with test data
    dream_manager = DreamManager(long_term_memory=ltm, heart=heart, body=body)
    
    # Create profiler
    profiler = ComponentProfiler(output_dir=os.path.join(parent_dir, "profile_results"))
    
    # Profile dream cycle
    logger.info("Profiling dream cycle with 500 memories...")
    result = profiler.profile_dream_cycle(dream_manager, memory_count=500)
    logger.info(f"Dream cycle completed in {result['profile']['elapsed_seconds']:.4f} seconds")
    
    # Profile memory fragmentation calculation
    logger.info("Profiling memory fragmentation calculation...")
    fragmentation_result = profiler.profile_function(
        dream_manager._calculate_memory_fragmentation,
        name="memory_fragmentation",
        iterations=10
    )
    logger.info(f"Memory fragmentation calculation: {fragmentation_result['profile']['avg_time_seconds']:.4f} seconds per iteration")
    
    # Profile memory consolidation specifically
    logger.info("Profiling memory consolidation...")
    consolidation_result = profiler.profile_function(
        dream_manager._consolidate_memories,
        name="memory_consolidation",
        iterations=5
    )
    logger.info(f"Memory consolidation: {consolidation_result['profile']['avg_time_seconds']:.4f} seconds per iteration")
    
    return profiler


def profile_fragment_routing():
    """
    Profile the fragment routing algorithms in FragmentManager.
    """
    logger.info("\n=== Profiling Fragment Routing ===")
    
    # Initialize dependencies
    body = Body()
    
    # Initialize FragmentManager
    fragment_manager = FragmentManager(body=body)
    
    # Create profiler
    profiler = ComponentProfiler(output_dir=os.path.join(parent_dir, "profile_results"))
    
    # Profile fragment analysis
    logger.info("Profiling fragment analysis...")
    analysis_result = profiler.profile_fragment_analysis(fragment_manager, input_count=100)
    logger.info(f"Fragment analysis completed in {analysis_result['profile']['elapsed_seconds']:.4f} seconds")
    
    # Profile routing modification
    logger.info("Profiling routing modification by fragments...")
    test_organs = [
        {"id": "organ1", "capabilities": ["math", "logic"], "health": 0.9},
        {"id": "organ2", "capabilities": ["creativity", "art"], "health": 0.8},
        {"id": "organ3", "capabilities": ["security", "validation"], "health": 0.95},
        {"id": "organ4", "capabilities": ["memory", "history"], "health": 0.85}
    ]
    
    routing_result = profiler.profile_function(
        lambda: [fragment_manager.modify_routing_by_fragments(cap, test_organs) 
                for cap in ["math", "creativity", "security", "memory"]],
        name="routing_modification",
        iterations=50
    )
    logger.info(f"Routing modification: {routing_result['profile']['avg_time_seconds']:.4f} seconds per iteration")
    
    return profiler


def profile_memory_operations():
    """
    Profile memory operations in Left and Right Hemisphere.
    """
    logger.info("\n=== Profiling Memory Operations ===")
    
    # Initialize memory systems
    stm = ShortTermMemory(buffer_size=200)
    ltm = LongTermMemory()
    
    # Create profiler
    profiler = ComponentProfiler(output_dir=os.path.join(parent_dir, "profile_results"))
    
    # Profile STM operations
    logger.info("Profiling STM operations...")
    stm_results = profiler.profile_memory_operations(stm, operation_count=200)
    logger.info(f"STM store operations: {stm_results['store']['profile']['avg_time_seconds']:.4f} seconds")
    logger.info(f"STM search operations: {stm_results['search']['profile']['avg_time_seconds']:.4f} seconds")
    logger.info(f"STM get_all operations: {stm_results['get_all']['profile']['avg_time_seconds']:.4f} seconds")
    
    # Profile LTM operations
    logger.info("Profiling LTM operations...")
    ltm_results = profiler.profile_memory_operations(ltm, operation_count=200)
    logger.info(f"LTM store operations: {ltm_results['store']['profile']['avg_time_seconds']:.4f} seconds")
    logger.info(f"LTM search operations: {ltm_results['search']['profile']['avg_time_seconds']:.4f} seconds")
    logger.info(f"LTM get_all operations: {ltm_results['get_all']['profile']['avg_time_seconds']:.4f} seconds")
    
    # Profile specific memory operations under scale
    logger.info("Profiling memory operations with larger datasets...")
    
    # Generate larger dataset for LTM
    logger.info("Generating 1000 test memories...")
    for i in range(1000):
        ltm.store({
            "id": f"test_mem_{i}",
            "content": f"Test memory {i} with some content for profiling",
            "timestamp": datetime.now().isoformat(),
            "tag": f"tag_{i % 10}"
        })
    
    # Profile memory search with large dataset
    logger.info("Profiling memory search with 1000 memories...")
    search_result = profiler.profile_function(
        lambda: [ltm.search(f"memory {i}") for i in range(100)],
        name="ltm_search_large",
        iterations=5
    )
    logger.info(f"LTM search with large dataset: {search_result['profile']['avg_time_seconds']:.4f} seconds per iteration")
    
    return profiler


def profile_heart_driven_timing():
    """
    Profile heart-driven timing and event routing.
    """
    logger.info("\n=== Profiling Heart-Driven Timing ===")
    
    # Initialize components
    body = Body()
    heart = Heart(body=body)
    
    # Create profiler
    profiler = ComponentProfiler(output_dir=os.path.join(parent_dir, "profile_results"))
    
    # Profile body event routing
    logger.info("Profiling body event routing...")
    
    # Create dummy components that will receive signals
    class DummyComponent:
        def __init__(self, name):
            self.name = name
            self.signals_received = 0
            
        def receive_signal(self, signal):
            self.signals_received += 1
            return True
    
    # Register dummy components
    components = [DummyComponent(f"component_{i}") for i in range(10)]
    for i, comp in enumerate(components):
        body.register_module(comp.name, comp)
    
    # Profile signal routing
    logger.info("Profiling signal routing with 10 components and 1000 signals...")
    routing_result = profiler.profile_function(
        lambda: [body.route_signal("source", f"component_{i % 10}", {"type": "test", "data": f"signal {i}"}) 
                for i in range(1000)],
        name="body_signal_routing",
        iterations=5
    )
    logger.info(f"Body signal routing: {routing_result['profile']['avg_time_seconds']:.4f} seconds per iteration")
    
    # Profile heart pulse generation
    logger.info("Profiling heart pulse generation...")
    
    def heart_beat_cycle():
        heart.start()
        time.sleep(1)  # Allow a few pulses
        heart.stop()
    
    pulse_result = profiler.profile_function(
        heart_beat_cycle,
        name="heart_pulse_generation",
        iterations=3
    )
    logger.info(f"Heart pulse generation: {pulse_result['profile']['elapsed_seconds']:.4f} seconds")
    
    return profiler
    

def main():
    """
    Run comprehensive profiling of BlackwallV2 core algorithms.
    """
    logger.info("Starting BlackwallV2 performance profiling...")
    start_time = time.time()
    
    # Profile each core algorithm
    dream_profiler = profile_memory_consolidation()
    fragment_profiler = profile_fragment_routing()
    memory_profiler = profile_memory_operations()
    heart_profiler = profile_heart_driven_timing()
    
    # Save combined results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dream_profiler.save_results(f"memory_consolidation_profile_{timestamp}.json")
    fragment_profiler.save_results(f"fragment_routing_profile_{timestamp}.json")
    memory_profiler.save_results(f"memory_operations_profile_{timestamp}.json")
    heart_profiler.save_results(f"heart_timing_profile_{timestamp}.json")
    
    # Create combined summary
    summary_file = os.path.join(parent_dir, "profile_results", f"profile_summary_{timestamp}.txt")
    with open(summary_file, 'w') as f:
        f.write("BlackwallV2 Performance Profiling Summary\n")
        f.write("======================================\n\n")
        f.write(f"Profiling completed on: {datetime.now().isoformat()}\n")
        f.write(f"Total profiling time: {time.time() - start_time:.2f} seconds\n\n")
        
        f.write("Key Metrics:\n")
        f.write("1. Memory Consolidation:\n")
        f.write("   - Check detailed results in memory_consolidation_profile_*.json\n\n")
        
        f.write("2. Fragment Routing:\n")
        f.write("   - Check detailed results in fragment_routing_profile_*.json\n\n")
        
        f.write("3. Memory Operations:\n")
        f.write("   - Check detailed results in memory_operations_profile_*.json\n\n")
        
        f.write("4. Heart-Driven Timing:\n")
        f.write("   - Check detailed results in heart_timing_profile_*.json\n\n")
        
        f.write("Next Steps:\n")
        f.write("1. Analyze the profile results to identify bottlenecks\n")
        f.write("2. Prioritize optimization targets based on performance impact\n")
        f.write("3. Implement optimizations for highest-impact components\n")
        f.write("4. Re-profile to verify improvements\n")
    
    logger.info(f"Profiling complete! Results saved to {parent_dir}/profile_results/")
    logger.info(f"Summary available at: {summary_file}")


if __name__ == "__main__":
    main()
