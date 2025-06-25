"""
Heart Module Test

This script demonstrates the heart module functionality in isolation,
showing how it manages system pulses and triggers various cycles.
"""

import sys
import time
from pathlib import Path

# Add the root directory to the path
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"
sys.path.insert(0, str(implementation_dir))

# Create a mock body class for testing
class MockBody:
    def __init__(self):
        self.modules = {}
        self.events_received = []
    
    def register_module(self, name, module):
        self.modules[name] = module
        print(f"[MockBody] Registered module: {name}")
        return True
    
    def emit_event(self, event_name, data=None):
        self.events_received.append((event_name, data))
        print(f"[MockBody] Event received: {event_name}")
        return True

# Create a mock brainstem class for testing
class MockBrainstem:
    def __init__(self):
        self.pulses_received = 0
    
    def pulse(self, beat_count=None):
        self.pulses_received += 1
        print(f"[MockBrainstem] Pulse received: {beat_count}")
        return True
    
    def _consolidate_memory(self):
        print("[MockBrainstem] Memory consolidation triggered")
        return True

# Import and test the heart module
try:
    # Using importlib to load the module from file path
    import importlib.util
    spec = importlib.util.spec_from_file_location("heart", root_dir / "heart.py")
    heart_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(heart_module)
    Heart = heart_module.Heart
    
    print("\nHeart module imported successfully\n")
    
    # Create the test components
    mock_body = MockBody()
    mock_brainstem = MockBrainstem()
    
    # Create and test the heart
    heart = Heart(brainstem=mock_brainstem, body=mock_body)
    
    print("\n1. Testing basic heart functionality:")
    print("-----------------------------------")
    
    # Run a few cycles
    print("\nRunning 12 cycles (should trigger status report at beat 5 and maintenance at beat 10):")
    heart.start(cycles=12)
    
    # Check the status
    status = heart.get_status()
    print(f"\nHeart status: {status}")
    
    # Check events received by the body
    print(f"\nEvents received by body: {len(mock_body.events_received)}")
    event_types = set(event[0] for event in mock_body.events_received)
    print(f"Event types: {event_types}")
    
    # Check pulses received by brainstem
    print(f"Pulses received by brainstem: {mock_brainstem.pulses_received}")
    
    print("\n2. Testing background thread heart:")
    print("----------------------------------")
    
    # Reset the mocks
    mock_body = MockBody()
    mock_brainstem = MockBrainstem()
    heart = Heart(brainstem=mock_brainstem, body=mock_body)
    
    # Set faster rate for testing
    heart.set_rate(0.2)  # 5 beats per second
    
    # Start in background
    print("\nStarting heart in background...")
    heart.start()
    
    # Wait a bit
    print("Waiting 3 seconds...")
    time.sleep(3)
    
    # Stop the heart
    print("Stopping heart...")
    heart.stop()
    
    # Check the status
    status = heart.get_status()
    print(f"\nHeart status after background run: {status}")
    
    # Check pulses received by brainstem
    print(f"Pulses received by brainstem: {mock_brainstem.pulses_received}")
    
    print("\nTest complete.")
    
except ImportError as e:
    print(f"Error importing heart module: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
