"""
BlackwallV2 Demo Application

This script demonstrates the core functionality of the BlackwallV2 biomimetic AI system,
including fragment identity, dual-hemisphere memory, recursive processing, 
dream cycle memory consolidation, and fragment-aware routing.
"""

import os
import sys
import argparse
from pathlib import Path

# Parse command line arguments
parser = argparse.ArgumentParser(description='BlackwallV2 Demo')
parser.add_argument('--enable-dreams', action='store_true', help='Enable dream cycles')
parser.add_argument('--enable-fragments', action='store_true', help='Enable fragment-aware routing')
parser.add_argument('--memory-path', type=str, help='Path to memory file')
parser.add_argument('--llm-enabled', action='store_true', help='Enable LLM integration if available')
args = parser.parse_args()

# Add parent directories to path for imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "root"))

# Import core components
from root.brainstem import Brainstem
from root.dream_manager import DreamManager
from root.fragment_manager import FragmentManager
from root.Left_Hemisphere import ShortTermMemory
from root.Right_Hemisphere import LongTermMemory
from root.body import Body
from root.heart import Heart

# Try to import LLM components if enabled
if args.llm_enabled:
    try:
        sys.path.append(str(root_dir / "llm_integration"))
        from llm_integration.llm_interface import LLMInterface
        llm_available = True
        print("LLM integration loaded successfully")
    except ImportError:
        print("LLM integration not available, falling back to simulation mode")
        llm_available = False

def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("       BlackwallV2 / Lyra Blackwall Demo")
    print("  Biomimetic AI Architecture based on T.R.E.E.S. Framework")
    print("=" * 60)
    print("\nThis demo showcases the core concepts of BlackwallV2, including:")
    print("- Fragment-based identity with multiple specialized personas")
    print("- Dual-hemisphere memory (short-term and long-term)")
    print("- Biomimetic structure with brainstem, body, and soul components")
    print("- Recursive processing and symbolic compression")
    
    # Print enabled features
    features = []
    if args.enable_dreams:
        features.append("Dream Cycle Memory Consolidation")
    if args.enable_fragments:
        features.append("Fragment-Aware Signal Routing")
    if args.llm_enabled and 'llm_available' in globals() and llm_available:
        features.append("LLM Integration (Active)")
    elif args.llm_enabled:
        features.append("LLM Integration (Simulated)")
        
    if features:
        print("\nEnabled advanced features:")
        for feature in features:
            print(f"- {feature}")
            
    print("\nEnter 'exit' or 'quit' to end the demo.")
    print("Commands: help, status, dream (force dream cycle), fragments (show levels)")
    print("=" * 60 + "\n")

def load_memories(ltm, memory_path):
    """Load memories from file."""
    if not os.path.exists(memory_path):
        print(f"Memory file not found: {memory_path}")
        return False
        
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            import json
            memories = json.load(f)
            
        if isinstance(memories, list):
            for memory in memories:
                ltm.memory.append(memory)
            return len(memories)
        elif isinstance(memories, dict) and 'memories' in memories:
            for memory in memories['memories']:
                ltm.memory.append(memory)
            return len(memories['memories'])
        else:
            print("Invalid memory file format")
            return False
    except Exception as e:
        print(f"Error loading memories: {e}")
        return False

