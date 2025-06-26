"""
Optimized River Heart

An enhanced and optimized heart system that implements the "lazy river" concept for controlling
information flow through the BlackwallV2 system with improved performance.

Optimization features:
1. Targeted signal distribution instead of broadcasting
2. Component subscription system for heartbeat events
3. Signal batching for improved throughput
4. Adaptive timing based on system load
5. Priority-based pulse channels
6. Performance monitoring and metrics
"""

import time
import threading
import random
from datetime import datetime
from collections import defaultdict, deque
import weakref


class OptimizedRiverHeart:
    """
    The OptimizedRiverHeart implements the lazy river concept with performance enhancements.
    
    Key optimizations:
    - Subscription-based signals instead of broadcasting
    - Efficient signal batching
    - Adaptive timing based on system load
    - Priority-based pulse channels
    - Performance metrics collection
    """
    
    # Signal priority levels
    PRIORITY_CRITICAL = 0
    PRIORITY_HIGH = 1
    PRIORITY_NORMAL = 2
    PRIORITY_LOW = 3
    PRIORITY_BACKGROUND = 4
    
    def __init__(self, brainstem=None, body=None, queue_manager=None):
        """Initialize optimized river heart with references to other system components."""
        self.brainstem = brainstem
        self.body = body
        self.queue_manager = queue_manager
        
        # Flow control parameters
        self.flow_rate = 1.0  # Default: 1 beat per second
        self.river_width = 10  # Default: 10 items per beat
        self.depth_variance = 0.2  # Allow natural variance of ±20% in capacity
        self.seasonal_cycle = 100  # Beats per full seasonal cycle
        
        # System state
        self.flowing = False
        self.flow_count = 0
        self.last_flow_time = None
        self.thread = None
        self.state = "dry"  # dry, flowing, flooding, drought
        
        # Current processing capacity (adjusted each beat)
        self.current_capacity = self.river_width
        
        # Performance metrics
        self.metrics = {
            "pulse_times": deque(maxlen=100),  # Keep last 100 pulse times
            "signal_counts": defaultdict(int),  # Count by signal type
            "component_signal_counts": defaultdict(int),  # Count by component
            "avg_pulse_time": 0.0,
            "max_pulse_time": 0.0,
            "total_signals": 0,
        }
        
        # Cache results of expensive operations
        self._capacity_cache = {}  # Cache capacity calculations
        
        # Signal subscription system - components subscribe to specific events
        self.subscribers = defaultdict(set)  # event_type -> set of component names
        self.component_info = {}  # component_name -> (component_ref, priority)
        
        # Priority queues for signals - deques are more efficient than regular lists for queue operations
        self.priority_queues = {
            self.PRIORITY_CRITICAL: deque(),
            self.PRIORITY_HIGH: deque(),
            self.PRIORITY_NORMAL: deque(),
            self.PRIORITY_LOW: deque(),
            self.PRIORITY_BACKGROUND: deque(),
        }
        
        # River sections (like heart cycles but more nature-inspired)
        self.river_sections = {
            "shoreline_maintenance": {  # System maintenance
                "frequency": 10,  # Every 10 beats
                "last_time": None
            },
            "underwater_currents": {  # Memory consolidation
                "frequency": 50,
                "last_time": None
            },
            "deep_pools": {  # Dream cycles
                "frequency": 100,
                "last_time": None
            },
            "river_health": {  # Status reports
                "frequency": 5,
                "last_time": None
            },
            "flow_monitoring": {  # Queue statistics
                "frequency": 20,
                "last_time": None
            },
            "rapids": {  # Periods of faster processing for emergent needs
                "frequency": 33,
                "duration": 3,  # Lasts for 3 beats
                "active": False,
                "last_time": None
            },
            "gentle_pools": {  # Periods of deeper reflection and integration
                "frequency": 75,
                "duration": 5,  # Lasts for 5 beats
                "active": False,
                "last_time": None
            }
        }
        
        # Section trigger cache - avoid recalculating triggers for each beat
        self._section_trigger_cache = {}  # beat_count -> {section_name: should_trigger}
        
        print("[OptimizedRiverHeart] Initialized with flow rate:", self.flow_rate, 
              "and river width:", self.river_width)
    
    def register_with_body(self, body):
        """Register this heart with a body system."""
        self.body = body
        if self.body:
            self.body.register_module("river_heart", self)
            print("[OptimizedRiverHeart] Registered with body system")
            return True
        return False
    
    def set_queue_manager(self, queue_manager):
        """Connect the heart to a queue manager for information flow control."""
        self.queue_manager = queue_manager
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.river_width)
            print("[OptimizedRiverHeart] Connected to queue manager")
            return True
        return False
    
    def set_river_width(self, width):
        """Set the river's width (items processed per beat)."""
        self.river_width = max(1, width)  # Ensure at least 1
        self.current_capacity = self.river_width  # Reset current capacity
        
        # Clear capacity cache as it's now invalid
        self._capacity_cache.clear()
        
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.river_width)
        print(f"[OptimizedRiverHeart] River width set to {self.river_width}")
        return True
    
    def start_flow(self, cycles=None):
        """Start the heart's flow."""
        if self.flowing:
            print("[OptimizedRiverHeart] Already flowing.")
            return False
        
        self.flowing = True
        self.state = "flowing"
        
        # If cycles specified, run for that many beats
        if cycles:
            self._run_for_cycles(cycles)
        else:
            # Otherwise start in background thread
            self._start_background()
            
        return True
    
    def _run_for_cycles(self, cycles):
        """Run the heart for a specified number of cycles."""
        print(f"[OptimizedRiverHeart] Starting flow for {cycles} cycles")
        for _ in range(cycles):
            self.flow_pulse()
            time.sleep(self.flow_rate)
        self.flowing = False
        self.state = "dry"
        print("[OptimizedRiverHeart] Completed cycle run")
    
    def _start_background(self):
        """Start heart in background thread."""
        if self.thread and self.thread.is_alive():
            print("[OptimizedRiverHeart] Background flow already running")
            return False
        
        print("[OptimizedRiverHeart] Starting background flow")
        self.thread = threading.Thread(
            target=self._flow_loop,
            name="OptimizedRiverHeartThread",
            daemon=True  # Allow program to exit even if thread is running
        )
        self.thread.start()
        return True
    
    def _flow_loop(self):
        """Internal loop for continuous flowing with adaptive timing."""
        print("[OptimizedRiverHeart] Beginning flow loop")
        while self.flowing:
            start_time = time.time()
            self.flow_pulse()
            
            # Calculate how long the pulse took
            pulse_time = time.time() - start_time
            
            # Track the pulse time
            self.metrics["pulse_times"].append(pulse_time)
            self.metrics["avg_pulse_time"] = sum(self.metrics["pulse_times"]) / len(self.metrics["pulse_times"])
            self.metrics["max_pulse_time"] = max(self.metrics["pulse_times"])
            
            # Dynamically adjust sleep time based on pulse processing time
            # Don't sleep less than 10% of the intended rate to prevent overloading
            sleep_time = max(0.1 * self.flow_rate, self.flow_rate - pulse_time)
            
            # Adjust for priority queue content - less sleep if high priority items waiting
            if self.priority_queues[self.PRIORITY_CRITICAL] or self.priority_queues[self.PRIORITY_HIGH]:
                sleep_time *= 0.5  # Reduce sleep time for faster processing of important signals
                
            time.sleep(sleep_time)
            
        print("[OptimizedRiverHeart] Flow loop ended")
    
    def stop_flow(self):
        """Stop the heart's flowing."""
        if not self.flowing:
            print("[OptimizedRiverHeart] Already dry")
            return True
            
        print("[OptimizedRiverHeart] Drying up...")
        self.flowing = False
        self.state = "drying"
        
        # Wait for thread to end if it exists
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)  # Wait up to 2 seconds
            if self.thread.is_alive():
                print("[OptimizedRiverHeart] Warning: Flow thread didn't stop cleanly")
            
        self.state = "dry"
        print("[OptimizedRiverHeart] Stopped")
        return True
    
    def set_flow_rate(self, rate):
        """Set the flow rate in seconds between beats."""
        if rate <= 0:
            print("[OptimizedRiverHeart] Error: Rate must be positive")
            return False
            
        self.flow_rate = rate
        print(f"[OptimizedRiverHeart] Flow rate set to {rate} seconds")
        return True
    
    def _adjust_capacity_for_natural_variance(self):
        """Apply natural variance to processing capacity to simulate river depth changes."""
        # Check if we have a recent cached calculation for the current beat
        cache_key = self.flow_count % 10  # Reuse calculations every 10 beats
        if cache_key in self._capacity_cache:
            self.current_capacity = self._capacity_cache[cache_key]
            return
            
        # Calculate a variance factor between (1-depth_variance) and (1+depth_variance)
        variance_factor = 1.0 + random.uniform(-self.depth_variance, self.depth_variance)
        
        # Apply seasonal effect (sinusoidal pattern over the seasonal cycle)
        season_position = self.flow_count % self.seasonal_cycle
        season_factor = 1.0 + 0.1 * (
            -0.5 * (season_position - (self.seasonal_cycle / 2)) / (self.seasonal_cycle / 2)
        )
        
        # Check for special river sections that affect capacity
        rapids_active = self.river_sections["rapids"]["active"]
        pools_active = self.river_sections["gentle_pools"]["active"]
        
        # Apply modifiers
        capacity_modifier = variance_factor * season_factor
        if rapids_active:
            capacity_modifier *= 1.5  # 50% more capacity during rapids
        if pools_active:
            capacity_modifier *= 0.7  # 30% less capacity during gentle pools (deeper reflection)
            
        # Calculate new capacity
        new_capacity = round(self.river_width * capacity_modifier)
        self.current_capacity = max(1, new_capacity)  # Ensure at least 1
        
        # Cache the calculation
        self._capacity_cache[cache_key] = self.current_capacity
        
        # Update queue manager with new capacity
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.current_capacity)
    
    def subscribe(self, component_name, component_ref, event_types, priority=None):
        """
        Subscribe a component to specific event types with a given priority.
        
        Args:
            component_name: The name of the component
            component_ref: Reference to the component object
            event_types: List of event types to subscribe to
            priority: Priority level (default: PRIORITY_NORMAL)
        """
        if priority is None:
            priority = self.PRIORITY_NORMAL
            
        # Store weak reference to avoid reference cycles
        self.component_info[component_name] = (weakref.ref(component_ref), priority)
        
        # Add component to subscribers for each event type
        for event_type in event_types:
            self.subscribers[event_type].add(component_name)
            
        return True
    
    def unsubscribe(self, component_name, event_types=None):
        """
        Unsubscribe a component from event types.
        
        Args:
            component_name: The name of the component
            event_types: List of event types to unsubscribe from (None = all)
        """
        # Remove from all event types if None specified
        if event_types is None:
            for subscribers in self.subscribers.values():
                subscribers.discard(component_name)
            
            # Remove component info
            if component_name in self.component_info:
                del self.component_info[component_name]
        else:
            # Remove from specified event types
            for event_type in event_types:
                if event_type in self.subscribers:
                    self.subscribers[event_type].discard(component_name)
                    
        return True
    
    def enqueue_signal(self, event_type, payload, target_components=None, priority=None):
        """
        Enqueue a signal for processing during the next pulse.
        
        Args:
            event_type: Type of the event
            payload: Event data
            target_components: Specific components to send to (default: use subscribers)
            priority: Priority level (default: PRIORITY_NORMAL)
        """
        if priority is None:
            priority = self.PRIORITY_NORMAL
            
        # Create signal object
        signal = {
            "event_type": event_type,
            "payload": payload,
            "target_components": target_components,
            "timestamp": datetime.now(),
        }
        
        # Add to appropriate priority queue
        self.priority_queues[priority].append(signal)
        return True
    
    def flow_pulse(self):
        """Trigger a system pulse/flow with optimized signal distribution."""
        start_time = time.time()
        now = datetime.now()
        self.flow_count += 1
        self.last_flow_time = now
        
        # Adjust capacity based on natural variance and cycles
        self._adjust_capacity_for_natural_variance()
        
        # Process signals in priority order (batched for efficiency)
        self._process_signal_queues()
        
        # Check for special river sections
        self._check_river_section_triggers()
        
        # Notify the queue manager first (for controlled concurrency)
        if self.queue_manager and hasattr(self.queue_manager, "on_heartbeat"):
            self.queue_manager.on_heartbeat({
                "beat": self.flow_count,
                "time": now,
                "source": "optimized_river_heart",
                "pulse_capacity": self.current_capacity
            })
        
        # Send standard heartbeat event to all heartbeat subscribers
        self._send_targeted_event("heartbeat", {
            "beat": self.flow_count,
            "time": now,
            "source": "optimized_river_heart",
            "capacity": self.current_capacity
        })
        
        # Notify the brainstem directly (as this is a critical component)
        if self.brainstem:
            if hasattr(self.brainstem, "pulse"):
                self.brainstem.pulse(self.flow_count)
        
        # Track metrics
        pulse_duration = time.time() - start_time
        self.metrics["pulse_times"].append(pulse_duration)
        
        # Log heartbeat periodically
        if self.flow_count % 10 == 0 or self.flow_count < 5:
            timestamp = now.strftime("%H:%M:%S.%f")[:-3]
            print(f"[OptimizedRiverHeart] Flow {self.flow_count} @ {timestamp}, capacity: {self.current_capacity}, " +
                  f"duration: {pulse_duration:.4f}s")
    
    def _process_signal_queues(self):
        """Process all signal queues in priority order."""
        # Process queues in strict priority order
        for priority in sorted(self.priority_queues.keys()):
            queue = self.priority_queues[priority]
            
            # Process up to current capacity signals from this queue
            signals_to_process = min(len(queue), self.current_capacity)
            
            if signals_to_process > 0:
                # Batch signals by target component for efficiency
                batched_signals = defaultdict(list)
                
                # Pull signals from queue
                for _ in range(signals_to_process):
                    if not queue:  # Safety check
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
                        component_ref, _ = self.component_info[component_name]
                        component = component_ref()
                        
                        if component:  # Check if weakref is still valid
                            # Check if component supports batch processing
                            if hasattr(component, "receive_signal_batch"):
                                component.receive_signal_batch(signals)
                                self.metrics["component_signal_counts"][component_name] += len(signals)
                            else:
                                # Fall back to individual processing
                                for signal in signals:
                                    if hasattr(component, "receive_signal"):
                                        component.receive_signal("optimized_river_heart", signal)
                                        self.metrics["component_signal_counts"][component_name] += 1
    
    def _send_targeted_event(self, event_type, payload):
        """Send an event to subscribed components only."""
        if event_type in self.subscribers:
            for component_name in self.subscribers[event_type]:
                if component_name in self.component_info:
                    component_ref, _ = self.component_info[component_name]
                    component = component_ref()
                    
                    if component and hasattr(component, "receive_signal"):  
                        component.receive_signal("optimized_river_heart", {
                            "type": event_type,
                            "data": payload
                        })
    
    def _check_river_section_triggers(self):
        """Check if any river sections need to be triggered with optimized calculations."""
        # Check cache first - avoid recalculating for repeating patterns
        cache_key = self.flow_count % 100  # Reuse calculations for repeating beat patterns
        
        if cache_key in self._section_trigger_cache:
            triggers = self._section_trigger_cache[cache_key]
        else:
            # Calculate which sections should trigger
            triggers = {}
            for section_name, section_data in self.river_sections.items():
                frequency = section_data.get("frequency", 1)
                
                # Special handling for duration-based sections
                if section_name in ["rapids", "gentle_pools"]:
                    # Check if we should enter this section
                    triggers[f"enter_{section_name}"] = (self.flow_count % frequency == 0)
                    
                    # Check if we should exit this section
                    if section_data["active"]:
                        duration = section_data.get("duration", 3)
                        triggers[f"exit_{section_name}"] = (self.flow_count % frequency == duration)
                    else:
                        triggers[f"exit_{section_name}"] = False
                else:
                    # Regular section trigger
                    triggers[section_name] = (self.flow_count % frequency == 0)
                    
            # Cache the calculation
            self._section_trigger_cache[cache_key] = triggers
        
        # Now handle the sections based on trigger status
        for section_name, section_data in self.river_sections.items():
            # Special handling for duration-based sections (rapids, gentle_pools)
            if section_name in ["rapids", "gentle_pools"]:
                # Check if we should enter this section
                if triggers.get(f"enter_{section_name}", False):
                    section_data["active"] = True
                    section_data["last_time"] = datetime.now()
                    
                    # Emit event to subscribers only
                    self._send_targeted_event(f"enter_{section_name}", {
                        "beat": self.flow_count,
                        "source": "optimized_river_heart"
                    })
                
                # Check if we should exit this section
                elif triggers.get(f"exit_{section_name}", False):
                    section_data["active"] = False
                    
                    # Emit event to subscribers only
                    self._send_targeted_event(f"exit_{section_name}", {
                        "beat": self.flow_count,
                        "source": "optimized_river_heart"
                    })
            elif triggers.get(section_name, False):
                # Regular one-time section trigger
                section_data["last_time"] = datetime.now()
                
                # Map section names to trigger methods
                section_to_method = {
                    "shoreline_maintenance": self._trigger_maintenance,
                    "underwater_currents": self._trigger_memory_consolidation,
                    "deep_pools": self._trigger_dream,
                    "river_health": self._trigger_status_report,
                    "flow_monitoring": self._trigger_queue_stats
                }
                
                # Trigger the appropriate method
                if section_name in section_to_method:
                    section_to_method[section_name]()
    
    def _trigger_maintenance(self):
        """Trigger system maintenance cycle."""
        self._send_targeted_event("maintenance", {
            "beat": self.flow_count,
            "source": "optimized_river_heart"
        })
    
    def _trigger_memory_consolidation(self):
        """Trigger memory consolidation cycle."""
        if self.brainstem and hasattr(self.brainstem, "_consolidate_memory"):
            # Direct call to brainstem for this critical function
            self.brainstem._consolidate_memory()
            
        self._send_targeted_event("memory_consolidation", {
            "beat": self.flow_count,
            "source": "optimized_river_heart"
        })
    
    def _trigger_dream(self):
        """Trigger dream cycle for identity reinforcement."""
        self._send_targeted_event("dream", {
            "beat": self.flow_count,
            "source": "optimized_river_heart"
        })
    
    def _trigger_status_report(self):
        """Trigger a system status report with metrics."""
        # Prepare performance metrics
        performance_data = {
            "avg_pulse_time": self.metrics["avg_pulse_time"],
            "max_pulse_time": self.metrics["max_pulse_time"],
            "total_signals": self.metrics["total_signals"],
            "top_signals": sorted(
                self.metrics["signal_counts"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],  # Top 5 signals
            "top_components": sorted(
                self.metrics["component_signal_counts"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],  # Top 5 components
        }
        
        print(f"[OptimizedRiverHeart] Status Report: Flow #{self.flow_count}, " +
              f"Avg pulse: {performance_data['avg_pulse_time']:.4f}s, " +
              f"Total signals: {performance_data['total_signals']}")
              
        self._send_targeted_event("status_report", {
            "beat": self.flow_count,
            "source": "optimized_river_heart",
            "state": self.state,
            "capacity": self.current_capacity,
            "performance": performance_data
        })
    
    def _trigger_queue_stats(self):
        """Get queue statistics if queue manager is available."""
        if self.queue_manager and hasattr(self.queue_manager, "get_stats"):
            stats = self.queue_manager.get_stats()
            
            # Analyze current queue load
            total_waiting = sum(len(q) for q in self.priority_queues.values())
            critical_waiting = len(self.priority_queues[self.PRIORITY_CRITICAL])
            high_waiting = len(self.priority_queues[self.PRIORITY_HIGH])
            
            queue_stats = {
                "total_waiting": total_waiting,
                "critical_waiting": critical_waiting,
                "high_waiting": high_waiting,
                "queue_manager_stats": stats
            }
            
            print(f"[OptimizedRiverHeart] Flow Monitoring: Waiting signals: {total_waiting}, " +
                  f"Critical: {critical_waiting}, High: {high_waiting}")
            
            # Adaptive flow rate - adjust based on queue pressure
            self._adjust_flow_rate_for_load(queue_stats)
    
    def _adjust_flow_rate_for_load(self, queue_stats):
        """Adaptively adjust flow rate based on queue pressure."""
        base_rate = 1.0  # Default rate
        total_waiting = queue_stats["total_waiting"]
        critical_waiting = queue_stats["critical_waiting"]
        
        # If critical signals are waiting, speed up dramatically
        if critical_waiting > 0:
            adjustment_factor = max(0.3, 1.0 - (critical_waiting * 0.1))
            new_rate = base_rate * adjustment_factor
            
        # If lots of signals are waiting, speed up moderately
        elif total_waiting > self.current_capacity * 3:
            adjustment_factor = max(0.5, 1.0 - (total_waiting / (self.current_capacity * 10)))
            new_rate = base_rate * adjustment_factor
            
        # If very few signals, slow down slightly to conserve resources
        elif total_waiting < self.current_capacity * 0.5:
            adjustment_factor = min(1.5, 1.0 + 0.1)
            new_rate = base_rate * adjustment_factor
            
        else:
            # Keep normal rate
            new_rate = base_rate
        
        # Don't change rate too drastically
        if abs(new_rate - self.flow_rate) > 0.2:
            self.set_flow_rate(new_rate)
    
    def get_status(self):
        """Get the optimized river heart's status information with performance metrics."""
        # Calculate average and max pulse times
        avg_time = sum(self.metrics["pulse_times"]) / max(1, len(self.metrics["pulse_times"]))
        max_time = max(self.metrics["pulse_times"]) if self.metrics["pulse_times"] else 0
        
        return {
            "flowing": self.flowing,
            "flow_count": self.flow_count,
            "flow_rate": self.flow_rate,
            "state": self.state,
            "last_flow": self.last_flow_time,
            "river_width": self.river_width,
            "current_capacity": self.current_capacity,
            "performance": {
                "avg_pulse_time": avg_time,
                "max_pulse_time": max_time,
                "total_signals": self.metrics["total_signals"],
                "queue_sizes": {
                    priority: len(queue) 
                    for priority, queue in self.priority_queues.items()
                },
                "subscriber_count": sum(len(subs) for subs in self.subscribers.values()),
            }
        }
    
    def receive_signal(self, source, payload):
        """Receive signal from the body system with priority handling."""
        message_type = payload.get("type", "")
        priority = payload.get("priority", self.PRIORITY_NORMAL)
        
        if message_type == "set_flow_rate":
            rate = payload.get("data", {}).get("rate")
            if rate:
                self.set_flow_rate(rate)
        elif message_type == "set_river_width":
            width = payload.get("data", {}).get("width")
            if width:
                self.set_river_width(width)
        elif message_type == "start_flow":
            cycles = payload.get("data", {}).get("cycles")
            self.start_flow(cycles=cycles)
        elif message_type == "stop_flow":
            self.stop_flow()
        elif message_type.startswith("enqueue_"):
            # Handle enqueued signals with provided priority
            event_type = message_type[8:]  # Remove "enqueue_" prefix
            self.enqueue_signal(
                event_type, 
                payload.get("data", {}),
                target_components=payload.get("target_components"),
                priority=priority
            )
        else:
            # Track the signal
            self.metrics["signal_counts"][message_type] += 1
            self.metrics["total_signals"] += 1
            
            # Handle normally
            print(f"[OptimizedRiverHeart] Received signal: {message_type} from {source}")
        
        return True
    
    def get_metrics(self):
        """Get performance metrics for the heart system."""
        # Calculate derived metrics
        if self.metrics["pulse_times"]:
            avg_time = sum(self.metrics["pulse_times"]) / len(self.metrics["pulse_times"])
            max_time = max(self.metrics["pulse_times"])
        else:
            avg_time = 0
            max_time = 0
            
        # Extract top signals and components
        top_signals = sorted(
            self.metrics["signal_counts"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 signals
        
        top_components = sorted(
            self.metrics["component_signal_counts"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 components
        
        return {
            "avg_pulse_time": avg_time,
            "max_pulse_time": max_time,
            "total_signals": self.metrics["total_signals"],
            "top_signals": top_signals,
            "top_components": top_components,
            "queue_sizes": {
                priority: len(queue) 
                for priority, queue in self.priority_queues.items()
            },
            "subscriber_count": sum(len(subs) for subs in self.subscribers.values()),
        }


# Compatibility layer for existing code
class OptimizedHeart:
    """Compatibility wrapper for basic Heart interface."""
    
    def __init__(self, brainstem):
        """Initialize heart with reference to brainstem."""
        self.river_heart = OptimizedRiverHeart(brainstem=brainstem)
        self.heartbeat_rate = 1.0
        self.alive = False

    def start(self, cycles=5):
        """Start the heart's pulse loop."""
        self.alive = True
        self.river_heart.set_flow_rate(self.heartbeat_rate)
        self.river_heart.start_flow(cycles=cycles)
        self.alive = self.river_heart.flowing

    def pulse(self, interval=None):
        """Trigger a system pulse via brainstem."""
        self.river_heart.flow_pulse()
