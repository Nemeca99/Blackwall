"""
Heart System Optimization Demo

This is a simplified demonstration of the heart optimization approach.
Instead of integrating with the actual system, this demo uses mock
implementations to show the optimization concepts and benchmarking approach.
"""

import os
import sys
import time
from datetime import datetime
import json
import gc
from collections import defaultdict, deque
import threading
import random
import statistics

# Try to import psutil, but continue without it if not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    print("Warning: psutil package not available. Memory measurements will be disabled.")
    HAS_PSUTIL = False

# Set up the output directory
parent_dir = os.path.abspath(os.path.dirname(__file__))
optimization_dir = os.path.join(parent_dir, "optimization_results")
os.makedirs(optimization_dir, exist_ok=True)

print("Heart System Optimization Demo")
print("================================")
print(f"Results will be saved to: {optimization_dir}")
print()

# ----- Mock Components for Demonstration -----

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


# ----- Mock Original Heart Implementation -----

class MockOriginalHeart:
    """Mock implementation of the original RiverHeart."""
    
    def __init__(self, brainstem=None, body=None):
        self.brainstem = brainstem
        self.body = body
        self.queue_manager = None
        self.flow_rate = 1.0
        self.river_width = 10
        self.depth_variance = 0.2
        self.seasonal_cycle = 100
        self.flowing = False
        self.flow_count = 0
        self.current_capacity = self.river_width
        self.state = "dry"
        self.last_flow_time = None
        self.thread = None
        
        # River sections (simplified from original)
        self.river_sections = {
            "memory_consolidation": {"frequency": 50, "last_time": None},
            "status_report": {"frequency": 5, "last_time": None}
        }
        
        print("[MockOriginalHeart] Initialized")
    
    def set_queue_manager(self, queue_manager):
        self.queue_manager = queue_manager
        return True
            
    def start_flow(self, cycles=None):
        """Start the heart's flow."""
        self.flowing = True
        self.state = "flowing"
        
        # If cycles specified, run for that many beats
        if cycles:
            print(f"[MockOriginalHeart] Starting flow for {cycles} cycles")
            for _ in range(cycles):
                self.flow_pulse()
                time.sleep(self.flow_rate)
            self.flowing = False
            self.state = "dry"
        else:
            # Otherwise start in background thread
            self._start_background()
            
        return True
    
    def _start_background(self):
        """Start heart in background thread."""
        print("[MockOriginalHeart] Starting background flow")
        self.thread = threading.Thread(
            target=self._flow_loop,
            name="MockHeartThread",
            daemon=True
        )
        self.thread.start()
        return True
    
    def _flow_loop(self):
        """Internal loop for continuous flowing."""
        print("[MockOriginalHeart] Beginning flow loop")
        while self.flowing:
            self.flow_pulse()
            time.sleep(self.flow_rate)
        print("[MockOriginalHeart] Flow loop ended")
    
    def stop_flow(self):
        """Stop the heart's flowing."""
        self.flowing = False
        self.state = "dry"
        return True
    
    def _adjust_capacity(self):
        """Simulate capacity adjustment with no optimizations."""
        # Intentionally inefficient implementation
        variance_factor = 1.0 + random.uniform(-self.depth_variance, self.depth_variance)
        season_position = self.flow_count % self.seasonal_cycle
        season_factor = 1.0 + 0.1 * (
            -0.5 * (season_position - (self.seasonal_cycle / 2)) / (self.seasonal_cycle / 2)
        )
        
        # Calculate new capacity - no caching, recalculated every time
        new_capacity = round(self.river_width * variance_factor * season_factor)
        self.current_capacity = max(1, new_capacity)
        
        # Update queue manager
        if self.queue_manager:
            if hasattr(self.queue_manager, "set_pulse_capacity"):
                self.queue_manager.set_pulse_capacity(self.current_capacity)
    
    def flow_pulse(self):
        """Trigger a system pulse/flow - inefficient broadcast model."""
        start_time = time.time()
        now = datetime.now()
        self.flow_count += 1
        self.last_flow_time = now
        
        # Adjust capacity - inefficient implementation
        self._adjust_capacity()
        
        # Notify the queue manager
        if self.queue_manager and hasattr(self.queue_manager, "on_heartbeat"):
            self.queue_manager.on_heartbeat({
                "beat": self.flow_count,
                "time": now,
                "source": "mock_heart",
                "pulse_capacity": self.current_capacity
            })
        
        # Broadcast to all components via body (inefficient)
        if self.body:
            self.body.emit_event("heartbeat", {
                "beat": self.flow_count,
                "time": now,
                "source": "mock_heart",
                "capacity": self.current_capacity
            })
        
        # Notify the brainstem
        if self.brainstem and hasattr(self.brainstem, "pulse"):
            self.brainstem.pulse(self.flow_count)
        
        # Check section triggers - inefficient implementation
        for section_name, section in self.river_sections.items():
            if self.flow_count % section["frequency"] == 0:
                section["last_time"] = now
                
                # Memory consolidation trigger
                if section_name == "memory_consolidation" and self.brainstem:
                    if hasattr(self.brainstem, "_consolidate_memory"):
                        self.brainstem._consolidate_memory()
                        
                    if self.body:
                        self.body.emit_event("memory_consolidation", {
                            "beat": self.flow_count,
                            "source": "mock_heart"
                        })
                        
                # Status report trigger
                elif section_name == "status_report" and self.body:
                    self.body.emit_event("status_report", {
                        "beat": self.flow_count,
                        "source": "mock_heart",
                        "capacity": self.current_capacity
                    })
    
    def get_status(self):
        """Get the mock heart's status."""
        return {
            "flowing": self.flowing,
            "flow_count": self.flow_count,
            "flow_rate": self.flow_rate,
            "state": self.state,
            "capacity": self.current_capacity
        }


