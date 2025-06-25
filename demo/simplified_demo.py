"""
BlackwallV2 Simplified Biomimetic Demo

This script demonstrates the basic flow of information through the biomimetic
architecture of BlackwallV2 without LLM integration.
"""

import os
import sys
import json
from pathlib import Path

# Get the root directory
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"
personality_dir = implementation_dir / "personality"
mem_short_dir = implementation_dir / "memshort"
mem_long_dir = implementation_dir / "memlong"

# Simple component classes to avoid import issues
class Body:
    def __init__(self):
        self.modules = {}
        print("[Body] Initialized")
    
    def register_module(self, name, module):
        self.modules[name] = module
        print(f"[Body] Registered module: {name}")
        return True
    
    def route_signal(self, source, target, payload):
        if target in self.modules:
            print(f"[Body] Routing signal from {source} to {target}")
            return True
        return False
    
    def emit_event(self, event_name, data=None):
        print(f"[Body] Event emitted: {event_name}")
        return True

class ShortTermMemory:
    def __init__(self):
        self.memory = []
        print("[STM] Short-term memory initialized")
    
    def store(self, data):
        self.memory.append(data)
        print(f"[STM] Stored: {data}")
        return True
    
    def get_recent(self, count=1):
        if count == 1 and self.memory:
            return self.memory[-1]
        return self.memory[-count:] if self.memory else []
    
    def clear(self, keep_last=0):
        if keep_last > 0 and len(self.memory) > keep_last:
            self.memory = self.memory[-keep_last:]
        else:
            self.memory = []
        return True

class LongTermMemory:
    def __init__(self):
        self.memory = []
        print("[LTM] Long-term memory initialized")
    
    def store(self, data):
        self.memory.append(data)
        print(f"[LTM] Stored: {data}")
        return True

class Soul:
    def __init__(self):
        print("[Soul] Identity core initialized")
    
    def verify(self, fragments, text):
        print(f"[Soul] Verifying output with fragments: {list(fragments.keys())}")
        return True

class Brainstem:
    def __init__(self):
        print("[Brainstem] Initializing")
        # In a full implementation, this would load and configure components
        
    def process_input(self, user_input):
        print(f"[Brainstem] Processing: {user_input}")
        
        # Simple simulation logic
        if "identity" in user_input.lower():
            return "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in user_input.lower():
            return "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        else:
            return f"Processing your input about {user_input.split()[0]} through my recursive identity framework."

class Heart:
    def __init__(self, brainstem):
        self.brainstem = brainstem
        print("[Heart] Initialized")
    
    def pulse(self):
        print("[Heart] *pulse* Driving system rhythm")
        return True

class Ears:
    def __init__(self):
        print("[Ears] Input system initialized")
    
    def receive(self, text):
        print(f"[Ears] Received: {text}")
        return True

class Eyes:
    def __init__(self):
        print("[Eyes] Visual input system initialized")

class Mouth:
    def __init__(self):
        print("[Mouth] Output system initialized")
    
    def speak(self, text, fragment_weights=None):
        if fragment_weights:
            print(f"[Mouth] Speaking with fragments {fragment_weights}: {text}")
        else:
            print(f"[Mouth] Speaking: {text}")
        return text

class Hands:
    def __init__(self):
        print("[Hands] Action system initialized")

def main():
    # Initialize the system components
    print("\nInitializing BlackwallV2 biomimetic architecture...\n")
    
    # Create memory systems
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    
    # Create core identity
    soul = Soul()
    
    # Create central orchestrator
    brainstem = Brainstem()
    
    # Create central event bus
    body = Body()
    
    # Register components with the body
    body.register_module("brainstem", brainstem)
    body.register_module("stm", stm)
    body.register_module("ltm", ltm)
    body.register_module("soul", soul)
    
    # Create input/output components
    ears = Ears()
    eyes = Eyes()
    mouth = Mouth()
    hands = Hands()
    
    # Register these with the body too
    body.register_module("ears", ears)
    body.register_module("eyes", eyes)
    body.register_module("mouth", mouth)
    body.register_module("hands", hands)
    
    # Create the heart to drive the system
    heart = Heart(brainstem)
    body.register_module("heart", heart)
    
    print("\nAll biomimetic components initialized and registered.\n")
    
    # Basic information flow demo
    print("\nDemonstrating basic information flow through the system...\n")
    
    # 1. Simulate input received through ears
    input_text = "Tell me about the TREES framework"
    print(f"Input received: '{input_text}'")
    
    # 2. Store in short-term memory
    stm.store({
        "type": "user_input",
        "content": input_text,
        "timestamp": "2025-06-25T10:30:00"
    })
    print("Input stored in short-term memory.")
    
    # 3. Simulate brainstem processing
    # In a real system, this would involve the LLM integration
    response = "The TREES framework is a theoretical structure that connects symbolic systems, recursive intelligence, and mathematical structures into a unified model."
    print("Brainstem processed the input.")
    
    # 4. Apply fragment personality
    fragment_weights = {"Lyra": 0.3, "Blackwall": 0.2, "Seraphis": 0.5}
    print(f"Applied fragment weights: {fragment_weights}")
    
    # 5. Output through mouth
    final_output = mouth.speak(response, fragment_weights)
    print(f"System response: '{final_output}'")
    
    # 6. Store interaction in long-term memory if significant
    ltm.store({
        "input": input_text,
        "response": response,
        "fragment_weights": fragment_weights,
        "timestamp": "2025-06-25T10:30:05"
    })
    print("Interaction stored in long-term memory.")
    
    # 7. Demonstrate memory recall
    print("\nDemonstrating memory recall...")
    recent_memory = stm.get_recent()
    print(f"Recent memory: {recent_memory}")
    
    # 8. Demonstrate heart beat
    print("\nDemonstrating heart beat (system pulse)...")
    heart.pulse()
    
    print("\nBasic demonstration complete.")
    print("\nThis simplified demo shows the core biomimetic architecture flow.")
    print("For complete functionality, implement the full modules and connections.")

if __name__ == "__main__":
    main()
