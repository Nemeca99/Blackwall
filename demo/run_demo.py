"""
BlackwallV2 Demo Application

This script demonstrates the core functionality of the BlackwallV2 biomimetic AI system,
including fragment identity, dual-hemisphere memory, and recursive processing.
"""

import os
import sys
from pathlib import Path

# Add parent directories to path for imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "root"))

# Import core components
from root.brainstem import Brainstem

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
    print("\nEnter 'exit' or 'quit' to end the demo.")
    print("=" * 60 + "\n")

def run_demo():
    """Run the BlackwallV2 demo."""
    print_header()
    
    # Initialize the brainstem (central orchestrator)
    brainstem = Brainstem()
    
    # Main interaction loop
    running = True
    while running:
        try:
            # Get user input
            user_input = input("\nYou: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("\nThank you for exploring the BlackwallV2 demo.")
                running = False
                continue
            
            # Process the input through the brainstem
            response = brainstem.process_input(user_input)
            
            # Display the response
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