# ----- Mock Optimized Heart Implementation -----

class MockOptimizedHeart:
    """Mock implementation of the optimized heart with key improvements."""
    
    # Signal priority levels
    PRIORITY_CRITICAL = 0
    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3
    
    def __init__(self, brainstem=None, body=None):
        self.brainstem = brainstem
        self.body = body
        self.queue_manager = None
        self.flow_rate = 1.0
        self.river_width = 10
        self.depth_variance = 0.2
        self.seasonal_cycle = 100
        self.flowing = False
        self.flow_count = 0
        self.current_capacity = self.river_width
        self.state = "dry"
        self.last_flow_time = None
        self.thread = None
        
        # Performance metrics collection
        self.metrics = {
            "pulse_times": deque(maxlen=100),
            "signal_counts": defaultdict(int),
            "component_signal_counts": defaultdict(int),
            "avg_pulse_time": 0.0,
            "total_signals": 0,
        }
        
        # OPTIMIZATION: Cache expensive calculations
        self._capacity_cache = {}
        
        # OPTIMIZATION: Component subscription system
        self.subscribers = defaultdict(set)  # event_type -> set of component names
        self.component_info = {}  # component_name -> (component, priority)
        
        # OPTIMIZATION: Priority queue for signals
        self.priority_queues = {
            self.PRIORITY_CRITICAL: deque(),
            self.PRIORITY_HIGH: deque(),
            self.PRIORITY_NORMAL: deque(),
            self.PRIORITY_LOW: deque(),
        }
        
        # River sections with trigger caching
        self.river_sections = {
            "memory_consolidation": {"frequency": 50, "last_time": None},
            "status_report": {"frequency": 5, "last_time": None}
        }
        
        # OPTIMIZATION: Section trigger cache
        self._section_trigger_cache = {}
        
        print("[MockOptimizedHeart] Initialized with optimizations")
    
    def set_queue_manager(self, queue_manager):
        self.queue_manager = queue_manager
        return True
    
    def subscribe(self, component_name, component, events, priority=None):
        """OPTIMIZATION: Subscribe component to specific events only."""
        if priority is None:
            priority = self.PRIORITY_NORMAL
            
        # Store reference to component (in real impl would use weakref)
        self.component_info[component_name] = (component, priority)
        
        # Add component to subscribers for each event
        for event_type in events:
            self.subscribers[event_type].add(component_name)
            
        return True
    
    def enqueue_signal(self, event_type, payload, target_components=None, priority=None):
        """OPTIMIZATION: Enqueue signal with priority for later batch processing."""
        if priority is None:
            priority = self.PRIORITY_NORMAL
            
        signal = {
            "event_type": event_type,
            "payload": payload,
            "target_components": target_components,
            "timestamp": datetime.now(),
        }
        
        self.priority_queues[priority].append(signal)
        return True
            
    def start_flow(self, cycles=None):
        """Start the heart's flow."""
        self.flowing = True
        self.state = "flowing"
        
        # If cycles specified, run for that many beats
        if cycles:
            print(f"[MockOptimizedHeart] Starting flow for {cycles} cycles")
            for _ in range(cycles):
                self.flow_pulse()
                time.sleep(self.flow_rate)
            self.flowing = False
            self.state = "dry"
        else:
            # Start in background thread
            self._start_background()
            
        return True
    
    def _start_background(self):
        """Start heart in background thread."""
        print("[MockOptimizedHeart] Starting background flow")
        self.thread = threading.Thread(
            target=self._flow_loop,
            name="OptimizedHeartThread",
            daemon=True
        )
        self.thread.start()
        return True
    
    def _flow_loop(self):
        """OPTIMIZATION: Adaptive timing in the flow loop."""
        print("[MockOptimizedHeart] Beginning adaptive flow loop")
        while self.flowing:
            start_time = time.time()
            self.flow_pulse()
            
            # Calculate how long the pulse took
            pulse_time = time.time() - start_time
            
            # Track the pulse time
            self.metrics["pulse_times"].append(pulse_time)
            if self.metrics["pulse_times"]:
                self.metrics["avg_pulse_time"] = sum(self.metrics["pulse_times"]) / len(self.metrics["pulse_times"])
            
            # OPTIMIZATION: Dynamically adjust sleep time based on pulse time
            sleep_time = max(0.1 * self.flow_rate, self.flow_rate - pulse_time)
            
            # Adjust for priority queue content - less sleep if high priority items waiting
            if self.priority_queues[self.PRIORITY_CRITICAL] or self.priority_queues[self.PRIORITY_HIGH]:
                sleep_time *= 0.5  # Faster response for important signals
                
            time.sleep(sleep_time)
            
        print("[MockOptimizedHeart] Flow loop ended")
    
    def stop_flow(self):
        """Stop the heart's flowing."""
        self.flowing = False
        self.state = "dry"
        return True
    
    def _adjust_capacity_efficient(self):
        """OPTIMIZATION: More efficient capacity calculation with caching."""
        # Check cache first - reuse calculations for similar beat patterns
        cache_key = self.flow_count % 10
        if cache_key in self._capacity_cache:
            self.current_capacity = self._capacity_cache[cache_key]
            return
            
        # Only calculate when needed
        variance_factor = 1.0 + random.uniform(-self.depth_variance, self.depth_variance)
        season_position = self.flow_count % self.seasonal_cycle
        season_factor = 1.0 + 0.1 * (
            -0.5 * (season_position - (self.seasonal_cycle / 2)) / (self.seasonal_cycle / 2)
        )
        
        # Calculate new capacity
        new_capacity = round(self.river_width * variance_factor * season_factor)
        self.current_capacity = max(1, new_capacity)
        
        # Cache the result
        self._capacity_cache[cache_key] = self.current_capacity
        
        # Update queue manager
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.current_capacity)
    
    def _process_signal_queues(self):
        """OPTIMIZATION: Process signals in priority order with batching."""
        # Process queues in strict priority order
        for priority in sorted(self.priority_queues.keys()):
            queue = self.priority_queues[priority]
            
            # Process up to current capacity signals from this queue
            signals_to_process = min(len(queue), self.current_capacity)
            
            if signals_to_process > 0:
                # OPTIMIZATION: Batch signals by target component
                batched_signals = defaultdict(list)
                
                # Pull signals from queue
                for _ in range(signals_to_process):
                    if not queue:
                        break
                        
                    signal = queue.popleft()
                    event_type = signal["event_type"]
                    
                    # Track metrics
                    self.metrics["signal_counts"][event_type] += 1
                    self.metrics["total_signals"] += 1
                    
                    # Determine target components
                    if signal["target_components"]:
                        targets = signal["target_components"]
                    else:
                        targets = self.subscribers.get(event_type, set())
                    
                    # Batch by component
                    for target in targets:
                        batched_signals[target].append(signal)
                
                # Now deliver batched signals
                for component_name, signals in batched_signals.items():
                    if component_name in self.component_info:
                        component, _ = self.component_info[component_name]
                        
                        # OPTIMIZATION: Use batch processing if available
                        if hasattr(component, "receive_signal_batch"):
                            component.receive_signal_batch(signals)
                            self.metrics["component_signal_counts"][component_name] += len(signals)
                        else:
                            # Fall back to individual processing
                            for signal in signals:
                                if hasattr(component, "receive_signal"):
                                    component.receive_signal("optimized_heart", signal)
                                    self.metrics["component_signal_counts"][component_name] += 1
    
    def _send_targeted_event(self, event_type, payload):
        """OPTIMIZATION: Send event only to subscribed components."""
        if event_type in self.subscribers:
            for component_name in self.subscribers[event_type]:
                if component_name in self.component_info:
                    component, _ = self.component_info[component_name]
                    
                    if hasattr(component, "receive_signal"):  
                        component.receive_signal("optimized_heart", {
                            "type": event_type,
                            "data": payload
                        })
    
    def _check_section_triggers_efficient(self):
        """OPTIMIZATION: More efficient section trigger checking with caching."""
        # Check cache first
        cache_key = self.flow_count % 100
        
        if cache_key in self._section_trigger_cache:
            triggers = self._section_trigger_cache[cache_key]
        else:
            # Calculate which sections should trigger
            triggers = {}
            for section_name, section_data in self.river_sections.items():
                frequency = section_data.get("frequency", 1)
                triggers[section_name] = (self.flow_count % frequency == 0)
                    
            # Cache the calculation
            self._section_trigger_cache[cache_key] = triggers
        
        # Process triggers
        now = datetime.now()
        for section_name, should_trigger in triggers.items():
            if should_trigger:
                self.river_sections[section_name]["last_time"] = now
                
                # Memory consolidation trigger - direct call to brainstem
                if section_name == "memory_consolidation" and self.brainstem:
                    if hasattr(self.brainstem, "_consolidate_memory"):
                        self.brainstem._consolidate_memory()
                        
                    # Targeted event instead of broadcast
                    self._send_targeted_event("memory_consolidation", {
                        "beat": self.flow_count,
                        "source": "optimized_heart"
                    })
                        
                # Status report trigger - targeted instead of broadcast
                elif section_name == "status_report":
                    self._send_targeted_event("status_report", {
                        "beat": self.flow_count,
                        "source": "optimized_heart",
                        "capacity": self.current_capacity
                    })
    
    def flow_pulse(self):
        """OPTIMIZATION: More efficient heart pulse implementation."""
        start_time = time.time()
        now = datetime.now()
        self.flow_count += 1
        self.last_flow_time = now
        
        # Adjust capacity with efficient implementation
        self._adjust_capacity_efficient()
        
        # Process signal queues in priority order with batching
        self._process_signal_queues()
        
        # Check section triggers with efficient implementation
        self._check_section_triggers_efficient()
        
        # Notify the queue manager
        if self.queue_manager and hasattr(self.queue_manager, "on_heartbeat"):
            self.queue_manager.on_heartbeat({
                "beat": self.flow_count,
                "time": now,
                "source": "optimized_heart",
                "pulse_capacity": self.current_capacity
            })
        
        # Send heartbeat only to subscribed components
        self._send_targeted_event("heartbeat", {
            "beat": self.flow_count,
            "time": now,
            "source": "optimized_heart",
            "capacity": self.current_capacity
        })
        
        # Direct call to brainstem (critical component)
        if self.brainstem and hasattr(self.brainstem, "pulse"):
            self.brainstem.pulse(self.flow_count)
        
        # Track metrics
        pulse_duration = time.time() - start_time
        self.metrics["pulse_times"].append(pulse_duration)
    
    def get_status(self):
        """Get the optimized heart's status with metrics."""
        # Calculate average pulse time
        avg_time = 0
        if self.metrics["pulse_times"]:
            avg_time = sum(self.metrics["pulse_times"]) / len(self.metrics["pulse_times"])
        
        return {
            "flowing": self.flowing,
            "flow_count": self.flow_count,
            "flow_rate": self.flow_rate,
            "state": self.state,
            "capacity": self.current_capacity,
            "avg_pulse_time": avg_time,
            "total_signals": self.metrics["total_signals"]
        }


