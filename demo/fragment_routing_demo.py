"""
Fragment Integration Demo - Demonstrates fragment-aware routing in BlackwallV2

This demo showcases how the fragment system integrates with the routing mechanism,
allowing personality fragments to influence routing decisions based on their current
activation levels and specialized capabilities.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import importlib
import json

# Import standardized logging
from demo_logging import setup_demo_logger, print_and_log, DemoLogger

# Set up the necessary paths
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"

sys.path.insert(0, str(implementation_dir))
sys.path.insert(0, str(root_dir))

# Import core modules
try:
    Router = importlib.import_module('router').Router
    Body = importlib.import_module('body').Body
    FragmentManager = importlib.import_module('fragment_manager').FragmentManager
    Brainstem = importlib.import_module('brainstem').Brainstem
    
    print("\nCore modules imported successfully\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Using imported DemoLogger and print_and_log from demo_logging.py


class TestOrgan:
    """
    Test organ with various capabilities for routing demonstration.
    """
    def __init__(self, name, capabilities, health=1.0):
        self.name = name
        self.capabilities = capabilities
        self.health = health
        
    def register_with_router(self, router):
        """Register this organ with the router."""
        return {
            "name": self.name,
            "capabilities": self.capabilities,
            "health": self.health
        }
        
    def process(self, data):
        """Process the data."""
        return f"{self.name} processed: {data}"
        
    def receive_signal(self, signal):
        """Handle signals."""
        if isinstance(signal, dict):
            command = signal.get('command')
            if command == 'process':
                return {'result': self.process(signal.get('data', 'No data'))}
        return {'status': 'unknown_signal'}


def run_fragment_routing_demo():
    """Run the fragment routing demonstration"""
    # Set up logging
    logger = DemoLogger(demo_name="Fragment Routing Demo")
    
    print_and_log(logger, "Starting Fragment Integration Demo", "INFO")
    print_and_log(logger, "=" * 50)
    
    # Create core components
    print_and_log(logger, "Creating system components...")
    
    router = Router()
    body = Body()
    
    # Create brainstem
    brainstem = Brainstem()
    
    # Create fragment manager
    fragment_manager = FragmentManager(
        router=router,
        body=body,
        logger=logger
    )
    
    # Register with body
    body.register_module("fragment_manager", fragment_manager)
    body.register_module("brainstem", brainstem)
    
    print_and_log(logger, "System components initialized")
    
    # Phase 1: Create test organs with different capabilities
    print_and_log(logger, "\nPhase 1: Creating test organs...")
    
    # Create organs for different domains with specific capabilities
    math_organ = TestOrgan("MathOrgan", ["math", "calculation", "logic"], 0.95)
    language_organ = TestOrgan("LanguageOrgan", ["language", "translation", "text"], 0.9)
    memory_organ = TestOrgan("MemoryOrgan", ["memory", "history", "recall"], 0.85)
    creative_organ = TestOrgan("CreativeOrgan", ["creativity", "art", "imagination"], 0.8)
    security_organ = TestOrgan("SecurityOrgan", ["security", "validation", "protection"], 0.9)
    
    # Register organs with router
    organs = [math_organ, language_organ, memory_organ, creative_organ, security_organ]
    router.broadcast_registration_request(organs)
    
    print_and_log(logger, f"Registered {len(organs)} test organs with router")
    
    # Display routing table
    print_and_log(logger, "\nInitial Routing Table:")
    for organ_id, info in router.get_routing_table().items():
        caps = ", ".join(info.get("capabilities", []))
        print_and_log(logger, f"  {organ_id}: {info['name']} - Capabilities: {caps}")
    
    # Phase 2: Basic Routing (without fragment influence)
    print_and_log(logger, "\nPhase 2: Basic routing without fragment influence...")
      # Find organs for different capabilities
    for capability in ["math", "language", "memory", "creativity", "security"]:
        organs = router.find_organs_by_capability(capability)
        if isinstance(organs, list):
            organs_str = ", ".join([o.get("name", "Unknown") if isinstance(o, dict) else str(o) for o in organs])
        else:
            organs_str = str(organs)
        print_and_log(logger, f"Organs with '{capability}' capability: {organs_str}")
    
    # Phase 3: Integrate fragment manager with router
    print_and_log(logger, "\nPhase 3: Integrating fragment manager with router...")
    success = fragment_manager.integrate_with_router()
    if success:
        print_and_log(logger, "Fragment manager successfully integrated with router", "SUCCESS")
    else:
        print_and_log(logger, "Failed to integrate fragment manager with router", "ERROR")
        
    # Display current fragment levels
    print_and_log(logger, "\nCurrent fragment activation levels:")
    for fragment, level in fragment_manager.get_activation_levels().items():
        print_and_log(logger, f"  {fragment}: {level}")
      # Phase 4: Routing with default fragment influence
    print_and_log(logger, "\nPhase 4: Routing with default fragment influence...")
    for capability in ["math", "language", "memory", "creativity", "security"]:
        organs = router.find_organs_by_capability(capability)
        if isinstance(organs, list):
            organs_str = ", ".join([o.get("name", "Unknown") if isinstance(o, dict) else str(o) for o in organs])
        else:
            organs_str = str(organs)
        print_and_log(logger, f"Organs with '{capability}' capability: {organs_str}")
    # Phase 5: Adjusting fragment levels and observing routing changes
    print_and_log(logger, "\nPhase 5: Adjusting fragment levels...")
    
    # Test different fragment dominant scenarios
    scenarios = [
        {
            "name": "Obelisk Dominant (Logic/Math)",
            "adjustments": {"Obelisk": 40.0, "Lyra": -10.0, "Nyx": -10.0}
        },
        {
            "name": "Seraphis Dominant (Language/Empathy)",
            "adjustments": {"Seraphis": 40.0, "Obelisk": -20.0}
        },
        {
            "name": "Blackwall Dominant (Security)",
            "adjustments": {"Blackwall": 40.0, "Seraphis": -20.0}
        },
        {
            "name": "Echoe Dominant (Memory/History)",
            "adjustments": {"Echoe": 40.0, "Blackwall": -20.0}
        },
        {
            "name": "Nyx Dominant (Creativity/Exploration)",
            "adjustments": {"Nyx": 40.0, "Echoe": -20.0}
        }
    ]
    
    # Test each scenario
    for scenario in scenarios:
        print_and_log(logger, f"\nTesting scenario: {scenario['name']}")
        
        # Adjust fragment levels
        fragment_manager.adjust_fragment_levels(scenario['adjustments'])
        
        # Display updated fragment levels
        print_and_log(logger, "Updated fragment activation levels:")
        fragment_levels = fragment_manager.get_activation_levels()
        for fragment, level in fragment_levels.items():
            print_and_log(logger, f"  {fragment}: {level}")
            
        print_and_log(logger, f"Dominant fragment: {fragment_manager.get_dominant_fragment()}")
          # Test routing priorities under this fragment configuration
        print_and_log(logger, "\nTesting routing priorities:")
        for capability in ["math", "language", "memory", "creativity", "security"]:
            organs = router.find_organs_by_capability(capability)
            if isinstance(organs, list):
                organs_str = ", ".join([o.get("name", "Unknown") if isinstance(o, dict) else str(o) for o in organs])
            else:
                organs_str = str(organs)
            print_and_log(logger, f"  '{capability}' → {organs_str}")
        
        # Small pause for readability
        time.sleep(0.5)
    
    # Phase 6: Testing input-driven fragment adjustments
    print_and_log(logger, "\nPhase 6: Testing input-driven fragment adjustments...")
    
    # Reset fragments to baseline
    fragment_manager.reset_to_default()
    print_and_log(logger, "Reset fragments to default levels")
    
    # Test inputs that should trigger different fragments
    test_inputs = [
        "Calculate the square root of 144 and analyze the result logically",
        "How does it feel when someone shows compassion and empathy?",
        "Please remember my previous request and maintain continuity",
        "We need to ensure security and protect the system from threats",
        "I wonder what creative possibilities we could explore together"
    ]
    
    for input_text in test_inputs:
        print_and_log(logger, f"\nAnalyzing input: '{input_text}'")
        
        # Analyze input and adjust fragments
        adjustments = fragment_manager.analyze_input_for_fragments(input_text)
        if adjustments:
            print_and_log(logger, "Fragment adjustments based on input:")
            for fragment, adj in adjustments.items():
                print_and_log(logger, f"  {fragment}: {adj:+.1f}")
                
            # Apply the adjustments
            fragment_manager.adjust_fragment_levels(adjustments)
            
            # Show updated dominant fragment
            print_and_log(logger, f"Updated dominant fragment: {fragment_manager.get_dominant_fragment()}")
            
            # Test a relevant capability based on the input
            if "calculate" in input_text.lower() or "logically" in input_text.lower():
                capability = "math"
            elif "feel" in input_text.lower() or "empathy" in input_text.lower():
                capability = "language" 
            elif "remember" in input_text.lower() or "previous" in input_text.lower():
                capability = "memory"
            elif "security" in input_text.lower() or "protect" in input_text.lower():
                capability = "security"
            elif "creative" in input_text.lower() or "explore" in input_text.lower():
                capability = "creativity"
            else:
                capability = "math"  # Default
                  # Check routing decision
            organs = router.find_organs_by_capability(capability)
            if isinstance(organs, list):
                organs_str = ", ".join([o.get("name", "Unknown") if isinstance(o, dict) else str(o) for o in organs])
            else:
                organs_str = str(organs)
            print_and_log(logger, f"Routing decision for '{capability}': {organs_str}")
        else:
            print_and_log(logger, "No fragment adjustments detected")
        
        # Small pause for readability
        time.sleep(0.5)
    
    # Phase 7: Restore original routing
    print_and_log(logger, "\nPhase 7: Restoring original routing...")
    fragment_manager.restore_router()
    
    print_and_log(logger, "\nFragment Integration Demo completed", "SUCCESS")
    print_and_log(logger, "=" * 50)


if __name__ == "__main__":
    run_fragment_routing_demo()
