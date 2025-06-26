"""
Performance Profiler for BlackwallV2 Components

This tool provides profiling capabilities for BlackwallV2 components,
helping identify performance bottlenecks and optimization opportunities.
"""

import os
import time
import json
import cProfile
import pstats
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
import sys

# Add parent directory to path so we can import BlackwallV2 components
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import logger
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Profiler")

class ComponentProfiler:
    """Profiles individual BlackwallV2 components for performance optimization."""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the profiler.
        
        Args:
            output_dir: Directory to save profiling results
        """
        if not output_dir:
            output_dir = os.path.join(parent_dir, "profile_results")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.results = {}
        self.current_test = None
        
    def profile_function(self, 
                       func: Callable, 
                       *args, 
                       name: Optional[str] = None, 
                       iterations: int = 1,
                       **kwargs) -> Dict[str, Any]:
        """
        Profile a single function.
        
        Args:
            func: Function to profile
            *args: Function arguments
            name: Name for this profiling run
            iterations: Number of times to run the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Dict with profiling results
        """
        if not name:
            name = func.__name__
            
        # Create profiler
        pr = cProfile.Profile()
        
        # Start timing
        start_time = time.time()
        results = []
        
        # Run the function with profiling
        for i in range(iterations):
            # Start profiling
            pr.enable()
            
            # Run function
            try:
                result = func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in function {name}: {e}")
                results.append(None)
                
            # Stop profiling
            pr.disable()
            
        # Calculate time
        elapsed = time.time() - start_time
        
        # Format profiling statistics
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        
        # Save the results
        profile_data = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": elapsed,
            "iterations": iterations,
            "avg_time_seconds": elapsed / iterations,
            "profile_stats": s.getvalue()
        }
        
        # Save profile data
        self.results[name] = profile_data
        
        # Return the result and profiling data
        return {
            "results": results,
            "profile": profile_data
        }
    
    def profile_dream_cycle(self, dream_manager, memory_count: int = 100) -> Dict[str, Any]:
        """
        Profile a dream cycle operation.
        
        Args:
            dream_manager: DreamManager instance
            memory_count: Number of test memories to generate
            
        Returns:
            Dict with profiling results
        """
        from root.Right_Hemisphere import LongTermMemory
        
        # Create a test LTM instance
        ltm = LongTermMemory()
        
        # Generate test memories
        for i in range(memory_count):
            ltm.store({
                "id": f"mem_{i}",
                "tag": f"tag_{i % 5}",  # Create 5 different tags
                "type": "memory",
                "timestamp": datetime.now().isoformat(),
                "content": f"Test memory {i} with some content for profiling purposes."
            })
        
        # Assign LTM to dream manager
        original_ltm = dream_manager.ltm
        dream_manager.ltm = ltm
        
        # Profile dream cycle
        result = self.profile_function(
            dream_manager.enter_dream_cycle, 
            name="dream_cycle", 
            iterations=1
        )
        
        # Restore original LTM
        dream_manager.ltm = original_ltm
        
        return result
    
    def profile_fragment_analysis(self, fragment_manager, input_count: int = 100) -> Dict[str, Any]:
        """
        Profile fragment analysis operation.
        
        Args:
            fragment_manager: FragmentManager instance
            input_count: Number of test inputs to generate
            
        Returns:
            Dict with profiling results
        """
        test_inputs = [
            "Calculate the derivative of x^2 + 3x + 5",
            "What security measures should I implement for my API?",
            "Let's create something innovative and new",
            "Tell me about the history of quantum physics",
            "I feel sad today and need some encouragement"
        ]
        
        # Profile function that runs fragment analysis multiple times
        def run_fragment_analysis():
            results = []
            for _ in range(input_count):
                input_text = test_inputs[_ % len(test_inputs)]
                result = fragment_manager.analyze_input_for_fragments(input_text)
                results.append(result)
            return results
        
        return self.profile_function(
            run_fragment_analysis,
            name="fragment_analysis",
            iterations=1
        )
    
    def profile_memory_operations(self, memory_instance, operation_count: int = 100) -> Dict[str, Any]:
        """
        Profile memory operations (store, retrieve, search).
        
        Args:
            memory_instance: Memory instance (LTM or STM)
            operation_count: Number of operations to perform
            
        Returns:
            Dict with profiling results
        """
        # Store operations
        store_result = self.profile_function(
            lambda: [memory_instance.store({
                "id": f"prof_mem_{i}",
                "content": f"Profiling memory operation {i}",
                "timestamp": datetime.now().isoformat()
            }) for i in range(operation_count)],
            name=f"{memory_instance.__class__.__name__}_store",
            iterations=1
        )
        
        # Search operations
        search_result = self.profile_function(
            lambda: [memory_instance.search(f"operation {i % 10}") for i in range(operation_count)],
            name=f"{memory_instance.__class__.__name__}_search",
            iterations=1
        )
        
        # Get operations
        get_result = self.profile_function(
            lambda: [memory_instance.get_all() for _ in range(10)],
            name=f"{memory_instance.__class__.__name__}_get_all",
            iterations=1
        )
        
        return {
            "store": store_result,
            "search": search_result,
            "get_all": get_result
        }
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """
        Save profiling results to file.
        
        Args:
            filename: Optional filename
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"profile_results_{timestamp}.json"
            
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert results to serializable format
        serializable_results = {}
        for name, data in self.results.items():
            serializable_results[name] = {
                "name": data["name"],
                "timestamp": data["timestamp"],
                "elapsed_seconds": data["elapsed_seconds"],
                "iterations": data["iterations"],
                "avg_time_seconds": data["avg_time_seconds"]
            }
            # Don't include full profile stats in JSON
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, indent=2)
            logger.info(f"Saved profile results to {filepath}")
            
            # Save detailed stats to a separate file
            stats_file = os.path.join(self.output_dir, f"profile_stats_{timestamp}.txt")
            with open(stats_file, 'w', encoding='utf-8') as f:
                f.write("BlackwallV2 Profiling Results\n")
                f.write("============================\n\n")
                for name, data in self.results.items():
                    f.write(f"Function: {name}\n")
                    f.write(f"Timestamp: {data['timestamp']}\n")
                    f.write(f"Elapsed: {data['elapsed_seconds']:.6f} seconds\n")
                    f.write(f"Iterations: {data['iterations']}\n")
                    f.write(f"Average time: {data['avg_time_seconds']:.6f} seconds\n")
                    f.write("\nProfile Statistics:\n")
                    f.write(data['profile_stats'])
                    f.write("\n" + "="*50 + "\n\n")
                    
            logger.info(f"Saved detailed profile statistics to {stats_file}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving profile results: {e}")
            return ""

# If run directly, show usage
if __name__ == "__main__":
    print("BlackwallV2 Performance Profiler")
    print("===============================")
    print("This module provides profiling tools. Import it from your test scripts.")
    print("\nExample usage:")
    print("  from tools.performance_profiler import ComponentProfiler")
    print("  profiler = ComponentProfiler()")
    print("  profiler.profile_dream_cycle(dream_manager)")
    print("  profiler.save_results()")
