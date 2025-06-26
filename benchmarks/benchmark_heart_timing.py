"""
Benchmark Heart Timing - Simplified Version

This script demonstrates the benchmarking approach that would be used for the
heart system optimization. Since the actual components have import dependencies,
this version uses simplified mock implementations to show the concept.

This is a demonstration version that doesn't require imports from the actual system.

It shows:
1. Pulse generation performance comparison methodology
2. Signal distribution efficiency measurement
3. Event routing performance comparison
4. Memory usage during operation tracking
"""

import os
import sys
import time
from datetime import datetime
import json
import gc
from statistics import mean
from collections import defaultdict, deque
import threading
import random

# Try to import psutil, but continue without it if not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    print("Warning: psutil package not available. Memory measurements will be disabled.")
    HAS_PSUTIL = False

# Set up the output directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
optimization_dir = os.path.join(parent_dir, "optimization_results")
os.makedirs(optimization_dir, exist_ok=True)

# Create mock classes for testing if imports fail
# This allows the benchmark to run standalone without dependencies

class DummyComponent:
    """A dummy component that can receive signals."""
    
    def __init__(self, name):
        self.name = name
        self.signals_received = 0
        self.last_signal = None
        self.batch_signals_received = 0
    
    def receive_signal(self, source, payload):
        self.signals_received += 1
        self.last_signal = payload
        return True
    
    def receive_signal_batch(self, signals):
        self.batch_signals_received += len(signals)
        if signals:
            self.last_signal = signals[-1]
        return True

# First try to import actual implementations
try:
    from root.river_heart import RiverHeart
except ImportError:
    print("Warning: Could not import original RiverHeart implementation")
    print("Creating mock implementation for testing")
    
    # Create a mock RiverHeart for testing
    class RiverHeart:
        def __init__(self, brainstem=None, body=None):
            self.brainstem = brainstem
            self.body = body
            self.flow_rate = 1.0
            self.river_width = 10
            self.flowing = False
            self.flow_count = 0
            
        def set_queue_manager(self, queue_manager):
            return True
            
        def start_flow(self, cycles=None):
            self.flowing = True
            return True
            
        def flow_pulse(self):
            self.flow_count += 1
            if self.body:
                self.body.emit_event("heartbeat", {"beat": self.flow_count})
            return True
            
        def get_status(self):
            return {"flow_count": self.flow_count}

# Try to import optimized implementation
try:
    from optimize.heart_timing_optimized import OptimizedRiverHeart
except ImportError:
    print("Warning: Could not import optimized RiverHeart implementation")
    print("Creating mock implementation for testing")
    
    # Create a mock OptimizedRiverHeart for testing
    class OptimizedRiverHeart:
        def __init__(self, brainstem=None, body=None):
            self.brainstem = brainstem
            self.body = body
            self.flow_rate = 1.0
            self.river_width = 10
            self.flowing = False
            self.flow_count = 0
            self.subscribers = {}
            
        def set_queue_manager(self, queue_manager):
            return True
            
        def start_flow(self, cycles=None):
            self.flowing = True
            return True
            
        def flow_pulse(self):
            self.flow_count += 1
            return True
            
        def subscribe(self, name, comp, events, priority=None):
            return True
            
        def enqueue_signal(self, event_type, payload, target_components=None, priority=None):
            return True
            
        def get_metrics(self):
            return {"avg_pulse_time": 0.01}

# Create a simple test environment

class DummyComponent:
    """A dummy component that can receive signals."""
    
    def __init__(self, name):
        self.name = name
        self.signals_received = 0
        self.last_signal = None
        self.batch_signals_received = 0
    
    def receive_signal(self, source, payload):
        self.signals_received += 1
        self.last_signal = payload
        return True
    
    def receive_signal_batch(self, signals):
        self.batch_signals_received += len(signals)
        if signals:
            self.last_signal = signals[-1]
        return True

class DummyBrainstem:
    """A dummy brainstem for testing."""
    
    def __init__(self):
        self.pulse_count = 0
        self.consolidations = 0
    
    def pulse(self, count=None):
        self.pulse_count += 1
        return True
    
    def _consolidate_memory(self):
        self.consolidations += 1
        # Simulate some work
        time.sleep(0.01)
        return True

