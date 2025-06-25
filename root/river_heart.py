"""
River Heart

An enhanced heart system that implements the "lazy river" concept for controlling
information flow through the BlackwallV2 system.

The river heart:
- Controls both flow rate (heartbeat frequency) and river width (pulse capacity)
- Maintains consistent, predictable flow of information
- Ensures no component gets overwhelmed with too much to process at once
- Creates a natural cycle of processing, memory consolidation, and identity reinforcement
"""

import time
import threading
import random
from datetime import datetime

class RiverHeart:
    """
    The RiverHeart implements the lazy river concept for information flow.
    
    Key properties:
    - flow_rate: The speed of the river (heartbeats per second)
    - river_width: The width of the river (items processed per beat)
    - depth_variance: Natural variation in processing capacity to simulate river depth
    - seasonal_cycles: Longer-term cycles that affect processing priorities
    """
    
    def __init__(self, brainstem=None, body=None, queue_manager=None):
        """Initialize river heart with references to other system components."""
        self.brainstem = brainstem
        self.body = body
        self.queue_manager = queue_manager
        
        # Flow control parameters
        self.flow_rate = 1.0  # Default: 1 beat per second (like heart.heartbeat_rate)
        self.river_width = 10  # Default: 10 items per beat (like heart.pulse_capacity)
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
        
        print("[RiverHeart] Initialized with flow rate:", self.flow_rate, 
              "and river width:", self.river_width)
    
    def register_with_body(self, body):
        """Register this heart with a body system."""
        self.body = body
        if self.body:
            self.body.register_module("river_heart", self)
            print("[RiverHeart] Registered with body system")
            return True
        return False
    
    def set_queue_manager(self, queue_manager):
        """Connect the heart to a queue manager for information flow control."""
        self.queue_manager = queue_manager
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.river_width)
            print("[RiverHeart] Connected to queue manager")
            return True
        return False
    
    def set_river_width(self, width):
        """
        Set the river's width (items processed per beat).
        
        This is like setting how many items can flow through
        the system with each heartbeat.
        """
        self.river_width = max(1, width)  # Ensure at least 1
        self.current_capacity = self.river_width  # Reset current capacity
        
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.river_width)
        print(f"[RiverHeart] River width set to {self.river_width}")
        return True
    
    def start_flow(self, cycles=None):
        """Start the heart's flow."""
        if self.flowing:
            print("[RiverHeart] Already flowing.")
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
        print(f"[RiverHeart] Starting flow for {cycles} cycles")
        for _ in range(cycles):
            self.flow_pulse()
            time.sleep(self.flow_rate)
        self.flowing = False
        self.state = "dry"
        print("[RiverHeart] Completed cycle run")
    
    def _start_background(self):
        """Start heart in background thread."""
        if self.thread and self.thread.is_alive():
            print("[RiverHeart] Background flow already running")
            return False
        
        print("[RiverHeart] Starting background flow")
        self.thread = threading.Thread(
            target=self._flow_loop,
            name="RiverHeartThread",
            daemon=True  # Allow program to exit even if thread is running
        )
        self.thread.start()
        return True
    
    def _flow_loop(self):
        """Internal loop for continuous flowing."""
        print("[RiverHeart] Beginning flow loop")
        while self.flowing:
            self.flow_pulse()
            time.sleep(self.flow_rate)
        print("[RiverHeart] Flow loop ended")
    
    def stop_flow(self):
        """Stop the heart's flowing."""
        if not self.flowing:
            print("[RiverHeart] Already dry")
            return True
            
        print("[RiverHeart] Drying up...")
        self.flowing = False
        self.state = "drying"
        
        # Wait for thread to end if it exists
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)  # Wait up to 2 seconds
            if self.thread.is_alive():
                print("[RiverHeart] Warning: Flow thread didn't stop cleanly")
            
        self.state = "dry"
        print("[RiverHeart] Stopped")
        return True
    
    def set_flow_rate(self, rate):
        """Set the flow rate in seconds between beats."""
        if rate <= 0:
            print("[RiverHeart] Error: Rate must be positive")
            return False
            
        self.flow_rate = rate
        print(f"[RiverHeart] Flow rate set to {rate} seconds")
        return True
        
    def _adjust_capacity_for_natural_variance(self):
        """Apply natural variance to processing capacity to simulate river depth changes."""
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
        
        # Update queue manager with new capacity
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.current_capacity)
    
    def flow_pulse(self):
        """
        Trigger a system pulse/flow.
        
        This is the main function that drives the system rhythm,
        notifying all components of the flow and triggering
        various cycles based on their frequencies.
        """
        now = datetime.now()
        self.flow_count += 1
        self.last_flow_time = now
        
        # Adjust capacity based on natural variance and cycles
        self._adjust_capacity_for_natural_variance()
        
        # Format only needed for display
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]
        
        # Notify the queue manager first (for controlled concurrency)
        if self.queue_manager and hasattr(self.queue_manager, "on_heartbeat"):
            self.queue_manager.on_heartbeat({
                "beat": self.flow_count,
                "time": now,
                "source": "river_heart",
                "pulse_capacity": self.current_capacity
            })
        
        # Notify the body (event bus) next
        if self.body:
            self.body.emit_event("heartbeat", {
                "beat": self.flow_count,
                "time": now,
                "source": "river_heart",
                "capacity": self.current_capacity
            })
        
        # Notify the brainstem directly
        if self.brainstem:
            if hasattr(self.brainstem, "pulse"):
                self.brainstem.pulse(self.flow_count)
        
        # Check for special river sections
        self._check_river_section_triggers()
        
        if self.flow_count % 10 == 0 or self.flow_count < 5:
            print(f"[RiverHeart] Flow {self.flow_count} @ {timestamp}, capacity: {self.current_capacity}")
    
    def _check_river_section_triggers(self):
        """Check if any river sections need to be entered or triggered."""
        # Handle special river sections with duration (rapids, gentle pools)
        for section_name in ["rapids", "gentle_pools"]:
            section = self.river_sections[section_name]
            
            # Check if we should enter this section
            if self.flow_count % section["frequency"] == 0:
                section["active"] = True
                section["last_time"] = datetime.now()
                print(f"[RiverHeart] Entering {section_name}")
                
                # Emit event
                if self.body:
                    self.body.emit_event(f"enter_{section_name}", {
                        "beat": self.flow_count,
                        "source": "river_heart"
                    })
                    
            # Check if we should exit this section
            elif section["active"] and (self.flow_count % section["frequency"] == section["duration"]):
                section["active"] = False
                print(f"[RiverHeart] Exiting {section_name}")
                
                # Emit event
                if self.body:
                    self.body.emit_event(f"exit_{section_name}", {
                        "beat": self.flow_count,
                        "source": "river_heart"
                    })
        
        # Handle one-time triggers
        for section_name, section_data in self.river_sections.items():
            # Skip special sections with duration
            if section_name in ["rapids", "gentle_pools"]:
                continue
                
            frequency = section_data["frequency"]
            
            if self.flow_count % frequency == 0:
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
        print("[RiverHeart] Triggering shoreline maintenance")
        if self.body:
            self.body.emit_event("maintenance", {
                "beat": self.flow_count,
                "source": "river_heart"
            })
    
    def _trigger_memory_consolidation(self):
        """Trigger memory consolidation cycle."""
        print("[RiverHeart] Triggering underwater currents (memory consolidation)")
        if self.brainstem and hasattr(self.brainstem, "_consolidate_memory"):
            # WARNING: Accessing protected member _consolidate_memory. Consider using a public method if available.
            self.brainstem._consolidate_memory()
            
        if self.body:
            self.body.emit_event("memory_consolidation", {
                "beat": self.flow_count,
                "source": "river_heart"
            })
    
    def _trigger_dream(self):
        """Trigger dream cycle for identity reinforcement."""
        print("[RiverHeart] Entering deep pools (dream cycle)")
        if self.body:
            self.body.emit_event("dream", {
                "beat": self.flow_count,
                "source": "river_heart"
            })
    
    def _trigger_status_report(self):
        """Trigger a system status report."""
        print(f"[RiverHeart] River Health Report: {self.flow_count} flows, state={self.state}")
        
        # Collect status from components if body is available
        if self.body:
            self.body.emit_event("status_report", {
                "beat": self.flow_count,
                "source": "river_heart",
                "state": self.state,
                "capacity": self.current_capacity
            })
    
    def _trigger_queue_stats(self):
        """Get queue statistics if queue manager is available."""
        if self.queue_manager and hasattr(self.queue_manager, "get_stats"):
            stats = self.queue_manager.get_stats()
            print(f"[RiverHeart] Flow Monitoring: {stats}")
    
    def get_status(self):
        """Get the river heart's status information."""
        return {
            "flowing": self.flowing,
            "flow_count": self.flow_count,
            "flow_rate": self.flow_rate,
            "state": self.state,
            "last_flow": self.last_flow_time,
            "river_sections": self.river_sections,
            "river_width": self.river_width,
            "current_capacity": self.current_capacity
        }

    def receive_signal(self, source, payload):
        """Receive signal from the body system."""
        message_type = payload.get("type", "")
        
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
        else:
            print(f"[RiverHeart] Received signal: {message_type} from {source}")
        
        return True
