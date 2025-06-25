"""
BlackwallV2 Basic Biomimetic Demo

This script demonstrates the basic flow of information through the biomimetic
architecture of BlackwallV2 without LLM integration.
"""

import os
import sys
from pathlib import Path
import importlib.util

# Get absolute paths
current_file = Path(__file__).resolve()
demo_dir = current_file.parent
implementation_dir = demo_dir.parent
root_dir = implementation_dir / 'root'

# Print paths for debugging
print(f"Current file: {current_file}")
print(f"Demo directory: {demo_dir}")
print(f"Implementation directory: {implementation_dir}")
print(f"Root directory: {root_dir}")

# Ensure implementation_dir is in sys.path
if str(implementation_dir) not in sys.path:
    sys.path.insert(0, str(implementation_dir))

# Import using direct file paths
def import_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module {module_name} at {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import all necessary modules
try:
    # Core modules
    body_module = import_from_file("body", root_dir / "body.py")
    Body = body_module.Body
    
    brainstem_module = import_from_file("brainstem", root_dir / "brainstem.py")
    Brainstem = brainstem_module.Brainstem
    
    left_hem_module = import_from_file("Left_Hemisphere", root_dir / "Left_Hemisphere.py")
    ShortTermMemory = left_hem_module.ShortTermMemory
    
    right_hem_module = import_from_file("Right_Hemisphere", root_dir / "Right_Hemisphere.py")
    LongTermMemory = right_hem_module.LongTermMemory
    
    soul_module = import_from_file("soul", root_dir / "soul.py")
    Soul = soul_module.Soul
    
    heart_module = import_from_file("heart", root_dir / "heart.py")
    Heart = heart_module.Heart
    
    mouth_module = import_from_file("mouth", root_dir / "mouth.py")
    Mouth = mouth_module.Mouth
    
    ears_module = import_from_file("ears", root_dir / "ears.py")
    Ears = ears_module.Ears
    
    eyes_module = import_from_file("eyes", root_dir / "eyes.py")
    Eyes = eyes_module.Eyes
    
    hands_module = import_from_file("hands", root_dir / "hands.py")
    Hands = hands_module.Hands
    
    print("Successfully imported all modules")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def main():
    # Initialize the system components
    print("Initializing BlackwallV2 biomimetic architecture...\n")
    
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
    
    print("All biomimetic components initialized and registered.\n")
    
    # Basic information flow demo
    print("Demonstrating basic information flow through the system...\n")
    
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

if __name__ == "__main__":
    main()
