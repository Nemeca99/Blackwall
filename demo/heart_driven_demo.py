"""
BlackwallV2 Heart-Driven Demo

This script demonstrates the heart-driven biomimetic architecture of BlackwallV2,
showing how the heart module drives the overall system rhythm.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Set up the necessary paths
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"

# Simple component classes for the demo
class Body:
    def __init__(self):
        self.modules = {}
        self.event_handlers = {}
        print("[Body] Initialized")
    
    def register_module(self, name, module):
        self.modules[name] = module
        print(f"[Body] Registered module: {name}")
        return True
    
    def register_handler(self, event_name, module_name, callback):
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append((module_name, callback))
        print(f"[Body] Registered handler for event '{event_name}' from {module_name}")
        return True
    
    def emit_event(self, event_name, data=None):
        if event_name not in self.event_handlers:
            print(f"[Body] No handlers for event: {event_name}")
            return False
        
        print(f"[Body] Emitting event: {event_name}")
        for module_name, callback in self.event_handlers[event_name]:
            try:
                callback(data)
            except Exception as e:
                print(f"[Body] Error in {module_name} handler for {event_name}: {e}")
        
        return True
    
    def route_signal(self, source, target, payload):
        if target in self.modules:
            if hasattr(self.modules[target], "receive_signal"):
                print(f"[Body] Routing signal from {source} to {target}")
                self.modules[target].receive_signal(source, payload)
                return True
        print(f"[Body] Cannot route to {target}")
        return False

class ShortTermMemory:
    def __init__(self):
        self.memory = []
        self.max_capacity = 20
        print("[STM] Short-term memory initialized")
    
    def store(self, data):
        self.memory.append({
            **data,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"[STM] Stored: {data}")
        return True
    
    def get_recent(self, count=1):
        return self.memory[-count:] if self.memory else []
    
    def on_heartbeat(self, data):
        if len(self.memory) > 0 and data.get("beat", 0) % 5 == 0:
            print(f"[STM] Memory status: {len(self.memory)} items in buffer")
    
    def on_memory_consolidation(self, data):
        print("[STM] Preparing memory for consolidation...")
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        
        if message_type == "store":
            self.store(payload.get("data", {}))
        
        return True

class LongTermMemory:
    def __init__(self):
        self.memory = []
        print("[LTM] Long-term memory initialized")
    
    def store(self, data):
        self.memory.append({
            **data,
            "timestamp": datetime.now().isoformat(),
        })
        print(f"[LTM] Stored: {data}")
        return True
    
    def on_memory_consolidation(self, data):
        print("[LTM] Receiving consolidated memory...")
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        
        if message_type == "store":
            self.store(payload.get("data", {}))
        
        return True

class Soul:
    def __init__(self):
        self.identity = "Lyra Blackwall"
        self.core_values = ["integrity", "wisdom", "curiosity"]
        print("[Soul] Identity core initialized")
    
    def verify(self, fragments, text):
        print(f"[Soul] Verifying output with fragments: {list(fragments.keys())}")
        return True
    
    def on_dream(self, data):
        print(f"[Soul] Reinforcing identity: {self.identity}")
        print(f"[Soul] Core values: {', '.join(self.core_values)}")
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        print(f"[Soul] Received signal: {message_type} from {source}")
        return True

class Brainstem:
    def __init__(self, body=None):
        self.body = body
        print("[Brainstem] Initialized")
    
    def process_input(self, user_input):
        print(f"[Brainstem] Processing: {user_input}")
        
        # Simple simulation logic
        if "identity" in user_input.lower():
            return "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in user_input.lower():
            return "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        else:
            return f"Processing your input about {user_input.split()[0]} through my recursive identity framework."
    
    def consolidate_memory(self):
        """Consolidate short-term to long-term memory."""
        print("[Brainstem] Initiating memory consolidation...")
        
        if not self.body:
            return False
        
        # Signal STM to prepare for consolidation
        self.body.route_signal(
            source="brainstem",
            target="stm",
            payload={"type": "prepare_consolidation"}
        )
        
        # Get recent memories (would be processed in a real system)
        if "stm" in self.body.modules:
            stm = self.body.modules["stm"]
            recent_memories = stm.get_recent(5)
            
            # Create a summary (in a full implementation, this would use the LLM)
            if recent_memories:
                summary = f"Consolidated {len(recent_memories)} memories"
                
                # Store in LTM
                self.body.route_signal(
                    source="brainstem",
                    target="ltm",
                    payload={
                        "type": "store", 
                        "data": {
                            "summary": summary, 
                            "memories": recent_memories
                        }
                    }
                )
        
        return True
    
    def pulse(self, beat_count):
        """Handle system pulse."""
        if beat_count % 10 == 0:
            print(f"[Brainstem] System pulse {beat_count}")
    
    def on_memory_consolidation(self, data):
        """Handle memory consolidation event."""
        self.consolidate_memory()
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        
        if message_type == "process_input":
            response = self.process_input(payload.get("data", {}).get("input", ""))
            
            # Route to mouth for output
            if self.body:
                self.body.route_signal(
                    source="brainstem",
                    target="mouth",
                    payload={
                        "type": "speak",
                        "data": {"response": response}
                    }
                )
        
        return True

class Ears:
    def __init__(self, body=None):
        self.body = body
        print("[Ears] Input system initialized")
    
    def receive(self, text):
        print(f"[Ears] Received: {text}")
        
        # Store in STM
        if self.body:
            self.body.route_signal(
                source="ears",
                target="stm",
                payload={
                    "type": "store",
                    "data": {
                        "role": "user",
                        "content": text
                    }
                }
            )
            
            # Send to brainstem for processing
            self.body.route_signal(
                source="ears",
                target="brainstem",
                payload={
                    "type": "process_input",
                    "data": {"input": text}
                }
            )
        
        return True

class Mouth:
    def __init__(self):
        print("[Mouth] Output system initialized")
    
    def speak(self, text, fragment_weights=None):
        if fragment_weights:
            print(f"[Mouth] Speaking with fragments {fragment_weights}: {text}")
        else:
            print(f"[Mouth] Speaking: {text}")
        return text
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        
        if message_type == "speak":
            response = payload.get("data", {}).get("response", "")
            self.speak(response)
        
        return True

# Import the enhanced heart module
try:
    # Using importlib to load the module from file path
    import importlib.util
    spec = importlib.util.spec_from_file_location("heart", root_dir / "heart.py")
    if spec is None:
        raise ImportError(f"Could not find heart module at {root_dir / 'heart.py'}")
    
    heart_module = importlib.util.module_from_spec(spec)
    sys.modules["heart"] = heart_module
    spec.loader.exec_module(heart_module)
    Heart = heart_module.Heart
    
    print("\nHeart module imported successfully\n")
except ImportError as e:
    print(f"Error importing heart module: {e}")
    sys.exit(1)

def main():
    print("\nInitializing BlackwallV2 biomimetic architecture with heart...\n")
    
    # Create the body (central nervous system)
    body = Body()
    
    # Create memory systems
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    
    # Create core identity
    soul = Soul()
    
    # Create central orchestrator
    brainstem = Brainstem(body=body)
    
    # Create input/output components
    ears = Ears(body=body)
    mouth = Mouth()
    
    # Register components with the body
    body.register_module("stm", stm)
    body.register_module("ltm", ltm)
    body.register_module("soul", soul)
    body.register_module("brainstem", brainstem)
    body.register_module("ears", ears)
    body.register_module("mouth", mouth)
    
    # Create the heart to drive the system
    heart = Heart(brainstem=brainstem, body=body)
    body.register_module("heart", heart)
    
    # Register event handlers
    body.register_handler("heartbeat", "stm", stm.on_heartbeat)
    body.register_handler("memory_consolidation", "stm", stm.on_memory_consolidation)
    body.register_handler("memory_consolidation", "ltm", ltm.on_memory_consolidation)
    body.register_handler("memory_consolidation", "brainstem", brainstem.on_memory_consolidation)
    body.register_handler("dream", "soul", soul.on_dream)
    
    print("\nAll biomimetic components initialized and registered.\n")
    
    # Start the heart with faster rate for the demo
    heart.set_rate(0.5)
    heart.start()  # Start in background
    
    print("\nSimulating user interaction...\n")
    
    # Give the heart a chance to start beating
    time.sleep(1)
    
    # Simulate user inputs over time
    inputs = [
        "Tell me about your identity",
        "What is your purpose",
        "How does the TREES framework work"
    ]
    
    for user_input in inputs:
        print(f"\nUser: {user_input}")
        ears.receive(user_input)
        time.sleep(3)  # Wait for processing
    
    # Let the system run a bit longer to show heart cycles
    print("\nLetting the system continue to run for a while...")
    time.sleep(10)
    
    # Stop the heart
    print("\nStopping the system...")
    heart.stop()
    
    print("\nDemo complete.")

if __name__ == "__main__":
    main()