def run_demo():
    """Run the BlackwallV2 demo."""
    print_header()
    
    # Initialize the body (communication hub)
    body = Body()
    
    # Create memory components
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    # Ensure memory is initialized properly
    if not hasattr(ltm, 'memory') or ltm.memory is None:
        ltm.memory = []
    
    # Create heart
    heart = Heart()
    
    # Load memories if specified
    if args.memory_path:
        count = load_memories(ltm, args.memory_path)
        if count:
            print(f"Loaded {count} memories from {args.memory_path}")
    
    # Initialize the advanced components if enabled
    dream_manager = None
    fragment_manager = None
    
    if args.enable_dreams:
        dream_manager = DreamManager(
            long_term_memory=ltm,
            heart=heart,
            body=body
        )
        body.register_module("dream_manager", dream_manager)
        print("Dream Cycle system activated")
        
    if args.enable_fragments:
        fragment_manager = FragmentManager(
            router=None,  # We'll set this later
            body=body
        )
        body.register_module("fragment_manager", fragment_manager)
        print("Fragment-Aware Routing system activated")
    
    # Initialize the brainstem with all components
    brainstem = Brainstem()
    
    # Register core components with body
    body.register_module("brainstem", brainstem)
    body.register_module("heart", heart)
    body.register_module("stm", stm)
    body.register_module("ltm", ltm)
    
    print("System initialization complete\n")
    
    # Main interaction loop
    running = True
    while running:
        try:
            # Get user input
            user_input = input("\nYou: ")
            command = user_input.lower().strip()
            
            # Check for commands
            if command in ["exit", "quit"]:
                print("\nExiting BlackwallV2 demo. Thank you for exploring the system!")
                running = False
                continue
                
            elif command == "help":
                print("\nAvailable commands:")
                print("  help          - Show this help message")
                print("  status        - Show system status")
                if args.enable_dreams:
                    print("  dream         - Force a dream cycle")
                if args.enable_fragments:
                    print("  fragments     - Show current fragment levels")
                    print("  activate X Y  - Activate fragment X by amount Y")
                print("  exit/quit     - Exit the demo")
                continue
                
            elif command == "status":
                print("\nSystem status:")
                print(f"  STM entries: {len(stm.memory)}")
                print(f"  LTM entries: {len(ltm.memory)}")
                
                if args.enable_dreams and dream_manager:
                    # Check dream conditions
                    should_sleep, conditions = dream_manager.check_sleep_conditions()
                    print(f"  Dream cycle needed: {should_sleep}")
                    for key, value in conditions.items():
                        if isinstance(value, float):
                            print(f"  - {key}: {value:.4f}")
                        else:
                            print(f"  - {key}: {value}")
                
                if args.enable_fragments and fragment_manager:
                    # Get current dominant fragment
                    dominant = fragment_manager.get_dominant_fragment()
                    print(f"  Dominant fragment: {dominant}")
                continue
                
            elif command == "dream" and args.enable_dreams and dream_manager:
                print("Forcing dream cycle...")
                success = dream_manager.enter_dream_cycle()
                if success:
                    print("Dream cycle completed successfully")
                else:
                    print("Dream cycle failed")
                continue
                
            elif command == "fragments" and args.enable_fragments and fragment_manager:
                print("Current fragment activation levels:")
                for fragment, level in fragment_manager.get_activation_levels().items():
                    print(f"  {fragment}: {level:.1f}")
                continue
                
            elif command.startswith("activate ") and args.enable_fragments and fragment_manager:
                # Parse fragment name and value
                parts = command.split()
                if len(parts) == 3:
                    fragment = parts[1].capitalize()
                    try:
                        amount = float(parts[2])
                        print(f"Adjusting {fragment} by {amount}")
                        fragment_manager.adjust_fragment_levels({fragment: amount})
                        print("Fragment levels updated")
                    except ValueError:
                        print("Invalid amount, must be a number")
                else:
                    print("Usage: activate <fragment> <amount>")
                continue
            
            # Process the input through the brainstem
            response = brainstem.process_input(user_input)
            
            # Display the response with fragment markers
            if args.enable_fragments and fragment_manager:
                dominant = fragment_manager.get_dominant_fragment()
                print(f"\n[{dominant}] {response}")
            else:
                print(f"\nLyra Blackwall: {response}")
            
        except KeyboardInterrupt:
            print("\nDemo terminated by user.")
            running = False
        except Exception as e:
            print(f"\nError: {e}")
            print("Demo continuing...")
    
    print("\nDemo session ended.")

if __name__ == "__main__":
    run_demo()
