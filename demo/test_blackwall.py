"""
BlackwallV2 Basic Test Script

This script runs a simple test of the BlackwallV2 biomimetic AI system
to validate core functionality.
"""

import os
import sys
from pathlib import Path

# Add parent directories to path for imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

# Test the import paths
print(f"Testing import paths...")
print(f"Current directory: {current_dir}")
print(f"Root directory: {root_dir}")

# Import core components
try:
    sys.path.append(str(root_dir / "root"))
    from root.brainstem import Brainstem
    print("✓ Successfully imported Brainstem")
except ImportError as e:
    print(f"✗ Error importing Brainstem: {e}")
    sys.exit(1)

def run_test():
    """Run a basic test of the BlackwallV2 system."""
    print("\nRunning BlackwallV2 basic test...\n")
    
    # Initialize the brainstem
    try:
        brainstem = Brainstem()
        print("✓ Brainstem initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing Brainstem: {e}")
        return False
    
    # Test processing a simple input
    try:
        response = brainstem.process_input("Tell me about your identity.")
        print(f"✓ Processed input successfully")
        print(f"Response: {response}")
    except Exception as e:
        print(f"✗ Error processing input: {e}")
        return False
    
    # Test memory storage
    try:
        stm_entries = brainstem.stm.get_all()
        print(f"✓ Short-term memory contains {len(stm_entries)} entries")
    except Exception as e:
        print(f"✗ Error accessing short-term memory: {e}")
        return False
    
    print("\nTest completed successfully!")
    return True

if __name__ == "__main__":
    run_test()