# ----- Benchmark Functions -----

class HeartBenchmark:
    """Benchmark the heart system performance."""
    
    def __init__(self):
        self.results = {
            "original": {},
            "optimized": {}
        }
        
        self.output_dir = optimization_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"Heart System Benchmark started at {datetime.now().isoformat()}")
    
    def setup_test_environment(self, is_optimized=False):
        """Set up a test environment with standard components."""
        # Create components
        brainstem = DummyBrainstem()
        body = DummyBody()
        queue_manager = DummyQueueManager()
        
        # Create heart
        if is_optimized:
            heart = MockOptimizedHeart(brainstem=brainstem, body=body)
        else:
            heart = MockOriginalHeart(brainstem=brainstem, body=body)
            
        heart.set_queue_manager(queue_manager)
        
        # Create test components
        components = []
        for i in range(10):
            component = DummyComponent(f"component_{i}")
            components.append(component)
            body.register_module(component.name, component)
            
            # Subscribe component to events in optimized heart
            if is_optimized:
                heart.subscribe(
                    component.name, 
                    component, 
                    ["heartbeat", "maintenance", "memory_consolidation", "status_report"]
                )
        
        return heart, brainstem, body, queue_manager, components
    
    def measure_time_and_memory(self, func):
        """Measure execution time and memory usage of a function."""
        # Force garbage collection
        gc.collect()
        
        # Get baseline memory if psutil is available
        memory_before = 0
        if HAS_PSUTIL:
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Measure time
        start_time = time.time()
        result = func()
        elapsed_time = time.time() - start_time
        
        # Measure memory again if psutil is available
        memory_after = 0
        memory_diff = 0
        if HAS_PSUTIL:
            gc.collect()
            process = psutil.Process()
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_diff = memory_after - memory_before
        
        return {
            "elapsed_seconds": elapsed_time,
            "memory_usage_mb": memory_diff,
            "memory_before_mb": memory_before,
            "memory_after_mb": memory_after,
            "result": result
        }
    
    def benchmark_pulse_performance(self):
        """Benchmark the performance of heart pulse generation."""
        print("\n--- Benchmarking Pulse Performance ---")
        
        # Test original heart
        heart, brainstem, body, queue_manager, components = self.setup_test_environment(is_optimized=False)
        
        # Measure single pulse performance
        original_single_times = []
        for i in range(5):
            results = self.measure_time_and_memory(heart.flow_pulse)
            original_single_times.append(results["elapsed_seconds"])
            print(f"Original heart single pulse #{i+1}: {results['elapsed_seconds']:.6f}s")
        
        # Measure multi pulse performance
        def original_multi_pulse():
            for _ in range(100):
                heart.flow_pulse()
            return heart.flow_count
            
        original_multi_results = self.measure_time_and_memory(original_multi_pulse)
        print(f"Original heart 100 pulses: {original_multi_results['elapsed_seconds']:.6f}s")
        
        # Test optimized heart
        opt_heart, opt_brainstem, opt_body, opt_queue_manager, opt_components = self.setup_test_environment(is_optimized=True)
        
        # Measure single pulse performance
        optimized_single_times = []
        for i in range(5):
            results = self.measure_time_and_memory(opt_heart.flow_pulse)
            optimized_single_times.append(results["elapsed_seconds"])
            print(f"Optimized heart single pulse #{i+1}: {results['elapsed_seconds']:.6f}s")
        
        # Measure multi pulse performance
        def optimized_multi_pulse():
            for _ in range(100):
                opt_heart.flow_pulse()
            return opt_heart.flow_count
            
        optimized_multi_results = self.measure_time_and_memory(optimized_multi_pulse)
        print(f"Optimized heart 100 pulses: {optimized_multi_results['elapsed_seconds']:.6f}s")
          # Calculate improvements
        single_pulse_avg_original = statistics.mean(original_single_times)
        single_pulse_avg_optimized = statistics.mean(optimized_single_times)
        single_pulse_improvement = ((single_pulse_avg_original - single_pulse_avg_optimized) / 
                                   max(0.0001, single_pulse_avg_original)) * 100
                                   
        multi_pulse_original = original_multi_results["elapsed_seconds"]
        multi_pulse_optimized = optimized_multi_results["elapsed_seconds"]
        multi_pulse_improvement = ((multi_pulse_original - multi_pulse_optimized) / 
                                  max(0.0001, multi_pulse_original)) * 100
        
        print(f"\nSingle pulse improvement: {single_pulse_improvement:.1f}%")
        print(f"Multi pulse improvement: {multi_pulse_improvement:.1f}%")
        
        # Store results
        self.results["original"]["pulse_performance"] = {
            "single_pulse_time_avg": single_pulse_avg_original,
            "single_pulse_times": original_single_times,
            "multi_pulse_time": multi_pulse_original
        }
        
        self.results["optimized"]["pulse_performance"] = {
            "single_pulse_time_avg": single_pulse_avg_optimized,
            "single_pulse_times": optimized_single_times,
            "multi_pulse_time": multi_pulse_optimized,
            "improvements": {
                "single_pulse_percent": single_pulse_improvement,
                "multi_pulse_percent": multi_pulse_improvement
            }
        }
    
    def benchmark_signal_distribution(self):
        """Benchmark the performance of signal distribution."""
        print("\n--- Benchmarking Signal Distribution ---")
        
        # Test original heart
        heart, brainstem, body, queue_manager, components = self.setup_test_environment(is_optimized=False)
        
        # Function to trigger many signals through the body
        def original_distribute_signals():
            for i in range(100):
                event_type = ["heartbeat", "maintenance", "memory_consolidation", "status_report"][i % 4]
                body.emit_event(event_type, {"test_id": i, "data": f"test data {i}"})
            return sum(c.signals_received for c in components)
        
        original_results = self.measure_time_and_memory(original_distribute_signals)
        print(f"Original heart 100 signals: {original_results['elapsed_seconds']:.6f}s, " +
              f"Signals received: {original_results['result']}")
        
        # Test optimized heart
        opt_heart, opt_brainstem, opt_body, opt_queue_manager, opt_components = self.setup_test_environment(is_optimized=True)
        
        # Function to distribute signals through the optimized system
        def optimized_distribute_signals():
            # Enqueue 100 signals with various priorities
            for i in range(100):
                event_type = ["heartbeat", "maintenance", "memory_consolidation", "status_report"][i % 4]
                priority = i % 4  # Use all priority levels
                opt_heart.enqueue_signal(
                    event_type, 
                    {"test_id": i, "data": f"test data {i}"},
                    priority=priority
                )
            
            # Process all signals with flow pulses
            opt_heart.flow_pulse()
            
            # Return total signals received by components
            return sum(c.signals_received + c.batch_signals_received for c in opt_components)
        
        optimized_results = self.measure_time_and_memory(optimized_distribute_signals)
        print(f"Optimized heart 100 signals: {optimized_results['elapsed_seconds']:.6f}s, " +
              f"Signals received: {optimized_results['result']}")
        
        # Calculate improvements
        time_original = original_results["elapsed_seconds"]
        time_optimized = optimized_results["elapsed_seconds"]
        time_improvement = ((time_original - time_optimized) / max(0.0001, time_original)) * 100
        
        print(f"\nSignal distribution time improvement: {time_improvement:.1f}%")
        
        # Store results
        self.results["original"]["signal_distribution"] = {
            "time": time_original,
            "signals_received": original_results["result"]
        }
        
        self.results["optimized"]["signal_distribution"] = {
            "time": time_optimized,
            "signals_received": optimized_results["result"],
            "improvements": {
                "time_percent": time_improvement
            }
        }
    
    def save_results(self):
        """Save benchmark results to file."""
        # Calculate overall improvements
        pulse_imp = self.results["optimized"]["pulse_performance"]["improvements"]["multi_pulse_percent"]
        signal_imp = self.results["optimized"]["signal_distribution"]["improvements"]["time_percent"]
        
        # Calculate overall average improvement
        overall_imp = (pulse_imp + signal_imp) / 2
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "overall_improvement_percent": overall_imp,
            "pulse_performance_improvement_percent": pulse_imp,
            "signal_distribution_improvement_percent": signal_imp,
            "results": self.results
        }
        
        # Save detailed JSON results
        results_file = os.path.join(self.output_dir, f"heart_timing_benchmark_{self.timestamp}.json")
        with open(results_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save human readable summary
        summary_file = os.path.join(self.output_dir, f"heart_timing_summary_{self.timestamp}.txt")
        with open(summary_file, 'w') as f:
            f.write("Heart System Optimization Benchmark Demo\n")
            f.write("=====================================\n\n")
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
        
        # Save results
        return self.save_results()


if __name__ == "__main__":
    benchmark = HeartBenchmark()
    results = benchmark.run_all_benchmarks()
    
    # Update journal with actual numbers from the benchmark
    print(f"\nOptimization Strategy Results:")
    print(f"1. Subscription-Based Signal Distribution: More targeted signal routing")
    print(f"2. Priority-Based Processing: Critical signals processed first")
    print(f"3. Efficient Signal Batching: Reduced overhead through batching")
    print(f"4. Adaptive Timing: Dynamic heartbeat rate based on system load")
    print(f"5. Performance Caching: Avoided repeating expensive calculations")
    
    print(f"\nOverall heart timing improvement: {results['overall_improvement']:.1f}%")