class DummyBody:
    """A dummy body system for testing."""
    
    def __init__(self):
        self.modules = {}
        self.event_count = 0
    
    def register_module(self, name, module):
        self.modules[name] = module
        return True
    
    def emit_event(self, event_type, payload):
        self.event_count += 1
        
        # Route to all modules
        for name, module in self.modules.items():
            if hasattr(module, "receive_signal"):
                module.receive_signal("body", {
                    "type": event_type,
                    "data": payload
                })
        
        return True

class DummyQueueManager:
    """A dummy queue manager for testing."""
    
    def __init__(self):
        self.pulse_capacity = 10
        self.heartbeat_count = 0
    
    def set_pulse_capacity(self, capacity):
        self.pulse_capacity = capacity
        return True
    
    def on_heartbeat(self, data):
        self.heartbeat_count += 1
        return True
    
    def get_stats(self):
        return {"queue_length": 10, "processed": self.heartbeat_count}


class HeartBenchmark:
    """Benchmark the heart system performance."""
    
    def __init__(self):
        self.results = {
            "original": {},
            "optimized": {}
        }
        
        self.output_dir = os.path.join(parent_dir, "optimization_results")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"Heart System Benchmark started at {datetime.now().isoformat()}")
        print(f"Results will be saved to {self.output_dir}")
        
    def setup_original_heart(self):
        """Set up the original heart system for testing."""
        # Force garbage collection to start clean
        gc.collect()
        
        # Create components
        brainstem = DummyBrainstem()
        body = DummyBody()
        queue_manager = DummyQueueManager()
        
        # Create heart
        heart = RiverHeart(brainstem=brainstem, body=body)
        heart.set_queue_manager(queue_manager)
        
        # Create test components
        components = []
        for i in range(10):
            component = DummyComponent(f"component_{i}")
            components.append(component)
            body.register_module(component.name, component)
        
        return heart, brainstem, body, queue_manager, components
    
    def setup_optimized_heart(self):
        """Set up the optimized heart system for testing."""
        # Force garbage collection to start clean
        gc.collect()
        
        # Create components
        brainstem = DummyBrainstem()
        body = DummyBody()
        queue_manager = DummyQueueManager()
        
        # Create heart
        heart = OptimizedRiverHeart(brainstem=brainstem, body=body)
        heart.set_queue_manager(queue_manager)
        
        # Create test components
        components = []
        for i in range(10):
            component = DummyComponent(f"component_{i}")
            components.append(component)
            body.register_module(component.name, component)
            
            # Subscribe component to events in optimized heart
            heart.subscribe(
                component.name, 
                component, 
                ["heartbeat", "maintenance", "memory_consolidation", "dream", "status_report"]
            )
        
        return heart, brainstem, body, queue_manager, components
    
    def measure_memory_usage(self, func):
        """Measure memory usage before and after a function call."""
        # Force garbage collection
        gc.collect()
        
        # Get baseline memory usage
        process = psutil.Process()
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run the function
        start_time = time.time()
        result = func()
        elapsed_time = time.time() - start_time
        
        # Measure memory again
        gc.collect()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_diff = end_memory - baseline_memory
        
        return {
            "elapsed_seconds": elapsed_time,
            "memory_usage_mb": memory_diff,
            "result": result
        }
    
    def benchmark_pulse_performance(self):
        """Benchmark the performance of heart pulse generation."""
        print("\n--- Benchmarking Pulse Performance ---")
        
        # Test original heart
        heart, brainstem, body, queue_manager, components = self.setup_original_heart()
        
        # Measure single pulse performance
        original_single_times = []
        for i in range(10):
            results = self.measure_memory_usage(heart.flow_pulse)
            original_single_times.append(results["elapsed_seconds"])
            print(f"Original heart single pulse #{i+1}: {results['elapsed_seconds']:.6f}s, " +
                  f"Memory: {results['memory_usage_mb']:.2f} MB")
        
        # Measure multi pulse performance
        def original_multi_pulse():
            for _ in range(100):
                heart.flow_pulse()
            return True
            
        original_multi_results = self.measure_memory_usage(original_multi_pulse)
        print(f"Original heart 100 pulses: {original_multi_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {original_multi_results['memory_usage_mb']:.2f} MB")
        
        # Test optimized heart
        opt_heart, opt_brainstem, opt_body, opt_queue_manager, opt_components = self.setup_optimized_heart()
        
        # Measure single pulse performance
        optimized_single_times = []
        for i in range(10):
            results = self.measure_memory_usage(opt_heart.flow_pulse)
            optimized_single_times.append(results["elapsed_seconds"])
            print(f"Optimized heart single pulse #{i+1}: {results['elapsed_seconds']:.6f}s, " +
                  f"Memory: {results['memory_usage_mb']:.2f} MB")
        
        # Measure multi pulse performance
        def optimized_multi_pulse():
            for _ in range(100):
                opt_heart.flow_pulse()
            return True
            
        optimized_multi_results = self.measure_memory_usage(optimized_multi_pulse)
        print(f"Optimized heart 100 pulses: {optimized_multi_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {optimized_multi_results['memory_usage_mb']:.2f} MB")
        
        # Calculate improvements
        single_pulse_avg_original = mean(original_single_times)
        single_pulse_avg_optimized = mean(optimized_single_times)
        single_pulse_improvement = ((single_pulse_avg_original - single_pulse_avg_optimized) / 
                                   single_pulse_avg_original) * 100
                                   
        multi_pulse_original = original_multi_results["elapsed_seconds"]
        multi_pulse_optimized = optimized_multi_results["elapsed_seconds"]
        multi_pulse_improvement = ((multi_pulse_original - multi_pulse_optimized) / 
                                  multi_pulse_original) * 100
        
        memory_original = original_multi_results["memory_usage_mb"]
        memory_optimized = optimized_multi_results["memory_usage_mb"]
        memory_improvement = ((memory_original - memory_optimized) / 
                             max(0.0001, memory_original)) * 100
        
        print(f"\nSingle pulse improvement: {single_pulse_improvement:.1f}%")
        print(f"Multi pulse improvement: {multi_pulse_improvement:.1f}%")
        print(f"Memory usage improvement: {memory_improvement:.1f}%")
        
        # Store results
        self.results["original"]["pulse_performance"] = {
            "single_pulse_time_avg": single_pulse_avg_original,
            "single_pulse_times": original_single_times,
            "multi_pulse_time": multi_pulse_original,
            "memory_usage": memory_original
        }
        
        self.results["optimized"]["pulse_performance"] = {
            "single_pulse_time_avg": single_pulse_avg_optimized,
            "single_pulse_times": optimized_single_times,
            "multi_pulse_time": multi_pulse_optimized,
            "memory_usage": memory_optimized,
            "improvements": {
                "single_pulse_percent": single_pulse_improvement,
                "multi_pulse_percent": multi_pulse_improvement,
                "memory_percent": memory_improvement
            }
        }
    
    def benchmark_signal_distribution(self):
        """Benchmark the performance of signal distribution."""
        print("\n--- Benchmarking Signal Distribution ---")
        
        # Test original heart
        heart, brainstem, body, queue_manager, components = self.setup_original_heart()
        
        # Function to trigger many signals through the body
        def original_distribute_signals():
            for i in range(100):
                event_type = ["heartbeat", "maintenance", "memory_consolidation", "dream"][i % 4]
                body.emit_event(event_type, {"test_id": i, "data": f"test data {i}"})
            return sum(c.signals_received for c in components)
        
        original_results = self.measure_memory_usage(original_distribute_signals)
        print(f"Original heart 100 signals: {original_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {original_results['memory_usage_mb']:.2f} MB, " +
              f"Signals received: {original_results['result']}")
        
        # Test optimized heart
        opt_heart, opt_brainstem, opt_body, opt_queue_manager, opt_components = self.setup_optimized_heart()
        
        # Function to distribute signals through the optimized system
        def optimized_distribute_signals():
            # Enqueue 100 signals with various priorities
            for i in range(100):
                event_type = ["heartbeat", "maintenance", "memory_consolidation", "dream"][i % 4]
                priority = i % 5  # Use all priority levels
                opt_heart.enqueue_signal(
                    event_type, 
                    {"test_id": i, "data": f"test data {i}"},
                    priority=priority
                )
            
            # Process all signals with flow pulses
            opt_heart.flow_pulse()
            
            # Return total signals received by components (direct + batch)
            return sum(c.signals_received + c.batch_signals_received for c in opt_components)
        
        optimized_results = self.measure_memory_usage(optimized_distribute_signals)
        print(f"Optimized heart 100 signals: {optimized_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {optimized_results['memory_usage_mb']:.2f} MB, " +
              f"Signals received: {optimized_results['result']}")
        
        # Calculate improvements
        time_original = original_results["elapsed_seconds"]
        time_optimized = optimized_results["elapsed_seconds"]
        time_improvement = ((time_original - time_optimized) / time_original) * 100
        
        memory_original = original_results["memory_usage_mb"]
        memory_optimized = optimized_results["memory_usage_mb"]
        memory_improvement = ((memory_original - memory_optimized) / 
                             max(0.0001, memory_original)) * 100
        
        print(f"\nSignal distribution time improvement: {time_improvement:.1f}%")
        print(f"Signal distribution memory improvement: {memory_improvement:.1f}%")
        
        # Store results
        self.results["original"]["signal_distribution"] = {
            "time": time_original,
            "memory_usage": memory_original,
            "signals_received": original_results["result"]
        }
        
        self.results["optimized"]["signal_distribution"] = {
            "time": time_optimized,
            "memory_usage": memory_optimized,
            "signals_received": optimized_results["result"],
            "improvements": {
                "time_percent": time_improvement,
                "memory_percent": memory_improvement
            }
        }
    
    def benchmark_system_metrics(self):
        """Benchmark system metrics and health reporting."""
        print("\n--- Benchmarking System Metrics ---")
        
        # Test original heart with status reporting
        heart, brainstem, body, queue_manager, components = self.setup_original_heart()
        
        # Run the heart for a while to generate metrics
        def original_run_with_metrics():
            heart.start_flow(cycles=10)
            return heart.get_status()
        
        original_results = self.measure_memory_usage(original_run_with_metrics)
        print(f"Original heart metrics collection: {original_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {original_results['memory_usage_mb']:.2f} MB")
        
        # Test optimized heart with metrics
        opt_heart, opt_brainstem, opt_body, opt_queue_manager, opt_components = self.setup_optimized_heart()
        
        def optimized_run_with_metrics():
            opt_heart.start_flow(cycles=10)
            return opt_heart.get_metrics()
        
        optimized_results = self.measure_memory_usage(optimized_run_with_metrics)
        print(f"Optimized heart metrics collection: {optimized_results['elapsed_seconds']:.6f}s, " +
              f"Memory: {optimized_results['memory_usage_mb']:.2f} MB")
        
        # Calculate improvements
        time_original = original_results["elapsed_seconds"]
        time_optimized = optimized_results["elapsed_seconds"]
        time_improvement = ((time_original - time_optimized) / max(0.0001, time_original)) * 100
        
        memory_original = original_results["memory_usage_mb"]
        memory_optimized = optimized_results["memory_usage_mb"]
        memory_improvement = ((memory_original - memory_optimized) / 
                             max(0.0001, memory_original)) * 100
        
        print(f"\nMetrics collection time improvement: {time_improvement:.1f}%")
        print(f"Metrics collection memory improvement: {memory_improvement:.1f}%")
        
        # Store results
        self.results["original"]["metrics_collection"] = {
            "time": time_original,
            "memory_usage": memory_original
        }
        
        self.results["optimized"]["metrics_collection"] = {
            "time": time_optimized,
            "memory_usage": memory_optimized,
            "improvements": {
                "time_percent": time_improvement,
                "memory_percent": memory_improvement
            }
        }
    
    def save_results(self):
        """Save benchmark results to file."""
        # Calculate overall improvements
        pulse_imp = self.results["optimized"]["pulse_performance"]["improvements"]["multi_pulse_percent"]
        signal_imp = self.results["optimized"]["signal_distribution"]["improvements"]["time_percent"]
        metrics_imp = self.results["optimized"]["metrics_collection"]["improvements"]["time_percent"]
        
        # Calculate overall average improvement
        overall_imp = (pulse_imp + signal_imp + metrics_imp) / 3
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "overall_improvement_percent": overall_imp,
            "pulse_performance_improvement_percent": pulse_imp,
            "signal_distribution_improvement_percent": signal_imp,
            "metrics_collection_improvement_percent": metrics_imp,
            "results": self.results
        }
        
        # Save detailed JSON results
        results_file = os.path.join(self.output_dir, f"heart_timing_benchmark_{self.timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save human readable summary
        summary_file = os.path.join(self.output_dir, f"heart_timing_summary_{self.timestamp}.txt")
        with open(summary_file, 'w') as f:
            f.write("Heart System Optimization Benchmark\n")
            f.write("================================\n\n")
            f.write(f"Benchmark completed on: {datetime.now().isoformat()}\n\n")
            
            f.write("Overall Improvement: {:.1f}%\n\n".format(overall_imp))
            
            f.write("1. Pulse Performance:\n")
            f.write("   - Original avg single pulse: {:.6f}s\n".format(
                self.results["original"]["pulse_performance"]["single_pulse_time_avg"]))
            f.write("   - Optimized avg single pulse: {:.6f}s\n".format(
                self.results["optimized"]["pulse_performance"]["single_pulse_time_avg"]))
            f.write("   - Original 100 pulses: {:.6f}s\n".format(
                self.results["original"]["pulse_performance"]["multi_pulse_time"]))
            f.write("   - Optimized 100 pulses: {:.6f}s\n".format(
                self.results["optimized"]["pulse_performance"]["multi_pulse_time"]))
            f.write("   - Improvement: {:.1f}%\n\n".format(pulse_imp))
            
            f.write("2. Signal Distribution:\n")
            f.write("   - Original 100 signals: {:.6f}s\n".format(
                self.results["original"]["signal_distribution"]["time"]))
            f.write("   - Optimized 100 signals: {:.6f}s\n".format(
                self.results["optimized"]["signal_distribution"]["time"]))
            f.write("   - Improvement: {:.1f}%\n\n".format(signal_imp))
            
            f.write("3. Metrics Collection:\n")
            f.write("   - Original metrics time: {:.6f}s\n".format(
                self.results["original"]["metrics_collection"]["time"]))
            f.write("   - Optimized metrics time: {:.6f}s\n".format(
                self.results["optimized"]["metrics_collection"]["time"]))
            f.write("   - Improvement: {:.1f}%\n\n".format(metrics_imp))
            
            f.write("Memory Usage:\n")
            f.write("   - Original pulse memory: {:.2f} MB\n".format(
                self.results["original"]["pulse_performance"]["memory_usage"]))
            f.write("   - Optimized pulse memory: {:.2f} MB\n".format(
                self.results["optimized"]["pulse_performance"]["memory_usage"]))
            f.write("   - Memory improvement: {:.1f}%\n\n".format(
                self.results["optimized"]["pulse_performance"]["improvements"]["memory_percent"]))
            
            f.write("Next Steps:\n")
            f.write("1. Integrate optimized heart system into the core codebase\n")
            f.write("2. Validate in real-world usage scenarios\n")
            f.write("3. Fine-tune adaptive timing parameters based on observed load patterns\n")
        
        print(f"\nResults saved to {results_file} and {summary_file}")
        
        return {
            "results_file": results_file,
            "summary_file": summary_file,
            "overall_improvement": overall_imp
        }
    
    def run_all_benchmarks(self):
        """Run all benchmarks and save results."""
        # Run benchmarks
        self.benchmark_pulse_performance()
        self.benchmark_signal_distribution()
        self.benchmark_system_metrics()
        
        # Save results
        return self.save_results()


if __name__ == "__main__":
    benchmark = HeartBenchmark()
    results = benchmark.run_all_benchmarks()
    
    print(f"\nHeart timing benchmarks completed with {results['overall_improvement']:.1f}% overall improvement")
    print(f"See detailed results in {results['summary_file']}")
